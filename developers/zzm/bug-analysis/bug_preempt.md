* [2.6.22 - 2.6.24] change die_chain from atomic to raw notifiers {C::bug::irq::preempt::preempt::not NMI-safe,replace atomic_notifier_call_chain to raw_...}
  + [[file:2.6.22/rcu-preempt-fix-nmi-watchdog.patch][2.6.22]] {MOD::kernel}

		此处是在RT上将`atomic_notifier_call_chain()->raw notifier_call_chain()` 说是为了避免not NMI_safe in -rt。从源代码看，`atomic_notifier_call_chain()`调用了`rcu_read_lock()->preempt_disable()`为什么会产生`not NMI_safe`不大理解？？

		原子通知链(Atomic notifier chains)：通知链元素的回调函数（当事件发生时要执行的函数）在中断或原子操作上下文中运行，不允许阻塞。

				 /*
				 * It is illegal to block while in an RCU read-side critical section.
				 */
				int __kprobes __atomic_notifier_call_chain(struct atomic_notifier_head *nh,
					unsigned long val, void *v,
					int nr_to_call, int *nr_calls)
						{
							int ret;
						
							rcu_read_lock();
							ret = notifier_call_chain(&nh->head, val, v, nr_to_call, nr_calls);
							rcu_read_unlock();
							return ret;
						}

				#define rcu_read_lock() \
					do { \
						preempt_disable(); \
						__acquire(RCU); \
					} while(0)
		原始通知链(Raw notifierchains)：对通知链元素的回调函数没有任何限制，所有锁和保护机制都由调用者维护。

			int raw_notifier_call_chain(struct raw_notifier_head *nh,
			unsigned long val, void *v)
					{
						return __raw_notifier_call_chain(nh, val, v, -1, NULL);
					}
			
			int __raw_notifier_call_chain(struct raw_notifier_head *nh,
			      unsigned long val, void *v,
			      int nr_to_call, int *nr_calls)
					{
						return notifier_call_chain(&nh->head, val, v, nr_to_call, nr_calls);
					}		

			static int __kprobes notifier_call_chain(struct notifier_block **nl,
					unsigned long val, void *v,
					int nr_to_call,	int *nr_calls)
				{
					int ret = NOTIFY_DONE;
					struct notifier_block *nb, *next_nb;
				
					nb = rcu_dereference(*nl);
				
					while (nb && nr_to_call) {
						next_nb = rcu_dereference(nb->next);
						ret = nb->notifier_call(nb, val, v);
				
						if (nr_calls)
							(*nr_calls)++;
				
						if ((ret & NOTIFY_STOP_MASK) == NOTIFY_STOP_MASK)
							break;
						nb = next_nb;
						nr_to_call--;
					}
					return ret;
				}

--

* [2.6.22 - 2.6.25] rcu-various-fixups.patch {C::bug::crash::preempt::preempt::add rcu_read lock pair}
  + [[file:2.6.22/rcu-various-fixups.patch][2.6.22]]?

	增加`rcu_read_lock`和`rcu_read_unlock`，这两个函数用来标记一个RCU读过程的开始和结束。其实作用就是帮助检测宽限期是否结束。

--

* [2.6.22 - 2.6.25] arm-fix-atomic-cmpxchg.patch {C::bug::deadlock::preempt::preempt::replace orig irq_save with raw}
  + [[file:2.6.22/arm-fix-atomic-cmpxchg.patch][2.6.22]]

	此处用`raw_local_irq_save() 替换local_irq_save()`

		# define raw_local_irq_save(flags)		\
			do {					\
				BUILD_CHECK_IRQ_FLAGS(flags);	\
				local_irq_save(flags);		\
			} while (0)

		#if !defined(BUILD_CHECK_IRQ_FLAGS) && defined(typecheck)
		#define BUILD_CHECK_IRQ_FLAGS(flags)					\
			do {								\
				BUILD_BUG_ON(sizeof(flags) != sizeof(unsigned long));	\
				typecheck(unsigned long, flags);			\
			} while (0)
		#else
		#define BUILD_CHECK_IRQ_FLAGS(flags)
		#endif

		 #define local_irq_save(flags) \
		+	do {					\
		+		BUILD_CHECK_IRQ_FLAGS(flags);	\
		+		raw_local_irq_save(flags);	\
		+		trace_hardirqs_off();		\
		+	} while (0)

		此处应该只是对flags 进行check

