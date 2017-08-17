* [2.6.22 - 2.6.24] freeze with mcount_enabled=1 {C::bug::hang::deadlock::semantics::atomic_inc/dec tr->disabled}
  + [[file:2.6.22/latency-tracer-disable-across-trace-cmdline.patch][2.6.22]] {MOD::kernel}
--
* [2.6.22 - 2.6.29] patches/rt-kmap-scale-fix.patch {C::bug::deadlock::deadlock::semantics::keeping a free count & tracking kmap users}
  + [[file:2.6.22/rt-kmap-scale-fix.patch][2.6.22]]

  add more atomic globals to avoid deadlock
--
* [2.6.22 - 2.6.29] patches/bh-state-lock.patch {C::bug::deadlock::deadlock::mutex::add another spinlock to track buffer header}
  + [[file:2.6.22/bh-state-lock.patch][2.6.22]]

  use spin_lock instead of bit_spin_lock
--
* [2.6.23 - 2.6.24] RCU: synchronize_sched() workaround for CPU hotplug {C::bug::deadlock::deadlock::sync::workaround for deadlock}
  + [[file:2.6.23/rcu-new-4.patch][2.6.23]]
--
* [2.6.23 - 2.6.26] fix-circular-locking-deadlock.patch {C::bug::deadlock::deadlock::order::use the reverse locking order}
  + [[file:2.6.23/fix-circular-locking-deadlock.patch][2.6.23]]

  use the reverse locking order for splice
--
* [2.6.24 - 2.6.25] lost patch for mpc52xx spinlock {C::bug::deadlock::deadlock::mutex::spin_unlock before tty_flip_buffer_push}
  + [[file:2.6.24/kernel-bug-after-entering-something-from-login.patch][2.6.24]]

  add spin_unlock/lock pair
--
* [2.6.25         ] ftrace: remove printks from max hit {C::bug::deadlock::deadlock::semantics::remove printks from max hit}
  + [[file:2.6.25/ftrace-remove-max-printks.patch][2.6.25]]

  remove printk to avoid deadlock
--
* [2.6.25         ] ftrace: unlock the mutex on reading failure {C::bug::deadlock::deadlock::mutex::unlock the mutex on reading failure}
  + [[file:2.6.25/ftrace-unlock-mutex-in-output.patch][2.6.25]]

  release the lock on error path
--
* [2.6.25         ] ftrace-remove-print-of-max.patch {C::bug::deadlock::deadlock::semantics::remove printks from trace irqsoff}
  + [[file:2.6.25/ftrace-remove-print-of-max.patch][2.6.25]]

  remove printk to avoid deadlock
--
* [2.6.25 - 2.6.26] avoid deadlock related with PG_nonewrefs and swap_lock {C::bug::deadlock::deadlock::mutex::add spin_unlock}
  + [[file:2.6.25/rt-avoid-deadlock-in-swap.patch][2.6.25]]

  move the position of spin_unlock
--
* [2.6.25 - 2.6.29] deadlock on 2.6.24.3-rt3 {C::bug::deadlock::deadlock::mutex::add spin_unlock}
  + [[file:2.6.25/swap-spinlock-fix.patch][2.6.25]]

  similiar with rt-avoid-deadlock-in-swap.patch
--
* [2.6.25 - 2.6.29] fix printk in atomic hack {C::bug::deadlock::deadlock::mutex::skips releasing the lock if in printk - atomic and not the lock owner}
  + [[file:2.6.25/printk-in-atomic-hack-fix.patch][2.6.25]]

  prevents grabbing sleeping spinlocks in printk console drivers if we can't sleep
--
* [2.6.26 - 2.6.29] arm-omap-05.patch{C::bug::deadlock::deadlock::semantics::  ARM: OMAP: remove unnecessary locking in clk_get_rate()}
  + [[file:2.6.26/arm-omap-05.patch][2.6.26]]

  remove unnecessary lock
--
* [2.6.29         ] seqlock: serialize against writers{C::bug::deadlock::deadlock::semantics::seqlock: serialize against writers}
  + [[file:2.6.29/seqlock-serialize-against-writers.patch][2.6.29]]

  changes the internal seqlock_t implementation
