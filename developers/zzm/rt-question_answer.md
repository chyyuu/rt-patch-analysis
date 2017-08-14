Q4.

1.**何时需要添加`INIT_SWAIT_HEAD|SWAIT_EVENT|SWAIT_WAKE_ALL|SWAIT_EVENT_INTERRUPTIBLE`**

- https://lwn.net/Articles/577370/文章中提到，wait_queue的callback mechanism 对于实时内核是有问题的，因为回调机制是可以睡眠的，这阻止了使用原始的自旋锁来保护等待队列本身。
	
- https://lwn.net/Articles/661424/文中提到，Simple wait queues是一个简单的等待队列机制，但是这并不能作为添加另一个等待队列机制的理由。真正的驱动力是实时内核，the simple waitqueue allows fordeterministic behaviour -- IOW it has strictly bounded IRQ and lock hold times. 

- 因此，对于RT-linux是需添加`INIT_SWAIT_HEAD|SWAIT_EVENT|SWAIT_WAKE_ALL|SWAIT_EVENT_INTERRUPTIBLE`

- 相关patch中的添加：timers-prepare-for-full-preemption.patch

		+#ifdef CONFIG_PREEMPT_RT_FULL
		+ * Wait for a running timer
		+ */
		+static void wait_for_running_timer(struct timer_list *timer)
		+{
		+	struct timer_base *base;
		+	u32 tf = timer->flags;
		+
		+	if (tf & TIMER_MIGRATING)
		+		return;
		+
		+	base = get_timer_base(tf);
		+	swait_event(base->wait_for_running_timer,
		+		   base->running_timer != timer);
		+}
		+# define wakeup_timer_waiters(b)	swake_up_all(&(b)->wait_for_running_timer)
		+#else
		+static inline void wait_for_running_timer(struct timer_list *timer)
		+{
		+	cpu_relax();
		+}
		+
		+# define wakeup_timer_waiters(b)	do { } while (0)
		+#endif
		
		+#ifdef CONFIG_PREEMPT_RT_FULL
		+		init_swait_queue_head(&base->wait_for_running_timer);
		+#endif

2.**何时需要把`init_waitqueue_head|wait_event|wake_up_all|wait_event_interruptible`替
换为`init_swait_head|swait_event|swait_wake_all|swait_event_interruptible`**

- 相比于waitqueue,Simple wait queues作了如下调整：
 - mixing INTERRUPTIBLE and UNINTERRUPTIBLE sleeps on the same waitqueue;all wakeups are TASK_NORMAL in order to avoid O(n) lookups for the right sleeper state.
 
 *  the exclusive mode; because this requires preserving the list order and this is hard.

 * custom wake functions; because you cannot give any guarantees about random code.

- 相关patch的替换为：
	- completion-use-simple-wait-queues.patch
	- block-blk-mq-use-swait.patch
	- fs-dcache-use-swait_queue-instead-of-waitqueue.patch
	- powerpc-ps3-device-init.c-adapt-to-completions-using.patch

- waitqueue替换Simple wait queues的时刻：

	
	- 不再有回调机制，避免等待队列锁的竞争。
	- 在-RT，避免回调机制睡眠，采用swait。

Q5.


1.**何时需要添加get/put_cpu_light**

- `get/put_cpu_light`的宏定义为：
	
		 #define get_cpu_light()   ({migrate_disable();smp_processor_id();})
		 #define put_cpu_light()	migrate_enable(); 

-  `get_cpu_light`：关闭线程（进程）迁移，并且返回当前的`CPU_ID`；` put_cpu`：开启线程（进程）迁移

- 在`COMFIG_PREEMPT_RT_FULL`和`COMFIG_SMP`配置的情况下，需要添加`get/put_cpu_light`

**2.何时需要把`get/put_cpu`替换为`get/put_cpu_light`**

	get/put_cpu 宏定义：
	#define get_cpu() ({ preempt_disable(); smp_processor_id(); })
	#define put_cpu() preempt_enable()

- 其中对于`smp_processor_id()`的源代码中的注释为：


		/*
		 * smp_processor_id(): get the current CPU ID.
		 *
		 * if DEBUG_PREEMPT is enabled then we check whether it is
		 * used in a preemption-safe way. (smp_processor_id() is safe
		 * if it's used in a preemption-off critical section, or in
		 * a thread that is bound to the current CPU.)
		 *
		 * NOTE: raw_smp_processor_id() is for internal use only
		 * (smp_processor_id() is the preferred variant), but in rare
		 * instances it might also be used to turn off false positives
		 * (i.e. smp_processor_id() use that the debugging code reports but
		 * which use for some reason is legal). Don't use this to hack around
		 * the warning message, as your code might not work under PREEMPT.
		 */
