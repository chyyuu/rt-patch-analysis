* [2.6.22         ] clockevents-fix-resume-logic.patch {C::bug::idle::order::sync::resume clockevent device before resume tick}
  + [[file:2.6.22/clockevents-fix-resume-logic.patch][2.6.22]]   {MOD::arch/i386,arch/arm,arch/sh,arch/sparc64, kernel/time, include/linux}
    	
		增加了clock event mode 用来在系统处于空模式的C-states状态恢复过程中的恢复顺序，确保clockevent devices在tick之前被重新启动，避免定时器中断产生，而clock event devices还没有恢复。

--

* [2.6.22         ] cpuidle_hang_fix.patch {C::bug::hang::order::sync::idle handler to enable intr before returning from idle handler, set current driver to NULL when fail to attach on all devices}
  + [[file:2.6.22/cpuidle_hang_fix.patch][2.6.22]]  {MOD::dirvers/cpuidle}
  
	此处是为了阻止当ACPI处理器驱动被增加到一个不支持C-states的系统中，x86-64挂起。
	x86-64希望所有的空操作在返回之前都能够在使能中断。因此，这里通过增加else语句，来使能本地中断。

--

* [2.6.22         ] module-pde-race-fixes.patch {C::bug::crash::order::sync::module reloaded when still need to be used, add a atomic counter to counting reads and writes in progress}
  + [[file:2.6.22/module-pde-race-fixes.patch][2.6.22]]  {MOD::fs/proc,include/linux}
  
		没看明白

--

* [2.6.22         ] s_files-proc-generic-fix.patch {C::bug::na::order::sync::advance filevec_add_drain_all()}
  + [[file:2.6.22/s_files-proc-generic-fix.patch][2.6.22]]  {MOD::fs/proc}

	调整函数位置
   
--

* [2.6.22 - 2.6.25] More Fixes to TASKLET_STATE_SCHED WARN_ON() {C::bug::crash::order::sync::add statement}
  + [[file:2.6.22/tasklet-more-fixes.patch][2.6.22]]
  
			> BUG: at kernel/softirq.c:639 __tasklet_action()
			> 
			> Call Trace:
			>  [<ffffffff8106d5da>] dump_trace+0xaa/0x32a
			>  [<ffffffff8106d89b>] show_trace+0x41/0x5c
			>  [<ffffffff8106d8cb>] dump_stack+0x15/0x17
			>  [<ffffffff81094a97>] __tasklet_action+0xdf/0x12e
			>  
	从上边的Call Trace:中可以看出bug产生在__tasklet_action函数调用处，

			> the idea is while __tasklet_action is running the tasklet function
			> on CPU1, if a call to tasklet_schedule() on CPU2 is made, and if right
			> after we mark the TASKLET_STATE_SCHED bit we are preempted,
			> __tasklet_action on CPU1 might be able to re-run the function, clear the
			> bit and unlock the tasklet before CPU2 enters __tasklet_common_schedule.
			> Once __tasklet_common_schedule locks the tasklet, we will add the
			> tasklet to the list with the TASKLET_STATE_SCHED *unset*. 
	不是太能看明白，但是结果就是在没有设置`TASKLET_STATE_SCHED`的情况下，将tasklet 加入到list中，此处是增加对`TASKLET_STATE_SCHED`的判断来保证设置。
	

--

* [2.6.22 - 2.6.25] powerpc 2.6.21-rt1: fix kernel hang and/or  panic {C::bug::hang::order::order::restore preempt_none method}
  + [[file:2.6.22/preempt-irqs-ppc-celleb-beatic-eoi.patch][2.6.22]]

	这里是在threaded irq handler中出现的hangs，由于code path differs 在`PREEMPT_NONE`和`PREEMPT_RT`
	
		NONE: mask() -> unmask() -> eoi() 
	  	RT:   mask() -> eoi() -> unmask()
	
	修复的方法是重新将代码路径恢复到PREEMPT_NONE

--

