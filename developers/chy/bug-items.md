# 对 history.org中的bug分类进行进一步分析

## semantics

- migration  yxg

- preempt    zzm

- sched      zw

- irq/softirq  mym

## concurrency

- atomicity:  yxg

- order:      zzm

- deadlock:   zw

- livelock:   mym
  - cpu_chill -->> cpu_relax (实际上是pause指令，一般在忙等，循环)

get_online_cpu 语义已经修改了，导致会出现deadlock， nest_lock
ref cnt -->> rt_mutex   不能出现ABBA

cpu_hotplug_disable 可能会引入新的bug

====
 [[file:4.11/snd-pcm-fix-snd_pcm_stream_lock-irqs_disabled-splats.patch][snd-pcm-fix-snd_pcm_stream_lock-irqs_disabled-splats.patch]]
 	if (!substream->pcm->nonatomic)
-		local_irq_disable();
+		local_irq_disable_nort();
 	snd_pcm_stream_lock(substream);
 }
|BUG: sleeping function called from invalid context at kernel/locking/rtmutex.c:915
|in_atomic(): 0, irqs_disabled(): 1, pid: 5947, name: alsa-sink-ALC88
|CPU: 5 PID: 5947 Comm: alsa-sink-ALC88 Not tainted 3.18.7-rt1 #9
|Hardware name: MEDION MS-7848/MS-7848, BIOS M7848W08.404 11/06/2014
| ffff880409316240 ffff88040866fa38 ffffffff815bdeb5 0000000000000002
| 0000000000000000 ffff88040866fa58 ffffffff81073c86 ffffffffa03b2640
| ffff88040239ec00 ffff88040866fa78 ffffffff815c3d34 ffffffffa03b2640
|Call Trace:
| [<ffffffff815bdeb5>] dump_stack+0x4f/0x9e
| [<ffffffff81073c86>] __might_sleep+0xe6/0x150
| [<ffffffff815c3d34>] __rt_spin_lock+0x24/0x50
| [<ffffffff815c4044>] rt_read_lock+0x34/0x40
| [<ffffffffa03a2979>] snd_pcm_stream_lock+0x29/0x70 [snd_pcm]

在atomic context 中引入了mutex, 即snd_pcm_stream_lock， 会 sleeping



对于per_cpu而言，比较好的内核设计是：
n个cpu，则有 n个kernel_thread，每个cpu一个，不会出现在一个cpu上运行多个kernel_thread的情况。
这样，用per_cpu就很好了，即有本地的var可以访问，且不用担心对var的独占访问。因为不会在一个cpu上存在两个kernel_thread/process，且都会访问per_cpu的var.

我如何知道这个变量的访问是否可以在process context or kernel thread context?



# bug items

## 2.6.22.1-rt

### quicklist-release-before-free-page.patch 

BUG: sleeping function called from invalid context cc1(29651) at kernel/rtmutex.c:636

Not quite, it uses preempt_disable() to avoid migration and stick to a
cpu. Without that it might end up freeing pages from another quicklist.

How about this - compile tested only

We cannot call the page allocator with preemption-disabled, use the
per_cpu_locked construct to allow preemption while guarding the per cpu
data.

###  tasklet-fix-preemption-race.patch

Paul also pointed this out awhile back: http://lkml.org/lkml/2007/2/25/1


Anyway, I think I finally found the issue. Its a bit hard to explain,
but the idea is while __tasklet_action is running the tasklet function
on CPU1, if a call to tasklet_schedule() on CPU2 is made, and if right
after we mark the TASKLET_STATE_SCHED bit we are preempted,
__tasklet_action on CPU1 might be able to re-run the function, clear the
bit and unlock the tasklet before CPU2 enters __tasklet_common_schedule.
Once __tasklet_common_schedule locks the tasklet, we will add the
tasklet to the list with the TASKLET_STATE_SCHED *unset*. 

I've verified this race occurs w/ a WARN_ON in
__tasklet_common_schedule().

This fix avoids this race by making sure *after* we've locked the
tasklet that the STATE_SCHED bit is set before adding it to the list.