- 从注释中**`smp_processor_id()` is safe if it's used in a preemption-off critical section, or in a thread that is bound to the current CPU.**可以看出`smp_processor_id()`只要保证调用它的线程不被迁移到其他CPU上就可以，因此完全可以用`get/put_cpu_light`来替换`get/put_cpu`增加可抢占区域
- 对于-RT来说，`get_cpu()`既禁止了抢占，又可能对随后分配的可睡眠锁产生问题，因此选用只是禁止了迁移的`get_cpu_light`更加合适。
- 存在`get/put_cpu`替换为`get/put_cpu_light`的补丁有：

	- block-mq-drop-preempt-disable.patch
	- block-mq-use-cpu_light.patch
	- epoll-use-get-cpu-light.patch 等


**3.何时需要把`get_cpu_var` 替换为`get_cpu_light();&per_cpu();put_cpu_light()`;**

- `per_cpu()`：获得一个为用`DEFINE_PER_CPU`宏为CPU选择的一个每CPU数组元素，CPU由cpu指定，数组名称为name：`#define per_cpu(var, cpu)     (*((void)(cpu), &per_cpu__##var))`

- `gut_cpu_var`:先禁用内核抢占，然后在每CPU数组name中，为本地CPU选择元素：`#define get_cpu_var(var) (*({ preempt_disable(); &__get_cpu_var(var); }))`

- 此处同样存在-RT下，在调用`gut_cpu_var`时禁止抢占，同时可能会持有睡眠锁，在抢断禁止的情况可能产生调度，从而影响实时性。

 **4.何时需要把`get_cpu;per_cpu_ptr;put_cpu`替换为`get_cpu_light;per_cpu_ptr;spin_un/lock;put_cpu_light`**

- 相关补丁：PATCH: md: raid5: Make raid5_percpu handling RT aware
- `per_cpu_ptr(pointer, cpu)`返回每CPU数组中与cpu对应CPU元素地址，pointer给出数组地址： #define `per_cpu_ptr(ptr, cpu)` ({ (void)(cpu); (ptr); })
- 该函数`per_cpu_ptr()`返回了指定处理器上的惟一数据。这个函数不会禁止内核抢占，如果需要访问另外的处理器数据，一定要给数据加锁，因此对于-RT来说，如果为了扩大抢占区域，将preempt_disable()替换为migration_disable(),这将不能禁止其他处理器上的线程抢占，因此需要加`spin_un/lock`对`per_cpu`数据进行保护。


**5.何时需要把`get_cpu_var;put_cpu_var` 替换为`get_locked_var; put_locked_var OR  get_local_var;put_local_var`**

- 在patch：rt-local-irq-lock.patch中，定义`get_locked_var; put_locked_var OR  get_local_var;put_local_var`
   
	- 对于`get_local_var`的定义，如下：

			ifndef CONFIG_SMP
		   	 	#define get_locked_var(lvar, var)	get_cpu_var(var)
			else
			 	#define get_locked_var(lvar, var)					\
			    	(*({								\
			    		local_lock(lvar);					\
			    		this_cpu_ptr(&var);					\
			    	}))

			#define local_lock(lvar)					\
			do { __local_lock(&get_local_var(lvar)); } while (0)

			
			#define this_cpu_ptr(ptr) raw_cpu_ptr(ptr)
			
			#define raw_cpu_ptr(ptr)						\
				({									\
					__verify_pcpu_ptr(ptr);						\
					arch_raw_cpu_ptr(ptr);						\
				})

			#define arch_raw_cpu_ptr(ptr)				\
				({							\
					unsigned long tcp_ptr__;			\
					asm volatile("add " __percpu_arg(1) ", %0"	\
						     : "=r" (tcp_ptr__)			\
						     : "m" (this_cpu_off), "0" (ptr));	\
					(typeof(*(ptr)) __kernel __force *)tcp_ptr__;	\
				})
			
	- 对于`get_local_var`的定义如下：

			+#ifdef CONFIG_PREEMPT_RT_FULL
			+
				+#define get_local_var(var) (*({	\
				+	migrate_disable();	\
				+	this_cpu_ptr(&var);	}))
		    +#else
		    	+#define get_local_var(var)	get_cpu_var(var)
		    +#endif
			
	- 而`get_cpu_var()`的定义为（禁止了抢占）
	
			 `#define get_cpu_var(var) (*({ preempt_disable(); &__get_cpu_var(var); }))`

从代码中可以看出，在!RT或UP内核中`get_locked_var; put_locked_var OR  get_local_var;put_local_var`直接被定义为`get_cpu_var;put_cpu_var`。在-RT或SMP内核中，为增加抢占区域，将`preempt_disable()`替换为`migrate_disable()`。