* [2.6.22 - 2.6.26] s_files: free_write_pipe() fix {C::bug::data_err::order::sync::add cleanup var}
  + [[file:2.6.22/s_files-pipe-fix.patch][2.6.22]]

		make sure we free the inode before the file

		调整了函数位置

--

* [2.6.24 - 2.6.26] rt: PI-workqueue: fix barriers {C::bug::rtlatency::order::sync::The solution used is to nest plist structures.}
  + [[file:2.6.24/rt-workqueue-barrier.patch][2.6.24]]

	关于workqueue-barrier的修复，看不懂

	That is, the barrier will splice the worklist into itself, and enqueue itself
	as the next item to run (very first item, highest prio). The barrier will then
	run its own plist to completion before 'popping' back to the regular worklist.

	To avoid callstack nesting, run_workqueue is taught about this barrier stack.

--

* [2.6.24 - 2.6.26] rt: PI-workqueue: wait_on_work() fixup {C::bug::rtlatency::order::sync::using a wait_queue to target at a worklet in a nested list}
  + [[file:2.6.24/rt-wq-barrier-fix.patch][2.6.24]]

	此处用`wait_queue()`代替`wait_on_work()`,避免worklet in nested list complete too late.

--

* [2.6.25         ] ftrace: avoid lockdep annotation problems {C::bug::data_err::order::order::move the capturing of the timestamp outside of the raw spinlocksof ftrace}
 + [[file:2.6.25/ftrace-handle-time-outside-of-lockdep.patch][2.6.25]]

	这里应该是将可能含有睡眠锁`spin_lock`移出中断禁止区域。

--

* [2.6.25 - 2.6.26] x86_64: send NMI after nmi_show_regs on {C::bug::crash::order::order::send NMI after nmi_show_regs on}
  + [[file:2.6.25/nmi-watchdog-fix-1.patch][2.6.25]]

	这里是对NMI-watchdog设置顺序的修复，需要将`nmi_show_regs`对flag设置应该在send NMI之前。

--

* [2.6.25 - 2.6.26] wait for finish show_regs() before panic {C::bug::crash::order::order::clear nmi_show_regs after show_regs() is called}
  + [[file:2.6.25/nmi-watchdog-fix-4.patch][2.6.25]]

		

--

* [2.6.25 - 2.6.26] x86: nmi_watchdog NMI needed for irq_show_regs_callback() {C::bug::crash::order::order::change nmi_watchdog fucntion}
  + [[file:2.6.25/nmi-watchdog-fix-3.patch][2.6.25]]

		

--

* [   3.8 -   4.11] net: netfilter: Serialize xt_write_recseq sections on RT{C::bug::data_err::order::order::net: netfilter: Serialize xt_write_recseq sections on RT}
  + [[file:3.8/net-fix-iptable-xt-write-recseq-begin-rt-fallout.patch][3.8]]

	此处是netfilter在！RT中，需要`local_bh_disable()`对`xt_write_recseq`的隐含序列化，而在RT中则需要通过local_lock()进行明确的序列化。

--

* [  3.12 -    4.8] hwlat-detector: Use trace_clock_local if available{C::bug::data_err::order::semantics::hwlat-detector: Use trace_clock_local if available}
  + [[file:3.12/hwlat-detector-Use-trace_clock_local-if-available.patch][3.12]]

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
			

--

* [  3.14 -   3.18] net: ip_send_unicast_reply: add missing local serialization{C::bug::data_err::order::mutex::net: ip_send_unicast_reply: add missing local serialization}
  + [[file:3.14/net-ip_send_unicast_reply-add-missing-local-serializ.patch][3.14]]

	此处是用`get_locked_var()`代替了`get_cpu_light();和__get_cpu_var();`

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

--

* [  4.11         ] PCI: Use cpu_hotplug_disable() instead of get_online_cpus(){C::bug::deadlock::order::hardware::replace with cpu_hotplug_disable()}
  + [[file:4.11/`0020-PCI-Use-cpu_hotplug_disable-instead-of-get_online_cp.patch`][4.11]]

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

			用cpu_hotplug_disable(void)替代get_online_cpus(void)，这里可能是`get_online_cpus()`的递归调用可能导致死锁