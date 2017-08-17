


1. `[  4.11 ] [[file:4.11/0001-sched-clock-Fix-early-boot-preempt-assumption-in-__s.patch][4.11]]{C::bug::crash::preempt::irq::disabling irqs}`

	- 在系统初始阶段调用`local_irq_disable()`来禁止中断和抢占，保护读取sch->tick* 的准确性，


- `[   4.9 -   4.11] [[file:4.9/peterz-percpu-rwsem-rt.patch][4.9]]{C::bug::crash::preempt::preempt::remove preempt_disable variants}`
	
		/*
		 * We are in an RCU-sched read-side critical section, so the writer
		 * cannot both change sem->state from readers_fast and start checking
		 * counters while we are here. So if we see !sem->state, we know that
		 * the writer won't be checking until we're past the preempt_enable()
		 * and that one the synchronize_sched() is done, the writer will see
		 * anything we did within this RCU-sched read-size critical section.
		 * 
		 */	
		将percpu_down_read_preempt_disable()替换为percpu_down_read(),在percpu_down_read()中
		增加了preempt_disable/enable()对，增加了-RT的实时性，其实感觉此处不应算作bug，可以看做
		feature/performance.		
	

- `[   4.6 -   4.11][[file:4.6/drmradeoni915_Use_preempt_disableenable_rt()_where_recommended.patch][4.6]]{C::bug::deadlock::preempt::preempt::add preempt_disable/enable_rt() where recommended}`

	此处主要是`local_irq_disable()`替代为`local_lock_irq()`,根据在-RT下源代码（！RT下后者宏定义为前者）可以知道
		
		---------------local_irq_disable()源代码---------------------------
		#define local_irq_disable() \
    		do { raw_local_irq_disable(); trace_hardirqs_off(); } while (0)
		
		static inline void raw_local_irq_disable(void){  native_irq_disable(); }

		static inline void native_irq_disable(void){    asm volatile("cli": : :"memory");}

		---------------local_lock_irq()源代码---------------------------
		#define local_lock_irq(lvar)						\
			do { __local_lock_irq(&get_local_var(lvar)); } while (0)
		
		static inline void __local_lock_irq(struct local_irq_lock *lv)
			{
			spin_lock_irqsave(&lv->lock, lv->flags);
			LL_WARN(lv->owner);
			LL_WARN(lv->nestcnt);
			lv->owner = current;
			lv->nestcnt = 1;
			}
		static void spin_lock_irqsave(spinlock_t *lock, unsigned long f)
			{
				spin_lock(lock);
			}
		可以看出，前者禁止了本地中断，而后者没有禁止本地中断，只是获取了spin_lock()


- `[   3.8 -   4.11][[file:3.8/net-fix-iptable-xt-write-recseq-begin-rt-fallout.patch][3.8]]{C::bug::data_err::order::order::net: netfilter: Serialize xt_write_recseq sections on RT}`

	此处是netfilter在！RT中，需要`local_bh_disable()`对`xt_write_recseq`的隐含序列化，而在RT中则需要通过local_lock()进行明确的序列化。

- `[3.6 -   4.11][[file:3.6/softirq-preempt-fix-3-re.patch][3.6]]{C::bug::rtlatency::preempt::semantics::check preemption after reenable interrupts}`

	此处是避免在函数`raise_softirq_irqoff()(禁用中断，唤醒软中断)`以后，重新使能中断时被抢占，造成软中断线程被无限延迟，因此在调用`raise_softirq_irqoff()`并使能中断`local_irq_enable/restore`以后，在RT中增加`preempt_check_resched_rt（）`检查是否有抢占。
	