--
* [   3.0         ] rtc: Fix hrtimer deadlock{C::bug::deadlock::deadlock::semantics::add fun to disable timer here, not a real fix}
  + [[file:3.0/rtc-fix-hrtimer-deadlock.patch][3.0]]
--
* [   3.0 -   4.11] net-flip-lock-dep-thingy.patch{{C::bug::deadlock::deadlock::mutex::replace with _bh}
  + [[file:3.0/net-flip-lock-dep-thingy.patch][3.0]]
--
* [   3.0 -   4.11] sched: Disable CONFIG_RT_GROUP_SCHED on RT{C::bug::deadlock::deadlock::config::disable CONFIG_RT_GROUP_SCHED}
  + [[file:3.0/sched-disable-rt-group-sched-on-rt.patch][3.0]]
--
* [   3.2 -    3.6] softirq: Fix unplug deadlock{C::bug::deadlock::deadlock::semantics::add a check, rm some case and a new case to manage dead}
  + [[file:3.2/softirq-fix-unplug-deadlock.patch][3.2]]

  delaying the kthread_stop() until CPU_POST_DEAD
--
* [   3.2 -    4.0] ipc/mqueue: Add a critical section to avoid a deadlock{C::bug::deadlock::deadlock::preempt::diasble preempt}
  + [[file:3.2/ipc-mqueue-add-a-critical-section-to-avoid-a-deadlock.patch][3.2]]

  a higher priority task waits for lower priority task
--
* [   3.2 -   4.11] rcu: Frob softirq test{C::bug::deadlock::deadlock::semantics::add preempt count check}
  + [[file:3.2/peter_zijlstra-frob-rcu.patch][3.2]]
--
* [   3.4 -   4.11] futex: Fix bug on when a requeued RT task times out{C::bug::deadlock::deadlock::semantics::add macro and specific check}
  + [[file:3.4/futex-requeue-pi-fix.patch][3.4]]
--
* [   3.4 -   4.11] seqlock: Prevent rt starvation{C::bug::deadlock::deadlock::preempt::add fun to check and block}}
  + [[file:3.4/seqlock-prevent-rt-starvation.patch][3.4]]

  If a low prio writer gets preempted while holding the seqlock write locked, a high prio reader spins forever on RT
--
* [   3.6         ] mm: slab: Fix potential deadlock{C::bug::deadlock::deadlock::semantics::add macros and replace with it}
  + [[file:3.6/mm-slab-fix-potential-deadlock.patch][3.6]]

  recursive locking, acquire only the remote cpu lock
--
* [   3.6 -   4.11] perf: Make swevent hrtimer run in irq instead of softirq{C::bug::deadlock::deadlock::semantics::make field true}
  + [[file:3.6/perf-make-swevent-hrtimer-irqsafe.patch][3.6]]

  BUG: scheduling while atomic: ksoftirqd/21/141/0x00010003
  Make swevent hrtimer run in irq instead of softirq
--
* [   3.6 -   4.11] crypto: Convert crypto notifier chain to SRCU{C::bug::deadlock::deadlock::semantics::replace fun}
  + [[file:3.6/peterz-srcu-crypto-chain.patch][3.6]]

  crypto notifier deadlocks, maybe a bug on mainline
--
* [   3.8         ] printk: Fix rq->lock vs logbuf_lock unlock lock inversion{C::bug::deadlock::deadlock::semantics:: printk: Fix rq->lock vs logbuf_lock unlock lock inversion}
  + [[file:3.8/fix-rq-3elock-vs-logbuf_lock-unlock-race.patch][3.8]]

  reorder the lock operation
--
* [   3.8         ] of: fix recursive locking in of_get_next_available_child(){C::bug::deadlock::deadlock::semantics:: of: fix recursive locking in of_get_next_available_child()}
  + [[file:3.8/0001-of-fix-recursive-locking-in-of_get_next_available_ch.patch][3.8]]

  recursive locking
--
* [   3.8         ] powerpc/fsl-msi: use a different locklcass for the cascade interrupt{C::bug::deadlock::deadlock::semantics::powerpc/fsl-msi: use a different locklcass for the cascade interrupt}
  + [[file:3.8/powerpc-fsl-msi-use-a-different-locklcass-for-the-ca.patch][3.8]]

  not a bug
