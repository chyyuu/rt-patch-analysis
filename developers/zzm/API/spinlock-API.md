- `spin_lock/unlock `（RT与!RT不同）
	- ！RT中的`spin_lock/unlock `

			static __always_inline void spin_lock(spinlock_t *lock)
			{
				raw_spin_lock(&lock->rlock);
			}

			static __always_inline void spin_unlock(spinlock_t *lock)
			{
				raw_spin_unlock(&lock->rlock);
			}
	
			#define raw_spin_lock(lock)	_raw_spin_lock(lock)
			#define raw_spin_unlock(lock)	_raw_spin_unlock(lock)

			#ifndef CONFIG_INLINE_SPIN_LOCK
			void __lockfunc _raw_spin_lock(raw_spinlock_t *lock)
			{
				__raw_spin_lock(lock);
			}

			#ifdef CONFIG_UNINLINE_SPIN_UNLOCK
			void __lockfunc _raw_spin_unlock(raw_spinlock_t *lock)
			{
				__raw_spin_unlock(lock);
			}

			static inline void __raw_spin_lock(raw_spinlock_t *lock)
			{
				preempt_disable();
				spin_acquire(&lock->dep_map, 0, 0, _RET_IP_);
				LOCK_CONTENDED(lock, do_raw_spin_trylock, do_raw_spin_lock);
			}
			
			#endif /* !CONFIG_GENERIC_LOCKBREAK || CONFIG_DEBUG_LOCK_ALLOC */
			
			static inline void __raw_spin_unlock(raw_spinlock_t *lock)
			{
				spin_release(&lock->dep_map, 1, _RET_IP_);
				do_raw_spin_unlock(lock);
				preempt_enable();
			}

		
		- 从源代码可以看出，!RT中的spin_lock()直接调用了原始自旋锁，即自旋锁最多只能被一个可执行线程持有。并且显示的调用了`preempt_disable/enable()`
		- 如果一个执行线程试图获得一个已被持有的自旋锁，那么该线程就会一直进行忙循环-旋转-等待锁重新可用。
		- 在任意期间，自旋锁都可以防止多于一个的执行线程同时进入临界区。同一个锁可以用在多个位置。

				critical section（Y）：自旋锁的目的就是保护临界区
				uninterrupt（N）:在获取自旋锁之前就应该禁止中断（或者保证这段代码不会被中断抢
				占，否则需要使用下面要介绍的*_irq()或*_irqsave()），否则中断与进程（中断或进程）同时争用该自旋锁，会造成死锁。
				nopreempt （Y）：显示的调用了`preempt_disable/enable()`
				nomigrate （N）：禁用了抢占，同时也禁用了迁移
				nosfotirq （N）： 
				sleep/sched（N） ：在原子上下文上下文不允许睡眠和调度（但是这是需要程序员自己保证的）。

	- RT中的`spin_lock/unlock `
	
			#ifdef CONFIG_PREEMPT_RT_FULL
			# include <linux/spinlock_rt.h>
			#else /* PREEMPT_RT_FULL */

			#define spin_lock(lock)			rt_spin_lock(lock)

			void __lockfunc rt_spin_lock(spinlock_t *lock)
			{
				rt_spin_lock_fastlock(&lock->lock, rt_spin_lock_slowlock, true);
				spin_acquire(&lock->dep_map, 0, 0, _RET_IP_);
			}
			EXPORT_SYMBOL(rt_spin_lock);

			void __lockfunc rt_spin_unlock(spinlock_t *lock)
			{
				/* NOTE: we always pass in '1' for nested, for simplicity */
				spin_release(&lock->dep_map, 1, _RET_IP_);
				rt_spin_lock_fastunlock(&lock->lock, rt_spin_lock_slowunlock);
				migrate_enable();
			}
			EXPORT_SYMBOL(rt_spin_unlock);

			static inline void rt_spin_lock_fastlock(struct rt_mutex *lock,
					 void  (*slowfn)(struct rt_mutex *lock,
							 bool mg_off),
					 bool do_mig_dis)
			{
				might_sleep_no_state_check();
			
				if (do_mig_dis)
					migrate_disable();
			
				if (likely(rt_mutex_cmpxchg_acquire(lock, NULL, current)))
					return;
				else
					slowfn(lock, do_mig_dis);
			}

			static inline void rt_spin_lock_fastunlock(struct rt_mutex *lock,
					   void  (*slowfn)(struct rt_mutex *lock))
			{
				if (likely(rt_mutex_cmpxchg_release(lock, current, NULL)))
					return;
				else
					slowfn(lock);
			}

		- 从源代码可以看出在定义了RT_FULL中，会include 一个`spinlock_rt.h`的头文件,所有的`rt_spinlock`都在该头文件中定义。
		- `spin_lock`现实的调用了`migrate_disable/enable()`,并且获取了一个原子操作或者`rt_mutex`锁。
		- 标准linux内核在调用`spin_lock`时，需要确保没有中断抢占，或着禁止中断。而在RT中，中断线程化之后，中断禁止就没有必要，因为遇到这种状况后，中断线程将挂在等待队列上并放弃CPU让别的线程或进程来运行。等待队列就是解决这种死锁僵局的方法，每个spinlock都有一个等待队列，该等待队列是按进程或线程的优先级排队的。如果一个进程或线程竞争的spinlock已经被另一个线程保持，它将把自己挂在该spinlock的优先级化的等待队列上，然后发生调度把CPU让给别的进程或线程。需要特别注意，对于非线程化的中断，必须使用原来的spinlock。
		- spinlock被mutex化后会产生优先级反转（Priority Inversion）现象。 所谓优先级逆转，就是优先级高的进程由于优先级低的进程保持了竞争资源被迫等待，而让中间优先级的进程运行，优先级逆转将导致高优先级进程的抢占延迟增大，中间优先级的进程的执行时间的不确定性导致了高优先级进程抢占延迟的不确定性，因此为了保证实时性，必须消除优先级逆转现象。优先级继承协议（Priority Inheritance Protocol）和优先级顶棚协议（Priority Ceiling Protocol）（没有实现）就是专门针对优先级逆转问题提出的解决办法。所谓优先级继承，就是spinlock的保持者将继承高优先级的竞争者进程的优先级，从而能先于中间优先级进程运行，尽可能快地释放锁，这样高优先级进程就能很快得到竞争的spinlock，使得抢占延迟更确定，更短。
		- Spinlock被mutex化后引入的另一个问题就是死锁，典型的死锁有两种：一种为自锁，即一个spinlock保持者试图获得它已经保持的锁，很显然，这会导致该进程无法运行而死锁。另一种为非顺序锁而导致的，即进程 P1已经保持了spinlock LOCKA但是要获得进程P2已经保持的spinlock LOCKB，而进程P2要获得进程P1已经保持的spinlock LOCKA，这样进程P1和P2都将因为需要得到对方拥有的但永远不可能释放的spinlock而死锁。因此，在RT中引入了死锁检测机制，发生死锁会打印死锁路径并panic。

				critical section（Y）：自旋锁的目的就是保护临界区
				uninterrupt（N）:
				nopreempt （N）：
				nomigrate （Y）：显示的调用了`migrate_disable/enable()`
				nosfotirq （N）： 
				sleep/sched（Y）：没有改变preempt_count，非原子上下文，可以睡眠或调度。

