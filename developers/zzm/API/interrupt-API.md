


-  `local_irq_disable/enable（）`(在RT与！RT上并没有变化)

	- `local_irq_disable/enable`的功能是禁止和激活当前CPU上的所有中断的传递。这两个函数以单个汇编指令来实现，依赖于体系结构。分别通过`sti和sti来clear和set中断`。
	- 这两个API属于无条件禁止和开启中断，存在潜在的危险。即在使用*_diable()之前，可能已经禁止了中断。同样，在使用 *_enable()可在开始已经关闭中断的情况下无条件开启了中断。因此在使用这两个API时需要比较清楚地知道中断是否其他地方开启或关闭过。（否则可以使用下边 *_save/restore() API）。

				critical section（N）：虽然禁止了中断，但是不能阻止其他cpu上的线程对临界区的访问
				uninterrupt（Y）:禁止了中断
				nopreempt （Y）：因为禁止了中断，不能调度，因此禁止了强占 。
				nomigrate （Y）：RT上禁止了迁移，！RT上没有单独对迁移的操作。
				nosfotirq （Y）：禁用中断，同时也禁止了软中断 
				sleep/sched（N）：在禁止中断的原子上下文不允许睡眠和调度。
	
	- 源码：
	
			#define local_irq_enable() do { raw_local_irq_enable(); } while (0)
			#define local_irq_disable() do { raw_local_irq_disable(); } while (0)
			
			
			#define raw_local_irq_disable() arch_local_irq_disable()
			#define raw_local_irq_enable() arch_local_irq_enable()
			
			 
			 
			 static inline __attribute__((no_instrument_function)) __attribute
				__((no_instrument_function)) void arch_local_irq_disable(void)
				{
				 native_irq_disable();
				}
			
			static inline __attribute__((no_instrument_function)) __attribute
				__((no_instrument_function)) void arch_local_irq_enable(void)
				{
				 native_irq_enable();
				}
		


			static inline __attribute__((no_instrument_function)) void native_irq_disable(void)
				{
				 asm volatile("cli": : :"memory");
				}
			
			static inline __attribute__((no_instrument_function)) void native_irq_enable(void)
				{
				 asm volatile("sti": : :"memory");
				}

- `local_irq_save/restore（unsigned long flags）`（RT和！RT并没有变化）
	- 对 `local_irq_save`的调用将把当前中断状态保存到flags中，然后禁用当前处理器上的中断传递。注意, flags 被直接传递, 而不是通过指针来传递。
	-  `local_irq_restore()`则是对保存的中断状态恢复。
	-  **注意：**对这两个API的调用必须在同一个函数内进行。且对于以上介绍的这四个API既可以在中断上下文中使用，也可以在进程上下文中使用。

				critical section（N）：虽然禁止了中断，但是不能阻止其他cpu上的线程对临界区的访问
				uninterrupt（Y）:禁止了中断
				nopreempt （Y）：因为禁止了中断，不能调度，因此禁止了强占 。
				nomigrate （Y）：RT上禁止了迁移，！RT上没有单独对迁移的操作。
				nosfotirq （Y）：禁用中断同时也禁止了软中断 
				sleep/sched (Y)：在禁止中断的原子上下文不允许睡眠和调度。

	- 源码：
			
			#define local_irq_save(flags) do { raw_local_irq_save(flags); } while (0)
			#define local_irq_restore(flags) do { raw_local_irq_restore(flags); } while (0)
			
			#define raw_local_irq_save(flags) do { typecheck(unsigned long, flags); flags= 
			arch_local_irq_save(); } while (0)
			
			
			#define raw_local_irq_restore(flags) do { typecheck(unsigned long, flags); 
			arch_local_irq_restore(flags); } while (0)
			
			
			static inline __attribute__((no_instrument_function)) __attribute__
			((no_instrument_function)) unsigned long arch_local_irq_save(void)
			{
			 unsigned long flags = arch_local_save_flags();
			 arch_local_irq_disable();
			 return flags;
			}
			
			
			static inline __attribute__((no_instrument_function)) __attribute__
			((no_instrument_function)) void arch_local_irq_restore(unsigned long flags)
			{
			 native_restore_fl(flags);
			}
			
			
			static inline __attribute__((no_instrument_function)) __attribute__
			((no_instrument_function)) unsigned long arch_local_save_flags(void)
			{
			 return native_save_fl();
			}
			
			
			
			static inline __attribute__((no_instrument_function)) unsigned long native_save_fl(void)
			{
			 unsigned long flags;
			
			 asm volatile("# __raw_save_flags\n\t"
			       "pushf ; pop %0"
			       : "=rm" (flags)
			       :
			       : "memory");
			
			 return flags;
			}
			
			static inline __attribute__((no_instrument_function)) void native_restore_fl(unsigned long flags)
			{
			 asm volatile("push %0 ; popf"
			       :
			       :"g" (flags)
			       :"memory", "cc");
			}

