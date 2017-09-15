
-  对于直接调用了might_sleep函数的函数，如果把`might_sleep`去掉，会发生什么情况。

	- 去掉`might_sleep()`，如果内核在原子上下文中调用了可睡眠或可重新调度的函数，内核不会报错，会让系统错误的执行下去，可能在继续执行的过程中造成系统死锁或崩溃，而对于实时linux系统而言，在抢占禁止或原子上下文的情况下，产生睡眠或调度，会造成实时性性能变差或者系统crash。但是如果系统没有配置`CONFIG_DEBUG_ATOMIC_SLEEP`，`might_sleep()`是空函数，在内核中不起作用，去掉`might_sleep()`不会产生什么影响。在配置了`CONFIG_PREEMPT_VOLUNTARY`的情况下，稍微有点不同，但并没有太大的变化，不做讨论。如果打开了配置`CONFIG_DEBUG_ATOMIC_SLEEP`，会检查是否在原子上下文中调用了该函数，从而就像注释中说的那样"help to be able to catch problems early and not	be bitten later when the calling function happens to sleep"。

- 在经过了`might_sleep`函数的call graph（即包含了`might_sleep`的各条执行路径形成的图）中，如果没有`might_sleep`，是否会存在一种情况，某个执行路径A会产生调度，二某个执行路径B不允许调度，且这两个执行路径可以并发执行，这形成了某种不一致的情况。
	
	- 应该会存在上边的情况，因为在调用的过程中，如果没有或去掉了`might_sleep`,内核不能够检查是否该函数的调用处在原子上下文或中断上下文中，在SMP中，一个cpu处在进程上下文，从而有可能存在在函数调用过程中，执行路径A允许函数在执行过程中产生调度，而在另一个CPU上处在原子上下文，执行路径B在调用函数的过程中不允许睡眠或调度。两个CPU处在不同的上下文中并行执行同一可睡眠的函数。在UP中，应该同样存在这种在进程上下文和原子上下文中同时调用可睡眠或可调度的函数。

- 如何提供一种方法，能够在没有`might_sleep`的情况下，确保`atomic_context`下，不会出现调度。

	- 是否可以在原子上下文中，调用可能产生睡眠或调度的函数时，关闭时钟中断，从而禁止了调度。
	- 是否能够在产生调度条件时，判断当前上下文是否为原子上下文，然后置系统的请求调度标志，直到原子上下文结束，再调度。