--
* [   3.8 -   3.14] sched: Check for idle task in might_sleep(){C::bug::deadlock::deadlock::semantics::Idle is not allowed to call sleeping functions ever!}
  + [[file:3.8/might-sleep-check-for-idle.patch][3.8]]

  idle is not allowed to call sleeping functions
--
* [  3.10 -   3.18] x86/mce: Defer mce wakeups to threads for PREEMPT_RT{C::bug::deadlock::deadlock::semantics::mce: Defer mce wakeups to threads for PREEMPT_RT}
  + [[file:3.10/x86-mce-Defer-mce-wakeups-to-threads-for-PREEMPT_RT.patch][3.10]]
--
* [  3.12 -   4.11] ptrace: fix ptrace vs tasklist_lock race{C::bug::deadlock::deadlock::mutex::ptrace: fix ptrace vs tasklist_lock race}
  + [[file:3.12/ptrace-fix-ptrace-vs-tasklist_lock-race.patch][3.12]]
--
* [  3.12 -   4.11] mm/memcontrol: Don't call schedule_work_on in preemption disabled context{C::bug::deadlock::deadlock::preempt:: mm/memcontrol: Don't call schedule_work_on in preemption disabled context}
  + [[file:3.12/mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch][3.12]]

  BUG: sleeping function called from invalid context
--
* [  3.12 -   4.11] genirq: Do not invoke the affinity callback via a workqueue on RT{C::bug::deadlock::deadlock::softirq::genirq: Do not invoke the affinity callback via a workqueue on RT}
  + [[file:3.12/genirq-do-not-invoke-the-affinity-callback-via-a-wor.patch][3.12]]
--
* [  3.12 -   4.11] usb: Use _nort in giveback function{C::bug::deadlock::deadlock::irq:: usb: use _nort in giveback}
  + [[file:3.12/usb-use-_nort-in-giveback.patch][3.12]]

  BUG: sleeping function called from invalid context
--
* [  3.14         ] rt,sched,numa: Move task_numa_free() to __put_task_struct(), which -rt offloads {C::bug::deadlock::deadlock::semantics::rt,sched,numa: Move task_numa_free() to __put_task_struct()}
  + [[file:3.14/rt-sched-numa-Move-task_numa_free-to-__put_task_stru.patch][3.14]]
--
* [  3.14 -    4.0] rt: Make cpu_chill() use hrtimer instead of msleep(){C::bug::deadlock::deadlock::semantics::rt: Make cpu_chill() use hrtimer instead of msleep()}
  + [[file:3.14/rt-Make-cpu_chill-use-hrtimer-instead-of-msleep.patch][3.14]]
--
* [  3.14 -    4.0] timer: Raise softirq if there's irq_work{C::bug::deadlock::deadlock::semantics::timer: Raise softirq if there's irq_work}
  + [[file:3.14/timer-Raise-softirq-if-there-s-irq_work.patch][3.14]]
--
* [  3.14 -    4.0] rtmutex: use a trylock for waiter lock in trylock{C::bug::deadlock::deadlock::semantics:: rtmutex: use a trylock for waiter lock in trylock}
  + [[file:3.14/rtmutex-use-a-trylock-for-waiter-lock-in-trylock.patch][3.14]]
--
* [  3.14 -   4.11] leds: trigger: disable CPU trigger on -RT{C::bug::deadlock::deadlock::semantics::leds: trigger: disable CPU trigger on -RT}
  + [[file:3.14/leds-trigger-disable-CPU-trigger-on-RT.patch][3.14]]
--
* [  3.14 -   4.11] cpu_down: move migrate_enable() back{C::bug::deadlock::deadlock::semantics::cpu_down: move migrate_enable() back}
  + [[file:3.14/cpu_down_move_migrate_enable_back.patch][3.14]]
--
* [  3.14 -   4.11] arm/unwind: use a raw_spin_lock{C::bug::hang::deadlock::semantics:: arm/unwind: use a raw_spin_lock}
  + [[file:3.14/arm-unwind-use_raw_lock.patch][3.14]]

  spin_lock_irqsave in irq-off region