- `local_bh_disable/enable()`----禁用/使能本地halfbottom。 (RT和！RT是有区别的)
	- ！RT中 `local_bh_disable/enable()` 

			static inline void local_bh_disable(void)
			{
				__local_bh_disable_ip(_THIS_IP_, SOFTIRQ_DISABLE_OFFSET);
			}

			
			static __always_inline void __local_bh_disable_ip(unsigned long ip, unsigned int cnt)
			{
				preempt_count_add(cnt);
				barrier();
			}
			
			#define preempt_count_add(val)	__preempt_count_add(val)

		- 从代码中可以看出，该函数是通过增加本地CPU上的`__preempt_count`对应的softirq位来禁止softirq。
		- 每个cpu有一个per-cpu类型的int变量`preempt_count`，它描述了当前抢占信息。 
				该变量作用划分如下:
				
				 *         PREEMPT_MASK:    0x000000ff
				 *         SOFTIRQ_MASK:    0x0000ff00
				 *         HARDIRQ_MASK:    0x000f0000
				 *             NMI_MASK:    0x00100000
				 * PREEMPT_NEED_RESCHED:    0x80000000

					相应字段的值用来表示当前的嵌套次数。
				/*
				 * Are we doing bottom half or hardware interrupt processing?
				 * Are we in a softirq context? Interrupt context?
				 * in_softirq - Are we currently processing softirq or have bh disabled?
				 * in_serving_softirq - Are we currently processing softirq?
				 */
				#define in_irq()        (hardirq_count())
				#define in_softirq()        (softirq_count())
				#define in_interrupt()      (irq_count())
				#define in_serving_softirq()    (softirq_count() & SOFTIRQ_OFFSET)
		
				
		
		- 内核因此能使用几个宏判断调用进行嵌套判断，只有宏`local_bh_enable与第一个local_bh_disable`调用相匹配，可延迟函数才再次被激活（`do_softirq`）
		
				critical section（N）：虽然禁止了bh，但是不能禁止异步irq和其他cpu上的线程对临界区的访问
				uninterrupt（N）:
				nopreempt （Y）：因为增加了preempt_count，因此禁止抢占。
				nomigrate （N）：禁止了抢占，同时也禁止了迁移
				nosfotirq （Y）：禁止了bh，同样禁止软中断 
				sleep/sched（N）：在禁止抢占的原子上下文不允许睡眠和调度。

	- RT中 `local_bh_disable/enable()`
		
			static inline void local_bh_disable(void)
			{
				__local_bh_disable();
			}

			static inline void local_bh_enable(void)
			{
				__local_bh_enable();
			}

			void __local_bh_disable(void)
			{
				if (++current->softirq_nestcnt == 1)
					migrate_disable();
			}
			EXPORT_SYMBOL(__local_bh_disable);
			
			void __local_bh_enable(void)
			{
				if (WARN_ON(current->softirq_nestcnt == 0))
					return;
			
				local_irq_disable();
				if (current->softirq_nestcnt == 1 && current->softirqs_raised)
					do_current_softirqs();
				local_irq_enable();
			
				if (--current->softirq_nestcnt == 0)
					migrate_enable();
			}
			EXPORT_SYMBOL(__local_bh_enable);

	- 从代码中可以看出，`local_bh_disable/enable()`通过`current->softirq_nestcnt`来统计嵌套数，同样通过判断嵌套数以及`softirqs_raised`来执行`do_current_softirqs()`，并且该API不再禁止抢占，并显示的调用了`migrate_disable/enable()`。

				critical section（N）：虽然禁止了bh，但是不能异步irq和其他cpu上的线程对临界区的访问
				uninterrupt（N）:
				nopreempt （N）：
				nomigrate （Y）：显示的调用了`migrate_disable()`
				nosfotirq （Y）：禁止了bh，同样禁止软中断 
				sleep/sched（N）：