- `[   3.6 -   4.11][[file:3.6/upstream-net-rt-remove-preemption-disabling-in-netif_rx.patch][3.6]]{C::bug::crash::atomicity::preempt::replace with migration disable}`

		此处实际是preempt_disable/enable替换为migration_disable/enable()，解决了RT-kernel两
		个方面的问题：（1）实时性：对于enqueue_to_backlog()只需要保证不被迁移，不需要禁止抢占。
		（2）在RT上，禁止抢占的情况下调用enqueue_to_backlog()，可能产生重新调度，这在原子上下文是不允许的。

		内核的一个基本原则就是：在中断或者说原子上下文中，内核不能访问用户空间，而且内核是不能 
		睡眠的。也就是说在这种情况下，内核是不能调用有可能引起睡眠的任何函数。一般来讲原子上下
		文指的是在中断或软中断中，以及在持有自旋锁的时候。内核提供 了四个宏来判断是否处于这几种情况里：
		#define in_irq()     (hardirq_count()) //在处理硬中断中
		#define in_softirq()     (softirq_count()) //在处理软中断中
		#define in_interrupt()   (irq_count()) //在处理硬中断或软中断中
		#define in_atomic()     ((preempt_count() & ~PREEMPT_ACTIVE) != 0) 

- `[   3.4 -   4.11][[file:3.4/fs-dcache-use-cpu-chill-in-trylock-loops.patch][3.4]]{C::bug::hang::preempt::preempt::use cpu_chill instead}`

	此处为了避免RT中Retry loops forever when the modifying side was preempted,用`cpu_chill()`代替`cpu_relax()` on RT：`cpu_chill()`会睡眠一秒钟

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


- `[   3.4 -   4.11][[file:3.4/net-use-cpu-chill.patch][3.4]]{C::bug::hang::preempt::preempt::use cpu_chill instead}`

	与上一个补丁功能类似。


- `[   3.2 -   4.11][[file:3.2/arm-convert-boot-lock-to-raw.patch][3.2]]{C::bug::crash::preempt::preempt::replace with raw}`

	此处是将`spin_lock()`转换成`raw_spin_lock()`：因为`idle_sched_class->enqueue_task == null`,因此，当空闲任务在该锁上阻塞时，将不能被唤醒。


- `[   3.0 -   4.11][[file:3.0/md-raid5-percpu-handling-rt-aware.patch][3.0]]{C::bug::crash::preempt::preempt::add locks, and replace with _light to keep serialized}`
	
	- 此处是将`get_cpu()转换成get_cpu_light()`实质上是`preempt_disable->migration_disable`,目的是：（1）实时性：增加可抢占区域。（2）在RT上，禁止抢占的情况下（原子上下文），如果产生重新调度，或者获取睡眠锁，这在原子上下文是不允许的。并且此处在替换为`migration_diable`后增加了`spin_lock()`是为了避免在current CPU上产生抢占或中断，对`per_cpu`产生影响。
	
	- 因此，对于`per_CPU`相关的由`preempt_disable->migration_disable`，在对`per_cpu` var操作时，都应该增加相应的睡眠锁进行互斥保护。








- `[2.6.22 - 2.6.26][[file:2.6.22/preempt-realtime-powerpc-b2.patch][2.6.22]]{C::bug::crash::preempt::preempt::replace with raw}`

	此处是在`spin_lock()`转换成`raw_spin_lock()`修复entry_64.s产生的警告或错误。


- `[   3.2 -    3.8][[file:3.2/intel_idle-convert-i7300_idle_lock-to-raw-spinlock.patch][3.2]]{C::bug::crash::atomicity::preempt::replace with raw}`

	
	- 此处是在idle thread中将`idle_lock`由`spin_lock()`转换成`raw_spin_lock()`，因为在空闲任务中，调度队列为空，当获取`spin_lock`产生阻塞时，不能再次产生调度，唤醒idle thread。
	

- `[   3.2         ][[file:3.2/printk-disable-migration-instead-of-preemption.patch][3.2]]{C::bug::crash::preempt::preempt::replace preempt_disable with migrate_disable}`

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
	同时调用了`raw_local_irq_save(flags);与spin_lock(&logbuf_lock)`;因此直接调用`migration_disable`已经足够，并且持有睡眠锁，在原子上下文中是不允许的。	
	

