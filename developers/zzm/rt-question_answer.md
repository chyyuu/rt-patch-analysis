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
	
		- #define get_cpu_light()   ({migrate_disable();smp_processor_id();})
		- #define put_cpu_light()	migrate_enable(); 
		- `get_cpu_light`：关闭线程（进程）迁移，并且返回当前的`CPU_ID`；` put_cpu`：开启线程（进程）迁移

- 在COMFIG_PREEMPT_RT_FULL 和 COMFIG_SMP配置的情况下，需要添加`get/put_cpu_light`

**2.何时需要把`get/put_cpu`替换为`get/put_cpu_light`**

	get/put_cpu 宏定义：
	#define get_cpu() ({ preempt_disable(); smp_processor_id(); })
	#define put_cpu() preempt_enable()


- 存在`get/put_cpu`替换为`get/put_cpu_light`的补丁有：

	- block-mq-drop-preempt-disable.patch
	- block-mq-use-cpu_light.patch
	- epoll-use-get-cpu-light.patch


- 需要替换的时刻为：
	- 在-RT下，当调用了get_cpu()时禁止抢占，同时又持有睡眠锁的时候，这时可能会在抢断禁止的情况下产生调度（中断），从而对实时性产生影响甚至会死锁。
	

**3.何时需要把`get_cpu_var` 替换为`get_cpu_light();&per_cpu();put_cpu_light()`;**

- `per_cpu()`：获得一个为用`DEFINE_PER_CPU`宏为CPU选择的一个每CPU数组元素，CPU由cpu指定，数组名称为name：`#define per_cpu(var, cpu)     (*((void)(cpu), &per_cpu__##var))`

- `gut_cpu_var`:先禁用内核抢占，然后在每CPU数组name中，为本地CPU选择元素：`#define get_cpu_var(var) (*({ preempt_disable(); &__get_cpu_var(var); }))`

- 此处同样存在-RT下，在调用`gut_cpu_var`时禁止抢占，同时又持有睡眠锁的时候，可能会在抢断禁止的情况下产生调度（中断），从而影响实时性产生影响甚至会死锁。

 **4.何时需要把`get_cpu;per_cpu_ptr;put_cpu`替换为`get_cpu_light;per_cpu_ptr;spin_un/lock;put_cpu_light`**

- 相关补丁：PATCH: md: raid5: Make raid5_percpu handling RT aware
- `get_cpu;per_cpu_ptr;put_cpu`禁止了抢占，并且获取了本地CPU变量，但是本地非线程化的中断并没有禁止，有可能在对`per_cpu`变量操作时，造成中断，破坏`per_cpu`变量。通过`get_cpu_light;per_cpu_ptr;spin_un/lock;put_cpu_light`，可以禁止进程迁移，然后获取per_cpu lock保护了每CPU变量。


**5.何时需要把`get_cpu_var;put_cpu_var` 替换为`get_locked_var; put_locked_var OR  get_local_var;put_local_var`**

- 在patch：rt-local-irq-lock.patch中，定义`get_locked_var; put_locked_var OR  get_local_var;put_local_var`
	- 如果定义了`CONFIG_PREEMPT_RT_FULL`，local_lock定义为：

			+#ifdef CONFIG_PREEMPT_RT_FULL
			+
			+#define get_local_var(var) (*({	\
			+	migrate_disable();	\
			+	this_cpu_ptr(&var);	}))
			+
			+#define put_local_var(var) do {	\
			+	(void)&(var);		\
			+	migrate_enable();	\
			+} while (0)
			+
			+# define get_local_ptr(var) ({	\
			+	migrate_disable();	\
			+	this_cpu_ptr(var);	})
			+
			+# define put_local_ptr(var) do {	\
			+	(void)(var);			\
			+	migrate_enable();		\
			+} while (0)

	- 如果没有定义`CONFIG_PREEMPT_RT_FULL`，local_lock定义为：

		    +#else
		    +
		    +#define get_local_var(var)	get_cpu_var(var)
		    +#define put_local_var(var)	put_cpu_var(var)
		    +#define get_local_ptr(var)	get_cpu_ptr(var)
		    +#define put_local_ptr(var)	put_cpu_ptr(var)
		    +
		    +#endif

	- 而`get_cpu_var()`的定义为（禁止了抢占）
	
			 `#define get_cpu_var(var) (*({ preempt_disable(); &__get_cpu_var(var); }))`

				#define __get_cpu_var(var)per_cpu__##var
因此，在RT内核中，禁止抢占，同时又持有睡眠锁这是有问题。需要`get_cpu_var;put_cpu_var` 替换为`get_locked_var; put_locked_var OR  get_local_var;put_local_var`，增加了抢占区域，同时保护了per_cpu变量。



**6.如何理解 `from PATCH: mm/swap: Convert to percpu locked`**

		-	`lru_add_drain_cpu(get_cpu());`
		-	`put_cpu();`
		+	`lru_add_drain_cpu(local_lock_cpu(swapvec_lock));`
		+	`local_unlock_cpu(swapvec_lock);`

- 对`lru_add_drain_cpu(int cpu)`源代码解释为：Drain pages out of the cpu's pagevecs. Either"cpu" is the current CPU, and preemption has already been disabled; or"cpu" is being hot-unplugged, and is already dead.可见此处已经禁止抢占，而不需要在用get_cpu().

- 分析local_lock_cpu()的源码


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
	    
		/# `ifdef CONFIG_PREEMPT_RT_FULL`
		/# `define spin_lock_local(lock)		rt_spin_lock__no_mg(lock)`
		/# `define spin_trylock_local(lock)		rt_spin_trylock__no_mg(lock)`
		/# `define spin_unlock_local(lock)		rt_spin_unlock__no_mg(lock)`
		/#`else`
		/# `define spin_lock_local(lock)		spin_lock(lock)`
		/# `define spin_trylock_local(lock)		spin_trylock(lock)`
		/# `define spin_unlock_local(lock)		spin_unlock(lock)`
		/#`endif`
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
`local_lock_cpu()`最后只是获取了一个锁（但此处好像获取的是睡眠锁，而在抢占禁止的情况下不能使用睡眠锁？？）来保护per_cpu.

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

可以看出，通过`__rt_spin_lock(l)`禁止了进程迁移，并通过if-else 获取一个可睡眠锁，增加了可抢占区域，并保护了per_cpu变量。