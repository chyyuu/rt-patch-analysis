- `get/put_cpu`(RT和!RT相同)

		#define get_cpu() ({ preempt_disable(); smp_processor_id(); })
		#define put_cpu() preempt_enable()
		
		
		#define smp_processor_id() raw_smp_processor_id()
		#define raw_smp_processor_id() (this_cpu_read(cpu_number))

	- 通过禁止抢占，并返回当前cpu的id。
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
	- 从注释中**`smp_processor_id()` is safe if it's used in a preemption-off critical section, or in a thread that is bound to the current CPU.**可以看出`smp_processor_id()`只要保证调用它的线程不被迁移到其他CPU上就可以，但在！RT中并没有对migration相关的操作，因此采用`preempt_disable()`,在RT中可以用`get/put_cpu_light`来替换`get/put_cpu`增加可抢占区域

				critical section（N）：只是禁止抢占，但不能阻止本地cpu异步中断对per_cpu的同步访问，需要用相应的锁来保护。
				uninterrupt（N）:
				nopreempt （Y）：显示调用了`preempt_diable()`
				nomigrate （Y）：禁用了强占，因此禁用了迁移
				nosfotirq （N）： 
				sleep/sched（N）：抢占禁止的原子上下文禁止调度和睡眠。

- `get/put_cpu_light `（RT中使用）

	- get/put_cpu_light`的宏定义为：
	
		 #define get_cpu_light()   ({migrate_disable();smp_processor_id();})
		 #define put_cpu_light()	migrate_enable(); 

	- `get_cpu_light`：关闭线程（进程）迁移，并且返回当前的`CPU_ID`；`put_cpu`：开启线程（进程）迁移
				critical section（N）：只是禁止迁移，但不能阻止本地cpu异步中断以及其他线程抢占对per_cpu的同步访问，需要用相应的锁来保护。
				uninterrupt（N）:
				nopreempt （N）：
				nomigrate （Y）：显示调用了`migrate_disable/enable()`
				nosfotirq （N）： 
				sleep/sched（Y）：非原子上下文是可以睡眠或调度的。

- `local_lock/unlock[_irq]`

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

		`spin_lock_irqsave`代码参见`spinlock-API.md`

		#ifdef CONFIG_PREEMPT_RT_FULL
		
		#define get_local_var(var) (*({	\
			migrate_disable();	\
			this_cpu_ptr(&var);	}))
		
		#define put_local_var(var) do {	\
			(void)&(var);		\
			migrate_enable();	\
		} while (0)
		
		# define get_local_ptr(var) ({	\
			migrate_disable();	\
			this_cpu_ptr(var);	})
		
		# define put_local_ptr(var) do {	\
			(void)(var);			\
			migrate_enable();		\
		} while (0)
		
		#else
		
		#define get_local_var(var)	get_cpu_var(var)
		#define put_local_var(var)	put_cpu_var(var)
		#define get_local_ptr(var)	get_cpu_ptr(var)
		#define put_local_ptr(var)	put_cpu_ptr(var)
		
		#endif

	- 该API是对`per_cpu`变量的保护，在RT中禁用迁移，获取`spin_lock`锁，获取`per_cpu`变量。在！RT中，禁用中断，禁用抢占，获取原始自旋锁，获取`per_cpu`变量。

				critical section（Y）：获取spin_lock,保护临界区。
				uninterrupt（N/Y）:在RT中没有禁止中断，在!RT中禁止了中断。
				nopreempt （N/Y）：在RT中没有禁止抢占，在!RT中禁止了抢占。
				nomigrate （Y/Y）：禁止了迁移
				nosfotirq （N/Y）：在RT中没有禁止软中断，在!RT中禁止了中断。 
				sleep/sched（Y/N）：非原子上下文，可以睡眠和调度

- `local_lock`

			#define local_lock(lvar)					\
				do { __local_lock(&get_local_var(lvar)); } while (0)

			#ifdef CONFIG_PREEMPT_RT_FULL

			#define get_local_var(var) (*({		\
				       migrate_disable();	\
				       this_cpu_ptr(&var);	}))