--

* [2.6.22 - 2.6.26] nf_conntrack-fix-smp-processor-id.patch {C::bug::data_err::preempt::preempt::replace with raw}
  + [[file:2.6.22/nf_conntrack-fix-smp-processor-id.patch][2.6.22]]

		将`__get_cpu_var()替换为__raw_get_cpu_var()`

			 #define __get_cpu_var(var)			per_cpu__##var
			 #define __raw_get_cpu_var(var)			per_cpu__##var

		此处没有变化，只是重新构造了一下。

--

* [2.6.22 - 2.6.26] preempt-realtime-powerpc-b4.patch {C::bug::crash::preempt::preempt::preempt_disable added}
  + [[file:2.6.22/preempt-realtime-powerpc-b4.patch][2.6.22]]

	此处增加`preempt_disable/enable()来保护per_cpu` var
	
	此处的commit：BUG: `using smp_processor_id()` in preemptible [00000000] code: khvcd/280
	caller is .xmon_core+0xb8/0x8ec	
	
	可见是在可抢占区域使用`per_cpu` var.

--

* [2.6.22 - 2.6.26] preempt-realtime-powerpc-b2.patch {C::bug::crash::preempt::preempt::replace with raw}
  + [[file:2.6.22/preempt-realtime-powerpc-b2.patch][2.6.22]]

	在RT上用`raw_spin_lock代替spin_lock`来修复警告或错误
	
	估计是修复了引入mutex带来的警告或错误

--

* [2.6.22 - 2.6.29] call reboot notifier list when doing an emergency reboot {C::bug::hang::preempt::preempt::add emergency restart}
  + [[file:2.6.22/fix-emergency-reboot.patch][2.6.22]]

	此处如果处在可抢断环境中，增加reboot notifier list的调用，解决reboot 问题 
	
--

* [2.6.23 - 2.6.24] -rt scheduling: wakeup bug? {C::bug::rtlatency::preempt::preempt::move a section of code up}
	* + [[file:2.6.23/rt-wakeup-fix.patch][2.6.23]]

	关于实时唤醒，

			+		 * Sync wakeups (i.e. those types of wakeups where the waker
			+		 * has indicated that it will leave the CPU in short order)
			+		 * don't trigger a preemption, if the woken up task will run on
			+		 * this cpu. (in this case the 'I will reschedule' promise of
			+		 * the waker guarantees that the freshly woken up task is going
			+		 * to be considered on this CPU.)

--

* [2.6.24 - 2.6.25] kvm: move the apic timer migration {C::bug::crash::preempt::semantics::move the apic timer migration}
  + [[file:2.6.24/kvm-lapic-migrate-latency-fix.patch][2.6.24]]

	在RT-preempt，移动`kvm_migrate_apic_timer()`修复在等待队列中可能产生的sleeps。

		Move apic timer migration to a place where it does not cause the
		"might sleep while atomic" check. The original place calls 
		hrtimer_cancel in a preempt disabled region, which is fine in mainline,
		but preempt-rt changes hrtimer_cancel, that the caller sleeps on a
		wait_queue, when the callback of the timer is currently active.	

--

* [2.6.24 - 2.6.26] rcu-preempt-boost-fix.patch {C::bug::deadlock::preempt::preempt::add careful checks}
  + [[file:2.6.24/rcu-preempt-boost-fix.patch][2.6.24]]

		对rcu-preempt-boost fix	