**6.如何理解 `from PATCH: mm/swap: Convert to percpu locked`**

		-	`lru_add_drain_cpu(get_cpu());`
		-	`put_cpu();`
		+	`lru_add_drain_cpu(local_lock_cpu(swapvec_lock));`
		+	`local_unlock_cpu(swapvec_lock);`

- 对`lru_add_drain_cpu(int cpu)`源代码解释为：Drain pages out of the cpu's pagevecs. Either"cpu" is the current CPU, and preemption has already been disabled; or"cpu" is being hot-unplugged, and is already dead.可见此处已经禁止抢占，而不需要再用get_cpu().

- 分析`local_lock_cpu()`的源码

	    +#define local_lock_cpu(lvar)						\
	    +	({								\
	    +		local_lock(lvar);					\
	    +		smp_processor_id();					\
	    +	})
	    +	
	    +#define local_lock(lvar)					\
	    +	do { __local_lock(&get_local_var(lvar)); } while (0)
	    +	
	    +static inline void __local_lock(struct local_irq_lock *lv)
	    +{
	    +	if (lv->owner != current) {
	    +		spin_lock_local(&lv->lock);
	    +		LL_WARN(lv->owner);
	    +		LL_WARN(lv->nestcnt);
	    +		lv->owner = current;
	    +	}
	    +	lv->nestcnt++;
	    +}
	    +
	    
		# `ifdef CONFIG_PREEMPT_RT_FULL`
		# `define spin_lock_local(lock)		rt_spin_lock__no_mg(lock)`
		# `define spin_trylock_local(lock)		rt_spin_trylock__no_mg(lock)`
		# `define spin_unlock_local(lock)		rt_spin_unlock__no_mg(lock)`
		#`else`
		# `define spin_lock_local(lock)		spin_lock(lock)`
		# `define spin_trylock_local(lock)		spin_trylock(lock)`
		# `define spin_unlock_local(lock)		spin_unlock(lock)`
		#`endif`
	    void __lockfunc rt_spin_lock__no_mg(spinlock_t *lock)
	    {
	    	rt_spin_lock_fastlock(&lock->lock, rt_spin_lock_slowlock, false);
	    	spin_acquire(&lock->dep_map, 0, 0, _RET_IP_);
	    }

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
因为，`do_mig_dis`默认为false，因此`migrate_disable()`没有执行，`local_lock_cpu()`最后只是获取了一个原子操作或者`rt_mutex`锁，并没有禁止抢占或线程迁移（但此处好像不应该获取睡眠锁，在抢占禁止的情况下不能使用睡眠锁？？）来保护per_cpu.

Q12.

**1. 如何理解 lg_lock?**

	+#`ifndef CONFIG_PREEMPT_RT_FULL`
	+# define lg_lock_ptr		arch_spinlock_t
	+# define lg_do_lock(l)		arch_spin_lock(l)
	+# define lg_do_unlock(l)	arch_spin_unlock(l)
	+#else
	+# define lg_lock_ptr		struct rt_mutex
	+# define lg_do_lock(l)		__rt_spin_lock(l)
	+# define lg_do_unlock(l)	__rt_spin_unlock(l)
	+#endif


- 为了允许内核抢占，内核中的自旋锁需改为以下三种锁：
	- 把原来的`raw_spin_lock`改为`arch_spin_lock`（代表体系相关的原子操作的实现）；
	- 把原来的`spin_lock`改为`raw_spin_lock`（原始自旋锁）；
	- 实现一个新的`spin_lock`（可睡眠的自旋锁）；

- 在非RT内核中，`spin_lock`只是简单地调用`raw_spin_lock`，实际上他们是完全一样的。在RT内核中，`spin_lock`会使用信号量完成临界区的保护工作，带来的好处是同一个CPU可以有多个临界区同时工作，而原有的体系因为禁止抢占的原因，一旦进入临界区，其他临界区就无法运行，新的体系在允许使用同一个临界区的其他进程进行休眠等待，而不是强占着CPU进行自旋操作。

- `lg_lock`是`per_CPU`变量的保护锁，与体系结构有关，对于！RT采用与结构体相关的`arch_spin_lock`，对于RT定义为`__rt_spin_lock(l)`，分析一下该函数的源码：

    	void __lockfunc \__rt_spin_lock(struct rt_mutex *lock)
    	{
    			`rt_spin_lock_fastlock(lock, rt_spin_lock_slowlock, true)`;
    	}

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

可以看出，通过`__rt_spin_lock(l)`禁止了进程迁移，并通过if-else 获取一个原子操作，或者获取一个rt_mutex锁，增加了可抢占区域，并保护了`per_cpu`变量。