- `[   3.4 -   3.12][[file:3.4/rfc-sched-rt-fix-wait_task_interactive-to-test-rt_spin_lock-state.patch][3.4]]{C::bug::data_err::preempt::preempt::add state check}`

	此处是当任务调用`wait_task_interactive()`时，它会等待另一个任务到达某一状态时，但是这里并没有考
	虑到，在RT中`rt_spin_lock`会改变真是的任务状态（当等待的任务被阻塞，并等待唤醒），因此会返回不正确的结果。这里是通过`rt_spin_lock`来保存任务状态，然后通过`wait_task_interactive()`进行检查。	

- `[[file:2.6.22/clockevents-fix-resume-logic.patch][2.6.22]] {C::bug::idle::order::sync::resume clockevent device before resume tick}`


	- clock event mode的定义如下：
	
			enum clock_event_mode { 
			    CLOCK_EVT_MODE_UNUSED = 0, －－－－－－未使用 
			    CLOCK_EVT_MODE_SHUTDOWN, －－－－－－被软件shutdown 
			    CLOCK_EVT_MODE_PERIODIC, －－－－－－－工作状态，处于periodic模式，周期性产生event 
			    CLOCK_EVT_MODE_ONESHOT, －－－－－－－工作状态，处于one shot模式，event是一次性的 
			    CLOCK_EVT_MODE_RESUME, －－－－－－－处于系统resume中 
			};

	- 增加了clock event mode 用来在系统处于空模式的C-states状态恢复过程中的恢复顺序，确保clockevent devices在tick之前被重新启动，避免定时器中断产生，而clock event devices还没有恢复。2.6.23版本以后，该补丁被删除。

- `[[file:2.6.22/cpuidle_hang_fix.patch][2.6.22]]{C::bug::hang::order::sync::idle handler to enable intr before returning from idle handler, set current driver to NULL when fail to attach on all devices}`

	此处是为了阻止当ACPI处理器驱动被增加到一个不支持C-states的系统中，x86-64挂起。
	x86-64希望所有的空操作在返回之前都能够在使能中断。因此，这里通过增加else语句，来使能本地中断。

		

- `[  3.14 -   3.18][[file:3.14/net-ip_send_unicast_reply-add-missing-local-serializ.patch][3.14]]{C::bug::data_err::order::mutex::net: ip_send_unicast_reply: add missing local serialization}`

	- 此处是用`get_locked_var()`代替了`get_cpu_light();和__get_cpu_var();`

			# define get_local_ptr(var) ({	\
			migrate_disable();	\
			this_cpu_ptr(var);	})

			commit中提到此处是为了实现两个功能：

			The per-cpu here thus is assuming exclusivity serializing per cpu - so
			the use of get_cpu_ligh introduced in
			net-use-cpu-light-in-ip-send-unicast-reply.patch, which droped the
			preempt_disable in favor of a migrate_disable is probably wrong as this
			only handles the referencial consistency but not the serialization. To
			evade a preempt_disable here a local lock would be needed.
			
			Therapie:
				 * add local lock:
				 * and re-introduce local serialization:
			对于get_cpu_light()已经是替换了get_cpu()去掉了preempt_disable(),
			get_locked_var()可能更多地完成 re-introduce local serialization:而且，
			此处后续对per_cpu* 操作应该增加其他锁来防止并发（本地进程上下文和中断上下文）