--

* [2.6.25         ] pcounter-percpu-protect.patch {C::bug::data_err::preempt::preempt::add protection to per_cpu variables in pcounter addition}
  + [[file:2.6.25/pcounter-percpu-protect.patch][2.6.25]]

		此处增加`preempt_disable/enable()`来保护`per_cpu`变量

--

* [2.6.25 - 2.6.26] genhd-protect-percpu-var.patch {C::bug::data_err::preempt::preempt::protect use of smp_processor_id in genhd.h with preempt disable}
  + [[file:2.6.25/genhd-protect-percpu-var.patch][2.6.25]]

		此处是增加`preempt_disable/enable()`保护`per_cpu` var

--

* [2.6.26         ] ppc64-fix-preempt-unsafe-paths-accessing-per_cpu-variables {C::bug::data_err::preempt::preempt::Fix preempt unsafe paths accessing per_cpu variables}
  + [[file:2.6.26/ppc64-fix-preempt-unsafe-paths-accessing-per_cpu-variables.patch][2.6.26]]

			#define get_cpu_var_locked(var, cpuptr)			\
			(*({							\
				int __cpu = raw_smp_processor_id();		\
										\
				*(cpuptr) = __cpu;				\
				spin_lock(&__get_cpu_lock(var, __cpu));		\
				&__get_cpu_var_locked(var, __cpu);		\
			}))

			#define __get_cpu_var_locked(var, cpu) \
				per_cpu_var_locked(var, cpu)

			#define per_cpu_var_locked(var, cpu) \
			(*SHIFT_PERCPU_PTR(&__per_cpu_var_lock_var(var), per_cpu_offset(cpu)))

			#define __per_cpu_var_lock_var(var) per_cpu__##var##_locked

			#define get_cpu_var(var) (*({				\
				extern int simple_identifier_##var(void);	\
				preempt_disable();				\
				&__get_cpu_var(var); }))
			这里用get_cpu_var_locked(var, cpuptr)替换__get_cpu_var()
			用get_cpu_var() 替换preempt_disable;__get_cpu_var(),保护per_cpu var
			

--

* [2.6.26         ] ftrace-wakeup-rawspinlock.patch {C::bug::hang::preempt::preempt::ftrace: user raw spin lock for wakeup function trace}
  + [[file:2.6.26/ftrace-wakeup-rawspinlock.patch][2.6.26]]

		用`raw_local_irq_save();__raw_spin_lock()代替 spin_lock_irqsave()`
		用`local_irq_save(); __raw_spin_lock()代替 spin_lock_irqsave()`

			#define raw_local_irq_save(flags)				\
			do { (flags) = __raw_local_irq_save(); } while (0)

			static inline unsigned long __raw_local_irq_save(void)
				{
					unsigned long flags = __raw_local_save_flags();
				
					raw_local_irq_disable();
				
					return flags;
				}
			# define _raw_spin_lock(lock)		__raw_spin_lock(&(lock)->raw_lock)
			#define __raw_spin_lock(lock) __raw_spin_lock_flags(lock, 0)

			

			

--

* [2.6.26 - 2.6.29] nfs-stats-miss-preemption.patch {C::bug::rtlatency::preempt::preempt::nfs: fix missing preemption check}
  + [[file:2.6.26/nfs-stats-miss-preemption.patch][2.6.26]]

		`get_cpu()/put_cpu_no_preempt()->get_cpu()/put_cpu()`这里是一种对可抢占的一种优化，避免高优先级的任务长时间的延迟。

		NFS iostats use `get_cpu()/put_cpu_no_preempt()`. That misses a
		preemption check for no good reason and introduces long latencies when
		a wakeup of a higher priority task happens in the preempt disabled
		region.

--

