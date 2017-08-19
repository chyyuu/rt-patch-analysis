

- pattern 1

	- `atomic_notifier_call_chain()替换为raw notifier_call_chain()`

		
	- 此处是在RT上将`atomic_notifier_call_chain()->raw notifier_call_chain() `说是为了避免not `NMI_safe` in -rt。从源代码看，`atomic_notifier_call_chain()调用了rcu_read_lock()->preempt_disable()为什么会产生not NMI_safe不大理解？？`

	- 原子通知链(Atomic notifier chains)：通知链元素的回调函数（当事件发生时要执行的函数）在中断或原子操作上下文中运行，不允许阻塞。

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


	- 原始通知链(Raw notifierchains)：对通知链元素的回调函数没有任何限制，所有锁和保护机制都由调用者维护。

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
			        int nr_to_call, int *nr_calls)
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




- 相关patch
		
	-  [[file:2.6.22/rcu-preempt-fix-nmi-watchdog.patch][2.6.22]]
	
	
- pattern 2
	
	- `raw_local_irq_save() 替换local_irq_save()`
	- [[file:2.6.22/rt-mutex-core.patch][2.6.22]]在这个patch中对这两个宏做了定义，但不明白为什么产生了互相调用，可能跟配置有关系，但是怎么会互相调用？
	
	- 相关patch 
		- [[file:2.6.22/arm-fix-atomic-cmpxchg.patch][2.6.22]]
	
		

- pattern 3

	- `__get_cpu_var()替换为__raw_get_cpu_var()`

			#define __get_cpu_var(var)         per_cpu__##var
 			#define __raw_get_cpu_var(var)         per_cpu__##var
	
	-  在[[file:2.6.22/percpu-locked-mm.patch][2.6.22]] 对两个宏进行了定义，并没有变化，只是重构了一下
	-  相关patch 
		-  [[file:2.6.22/nf_conntrack-fix-smp-processor-id.patch][2.6.22]]
	

- pattern 4

	- 增加`preempt_disable/enable()来保护per_cpu` var
	
	- 此处的commit：BUG: using `smp_processor_id()` in preemptible [00000000] code: khvcd/280 caller is .xmon_core+0xb8/0x8ec
	- 可见这里是在可抢占区域中操作了`per_cpu`var,引入的bug。
	- 相关patch：
		-  [[file:2.6.22/preempt-realtime-powerpc-b4.patch][2.6.22]]
		- [[file:3.8/fix-2-2-slub-tid-must-be-retrieved-from-the-percpu-area-of-the-current-processor.patch][3.8]]

- pattern 5
	- `raw_spin_lock代替spin_lock`
	- 此处是在rt中对引入`spin_lock`的修复。因为`raw_spin_lock`是原始自旋锁，并不会引起抢占睡眠，而`spin_lock`在RT中是睡眠锁，在原子上下文，中断上下文，抢占禁止上下文是不可以调用的。
	- 相关patch
		- [[file:2.6.22/preempt-realtime-powerpc-b2.patch][2.6.22]]
		- [[file:2.6.25/pcounter-percpu-protect.patch][2.6.25]]
		- [[file:2.6.25/genhd-protect-percpu-var.patch][2.6.25]]
		- [[file:2.6.29/sched-generic-hide-smp-warning.patch][2.6.29]]

- pattern 6
	- 关于实时唤醒，跟RT相关性很大，但是没有看懂

		    +        * Sync wakeups (i.e. those types of wakeups where the waker
		    +        * has indicated that it will leave the CPU in short order)
		    +        * don't trigger a preemption, if the woken up task will run on
		    +        * this cpu. (in this case the 'I will reschedule' promise of
		    +        * the waker guarantees that the freshly woken up task is going
		    +        * to be considered on this CPU.)
	
	- 相关patch
		- [[file:2.6.23/rt-wakeup-fix.patch][2.6.23]]