- `[  3.12 -    4.8][[file:3.12/hwlat-detector-Use-trace_clock_local-if-available.patch][3.12]]{C::bug::data_err::order::semantics::hwlat-detector: Use trace_clock_local if available}`

			u64 notrace trace_clock_local(void)
			{
				u64 clock;
			
				/*
				 * sched_clock() is an architecture implemented, fast, scalable,
				 * lockless clock. It is not guaranteed to be coherent across
				 * CPUs, nor across CPU idle events.
				 */
				preempt_disable_notrace();
				clock = sched_clock();
				preempt_enable_notrace();
			
				return clock;
			}
			
			static inline void preempt_disable_notrace(void)
				{
					preempt_disable();
				}

			ktime_t ktime_get(void)
				{
					struct timekeeper *tk = &tk_core.timekeeper;
					unsigned int seq;
					ktime_t base;
					u64 nsecs;
				
					WARN_ON(timekeeping_suspended);
				
					do {
						seq = read_seqcount_begin(&tk_core.seq);
						base = tk->tkr_mono.base;
						nsecs = timekeeping_get_ns(&tk->tkr_mono);
				
					} while (read_seqcount_retry(&tk_core.seq, seq));
				
					return ktime_add_ns(base, nsecs);
				}
			这里是在调用ktime_get()时获取的是read_seq(),防止其他CPUs抢占read_seq(),
			对获取的time有影响，因此在available的地方选用trace_clock_local(void)
- `[   3.8         ][[file:3.8/fix-2-2-slub-tid-must-be-retrieved-from-the-percpu-area-of-the-current-processor.patch][3.8]]{C::bug::data_err::preempt::preempt::slub: Tid must be retrieved from the percpu area of the current proces}`

	此处加入`preempt_disable()`是为了避免在获取`Per_CPU`指针之后，对tid检查之前，被调度到其他CPU上，从而破坏了current `Per_CPU` var，但是在随后的补丁中去除了该补丁。在目前最新的内核中，并没有添加任何的限制，而是把Per_CPU指针和tid检查顺序调整了，并给出这样的commit：

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


- `[   3.0         ][[file:3.0/drivers-dca-convert-dcalock-to-raw.patch][3.0]]{C::bug::deadlock::preempt::preempt::replace with raw}`

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
		
	从源代码中可以看出在RT中`spin_lock_irqsave(lock, flags)`并没有禁止中断。
			

- `[2.6.29         ][[file:2.6.29/x86-pae-preempt-realtime-fix.patch][2.6.29]]{C::bug::crash::preempt::preempt::add preempt_disable protect}`

	此处在RT中，添加preempt_disable/enable()保护临界区资源。后续patch可能有更好办法。

- `[[file:2.6.29/sched-generic-hide-smp-warning.patch][2.6.29]]{C::bug::crash::preempt::preempt::use preempt_disable() to supress waring message}`

	此处增加`preempt_disable/enable()`来保护`per_CPU `var,后续的patch可能有更好的办法。

- `[[file:2.6.26/nfs-stats-miss-preemption.patch][2.6.26]]{C::bug::rtlatency::preempt::preempt::nfs: fix missing preemption check}`

	`get_cpu()/put_cpu_no_preempt()->get_cpu()/put_cpu()`这里是一种对可抢占的一种优化，避免高优先级的任务长时间的延迟。

- `[[file:2.6.26/ftrace-wakeup-rawspinlock.patch][2.6.26]]{C::bug::hang::preempt::preempt::ftrace: user raw spin lock for wakeup function trace}`
	
	此处是在fix RT中的`spin_lock`，因此用原始自旋锁代替`spin_lock`

-  `[2.6.22         ] [[file:2.6.22/module-pde-race-fixes.patch][2.6.22]] {C::bug::crash::order::sync::module reloaded when still need to be used, add a atomic counter to counting reads and writes in progress}`

	

* `[2.6.22         ] [[file:2.6.22/s_files-proc-generic-fix.patch][2.6.22]] {C::bug::na::order::sync::advance filevec_add_drain_all()}`

	此处变换了函数的位置