--
* [  3.14 -   4.11] block: mq: use cpu_light(){C::bug::deadlock::deadlock::semantics::block: mq: use cpu_light()}
  + [[file:3.14/block-mq-use-cpu_light.patch][3.14]]

  get_cpu() disables preemption and later we grab a lock, use get_cpu_light()
--
* [  3.14 -   4.11] net: sched: Use msleep() instead of yield(){C::bug::deadlock::deadlock::semantics::sched: Use msleep() instead of yield()}
  + [[file:3.14/net-sched-dev_deactivate_many-use-msleep-1-instead-o.patch][3.14]]

  thread waits for a lower priority thread
--
* [  3.18 -   4.11] workqueue: Prevent deadlock/stall on RT {C::bug::deadlock::deadlock::preempt::add preempt_enable/disable pairs ,call worker cord unconditionally}
  + [[file:3.18/workqueue-prevent-deadlock-stall.patch][3.18]]

  accessed data structures are not protected against scheduling due to the spinlock to rtmutex conversion
--
* [  3.18 -   4.11] cgroups: use simple wait in css_release() {C::bug::crash::deadlock::mutex::add simple_wait_queue}
  + [[file:3.18/cgroups-use-simple-wait-in-css_release.patch][3.18]]

  BUG: sleeping function called from invalid context
--
* [  3.18 -   4.11] block: blk-mq: Use swait {C::bug::crash::deadlock::mutex::replace with swait}
  + [[file:3.18/block-blk-mq-use-swait.patch][3.18]]

  BUG: sleeping function called from invalid context
--
* [   4.0         ] irq_work: Delegate non-immediate irq work to ksoftirqd{C::bug::deadlock::deadlock::softirq::delegate non-immediate irq work to ksoftirqd}
  + [[file:4.0/irq_work_Delegate_non-immediate_irq_work_to_ksoftirqd.patch][4.0]]

  delegating all non-immediate work to ksoftirqd
--
* [   4.0         ] kernel/irq_work: fix no_hz deadlock{C::bug::deadlock::deadlock::irq::upstream}
  + [[file:4.0/kernel-irq_work-fix-no_hz-deadlock.patch][4.0]]
--
* [   4.0 -   4.11] sunrpc: Make svc_xprt_do_enqueue() use get_cpu_light(){C::bug::deadlock::deadlock::preempt::conver the get_cpu() to get_cpu_light()}
  + [[file:4.0/sunrpc-make-svc_xprt_do_enqueue-use-get_cpu_light.patch][4.0]]

  BUG: sleeping function called from invalid context
--
* [   4.0 -   4.11] slub: Disable SLUB_CPU_PARTIAL{C::bug::deadlock::deadlock::config::add config}
  + [[file:4.0/slub-disable-SLUB_CPU_PARTIAL.patch][4.0]]

  BUG: sleeping function called from invalid context
--
* [   4.0 -   4.11] fs/aio: simple simple work{C::bug::deadlock::deadlock::preempt::replace with swork}
  + [[file:4.0/fs-aio-simple-simple-work.patch][4.0]]

  BUG: sleeping function called from invalid context
--
* [   4.0 -   4.11] sas-ata/isci: dont't disable interrupts in qc_issue handler{C::bug::deadlock::deadlock::irq::use loacl_irq_save_nort() do not disable irq}
  + [[file:4.0/sas-ata-isci-dont-t-disable-interrupts-in-qc_issue-h.patch][4.0]]

  BUG: sleeping function called from invalid context
--
* [   4.0 -   4.11] thermal: Defer thermal wakups to threads{C::bug::crash::deadlock::sched::defer thermal wakups}
  + [[file:4.0/thermal-Defer-thermal-wakups-to-threads.patch][4.0]]

  call schedule while we run in irq context
--
* [   4.0 -   4.11] snd/pcm: fix snd_pcm_stream_lock*() irqs_disabled() splats{C::bug::deadlock::deadlock::mutex::replace with nort lock}
  + [[file:4.0/snd-pcm-fix-snd_pcm_stream_lock-irqs_disabled-splats.patch][4.0]]

  BUG: sleeping function called from invalid context