* [2.6.29         ] suppress warning of smp_processor_id use.{C::bug::crash::preempt::preempt::use preempt_disable() to supress waring message}
  + [[file:2.6.29/sched-generic-hide-smp-warning.patch][2.6.29]]

		此处增加`preempt_disable/enable()`来保护`per_CPU `var,此处没有增加任何锁，不能保护本地中断异步抢占

--

* [2.6.29         ] x86-pae-preempt-realtime-fix.patch{C::bug::crash::preempt::preempt::add preempt_disable protect}
  + [[file:2.6.29/x86-pae-preempt-realtime-fix.patch][2.6.29]]

	此处在RT中，添加preempt_disable/enable()保护临界区资源

--

* [   3.0         ] drivers/dca: Convert dca_lock to a raw spinlock{C::bug::deadlock::preempt::preempt::replace with raw}
  + [[file:3.0/drivers-dca-convert-dcalock-to-raw.patch][3.0]]
	
			call trace 信息	  [   25.607517] igb 0000:01:00.0: DCA enabled
								[   25.607524] BUG: sleeping function called from invalid context at kernel/rtmutex.c:684
			
			#define raw_spin_lock_irqsave(lock, flags)			\
			do {						\
				typecheck(unsigned long, flags);	\
				flags = _raw_spin_lock_irqsave(lock);	\
			} while (0)
	
			#ifndef CONFIG_INLINE_SPIN_LOCK_IRQSAVE
			unsigned long __lockfunc _raw_spin_lock_irqsave(raw_spinlock_t *lock)
			{
				return __raw_spin_lock_irqsave(lock);
			}

			static inline unsigned long __raw_spin_lock_irqsave(raw_spinlock_t *lock)
				{
					unsigned long flags;
				
					local_irq_save(flags);
					preempt_disable();
					spin_acquire(&lock->dep_map, 0, 0, _RET_IP_);
					/*
					 * On lockdep we dont want the hand-coded irq-enable of
					 * do_raw_spin_lock_flags() code, because lockdep assumes
					 * that interrupts are not re-enabled during lock-acquire:
					 */
				#ifdef CONFIG_LOCKDEP
					LOCK_CONTENDED(lock, do_raw_spin_trylock, do_raw_spin_lock);
				#else
					do_raw_spin_lock_flags(lock, &flags);
				#endif
					return flags;
				}


			#define spin_lock_irqsave(lock, flags)			 \
			do {						 \
				typecheck(unsigned long, flags);	 \
				flags = 0;				 \
				spin_lock(lock);			 \
			} while (0)
		
	从源代码中可以看出在RT中`spin_lock_irqsave(lock, flags)`并没有禁止中断,只是获取睡眠锁。
	用`raw_spin_lock_irq_save()替换spin_lock_irqsave()`

--

* [   3.0 -   4.11] md: raid5: Make raid5_percpu handling RT aware{C::bug::crash::preempt::preempt::add locks, and replace with _light to keep serialized}
  + [[file:3.0/md-raid5-percpu-handling-rt-aware.patch][3.0]]

	此处是将`get_cpu()转换成get_cpu_light()`实质上是`preempt_disable->migration_disable`,目的
	是：（1）实时性：增加可抢占区域。（2）在RT上，禁止抢占的情况下（原子上下文），如果产生重新调度，
	或者获取睡眠锁，这在原子上下文是不允许的。并且此处在替换为`migration_diable`后增加了`spin_lock
	()`是为了避免在current CPU上产生抢占或中断，对`per_cpu`产生影响。
	
	因此，对于`per_CPU`相关的由`preempt_disable->migration_disable`，在对`per_cpu` var操作时，都应该增加相应的睡眠锁进行互斥保护。

--

