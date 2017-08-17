# semantics::sched

使用正则表达式`bug::\w+::sched`在history.org中搜索，找到的相关patch有

* disable-sched-rt-groups.patch
* sched-fix-dequeued-race.patch
* cpuhotplug-idle.patch
* sched-adjust-reset-on-fork-always.patch
* sched-consider-pi-boosting-in-setscheduler.patch
* sched-Init-idle-on_rq-in-init_idle.patch
* sched-enqueue-to-head.patch
* sched-Adjust-p-sched_reset_on_fork-when-nothing-else.patch
* sched-Fix-broken-setscheduler.patch
* mm-perform-lru_add_drain_all-remotely.patch

有规律可循的一类bug为调度及不当设置优先级引起的任务顺序错乱问题，相关patch有

* sched-enqueue-to-head.patch
* sched-consider-pi-boosting-in-setscheduler.patch
* sched-Fix-broken-setscheduler.patch

前两者都属于未正确将进程加入runqueue导致的问题，第三个属于优先级设置不当。以sched-enqueue-to-head.patch为例，假设某时刻一个CPU的runqueue上有任务

```
T1: SCHED_FIFO, prio 80
T2: SCHED_FIFO, prio 80
```

而T1在运行中执行了以下命令

```c
sys_sched_setscheduler(pid(T1), SCHED_FIFO, .prio = 90);
...
sys_sched_setscheduler(pid(T1), SCHED_FIFO, .prio = 80);
...
```

此时T1被另一个任务T3 (SCHED_FIFO, prio 95)抢占，当T3睡眠后调度器会选择T2而不是T1。这是由于`sched_setscheduler()`在将T1重新加入优先级为80的runqueue时直接将它加入了队列尾部。

该patch给出的解决方法是，若一个任务的优先级上升则加入高优先级队列的尾部，若优先级下降则加入低优先级队列的头部

```diff
--- linux-stable.orig/kernel/sched/core.c
+++ linux-stable/kernel/sched/core.c
@@ -4239,8 +4239,13 @@ recheck:
 
    if (running)
        p->sched_class->set_curr_task(rq);
-   if (on_rq)
-       enqueue_task(rq, p, 0);
+   if (on_rq) {
+       /*
+        * We enqueue to tail when the priority of a task is
+        * increased (user space view).
+        */
+       enqueue_task(rq, p, oldprio <= p->prio ? ENQUEUE_HEAD : 0);
+   }
 
    check_class_changed(rq, p, prev_class, oldprio);
    task_rq_unlock(rq, p, &flags);
```

一个对称的情况是T1先下调后提升优先级

```c
sys_sched_setscheduler(pid(T1), SCHED_FIFO, .prio = 70);
...
sys_sched_setscheduler(pid(T1), SCHED_FIFO, .prio = 80);
...
```

由于T1下调优先级后会被T2抢占，因此不会引起问题。在这类情况下，我们都应当遵循若一个任务的优先级上升则加入高优先级队列的尾部，若优先级下降则加入低优先级队列的头部的原则，以防止任务顺序错乱。

sched-consider-pi-boosting-in-setscheduler.patch则纠正了对优先级提升了的任务使用`setscheduler()`引起的任务顺序重排问题。在这类情况下，若要降低任务优先级，应当修改task struct中的参数，使得任务优先级回到正常状态时自动修改优先级，若要提高任务优先级，可以直接操作。

## concurrency::deadlock

使用正则表达式`bug::\w+::deadlock`在history.org中搜索，找到的相关patch有67个

