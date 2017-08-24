

- `lock/unlock_fpu_owner()`	

		#define lock_fpu_owner()	({ preempt_disable(); pagefault_disable(); })

		#define unlock_fpu_owner()	({ pagefault_enable(); preempt_enable(); })

		static inline void pagefault_disable(void)
			{
				migrate_disable();
				pagefault_disabled_inc();
				/*
				 * make sure to have issued the store before a pagefault
				 * can hit.
				 */
				barrier();
			}
			
			static inline void pagefault_enable(void)
			{
				/*
				 * make sure to issue those last loads/stores before enabling
				 * the pagefault handler again.
				 */
				barrier();
				pagefault_disabled_dec();
				migrate_enable();
			}

		
	- 为什么禁止抢占了，还要禁止迁移，是否禁止抢占不能保证禁止迁移？？？