* [   3.2         ] printk: Disable migration instead of preemption{C::bug::crash::preempt::preempt::replace preempt_disable with migrate_disable}
  + [[file:3.2/printk-disable-migration-instead-of-preemption.patch][3.2]]

	此处是`preemption_diable->migration_disable`，在vprintk的源代码中

		# vsprintk
		asmlinkage int vprintk( const char *fmt, va_list args)
		{
		         int printed_len = 0;
		         int current_log_level = default_message_loglevel;
		         unsigned long flags;
		         int this_cpu;
		         char *p;
		 
		         boot_delay_msec();
		 
		         preempt_disable();
		         /* This stops the holder of console_sem just where we want him */
		         raw_local_irq_save(flags);
		         this_cpu = smp_processor_id();
		 
		         /*
		          * Ouch, printk recursed into itself!
		          */
		         if (unlikely(printk_cpu == this_cpu)) {
		                 /*
		                  * If a crash is occurring during printk() on this CPU,
		                  * then try to get the crash message out but make sure
		                  * we can't deadlock. Otherwise just return to avoid the
		                  * recursion and return - but flag the recursion so that
		                  * it can be printed at the next appropriate moment:
		                  */
		                 if (!oops_in_progress) {
		                         recursion_bug = 1;
		                         goto out_restore_irqs;
		                 }
		                 zap_locks();
		         }
		 
		         lockdep_off();
		         spin_lock(&logbuf_lock);
		         printk_cpu = this_cpu;
		 
		         if (recursion_bug) {
		                 recursion_bug = 0;
		                 strcpy (printk_buf, recursion_bug_msg);
		                 printed_len = sizeof (recursion_bug_msg);
		         }
		         /* Emit the output into the temporary buffer */
		         printed_len += vscnprintf(printk_buf + printed_len,
		                                   sizeof (printk_buf) - printed_len, fmt, args);
		 
		 
		#ifdef  CONFIG_DEBUG_LL
		         printascii(printk_buf);
		#endif
		 
		         /*
		          * Copy the output into log_buf.  If the caller didn't provide
		          * appropriate log level tags, we insert them here
		          */
		         for (p = printk_buf; *p; p++) {
		                 if (new_text_line) {
		                         /* If a token, set current_log_level and skip over */
		                         if (p[0] == '<' && p[1] >= '0' && p[1] <= '7' &&
		                             p[2] == '>' ) {
		                                 current_log_level = p[1] - '0' ;
		                                 p += 3;
		                                 printed_len -= 3;
		                         }
		 
		                         /* Always output the token */
		                         emit_log_char( '<' );
		                         emit_log_char(current_log_level + '0' );
		                         emit_log_char( '>' );
		                         printed_len += 3;
		                         new_text_line = 0;
		 
		                         if (printk_time) {
		                                 /* Follow the token with the time */
		                                 char tbuf[50], *tp;
		                                 unsigned tlen;
		                                 unsigned long long t;
		                                 unsigned long nanosec_rem;
		 
		                                 t = cpu_clock(printk_cpu);
		                                 nanosec_rem = do_div(t, 1000000000);
		                                 tlen = sprintf (tbuf, "[%5lu.%06lu] " ,
		                                                 (unsigned long ) t,
		                                                 nanosec_rem / 1000);
		 
		                                 for (tp = tbuf; tp < tbuf + tlen; tp++)
		                                         emit_log_char(*tp);
		                                 printed_len += tlen;
		                         }
		 
		                         if (!*p)
		                                 break ;
		                 }
		 
		                 emit_log_char(*p);
		                 if (*p == '\n' )
		                         new_text_line = 1;
		         }
		 
		         /*
		          * Try to acquire and then immediately release the
		          * console semaphore. The release will do all the
		          * actual magic (print out buffers, wake up klogd,
		          * etc).
		          *
		          * The acquire_console_semaphore_for_printk() function
		          * will release 'logbuf_lock' regardless of whether it
		          * actually gets the semaphore or not.
		          */
		         if (acquire_console_semaphore_for_printk(this_cpu))
		                 release_console_sem();
		 
		         lockdep_on();
				 out_restore_irqs:
		         raw_local_irq_restore(flags);
		 
		         preempt_enable();
		         return printed_len;
		}
		同时调用了`raw_local_irq_save(flags);与spin_lock(&logbuf_lock)`;因此直接调用
		`migration_disable`已经足够，并且持有睡眠锁，在原子上下文中是不允许的。		