- pattern 7
	- 在RT-preempt，修复在等待队列中可能产生的sleeps。
	
			Move apic timer migration to a place where it does not cause the
			"might sleep while atomic" check. The original place calls 
			hrtimer_cancel in a preempt disabled region, which is fine in mainline,
			but preempt-rt changes hrtimer_cancel, that the caller sleeps on a
			wait_queue, when the callback of the timer is currently active. 
	
	- 这里是将回调函数可能引起在原子上下文中睡眠的函数migration other place。


	- 相关patch 
		- [[file:2.6.24/kvm-lapic-migrate-latency-fix.patch][2.6.24]]

- pattern 8
	- `用get_cpu_var_locked()替换__get_cpu_var()`
	-  `用get_cpu_var() 替换preempt_disable;__get_cpu_var()`
    
			#define get_cpu_var_locked(var, cpuptr)         \
			(*({                            \
			    int __cpu = raw_smp_processor_id();     \
			                            \
			    *(cpuptr) = __cpu;              \
			    spin_lock(&__get_cpu_lock(var, __cpu));     \
			    &__get_cpu_var_locked(var, __cpu);      \
			}))
						
			#define __per_cpu_var_lock_var(var) per_cpu__##var##_locked
			
			#define get_cpu_var(var) (*({               \
			    extern int simple_identifier_##var(void);   \
			    preempt_disable();              \
			    &__get_cpu_var(var); }))
		
	- 从他们的API可以看出`get_cpu_var_locked()`获取spin_lock(), 而`get_cpu_var()禁止了抢占`从而保护Percpu var.
	- 相关patch
			- [[file:2.6.26/ppc64-fix-preempt-unsafe-paths-accessing-per_cpu-variables.patch][2.6.26]]

- pattern 9
	- `用raw_local_irq_save();__raw_spin_lock()代替 spin_lock_irqsave()` 
	- `用local_irq_save(); __raw_spin_lock()代替 spin_lock_irqsave()`
	
			 # define raw_local_irq_save(flags)     \
		    do {                    \
		        BUILD_CHECK_IRQ_FLAGS(flags);   \
		        local_irq_save(flags);      \
		    } while (0)

				#define local_irq_save(flags) \
			do {					\
				BUILD_CHECK_IRQ_FLAGS(flags);	\
				raw_local_irq_save(flags);	\
				trace_hardirqs_off();		\
			} while (0)

	- 在RT中`spin_lock_irqsave()`并没有禁止中断，只是获取了`spin_lock()`,但不明白禁止中断在这里有什么关系。
	
	- 相关patch
		- [[file:2.6.26/ftrace-wakeup-rawspinlock.patch][2.6.26]]

- pattern 10
	-  `get_cpu()/put_cpu_no_preempt()替换为get_cpu()/put_cpu()`
	-  因为对于`put_cpu_no_preempt()`并没有进行preemption检查，从而产生抢占调度，这样有可能对高优先级任务造成长时间延迟，需要将其替换。
	- 相关patch
		-  [[file:2.6.26/nfs-stats-miss-preemption.patch][2.6.26]]

- pattern 11
	- 添加preempt_disable/enable()保护临界区资源
	- 相关patch
		- [[file:2.6.29/x86-pae-preempt-realtime-fix.patch][2.6.29]]

- pattern 12
	- `用raw_spin_lock_irq_save()替换spin_lock_irqsave()`

			call trace 信息	[   25.607517] igb 0000:01:00.0: DCA enabled
	   						[   25.607524] BUG: sleeping function called from invalid context at kernel/rtmutex.c:684
	- 从call trace可以看出是调用了睡眠函数，产生bug，分析这两个API源代码：
			
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
	`raw_spin_lock_irq_save()`禁止了中断、抢占。
	- 相关patch
		- [[file:3.0/drivers-dca-convert-dcalock-to-raw.patch][3.0]]