- `might_sleep()`函数主要是在配置了`CONFIG_DEBUG_ATOMIC_SLEEP`的情况下起作用（也就是在调试系统或系统发生crash后,需要检查内核错误），在正常编译情况下，`might_sleep()`并没有做任何事情，从源代码中可以看到：
		
			# define might_sleep() do { might_resched(); } while (0)
			#ifdef CONFIG_PREEMPT_VOLUNTARY
			extern int _cond_resched(void);
			# define might_resched() _cond_resched()
			#else
			# define might_resched() do { } while (0)
			#endif
	
	- 当配置了`CONFIG_DEBUG_ATOMIC_SLEEP`，打开内核调试选型，`might_sleep()`源代码的形式如下：

			#ifdef CONFIG_DEBUG_ATOMIC_SLEEP
			  void ___might_sleep(const char *file, int line, int preempt_offset);
			  void __might_sleep(const char *file, int line, int preempt_offset);
			/**
			 * might_sleep - annotation for functions that can sleep
			 *
			 * this macro will print a stack trace if it is executed in an atomic
			 * context (spinlock, irq-handler, ...).
			 *
			 * This is a useful debugging help to be able to catch problems early and not
			 * be bitten later when the calling function happens to sleep when it is not
			 * supposed to.
			 */
			# define might_sleep() \
				do { __might_sleep(__FILE__, __LINE__, 0); might_resched()

	从注释中可以看出`might_sleep()`作为一个宏，主要是表明该函数能够产生睡眠。但是在原子上下文中（注：原子上下文解释在下面），内核是不允许调用睡眠函数的。因此，这里`might_sleep()`通过打印堆栈信息，告诉调用者，是否在原子上下文中调用了该睡眠函数。在原子上下文中理论上不应该让当前的execution path进入sleep状态（一个拥有spinlock的进程进入sleep并不必然意味着系统就一定会deadlock等，但是对内核编程而言，还是应该尽量避免在原子上下文中产生睡眠，尤其对于实时操作系统，会影响实时性）。

	**注：**内核的一个基本原则就是：在中断或者说原子上下文中，内核不能访问用户空间，而且内核是不能睡眠的。也就是说在这种情况下，内核是不能调用有可能引起睡眠的任何函数。一般来讲原子上下文指的是在中断或软中断中，以及在持有自旋锁的时候。内核提供了四个宏来判断是否处于这几种情况里：

			#define in_irq()     (hardirq_count()) //在处理硬中断中
			#define in_softirq()     (softirq_count()) //在处理软中断中
			#define in_interrupt()   (irq_count()) //在处理硬中断或软中断中
			#define in_atomic()     ((preempt_count() & ~PREEMPT_ACTIVE) != 0) //包含以上所有情况

	这四个宏所访问的count都是`thread_info->preempt_count`。这个变量其实是一个位掩码。
	
	最低8位表示抢占计数，通常由`spin_lock/spin_unlock`修改，或程序员强制修改，同时表明内核容许的最大抢占深度是256。
	
	8－15位表示软中断计数，通常由`local_bh_disable/local_bh_enable`修改，同时表明内核容许的最大软中断深度是256。
	位16－27是硬中断计数，通常由`enter_irq/exit_irq`修改，同时表明内核容许的最大硬中断深度是4096。
	第28位是PREEMPT_ACTIVE标志。用代码表示就是：
	
			PREEMPT_MASK: 0x000000ff
			SOFTIRQ_MASK: 0x0000ff00
			HARDIRQ_MASK: 0x0fff0000
	
	凡是上面4个宏返回1得到地方都是原子上下文，是不容许内核访问用户空间，不容许内核睡眠的，不容许调用任何可能引起睡眠的函数。而且代表`thread_info->preempt_count`不是0，这就告诉内核，在这里面抢占被禁用。
	
	但是，对于in_atomic()来说，在启用抢占的情况下，它工作的很好，可以告诉内核目前是否持有自旋锁，是否禁用抢占等。但是，在没有启用抢占的情况下，`spin_lock`根本不修改`preempt_count`，所以即使内核调用了`spin_lock`，持有了自旋锁，`in_atomic()`仍然会返回0，错误的告诉内核目前在非原子上下文中。所以凡是依赖`in_atomic()`来判断是否在原子上下文的代码，在禁抢占的情况下都是有问题的。

			#ifdef CONFIG_DEBUG_ATOMIC_SLEEP
			static inline int preempt_count_equals(int preempt_offset)
			{
				int nested = preempt_count() + sched_rcu_preempt_depth();
			
				return (nested == preempt_offset);
			}
			
			void __might_sleep(const char *file, int line, int preempt_offset)
			{
				/*
				 * Blocking primitives will set (and therefore destroy) current->state,
				 * since we will exit with TASK_RUNNING make sure we enter with it,
				 * otherwise we will destroy state.
				 */
				WARN_ONCE(current->state != TASK_RUNNING && current->task_state_change,
						"do not call blocking ops when !TASK_RUNNING; "
						"state=%lx set at [<%p>] %pS\n",
						current->state,
						(void *)current->task_state_change,
						(void *)current->task_state_change);
			
				___might_sleep(file, line, preempt_offset);
			}
			EXPORT_SYMBOL(__might_sleep);
			
			void ___might_sleep(const char *file, int line, int preempt_offset)
			{
				/* Ratelimiting timestamp: */
				static unsigned long prev_jiffy;
			
				unsigned long preempt_disable_ip;
			
				/* WARN_ON_ONCE() by default, no rate limit required: */
				rcu_sleep_check();
			
				if ((preempt_count_equals(preempt_offset) && !irqs_disabled() &&
				     !is_idle_task(current)) ||
				    system_state == SYSTEM_BOOTING || system_state > SYSTEM_RUNNING ||
				    oops_in_progress)
					return;
			
				if (time_before(jiffies, prev_jiffy + HZ) && prev_jiffy)
					return;
				prev_jiffy = jiffies;
			
				/* Save this before calling printk(), since that will clobber it: */
				preempt_disable_ip = get_preempt_disable_ip(current);
			
				printk(KERN_ERR
					"BUG: sleeping function called from invalid context at %s:%d\n",
						file, line);
				printk(KERN_ERR
					"in_atomic(): %d, irqs_disabled(): %d, pid: %d, name: %s\n",
						in_atomic(), irqs_disabled(),
						current->pid, current->comm);
			
				if (task_stack_end_corrupted(current))
					printk(KERN_EMERG "Thread overran stack, or stack corrupted\n");
			
				debug_show_held_locks(current);
				if (irqs_disabled())
					print_irqtrace_events(current);
				if (IS_ENABLED(CONFIG_DEBUG_PREEMPT)
				    && !preempt_count_equals(preempt_offset)) {
					pr_err("Preemption disabled at:");
					print_ip_sym(preempt_disable_ip);
					pr_cont("\n");
				}
				dump_stack();
				add_taint(TAINT_WARN, LOCKDEP_STILL_OK);
			}
			EXPORT_SYMBOL(___might_sleep);
			#endif

			
	从代码中可以看出if语句通过两个函数`preempt_count_equals()`和 `irqs_disabled()`来判断当前的上下文是否是一个`atomic context`。`preempt_count_equals()`该函数通过判断preempt_count是否为0，而在上面提到的原子上下文都会改变`preempt_count`的值。`irq_disabled`则是用来判断当前中断是否开启。`__might_sleep`正是根据这些信息来判断当前正在执行的代码上下文是否是个atomic，如果不是，那么函数就直接返回了，因为一切正常。如果是，那么代码会继续执行，打印出相应的警告信息。代码通过`might_sleep`可以判断当前所调用的可睡眠的函数是否在atomic context。
