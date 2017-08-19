

- pattern 1
	- `cpu_hotplug_disable(void)替代get_online_cpus(void)`
	 
			void get_online_cpus(void)
			{
				might_sleep();
				if (cpu_hotplug.active_writer == current)
					return;
				cpuhp_lock_acquire_read();
				mutex_lock(&cpu_hotplug.lock);
				atomic_inc(&cpu_hotplug.refcount);
				mutex_unlock(&cpu_hotplug.lock);
			}

			#define mutex_lock(l)			_mutex_lock(l)

			void __lockfunc _mutex_lock(struct mutex *lock)
				{
					mutex_acquire(&lock->dep_map, 0, 0, _RET_IP_);
					rt_mutex_lock(&lock->lock);
				}

			void cpu_hotplug_disable(void)
				{
					cpu_maps_update_begin();
					cpu_hotplug_disabled++;
					cpu_maps_update_done();
				}

			void cpu_maps_update_begin(void)
				{
					mutex_lock(&cpu_add_remove_lock);
				}
	这里可能是`get_online_cpus()`的递归调用可能导致死锁。
	- 相关patch：
		- [[file:4.11/0020-PCI-Use-cpu_hotplug_disable-instead-of-get_online_cp.patch][4.11]]

- pattern 2
	- `get_locked_var()`代替了`get_cpu_light();和__get_cpu_var();`
	
			#define get_locked_var(lvar, var)					\
			    	(*({								\
			    		local_lock(lvar);					\
			    		this_cpu_ptr(&var);					\
			    	}))
				
			#define local_lock(lvar)					\
			do { __local_lock(&get_local_var(lvar)); } while (0)

			
			#define get_local_var(var) (*({	\
					migrate_disable();	\
					this_cpu_ptr(&var);	}))
			

			commit中提到此处是为了实现两个功能（我觉得这里最主要的是实现本地序列化的功能）：

			The per-cpu here thus is assuming exclusivity serializing per cpu - so
			the use of get_cpu_ligh introduced in
			net-use-cpu-light-in-ip-send-unicast-reply.patch, which droped the
			preempt_disable in favor of a migrate_disable is probably wrong as this
			only handles the referencial consistency but not the serialization. To
			evade a preempt_disable here a local lock would be needed.
			
			Therapie:
				 * add local lock:
				 * and re-introduce local serialization:

	- 相关patch：
		- [[file:3.14/net-ipsendunicast_reply-add-missing-local-serializ.patch][3.14]]



- pattern 3
	- `trace_clock_local(void)`替代`ktime_get()`
	
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
			
	这里是在调用ktime_get(),为了防止其他CPUs抢占`read_seq()`,对获取的time有影响，因此在available的地方选用`trace_clock_local(void)`。
	- 相关patch
		- [[file:3.12/hwlat-detector-Use-traceclocklocal-if-available.patch][3.12]]

- pattern 4
	- 增加local_lock()进行明确的序列化
	- 此处是netfilter在！RT中，需要`local_bh_disable()`对`xt_write_recseq`的隐含序列化，而在RT中则需要通过local_lock()进行明确的序列化。
	- 相关patch
		- [[file:3.8/net-fix-iptable-xt-write-recseq-begin-rt-fallout.patch][3.8]]

- pattern 5
	- `wait_queue()`代替`wait_on_work()`
	- 应该是避免worklet in nested list complete too late.
	- 相关patch
		- [[file:2.6.24/rt-wq-barrier-fix.patch][2.6.24]]

- pattern 6
	- workqueue-barrier的修复（看不太懂）
	
	That is, the barrier will splice the worklist into itself, and enqueue itself as the next item to run (very first item, highest prio). The barrier will then run its own plist to completion before 'popping' back to the regular worklist.

	To avoid callstack nesting, run_workqueue is taught about this barrier stack.

	
	- 相关patch
		- [[file:2.6.24/rt-workqueue-barrier.patch][2.6.24]]