--

* [   3.2 -   4.11] arm: Convert arm boot_lock to raw{C::bug::crash::preempt::preempt::replace with raw}
  + [[file:3.2/arm-convert-boot-lock-to-raw.patch][3.2]]

	此处是将`spin_lock()`转换成`raw_spin_lock()`：因为`idle_sched_class->enqueue_task ==
	null`,因此，当空闲任务在该锁上阻塞时，将不能被唤醒。

--

* [   3.4 -   3.12] sched/rt: Fix wait_task_interactive() to test rt_spin_lock state{C::bug::data_err::preempt::preempt::add state check}
  + [[`file:3.4/rfc-sched-rt-fix-wait_task_interactive-to-test-rt_spin_lock-state.patch`][3.4]]

		增加检测`rt_spin_lock（）`保存的状态，即检测是否一个正在睡眠等待另一个任务具有某种状态，但另一个任务却被阻塞到`rt_spin_lock（）`，这时可能会返回不正确的结果。
	
--

* [   3.4 -   4.11] net: Use cpu_chill() instead of cpu_relax(){C::bug::hang::preempt::preempt::use cpu_chill instead}
  + [[file:3.4/net-use-cpu-chill.patch][3.4]]

		此处为了避免RT中Retry loops forever when the modifying side was preempted,用`cpu_chill()`	代替`cpu_relax()` on RT：`cpu_chill()`会睡眠一秒钟

			#ifdef CONFIG_PREEMPT_RT_FULL
			/*
			 * Sleep for 1 ms in hope whoever holds what we want will let it go.
			 */
			void cpu_chill(void)
			{
				struct timespec tu = {
					.tv_nsec = NSEC_PER_MSEC,
				};
				unsigned int freeze_flag = current->flags & PF_NOFREEZE;
			
				current->flags |= PF_NOFREEZE;
				__hrtimer_nanosleep(&tu, NULL, HRTIMER_MODE_REL, CLOCK_MONOTONIC,
						    TASK_UNINTERRUPTIBLE);
				if (!freeze_flag)
					current->flags &= ~PF_NOFREEZE;
			}

--

* [   3.4 -   4.11] fs: dcache: Use cpu_chill() in trylock loops{C::bug::hang::preempt::preempt::use cpu_chill instead}
  + [[file:3.4/fs-dcache-use-cpu-chill-in-trylock-loops.patch][3.4]]

	与上一个补丁功能类似。

--

* [   3.6 -   4.11] softirq: Check preemption after reenabling interrupts{C::bug::rtlatency::preempt::semantics::check preemption after reenable interrupts}
  + [[file:3.6/softirq-preempt-fix-3-re.patch][3.6]]

	此处是避免在函数`raise_softirq_irqoff()(禁用中断，唤醒软中断)`以后，重新使能中断时被抢占，
	造成软中断线程被无限延迟，因此在调用`raise_softirq_irqoff()`并使能中断`local_irq_enable/
	restore`以后，在RT中增加`preempt_check_resched_rt（）`检查是否有抢占。

--