* latency-tracer-disable-across-trace-cmdline.patch
* rt-kmap-scale-fix.patch
* bh-state-lock.patch
* rcu-new-4.patch
* fix-circular-locking-deadlock.patch
* kernel-bug-after-entering-something-from-login.patch
* ftrace-remove-max-printks.patch
* ftrace-unlock-mutex-in-output.patch
* ftrace-remove-print-of-max.patch
* rt-avoid-deadlock-in-swap.patch
* swap-spinlock-fix.patch
* printk-in-atomic-hack-fix.patch
* arm-omap-05.patch
* seqlock-serialize-against-writers.patch
* rtc-fix-hrtimer-deadlock.patch
* net-flip-lock-dep-thingy.patch
* sched-disable-rt-group-sched-on-rt.patch
* softirq-fix-unplug-deadlock.patch
* ipc-mqueue-add-a-critical-section-to-avoid-a-deadlock.patch
* peter_zijlstra-frob-rcu.patch
* futex-requeue-pi-fix.patch
* seqlock-prevent-rt-starvation.patch
* mm-slab-fix-potential-deadlock.patch
* perf-make-swevent-hrtimer-irqsafe.patch
* peterz-srcu-crypto-chain.patch
* fix-rq-3elock-vs-logbuf_lock-unlock-race.patch
* 0001-of-fix-recursive-locking-in-of_get_next_available_ch.patch
* powerpc-fsl-msi-use-a-different-locklcass-for-the-ca.patch
* might-sleep-check-for-idle.patch
* x86-mce-Defer-mce-wakeups-to-threads-for-PREEMPT_RT.patch
* ptrace-fix-ptrace-vs-tasklist_lock-race.patch
* mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
* genirq-do-not-invoke-the-affinity-callback-via-a-wor.patch
* usb-use-_nort-in-giveback.patch
* rt-sched-numa-Move-task_numa_free-to-__put_task_stru.patch
* rt-Make-cpu_chill-use-hrtimer-instead-of-msleep.patch
* timer-Raise-softirq-if-there-s-irq_work.patch
* rtmutex-use-a-trylock-for-waiter-lock-in-trylock.patch
* leds-trigger-disable-CPU-trigger-on-RT.patch
* cpu_down_move_migrate_enable_back.patch
* arm-unwind-use_raw_lock.patch
* block-mq-use-cpu_light.patch
* net-sched-dev_deactivate_many-use-msleep-1-instead-o.patch
* workqueue-prevent-deadlock-stall.patch
* cgroups-use-simple-wait-in-css_release.patch
* block-blk-mq-use-swait.patch
* irq_work_Delegate_non-immediate_irq_work_to_ksoftirqd.patch
* kernel-irq_work-fix-no_hz-deadlock.patch
* sunrpc-make-svc_xprt_do_enqueue-use-get_cpu_light.patch
* slub-disable-SLUB_CPU_PARTIAL.patch
* fs-aio-simple-simple-work.patch
* sas-ata-isci-dont-t-disable-interrupts-in-qc_issue-h.patch
* thermal-Defer-thermal-wakups-to-threads.patch
* snd-pcm-fix-snd_pcm_stream_lock-irqs_disabled-splats.patch
* ARM-enable-irq-in-translation-section-permission-fau.patch
* x86-mce-use-swait-queue-for-mce-wakeups.patch
* rfc-arm-smp-__cpu_disable-fix-sleeping-function-called-from-invalid-context.patch
* mm--rt--Fix-generic-kmap_atomic-for-RT.patch
* drmi915_Use_local_lockunlock_irq()_in_intel_pipe_update_startend().patch
* sc16is7xx_Drop_bogus_use_of_IRQF_ONESHOT.patch
* drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
* mm-backing-dev-don-t-disable-IRQs-in-wb_congested_pu.patch
* connector-cn_proc-Protect-send_msg-with-a-local-lock.patch
* arm-kprobe-replace-patch_lock-to-raw-lock.patch
* cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
* char-random-don-t-print-that-the-init-is-done.patch
* Revert-random-invalidate-batched-entropy-after-crng-.patch

deadlock的成因多种多样，但如果同样的代码在Mainline Linux能正常运行而在RT Linux上发生deadlock，那么很有可能与RT Linux对spin_lock等同步元语语义的改变有关。

## 第一类

上述patch中出现最为频繁的问题是Stack Trace中显示**BUG: sleeping function called from invalid context**，对应的patch共有16个

* mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
* usb-use-_nort-in-giveback.patch
* cgroups-use-simple-wait-in-css_release.patch
* block-blk-mq-use-swait.patch
* sunrpc-make-svc_xprt_do_enqueue-use-get_cpu_light.patch
* slub-disable-SLUB_CPU_PARTIAL.patch
* fs-aio-simple-simple-work.patch
* sas-ata-isci-dont-t-disable-interrupts-in-qc_issue-h.patch
* snd-pcm-fix-snd_pcm_stream_lock-irqs_disabled-splats.patch
* ARM-enable-irq-in-translation-section-permission-fau.patch
* rfc-arm-smp-__cpu_disable-fix-sleeping-function-called-from-invalid-context.patch
* drmi915_Use_local_lockunlock_irq()_in_intel_pipe_update_startend().patch
* mm-backing-dev-don-t-disable-IRQs-in-wb_congested_pu.patch
* connector-cn_proc-Protect-send_msg-with-a-local-lock.patch
* arm-kprobe-replace-patch_lock-to-raw-lock.patch
* cpuset-Convert-callback_lock-to-raw_spinlock_t.patch

这类问题是由于RT Linux下spin_lock可睡眠引起的，最简单的解决方案就是将spin_lock、local_irq_save等函数换成对应的raw_spin_lock、local_irq_save_nort等函数，从而避免在不能睡眠的上下文中调用可睡眠函数的问题，但这样做有可能会影响系统的实时性，想要保持性能往往需要具体问题具体分析。

## 第二类

与上面一类patch原因相似的是Stack Trace中显示**BUG: scheduling while atomic**的bug，相关patch有

* acpi-rt-Convert-acpi_gbl_hardware-lock-back-to-a-raw.patch (分类为bug::crash::hardware)
* intel_idle-convert-i7300_idle_lock-to-raw-spinlock.patch (分类为bug::crash::atomicity)
* perf-make-swevent-hrtimer-irqsafe.patch

前两个patch都是通过将spin_lock切换为raw_spin_lock解决了问题。

## 第三类

另外bit_spin_lock在RT Linux中也可能导致deadlock，相关patch有

* bh-state-lock.patch
* drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch

添加一个额外的spin_lock替代其功能是最为简便的修复方法，并且不会影响系统的性能。

## 第四类

RT Linux下另一个可能的问题是高优先级任务忙等低优先级任务释放资源，相关patch有

* net-sched-dev_deactivate_many-use-msleep-1-instead-o.patch
* ipc-mqueue-add-a-critical-section-to-avoid-a-deadlock.patch

解决方法要么是主动睡眠以让低优先级任务运行，要么关闭抢占以让低优先级任务运行完而不被打断。

## 其他

总的来说RT Linux下的deadlock问题大部分是由spin_lock转换为rt_mutex引起的，但实际引发deadlock的情况(路径)可能很复杂。对这类问题，最通常的解决方法是"convert back to raw"，但如果想要保持系统性能，还需要维护者具体问题具体分析。