- `local_irq_disable/enable_nort`，`local_irq_disable/enable_rt `，`local_irq_save/restore_nort`，`local_irq_save/restore_rt`

	
	- 在/include/linux/irqflags.h中，定义了：
	

			/*
			 * local_irq* variants depending on RT/!RT
			 */
			#ifdef CONFIG_PREEMPT_RT_FULL
			# define local_irq_disable_nort()	do { } while (0)
			# define local_irq_enable_nort()	do { } while (0)
			# define local_irq_save_nort(flags)	local_save_flags(flags)
			# define local_irq_restore_nort(flags)	(void)(flags)
			# define local_irq_disable_rt()		local_irq_disable()
			# define local_irq_enable_rt()		local_irq_enable()
			#else
			# define local_irq_disable_nort()	local_irq_disable()
			# define local_irq_enable_nort()	local_irq_enable()
			# define local_irq_save_nort(flags)	local_irq_save(flags)
			# define local_irq_restore_nort(flags)	local_irq_restore(flags)
			# define local_irq_disable_rt()		do { } while (0)
			# define local_irq_enable_rt()		do { } while (0)
			#endif
	
	- 从定义可以看出，
		- `local_irq_disable/enable_nort()`在RT中并没有做任何操作。而在！RT中，仍然是`local_irq_disable/enable()`
		- `local_irq_disable/enable_rt `在RT中定义为`local_irq_disable/enable()`，在！RT中为空操作。
		- `local_irq_save/restore_nort`在！RT中保持初始`local_irq_disable/enable()`，但在RT中被定义为

				# define local_irq_save_nort(flags)	local_save_flags(flags)
				# define local_irq_restore_nort(flags)	(void)(flags)

				#define local_save_flags(flags)	raw_local_save_flags(flags)

				#define raw_local_save_flags(flags)			\
				do {						\
					typecheck(unsigned long, flags);	\
					flags = arch_local_save_flags();	\
				} while (0)

				static inline unsigned long arch_local_save_flags(void)
				{
					unsigned long flags;
					asm volatile("move $ccr,%0" : "=rm" (flags) : : "memory");
					return flags;
				}

		- 并没有禁止中断，只是返回了flags。
		- `local_irq_save/restore_rt`内核中没有看到对该API的定义。

- `cpu_lock_irqsave`

			#ifdef CONFIG_PREEMPT_RT_BASE
			# define cpu_lock_irqsave(cpu, flags)		\
				local_lock_irqsave_on(pa_lock, flags, cpu)

			#define local_lock_irqsave_on(lvar, _flags, cpu)			\
			do {								\
				__local_lock_irqsave(&per_cpu(lvar, cpu));		\
				_flags = per_cpu(lvar, cpu).flags;			\
			} while (0)

			static inline int __local_lock_irqsave(struct local_irq_lock *lv)
			{
				if (lv->owner != current) {
					__local_lock_irq(lv);
					return 0;
				} else {
					lv->nestcnt++;
					return 1;
				}
			}

			static inline void __local_lock_irq(struct local_irq_lock *lv)
			{
				spin_lock_irqsave(&lv->lock, lv->flags);
				LL_WARN(lv->owner);
				LL_WARN(lv->nestcnt);
				lv->owner = current;
				lv->nestcnt = 1;
			}

	- 从代码上看，`cpu_lock_irqsave（）`调用了	`spin_lock_irqsave`因此，对于RT，该API并没有禁止中断，其功能和RT`spin_lock`类似。

- `bh_uptodate_lock_irqsave`

		static inline unsigned long bh_uptodate_lock_irqsave(struct buffer_head *bh)
		{
			unsigned long flags;
		
		#ifndef CONFIG_PREEMPT_RT_BASE
			local_irq_save(flags);
			bit_spin_lock(BH_Uptodate_Lock, &bh->b_state);
		#else
			spin_lock_irqsave(&bh->b_uptodate_lock, flags);
		#endif
			return flags;
		}

		