- `spin_lock/unlock_irqsave/restore ` （RT和!RT有区别）
	- ！RT下的`spin_lock/unlock_irqsave/restore `

		
			#define spin_lock_irqsave(lock, flags)				\
			do {								\
				raw_spin_lock_irqsave(spinlock_check(lock), flags);	\
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

		- 从源代码可以看出，在!RT中，`spin_lock/unlock_irqsave/restore `调用了`local_irq_save()`(可以参考interrupt-API.md)禁用中断，并且显示的调用了`preempt_disable`(??为什么要调用抢占禁止，不是禁止中断以后就已经禁止抢占了？)。因此，该API禁止中断，禁止抢占，获取spinlock。

		
				critical section（Y）：自旋锁的目的就是保护临界区
				uninterrupt（Y）: 显示调用`local_irq_save()`
				nopreempt （Y）：显示的调用了`preempt_disable`
				nomigrate （Y）：禁止抢占，同时也禁止了迁移
				nosfotirq （Y）：禁止中断，也禁止了软中断 
				sleep/sched（N）：原子上下文不能睡眠和调度。

	- RT下的`spin_lock/unlock_irqsave/restore `

		
				#define spin_lock_irqsave(lock, flags)			 \
				do {						 \
					typecheck(unsigned long, flags);	 \
					flags = 0;				 \
					spin_lock(lock);			 \
				} while (0)
				
				#define spin_lock(lock)			rt_spin_lock(lock)

				其他代码请看`spin_lock()`

	
		- 从源代码中可以看出，在RT中`spin_lock_irqsave（）`并没有禁止中断，它的功能和RT中的`spin_lock()`基本一样。因此，需要注意的事项也一样。

			
				critical section（Y）：自旋锁的目的就是保护临界区
				uninterrupt（N）:
				nopreempt （N）：
				nomigrate （Y）：显示的调用了`migrate_disable/enable()`
				nosfotirq （N）： 
				sleep/sched（Y）：没有改变preempt_count，非原子上下文，可以睡眠或调度。

- `spin_lock/unlock_bh `（RT与！RT不同）

	- ！RT中的`spin_lock/unlock_bh `


			static __always_inline void spin_lock_bh(spinlock_t *lock)
			{
				raw_spin_lock_bh(&lock->rlock);
			}

			#define raw_spin_lock_bh(lock)		_raw_spin_lock_bh(lock)

			#ifndef CONFIG_INLINE_SPIN_LOCK_BH
			void __lockfunc _raw_spin_lock_bh(raw_spinlock_t *lock)
			{
				__raw_spin_lock_bh(lock);
			}
			EXPORT_SYMBOL(_raw_spin_lock_bh);
			#endif

			static inline void __raw_spin_lock_bh(raw_spinlock_t *lock)
			{
				__local_bh_disable_ip(_RET_IP_, SOFTIRQ_LOCK_OFFSET);
				spin_acquire(&lock->dep_map, 0, 0, _RET_IP_);
				LOCK_CONTENDED(lock, do_raw_spin_trylock, do_raw_spin_lock);
			}
			
			static __always_inline void __local_bh_disable_ip(unsigned long ip, unsigned int cnt)
			{
				preempt_count_add(cnt);
				barrier();
			}
			
		
		- 从代码中可以看出在！RT中`spin_lock_bh()`通过增加`preemt_count`来禁止bh(本地所有bh都不会执行)，同时也禁止了抢占（`preempt_count>0`），并且获取自旋锁`spin_lock`.
		- 在！RT中使用`spin_lock_bh()`防止本地cup上的bh抢占当前进程，因此禁用bh，同时防止其他CPU上的进程访问本地cup进程上的共享资源从而获取spin_lock().

				critical section（Y）：自旋锁的目的就是保护临界区
				uninterrupt（N）:
				nopreempt （Y）：`preemt_count>0`因此禁止抢占
				nomigrate （Y）：禁止抢占，也禁止了迁移
				nosfotirq （Y）：API功能 
				sleep/sched（N）：原子上下文不能睡眠和调度。

	- RT中的`spin_lock/unlock_bh `

		
			#define spin_lock_bh(lock)			\
				do {					\
					local_bh_disable();		\
					rt_spin_lock(lock);		\
				} while (0)
	
			static inline void local_bh_disable(void)
				{
					__local_bh_disable();
				}
	
			void __local_bh_disable(void)
				{
					if (++current->softirq_nestcnt == 1)
						migrate_disable();
				}
				EXPORT_SYMBOL(__local_bh_disable);
	
				`rt_spin_lock(lock)源码请看spin_lock()`

		- 这里在`local_bh_disable()`禁用了迁移，而在`rt_spin_lock(lock)`再次禁用迁移是否多余？？
		- 此处同样是通过current->nestcnt来判断是否禁用bh（current->nestcnt>1）以及嵌套层数。


				critical section（Y）：自旋锁的目的就是保护临界区
				uninterrupt（N）:
				nopreempt （N）：
				nomigrate （Y）：显示的调用了`migrate_disable/enable()`
				nosfotirq （Y）： 
				sleep/sched（Y）：没有改变preempt_count，非原子上下文，可以睡眠或调度。



- **补充---原子上下文：**

		内核的一个基本原则就是：在中断或者说原子上下文中，内核不能访问用户空间，而且内核是不能睡眠的。也就
		是说在这种情况下，内核是不能调用有可能引起睡眠的任何函数。一般来讲原子上下文指的是在中断或软中断
		中，以及在持有自旋锁的时候。内核提供了四个宏来判断是否处于这几种情况里：
	
			#define in_irq()     (hardirq_count()) //在处理硬中断中
			#define in_softirq()     (softirq_count()) //在处理软中断中
			#define in_interrupt()   (irq_count()) //在处理硬中断或软中断中
			#define in_atomic()     ((preempt_count() & ~PREEMPT_ACTIVE) != 0) //包含以上所有情况
	
		这四个宏所访问的count都是thread_info->preempt_count。这个变量其实是一个位掩码。
	
		最低8位表示抢占计数，通常由spin_lock/spin_unlock修改，或程序员强制修改，同时表明内核容许的最大抢占深度是256。
	
		8－15位表示软中断计数，通常由local_bh_disable/local_bh_enable修改，同时表明内核容许的最大软中断深度是256。
		位16－27是硬中断计数，通常由enter_irq/exit_irq修改，同时表明内核容许的最大硬中断深度是4096。
		第28位是PREEMPT_ACTIVE标志。用代码表示就是：
	
		PREEMPT_MASK: 0x000000ff
		SOFTIRQ_MASK: 0x0000ff00
		HARDIRQ_MASK: 0x0fff0000
	
		凡是上面4个宏返回1得到地方都是原子上下文，是不容许内核访问用户空间，不容许内核睡眠的，不容许调用任
		何可能引起睡眠的函数。而且代表thread_info->preempt_count不是0，这就告诉内核，在这里面抢占被禁用。

	
- `mutex_lock/unlock`

	- 在！RT中 `mutex_lock/unlock`


			/**
			 * mutex_lock - acquire the mutex
			 * @lock: the mutex to be acquired
			 *
			 * Lock the mutex exclusively for this task. If the mutex is not
			 * available right now, it will sleep until it can get it.
			 *
			 * The mutex must later on be released by the same task that
			 * acquired it. Recursive locking is not allowed. The task
			 * may not exit without first unlocking the mutex. Also, kernel
			 * memory where the mutex resides must not be freed with
			 * the mutex still locked. The mutex must first be initialized
			 * (or statically defined) before it can be locked. memset()-ing
			 * the mutex to 0 is not allowed.
			 *
			 * ( The CONFIG_DEBUG_MUTEXES .config option turns on debugging
			 *   checks that will enforce the restrictions and will also do
			 *   deadlock debugging. )
			 *
			 * This function is similar to (but not equivalent to) down().
			 */
				void __sched mutex_lock(struct mutex *lock)
				{
					might_sleep();
				
					if (!__mutex_trylock_fast(lock))
						__mutex_lock_slowpath(lock);
				}

		
		- 从注释中可以看到：
			- 任何时刻中只有一个任务可以持有mutex。
			- 给mutex上锁者必须负责给其再解锁，而且必须在同一上下文中，这就限制了mutex不适合内核同用户空间复杂的同步场景。
			- 不能递归的上锁和解锁。
			- 当持有一个mutex时，进程不可以退出。
			- mutex不能再中断或下半部中使用，即使mutex_trylock()也不行。

					critical section（Y）：mutex_lock的目的就是保护临界区
					uninterrupt（N）:
					nopreempt （N）：
					nomigrate （N）：
					nosfotirq （N）： 
					sleep/sched（Y）：非原子上下文，可以睡眠或调度(相当于二值信号量)。

	- 在RT中`mutex_lock/unlock`

			#define mutex_lock(l)			_mutex_lock(l)
	
			void __lockfunc _mutex_lock(struct mutex *lock)
			{
				mutex_acquire(&lock->dep_map, 0, 0, _RET_IP_);
				rt_mutex_lock(&lock->lock);
			}
	
			void __sched rt_mutex_lock(struct rt_mutex *lock)
			{
				rt_mutex_lock_state(lock, TASK_UNINTERRUPTIBLE);
			}
			EXPORT_SYMBOL_GPL(rt_mutex_lock);
	
			int __sched rt_mutex_lock_state(struct rt_mutex *lock, int state)
			{
				might_sleep();
			
				return rt_mutex_fastlock(lock, state, NULL, rt_mutex_slowlock);
			}

			static inline int
			rt_mutex_fastlock(struct rt_mutex *lock, int state,
					  struct ww_acquire_ctx *ww_ctx,
					  int (*slowfn)(struct rt_mutex *lock, int state,
							struct hrtimer_sleeper *timeout,
							enum rtmutex_chainwalk chwalk,
							struct ww_acquire_ctx *ww_ctx))
			{
				if (likely(rt_mutex_cmpxchg_acquire(lock, NULL, current)))
					return 0;
			
				return slowfn(lock, state, NULL, RT_MUTEX_MIN_CHAINWALK, ww_ctx);
			}
		`rt_mutex_fastlock`首先尝试快速获得lock，如果尝试无法成功，则调用rt_mutex_slowlock 继续获得锁。

					critical section（Y）：mutex_lock的目的就是保护临界区
					uninterrupt（N）:
					nopreempt （N）：
					nomigrate （N）：
					nosfotirq （N）： 
					sleep/sched（Y）：非原子上下文，可以睡眠或调度(相当于二值信号量)。

- `rt_spin_lock__no_mg`

			void __lockfunc rt_spin_lock__no_mg(spinlock_t *lock)
			{
				rt_spin_lock_fastlock(&lock->lock, rt_spin_lock_slowlock, false);
				spin_acquire(&lock->dep_map, 0, 0, _RET_IP_);
			}
			EXPORT_SYMBOL(rt_spin_lock__no_mg);

			static inline void rt_spin_lock_fastlock(struct rt_mutex *lock,
								 void  (*slowfn)(struct rt_mutex *lock,
										 bool mg_off),
								 bool do_mig_dis)
			{
				might_sleep_no_state_check();
			
				if (do_mig_dis)
					migrate_disable();
			
				if (likely(rt_mutex_cmpxchg_acquire(lock, NULL, current)))
					return;
				else
					slowfn(lock, do_mig_dis);
			}

- `bit_spin_lock`

			 /*
			 *  bit-based spin_lock()
			 *
			 * Don't use this unless you really need to: spin_lock() and spin_unlock()
			 * are significantly faster.
			 */
			static inline void bit_spin_lock(int bitnum, unsigned long *addr)
			{
				/*
				 * Assuming the lock is uncontended, this never enters
				 * the body of the outer loop. If it is contended, then
				 * within the inner loop a non-atomic test is used to
				 * busywait with less bus contention for a good time to
				 * attempt to acquire the lock bit.
				 */
				preempt_disable();
			#if defined(CONFIG_SMP) || defined(CONFIG_DEBUG_SPINLOCK)
				while (unlikely(test_and_set_bit_lock(bitnum, addr))) {
					preempt_enable();
					do {
						cpu_relax();
					} while (test_bit(bitnum, addr));
					preempt_disable();
				}
			#endif
				__acquire(bitlock);
			} 