- pattern 14
	- `get_cpu()转换成get_cpu_light()`
	
	- 此处实际上是`preempt_disable()---->migration_disable()`在RT中增加抢占区域，同时避免在抢占禁止的情况下获取睡眠锁。
	- `smp_processor_id()` is safe if it's used in a preemption-off critical section, or in a thread that is bound to the current CPU.可以看出`smp_processor_id()`只要保证调用它的线程不被迁移到其他CPU上就可以，因此完全可以用`get/put_cpu_light`来替换`get/put_cpu`增加可抢占区域。对于-RT来说，`get_cpu()`既禁止了抢占，又可能对随后分配的可睡眠锁产生问题，因此选用只是禁止了迁移的get_cpu_light更加合适。
	- [[file:3.0/md-raid5-percpu-handling-rt-aware.patch][3.0]]

- pattern 15
	- `preemption_diable替换为migration_disable`
	- 对于vprintk函数，禁用迁移已经足够
	- 相关patch
		- [[file:3.2/printk-disable-migration-instead-of-preemption.patch][3.2]]



- pattern 16
	- `spin_lock()转换成raw_spin_lock()`
	- 因为`idle_sched_class->enqueue_task == null`,因此，当空闲任务在该锁上阻塞时，队列任务为空，将不能再次被唤醒（应该是这样）。
	- 相关patch
		- [[file:3.2/arm-convert-boot-lock-to-raw.patch][3.2]]



- pattern 17
	- `cpu_chill()代替cpu_relax()`
	- 此处为了避免RT中Retry loops forever when the modifying side was preempted,用`cpu_chill()`	代替`cpu_relax()` on RT：`cpu_chill()`会睡眠一秒钟

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
	
	- 相关patch	
		- [[file:3.4/net-use-cpu-chill.patch][3.4]]
		- [[file:3.4/fs-dcache-use-cpu-chill-in-trylock-loops.patch][3.4]]
	

- pattern 19
	- RT中增加`preempt_check_resched_rt（）`检查是否有抢占。
	- 此处是避免在函数`raise_softirq_irqoff()(禁用中断，唤醒软中断)`以后，重新使能中断时被抢占，
	造成软中断线程被无限延迟，因此在调用`raise_softirq_irqoff()`并使能中断`local_irq_enable/
	restore`以后，在RT中增加`preempt_check_resched_rt（）`检查是否有抢占。
	- 相关patch
		- [[file:3.6/softirq-preempt-fix-3-re.patch][3.6]]

- pattern 20
	- 此处添加了`preempt_disable/enable_rt()`
		
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
	之所以加入`preempt_disable/enable_rt()`从以上的定义中可以看出，有些在RT中是需要禁止抢占，而在!RT中可能是不需要的。这里是在RT为了保证`ktime_get()`获取的准确性，增加`preempt_disable/enable_rt()`禁止在调用函数期间被其他CPU抢占。
	- 相关patch
		- [[file:4.6/drmradeoni915_Use_preempt_disableenable_rt()_where_recommended.patch][4.6]]
- pattern 21
	- 将`percpu_down_read_preempt_disable()替换为percpu_down_read()`
	- 在`percpu_down_read()中	增加了preempt_disable/enable()对`，在`percpu_down_read_preempt_disable()`只有`preempt_disable()`需要在其他地方`percpu_down_read_preempt_enable()`来使能抢占，故对于此处可以减少不可抢占区域，增加了-RT的实时性，其实感觉此处不应算作bug，可以看做feature/performance.
	
			/*
				 * We are in an RCU-sched read-side critical section, so the writer
				 * cannot both change sem->state from readers_fast and start checking
				 * counters while we are here. So if we see !sem->state, we know that
				 * the writer won't be checking until we're past the preempt_enable()
				 * and that one the synchronize_sched() is done, the writer will see
				 * anything we did within this RCU-sched read-size critical section.
				 * 
				 */	
 
	- 相关patch
		- [[file:4.9/peterz-percpu-rwsem-rt.patch][4.9]]



- pattern 22
	- 在系统初始阶段调用`local_irq_disable()`来禁止中断和抢占，保护读取sch->tick* 的准确性。

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
	- 相关patch
		- [[file:4.11/0001-sched-clock-Fix-early-boot-preempt-assumption-in-__s.patch][4.11]]