--
* [   4.0 -   4.11] ARM: enable irq in translation/section permission fault handlers{C::bug::deadlock::deadlock::irq::enable irq}
  + [[file:4.0/ARM-enable-irq-in-translation-section-permission-fau.patch][4.0]]

  BUG: sleeping function called from invalid context
--
* [   4.0 -   4.11] x86/mce: use swait queue for mce wakeups{C::bug::deadlock::deadlock::preempt::use swait queue for mce}
  + [[file:4.0/x86-mce-use-swait-queue-for-mce-wakeups.patch][4.0]]

  MCE irq hasn't been turned into schedulable threads and bugs on spin_lock (rt_mutex)
--
* [   4.4 -   4.11] ARM: smp: Move clear_tasks_mm_cpumask() call to __cpu_die(){C::bug::deadlock::deadlock::semantics::Move clear_tasks_mm_cpumask() call to __cpu_die()}
  + [[file:4.4/rfc-arm-smp-__cpu_disable-fix-sleeping-function-called-from-invalid-context.patch][4.4]]

  BUG: sleeping function called from invalid context
--
* [   4.6 -   4.11] mm: rt: Fix generic kmap_atomic for RT{C::bug::deadlock::deadlock::preempt::got converted to the _nort() variant}
  + [[file:4.6/mm--rt--Fix-generic-kmap_atomic-for-RT.patch][4.6]]

  scheduling while atomic/sleeping function called from invalid context
--
* [   4.6 -   4.11] drm,i915: Use local_lock/unlock_irq() in intel_pipe_update_start/end(){C::bug::deadlock::deadlock::irq::replace local_irq_enable with local_unlock_irq()}
  + [[file:4.6/drmi915_Use_local_lockunlock_irq()_in_intel_pipe_update_startend().patch][4.6]]

  BUG: sleeping function called from invalid context
--
* [   4.6 -    4.9] sc16is7xx: Drop bogus use of IRQF_ONESHOT{C::bug::deadlock::deadlock::irq::remove IRQF_ONESHOT parameter}
  + [[file:4.6/sc16is7xx_Drop_bogus_use_of_IRQF_ONESHOT.patch][4.6]]
--
* [   4.6 -   4.11] drivers/block/zram: Replace bit spinlocks with rtmutex for -rt{C::bug::deadlock::deadlock::mutex::Replace bit spinlocks with rtmutex }
  + [[file:4.6/drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch][4.6]]

  use spin_lock instead of bit_spin_lock
--
* [   4.6 -   4.11] mm: backing-dev: don't disable IRQs in wb_congested_put(){C::bug::deadlock::deadlock::irq::repalce local_irq_save() with its variant _nort()}
  + [[file:4.6/mm-backing-dev-don-t-disable-IRQs-in-wb_congested_pu.patch][4.6]]

  BUG: sleeping function called from invalid context
--
* [   4.9 -   4.11] connector/cn_proc: Protect send_msg() with a local lock on RT{C::bug::deadlock::deadlock::preempt::repace with local lock}
  + [[file:4.9/connector-cn_proc-Protect-send_msg-with-a-local-lock.patch][4.9]]

  BUG: sleeping function called from invalid context
--
* [   4.9 -   4.11] arm: kprobe: replace patch_lock to raw lock{C::bug::deadlock::deadlock::irq::replace with raw lock}
  + [[file:4.9/arm-kprobe-replace-patch_lock-to-raw-lock.patch][4.9]]

  BUG: sleeping function called from invalid context
--
* [  4.11         ] cpuset: Convert callback_lock to raw_spinlock_t{C::bug::deadlock::deadlock::mutex::replace with raw}
  + [[file:4.11/cpuset-Convert-callback_lock-to-raw_spinlock_t.patch][4.11]]

  BUG: sleeping function called from invalid context
--
* [  4.11         ] char/random: don't print that the init is done{C::bug::deadlock::deadlock::semantics::remove or delay printf info}
  + [[file:4.11/char-random-don-t-print-that-the-init-is-done.patch][4.11]]

  skip printk
--
* [  4.11         ] Revert "random: invalidate batched entropy after crng init"{C::bug::crash::deadlock::semantics::revert random}
  + [[file:4.11/Revert-random-invalidate-batched-entropy-after-crng-.patch][4.11]]

  reverts a previous commit