* [   3.8         ] FIX [2/2] slub: Tid must be retrieved from the percpu area of the current proces{C::bug::data_err::preempt::preempt::slub: Tid must be retrieved from the percpu area of the current proces}
  + [[file:3.8/fix-2-2-slub-tid-must-be-retrieved-from-the-percpu-area-of-the-current-processor.patch][3.8]]

	此处加入`preempt_disable()`是为了避免在获取`Per_CPU`指针之后，对tid检查之前，被调度到其他CPU
	上，从而破坏了current `Per_CPU` var，但是在随后的补丁中去除了该补丁。在目前最新的内核中，并没有
	添加任何的限制，而是把Per_CPU指针和tid检查顺序调整了，并给出这样的commit：

			/*
			 * Must read kmem_cache cpu data via this cpu ptr. Preemption is
			 * enabled. We may switch back and forth between cpus while
			 * reading from one cpu area. That does not matter as long
			 * as we end up on the original cpu again when doing the cmpxchg.
			 *
			 * We should guarantee that tid and kmem_cache are retrieved on
			 * the same cpu. It could be different if CONFIG_PREEMPT so we need
			 * to check if it is matched or not.
			 */
			do {
				tid = this_cpu_read(s->cpu_slab->tid);
				c = raw_cpu_ptr(s->cpu_slab);
			} while (IS_ENABLED(CONFIG_PREEMPT) &&
				 unlikely(tid != READ_ONCE(c->tid)));	

--

* [   4.6 -   4.11] drm,radeon,i915: Use preempt_disable/enable_rt() where recommended{}{C::bug::deadlock::preempt::preempt::add preempt_disable/enable_rt() where recommended}
  + [[`file:4.6/drmradeoni915_Use_preempt_disableenable_rt()_where_recommended.patch`][4.6]]

	此处添加了`preempt_disable/enable_rt()`
		
			#ifdef CONFIG_PREEMPT_RT_FULL
			# define preempt_disable_rt()		preempt_disable()
			# define preempt_enable_rt()		preempt_enable()
			# define preempt_disable_nort()		barrier()
			# define preempt_enable_nort()		barrier()
			#else
			# define preempt_disable_rt()		barrier()
			# define preempt_enable_rt()		barrier()
			# define preempt_disable_nort()		preempt_disable()
			# define preempt_enable_nort()		preempt_enable()
			#endif
	之所以加入`preempt_disable/enable_rt()`从以上的定义中可以看出，有些在RT中是需要禁止抢占，而在！RT中可能是不需要的。这里是在RT为了保证`ktime_get()`获取的准确性，增加`preempt_disable/enable_rt()`。

--

* [   4.9 -   4.11] locking/percpu-rwsem: Remove preempt_disable variants{C::bug::crash::preempt::preempt::remove preempt_disable variants}
  + [[file:4.9/peterz-percpu-rwsem-rt.patch][4.9]]

			/*
				 * We are in an RCU-sched read-side critical section, so the writer
				 * cannot both change sem->state from readers_fast and start checking
				 * counters while we are here. So if we see !sem->state, we know that
				 * the writer won't be checking until we're past the preempt_enable()
				 * and that one the synchronize_sched() is done, the writer will see
				 * anything we did within this RCU-sched read-size critical section.
				 * 
				 */	
		将`percpu_down_read_preempt_disable()替换为percpu_down_read(),在percpu_down_read()中
		增加了preempt_disable/enable()对`，增加了-RT的实时性，其实感觉此处不应算作bug，可以看做
		feature/performance.

--

* [  4.11         ] sched/clock: Fix early boot preempt assumption in __set_sched_clock_stable{C::bug::crash::preempt::irq::disabling irqs}
  + [[file:4.11/0001-sched-clock-Fix-early-boot-preempt-assumption-in-__s.patch][4.11]]

		在系统初始阶段调用`local_irq_disable()`来禁止中断和抢占，保护读取sch->tick* 的准确性。

		BUG: using smp_processor_id() in preemptible [00000000] code: swapper/0/1
		caller is debug_smp_processor_id+0x1c/0x1e
		CPU: 0 PID: 1 Comm: swapper/0 Not tainted 4.12.0-rc2-00108-g1c3c5ea #1
		Call Trace:
		dump_stack+0x110/0x192
		check_preemption_disabled+0x10c/0x128
		? set_debug_rodata+0x25/0x25
		debug_smp_processor_id+0x1c/0x1e
		sched_clock_init_late+0x27/0x87

		在Call Trace中可以看到启动阶段进行抢占禁止检测时，调用了dump_stack(),出现警告信息。