* `[2.6.22 - 2.6.24] [[file:2.6.22/rcu-preempt-fix-nmi-watchdog.patch][2.6.22]]{C::bug::irq::preempt::preempt::not NMI-safe,replace atomic_notifier_call_chain to raw_...}`

	此处是在RT上将`atomic_notifier_call_chain()->raw notifier_call_chain()` for rcu_lock()/unlock，在RT上需要作如此改变。

	原子通知链（ Atomic notifier chains ）：通知链元素的回调函数（当事件发生时要执行的函数）在中断或原子操作上下文中运行，不允许阻塞。

				struct atomic_notifier_head {
		        spinlock_t  lock;
		        struct  notifier_block *head;
				};
	原始通知链（ Raw notifierchains ）：对通知链元素的回调函数没有任何限制，所有锁和保护机制都由调用者维护。
	
	

* [2.6.22 - 2.6.25][[file:2.6.22/rcu-various-fixups.patch][2.6.22]] {C::bug::crash::preempt::preempt::add rcu_read lock pair}

	增加`rcu_read_lock`和`rcu_read_unlock`，这两个函数用来标记一个RCU读过程的开始和结束。其实作用就是帮助检测宽限期是否结束。

* [2.6.22 - 2.6.25] [[file:2.6.22/tasklet-more-fixes.patch][2.6.22]]{C::bug::crash::order::sync::add statement}

	此处通过增加检查（或循环检查）避免tasklet在上锁之后，增加到队列之前被竞争，并且避免队列中没有
	scheduled tasklets。

* [2.6.22 - 2.6.25] [[file:2.6.22/preempt-irqs-ppc-celleb-beatic-eoi.patch][2.6.22]]{C::bug::hang::order::order::restore preempt_none method}

	此处恢复preempt_none method 来修复kernel hang

* [2.6.22 - 2.6.26] [[file:2.6.22/nf_conntrack-fix-smp-processor-id.patch][2.6.22]] {C::bug::data_err::preempt::preempt::replace with raw}

	修复了在SMP上`get_cpu_var()`

* [2.6.22 - 2.6.26] [[file:2.6.22/preempt-realtime-powerpc-b4.patch][2.6.22]]{C::bug::crash::preempt::preempt::preempt_disable added}

	此处增加`preempt_disable/enable()来保护per_cpu` var

* [2.6.22 - 2.6.26] [[file:2.6.22/preempt-realtime-powerpc-b2.patch][2.6.22]] {C::bug::crash::preempt::preempt::replace with raw}


	在RT上用`raw_spin_lock代替spin_lock`来修复警告或错误。



* [2.6.22 - 2.6.26] [[file:2.6.22/s_files-pipe-fix.patch][2.6.22]] {C::bug::data_err::order::sync::add cleanup var}

	此处是确保在文件之前释放inode

* [2.6.22 - 2.6.29] [[file:2.6.22/fix-emergency-reboot.patch][2.6.22]]{C::bug::hang::preempt::preempt::add emergency restart}

	此处如果处在可抢断环境中，增加reboot notifier list的调用，解决reboot 问题 

* [2.6.23 - 2.6.24] [[file:2.6.23/rt-wakeup-fix.patch][2.6.23]] {C::bug::rtlatency::preempt::preempt::move a section of code up}

 	此处是一个唤醒修复操作在RT

* [2.6.24 - 2.6.25] [[file:2.6.24/kvm-lapic-migrate-latency-fix.patch][2.6.24]]{C::bug::crash::preempt::semantics::move the apic timer migration}

	在RT-preempt，移动`kvm_migrate_apic_timer()`修复在等待队列中可能产生的sleeps。

* [2.6.24 - 2.6.26] [[file:2.6.24/rt-workqueue-barrier.patch][2.6.24]] {C::bug::rtlatency::order::sync::The solution used is to nest plist structures.}

	此处通过fix barrier stack of run_workqueue ,to avoid callstack nesting.

* [2.6.24 - 2.6.26] [[file:2.6.24/rt-wq-barrier-fix.patch][2.6.24]]{C::bug::rtlatency::order::sync::using a wait_queue to target at a worklet in a nested list}

	此处用`wait_queue()`代替wait_on_work(),避免worklet in nested list complete too late.