### [2.6.22         ] preempt-realtime-gtod-fixups.patch
注意:write_seqlock_irqsave/irqrestore
Index: linux-rt.q/kernel/time/timekeeping.c
===================================================================
--- linux-rt.q.orig/kernel/time/timekeeping.c
+++ linux-rt.q/kernel/time/timekeeping.c
@@ -366,9 +366,13 @@ static int timekeeping_suspend(struct sy
 {
 	unsigned long flags;
 
+	/*
+	 * Read the CMOS outside the raw xtime_lock:
+	 */
+	timekeeping_suspend_time = read_persistent_clock();
+
 	write_seqlock_irqsave(&xtime_lock, flags);
 	timekeeping_suspended = 1;
-	timekeeping_suspend_time = read_persistent_clock();
 	write_sequnlock_irqrestore(&xtime_lock, flags);
 
 	clockevents_notify(CLOCK_EVT_NOTIFY_SUSPEND, NULL);


## 3.0-rt1

###  drivers-dca-convert-dcalock-to-raw.patch

 tglx: Fixed the domain allocation which was calling kzalloc from the
  	irq disabled section

### drivers-floppy-use-timer-del-sync.patch

### drivers-net-at91-make-mdio-protection-rt-safe.patch

###  drivers-net-ehea-mark-rx-irq-no-thread.patch

Without this patch, a simple scp file copy loop would fail quickly (usually
seconds). We have over two hours of sustained scp activity with the patch
applied.

### drivers-net-fix-livelock-issues.patch

reempt-RT runs into a live lock issue with the NETDEV_TX_LOCKED micro
optimization. The reason is that the softirq thread is rescheduling
itself on that return value. Depending on priorities it starts to
monoplize the CPU and livelock on UP systems.

### fs-add-missing-rcu-protection.patch

sys_ioprio_get() accesses __task_cred() without being in a RCU read
side critical section. tasklist_lock is not protecting that when
CONFIG_TREE_PREEMPT_RCU=y.

Add a rcu_read_lock/unlock() section around the code which accesses
__task_cred().	

### fs-ntfs-disable-interrupt-non-rt.patch

```
-		local_irq_save(flags);
+		local_irq_save_nort(flags);
 		kaddr = kmap_atomic(page, KM_BIO_SRC_IRQ);
 		for (i = 0; i < recs; i++)
 			post_read_mst_fixup((NTFS_RECORD*)(kaddr +
 					i * rec_size), rec_size);
 		kunmap_atomic(kaddr, KM_BIO_SRC_IRQ);
-		local_irq_restore(flags);
+		local_irq_restore_nort(flags);
```



# perf item

## 3.0-rt1

### block-shorten-interrupt-disabled-regions.patch

Moving the blk_sched_flush_plug() call out of the interrupt/preempt
disabled region in the scheduler allows us to replace
local_irq_save/restore(flags) by local_irq_disable/enable() in
blk_flush_plug().

###  epoll-use-get-cpu-light.patch

get/put_cpu --> get/put_cpu_light

# feature item (keep semantics)

## 3.0-rt1

### dmar-make-register-lock-raw.patch

###  drivers-net-gianfar-make-rt-aware.patch

The adjust_link() disables interrupts before taking the queue
locks. On RT those locks are converted to "sleeping" locks and
therefor the local_irq_save/restore must be converted to
local_irq_save/restore_nort.

# feature item (change semantics)

## 3.0-rt1

### mm-cgroup-page-bit-spinlock.patch

Bit spinlocks are not working on RT. Replace them.

```
+#ifndef CONFIG_PREEMPT_RT_BASE
 	/*
 	 * We know updates to pc->flags of page cache's stats are from both of
 	 * usual context or IRQ context. Disable IRQ to avoid deadlock.
 	 */
 	local_irq_save(*flags);
 	bit_spin_lock(PCG_MOVE_LOCK, &pc->flags);
+#else
+	spin_lock_irqsave(&pc->pcm_lock, *flags);
+#endif
```



# questions



### how to find unique patch set

## how to avoid bug

### when &where using might_sleep?

###  when & where using disable/enable_migration/preempt? net-core-preempt-fix.patch

### how to narrow lock for reduce latencies?  mm-fix-latency.patch

### how to add pt point?  preempt-realtime-usb.patch

## 用rid的方法分析？
- task_struct * p->migrate_disable +,-,set
- preempt_count +,-, set

## 用justa方法分析？
- 在in_atomic实现中，有注释 Do not use in_atomic() in driver code，why?

### 用数据挖掘的方法进行分类？

different patch。一样/不一样的标准是啥？



patch的来源 rt-patches 和 edf

分析patch的方法

分类

bug: keyword: fix, hang, bug, race dead lock, live lock,fali

perf: latency ,drops the idle latency, Shorten

feature: easy,  convert

# need to know

## other important item

###  change die_chain from atomic to raw notifiers
??? NMI-safe
	return atomic_notifier_chain_unregister(&die_chain, nb);
	return raw_notifier_chain_unregister(&die_chain, nb);
区别是啥？

### cpuidle_hang_fix.patch 
???

### pt-rt--core  preempt-realtime-core.patch

### pt-irqs-core  preempt-irqs-core.patch

### pt-rt-sched  preempt-irqs-core.patch

### pt-rt-timer  preempt-realtime-timer.patch

### pt-rt-softirqs-core  preempt-softirqs-core.patch

### get/put_cpu_var_locked   **quicklist-release-before-free-page.patch** 



https://lwn.net/Articles/106010/
raw_notifier_call_chain
There are, of course, a few nagging little problems to deal with. Some code in the system really *shouldn't* be preempted while holding a lock. In particular, code which might be in the middle of programming hardware registers, the page table handling code, and the scheduler itself need to be allowed to do their job in peace. It is hard, after all, to imagine a scenario where preempting the scheduler will lead to good things. So a number of places in the kernel cannot be switched from spinlocks to the new mutexes.

在2.6.22的patch:: change die_chain from atomic to raw notifiers中
atomic_notifier_call_chain --> raw_notifier_call_chain 
为何需要这样??


+#ifdef CONFIG_PREEMPT_RCU
+	return rcu_batches_completed();
+#else
 	return rcu_batches_completed_bh();
+#endif
rcu_batches_completed和rcu_batches_completed_bh的区别是啥？

能否确切地知道哪些地方是不能用new mutex来代替已有的spinlock的？

https://lwn.net/Articles/105948/

```
i've released the -T4 VP patch:

  http://redhat.com/~mingo/voluntary-preempt/voluntary-pree...

the big change in this release is the addition of PREEMPT_REALTIME,
which is a new implementation of a fully preemptible kernel model:

 - spinlocks and rwlocks use semaphores and are preemptible by default

 - the _irq variants of these locks do not disable interrupts but rely
   on IRQ threading to exclude against interrupt contexts.
```



https://lwn.net/Articles/107269/  Realtime preemption, part 2

To get to that point, Ingo had to make changes to a number of Linux mutual exclusion primitives which got in the way. One of those is per-CPU variables, which are based around the idea that, as long as each processor only works with its own copy of a variable, no locking is required to make that work safe. That assumption only holds, however, if threads are not preempted while manipulating per-CPU variables. So using a per-CPU variable requires disabling preemption, which runs counter to the whole "make everything preemptible" idea. To address this problem, Ingo introduced a new "locked" per-CPU variable type:

```
    DEFINE_PER_CPU_LOCKED(type, name);

    get_cpu_var_locked(var, cpu);
    put_cpu_var_locked(var, cpu);

```

Threads which use the "locked" type of per-CPU variable can be preempted while working with that variable - they can even be shifted to a different processor while sleeping. The result could be a thread updating the "wrong" processor's version of the variable. The lock will prevent race conditions, however, so, [as Ingo puts it](https://lwn.net/Articles/106567/), "'statistically' the variable is still per-CPU and update correctness is fully preserved."

Then, there is the issue of read-copy-update, which also depends on threads not being preempted while they hold a reference to RCU-protected data. Ingo's approach here was, essentially, to dump RCU in the realtime case and just go back to regular locking. This change is hard to do in any sort of automatic way, however, because the RCU read locking primitive (rcu_read_lock(), which, normally, just disables preemption) does not identify which data is being protected. So converting RCU code requires picking out a spinlock or semaphore which can be used to prevent races with writers, and to change the rcu_read_lock() calls to one of the many new variants:

```
    rcu_read_lock_sem(struct semaphore *sem);
    rcu_read_lock_down_read(struct rwsem *sem);
    rcu_read_lock_spin(spinlock_t *lock);
    ...

```

This API, Ingo notes, is still in flux. There does not seem to have been any benchmarking done yet to determine what effect these changes have on the scalability issues RCU was created to address.

Atomic kmaps were another problem. An atomic kmap is a mechanism used to quickly map a high memory page into the kernel's address space. It is, for all practical purposes, an implementation of per-CPU page table entries, and it has the same preemption issues. The solution here was the addition of a new function (kmap_atomic_rt()) which turns into a regular, non-atomic kmap when realtime preemption is enabled. In this case (as with many of the others) the low-latency imperative brings a small overall performance cost.

As a sort of side project, many users of semaphores in the kernel were changed over to the [completion](https://lwn.net/Articles/23993/) mechanism. Some new completion functions have been added to help with that process:

```
    int wait_for_completion_interruptible(struct completion *c);
    unsigned long wait_for_completion_timeout(struct completion *c,
                                              unsigned long timeout);
    unsigned long wait_for_completion_interruptible_timeout(struct completion *c,
                                              unsigned long timeout);

```

Quite a few other changes have gone in, but the idea should be clear by now: a vast number of changes are being made to the kernel's fundamental assumptions about locking and the execution environment. Few readers will be surprised to learn that the brave souls testing these patches have been encountering significant numbers of bugs. Those bugs are being squashed in a hurry, though, to the point that Ingo can [say](https://lwn.net/Articles/106567/):

I also think that this feature can and should be integrated into the upstream kernel sometime in the future. It will need improvements and fixes and lots of testing, but i believe the basic concept is sound and inclusion is manageable and desirable.

The interesting thing is that nobody has come forward to challenge that statement. As the realtime preemption patches become more stable, and the pressure for their inclusion starts to build, that situation may well change. It is hard to imagine a patch this intrusive going in without some sort of fight - especially when many developers are far from convinced about the goal of supporting realtime applications in Linux to begin with.

## history

RCU and Real Time: History
 2005: Preemptible RCU take 1 (in -rt)
 2007: Preemptible RCU take 2: nonatomic (in mainline)
 2009: Preemptible RCU take 3: scalable (in mainline)
 2012: Bug report claiming 200-microsecond latency spikes from RCU grace-period initialization

  – Which came as quite a surprise given ~30-microsecond latencies from
the entire kernel, not just RCU...
  – But further down in the email, there was a kernel-configuration
parameter that fully explained the difference in latency

  – NR_CPUS=4096!!!
​     • At which point: “You mean it only took 200 microseconds???” 
​     • Therefore...



# 配置/运行rt注意事项



There's a lot that must be done to get hard realtime performance under PREEMPT_RT. Here are the things I am aware of. Entries marked with an asterisk apply to your current position.

- Patch the kernel with PREEMPT_RT (as you already did), and enable CONFIG_PREEMPT_RT_FULL (which used to be called CONFIG_PREEMPT_RT, as you correctly derived).
- Disable processor frequency scaling (either by removing it from the kernel configuration or by changing the governor or its settings). (*)
  - Reasoning: Changing a core's frequency takes a while, during which the core does no useful work. This causes high latencies.
  - To remove this, look under the ACPI options in the kernel settings.
  - If you don't want to remove this capability from the kernel, you can set the cpufreq governor to "performance" to lock it into its highest frequency.
- Disable deep CPU sleep states
  - Reasoning: Like switching frequencies, Waking the CPU from a deep sleep can take a while.
  - Cyclictest does this for you (look up /dev/cpu_dma_latency to see how to do it in your application).
  - Alternatively, you can disable the "cpuidle" infrastructure in the kernel to prevent this from ever occurring.
- Set a high priority for the realtime thread, above 50 (preferably 99) (*)
  - Reasoning: You need to place your priority above the majority of the kernel -- much of a PREEMPT_RT kernel (including IRQs) runs at a priority of 50.
  - For cyclictest, you can do this with the "-p#" option, e.g. "-p99".
- Your application's memory must be locked. (*)
  - Reasoning: If your application's memory isn't locked, then the kernel may need to re-map some of your application's address space during execution, triggering high latencies.
  - For cyclictest, this may be done with the "-m" option.
  - To do this in your own application, see [the RT_PREEMPT howto](https://rt.wiki.kernel.org/index.php/RT_PREEMPT_HOWTO).
- You must unload the nvidia, nouveau, and i915 modules if they are loaded (or not build them in the first place) (*)
  - Reasoning: These are known to cause high latencies. Hopefully you don't need them on a realtime system :P
- Your realtime task must be coded to be realtime
  - For example, you cannot do file access or dynamic memory allocation via malloc(). Many system calls are off-limits (it's hard to find which ones are acceptable, IMO).
  - cyclictest is mostly already coded for realtime operation, as are many realtime audio applications. You do need to run it with the "-n" flag, however, or it will not use a realtime-safe sleep call.

The actual execution of cyclictest should have at least the following set of parameters:

```
sudo cyclictest -p99 -m -n
```
