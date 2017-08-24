-  `preempt_disable/enable` （实时与非实时并没有区别）

			#ifdef CONFIG_PREEMPT_COUNT
			
			#define preempt_disable() \
			do { \
				preempt_count_inc(); \
				barrier(); \
			} while (0)

			#define preempt_count_inc() preempt_count_add(1)

			void preempt_count_add(int val)
				{
				#ifdef CONFIG_DEBUG_PREEMPT
					/*
					 * Underflow?
					 */
					if (DEBUG_LOCKS_WARN_ON((preempt_count() < 0)))
						return;
				#endif
					__preempt_count_add(val);
				#ifdef CONFIG_DEBUG_PREEMPT
					/*
					 * Spinlock count overflowing soon?
					 */
					DEBUG_LOCKS_WARN_ON((preempt_count() & PREEMPT_MASK) >=
								PREEMPT_MASK - 10);
				#endif
					preempt_latency_start(val);
				}

				static __always_inline void __preempt_count_add(int val)
					{
						*preempt_count_ptr() += val;
					}
				static __always_inline volatile int *preempt_count_ptr(void)
				{
					return &current_thread_info()->preempt_count;
				}

	
	- 最终是对当前线程的中`current_thread_info()->preempt_count++`；注意`preempt_count`是`per_cup-var`.
	- 可能对于RT与！RT更多的会使用以下定义：

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

				critical section（N）：不能保护临界区，不能禁止本地中断或其他CPU上的进程（或中断）对临界区的访问
				uninterrupt（N）:
				nopreempt （Y）：
				nomigrate （Y）：禁止抢占，同时禁止了迁移
				nosfotirq （N）： 
				sleep/sched（N）：原子上下文不允许调度或睡眠

	

- `migrate_disable/enable `		

			void migrate_disable(void)
			{
				struct task_struct *p = current;
			
				if (in_atomic() || irqs_disabled()) {
			#ifdef CONFIG_SCHED_DEBUG
					p->migrate_disable_atomic++;
			#endif
					return;
				}
			#ifdef CONFIG_SCHED_DEBUG
				if (unlikely(p->migrate_disable_atomic)) {
					tracing_off();
					WARN_ON_ONCE(1);
				}
			#endif
			
				if (p->migrate_disable) {
					p->migrate_disable++;
					return;
				}
			
				/* get_online_cpus(); */
			
				preempt_disable();
				preempt_lazy_disable();
				pin_current_cpu();
				p->migrate_disable = 1;
			
				p->cpus_ptr = cpumask_of(smp_processor_id());
				p->nr_cpus_allowed = 1;
			
				preempt_enable();
			}
			EXPORT_SYMBOL(migrate_disable);

	- 线程迁移必须满足几个条件：
		
		- 线程必须不是正在运行。

	- 禁止抢占能够禁止迁移是否是因为：
		- 禁止了抢占，当前线程不能被抢占阻塞，因此会一直运行，直到能够阻塞，主动让出CPU或允许抢占为止，因此cpu不能主动迁移线程。？？