* [2.6.24 - 2.6.26] [[file:2.6.24/rcu-preempt-boost-fix.patch][2.6.24]] {C::bug::deadlock::preempt::preempt::add careful checks}

	此处是对`rcu-preempt-boost`的修复，通过增加检查

* [2.6.25         ] [[file:2.6.25/pcounter-percpu-protect.patch][2.6.25]] {C::bug::data_err::preempt::preempt::add protection to per_cpu variables in pcounter addition}

 	此处增加`preempt_disable/enable()`来保护`per_cpu`变量

* [2.6.25 - 2.6.26] [[file:2.6.25/genhd-protect-percpu-var.patch][2.6.25]] {C::bug::data_err::preempt::preempt::protect use of smp_processor_id in genhd.h with preempt disable}

	此处是增加`preempt_disable/enable()`保护`per_cpu` var在以后的patch中会有新的方法。

* [2.6.25 - 2.6.26] [[file:2.6.25/nmi-watchdog-fix-1.patch][2.6.25]]{C::bug::crash::order::order::send NMI after nmi_show_regs on}

	`nmi_watchdog`用于检测内核中关中断死锁(也称硬死锁)的情况，是调测内核死机或死锁问题的一大利器。内核中，如果代码编写不好可能会出现关中断死锁的情况，即进入内核态后，关中断，然后在内核态中死锁，或长时间运行，导致该CPU无法响应中断(因为中断已关)，也无法得到调度(对于没有启用内核抢占的内核来说)，外在表现可能为系统挂死、无法ping通、没有响应。而`nmi_watchdog`正是针对这种情况而设计的。
	其基本原理为：注册nmi中断(3号中断)，为不可屏蔽中断，由硬件定期触发(通过性能计数器)。在时钟中断中更新相关计数器，在nmi中断处理中，判断相关计数器是否更新，如果超过5s(默认情况下)没有更新，则触发`nmi_watchdog`，默认情况下，最终会进入panic流程。  

	此处是确保 send NMI 在nmi_show_regs 之后

* `[2.6.25 - 2.6.26] [[file:2.6.25/nmi-watchdog-fix-4.patch][2.6.25]]{C::bug::crash::order::order::clear nmi_show_regs after show_regs() is called}`

  	此处是确保:clear `nmi_show_regs 在 show_regs()`之后

* `[2.6.25 - 2.6.26][[file:2.6.25/nmi-watchdog-fix-3.patch][2.6.25]]{C::bug::crash::order::order::change nmi_watchdog fucntion}`

	此处是对RT kernel nmi-watchdog 不能立即返回lockup info 的修复。


* `[2.6.25 - 2.6.26] [[file:2.6.25/cycles-to-ns-trace-fix.patch][2.6.25]] {C::bug::data_err::time::preempt::preempt disable for getting time}`

		此处增添了preempt_disable/enable_notrace()函数对，preempt_disable/enable_notrace()的
		实际代码就是preempt_count + 1,增加preempt_disable 的嵌套层数，保护time获取值的准确性，后续补丁可能有更好方法。
		#define add_preempt_count_notrace(val)			\
		do { preempt_count() += (val); } while (0)

* `[2.6.26         ] [[file:2.6.26/ppc64-fix-preempt-unsafe-paths-accessing-per_cpu-variables.patch][2.6.26]]{C::bug::data_err::preempt::preempt::Fix preempt unsafe paths accessing per_cpu variables}`

  	以前用`spin_lock`保护的`per_CPU`变量，但在RT中，`spin_lock`进程照样会睡眠，然后调度到别的CPU上。因此，引入了一个新的宏来定义一种可以锁住的`per_CPU`变量。`DEFINE_PER_CPU_LOCKED`，就是这样的宏，通过`get_cpu_var_locked`来操作`per_CPU`变量。在后续的patch中去除了该宏和函数，

