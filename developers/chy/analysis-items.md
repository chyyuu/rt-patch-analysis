## rt-patchs intro
RT-Preempt把Linux变成一个完全可抢占的内核，改变有以下几点：

1.通过rtmutexes的重新实现使内核里的锁源语（使用自旋锁）可被抢占

2.以前被如spinlock_t和rwlock_t保护的临界区现在变得可以被抢占了。使用raw_spinlock_t创建不可抢占区域（在内核中）依旧是可能的（类似spinlock_t的相同API）。

3.为内核里的自旋锁和信号量实现优先级继承。更多优先级反转和优先级继承的信息请参考： http://www.embedded.com/story/OEG20020321S0023

4.把中断处理器变为可被抢占的内核线程：RT-Preempt patch在内核线程上下文中处理软中断处理器。

5.把老的Linux计时器API变成分别的几个基本结构，有针对高精度内核计时器的还有一个是针对超时的，这使得用户空间的POSIX计时器具有高精度。

https://linux.cn/article-6504-1.html

正如 Emde 在其10月5日的一篇博文中所描述的那样，实时 Linux 的应用领域正在日益扩大，由其原来主要服务的工业控制扩大到了汽车行业和电信业等领域，这表明资助的来源也应该得到拓宽。RTL 在汽车行业发展也很迅猛，以后会扩大并应用到铁路和航空电子设备上。无人机和机器人使用实时 Linux 的时机也已成熟。Emde 原文写道：“仅仅靠来自工控行业的资金来支撑全部的工作是不合理的，因为电信等其他行业也在享用实时 Linux 内核。”

据长期以来一直担任 OSADL 总经理的 Carsten Emde 博士介绍，支持内核实时特性的工作已经完成了将近 90％。 “这就像盖房子，”他解释说。 “主要的部件，如墙壁，窗户和门都已经安装到位，就实时内核来说，类似的主要部件包括：高精度定时器high-resolution timers，中断线程化机制interrupt threads和优先级可继承的互斥量priority-inheritance mutexes等。然后所剩下的就是需要一些边边角角的工作，就如同装修房子过程中还剩下铺设如地毯和墙纸等来完成最终的工程。”

以 Emde 观点来看，从技术的角度来说，实时 Linux 的性能已经可以媲美绝大多数其他的实时操作系统 - 但前提是你要不厌其烦地把所有的补丁都打上。 Emde 的原话如下：“该项目（LCTT 译注，指 RTL）的唯一目标就是提供一个满足实时性要求的 Linux 系统，使其无论运行状况如何恶劣都可以保证在确定的、可以预先定义的时间期限内对外界处理做出响应。这个目标已经实现，但需要你手动地将 RTL 提供的补丁添加到 Linux 内核主线的版本代码上，但将来的不用打补丁的实时 Linux 内核也能实现这个目标。唯一的，当然也是最重要的区别就是相应的维护工作将少得多，因为我们再也不用一次又一次移植那些独立于内核主线的补丁代码了。”

## PREEMPT_RT Patch Size

 2.6 ->3.x->4.x

version      file_changed lines_plus Lines_minus


## Summary of PREEMPT_RT primitives

### Locking Primitives


#### spinlock_t
Critical sections are preemptible. The _irq operations (e.g., spin_lock_irqsave()) do -not- disable hardware interrupts. Priority inheritance is used to prevent priority inversion. An underlying rt_mutex is used to implement spinlock_t in PREEMPT_RT (as well as to implement rwlock_t, struct semaphore, and struct rw_semaphore).

#### raw_spinlock_t
Special variant of spinlock_t that offers the traditional behavior, so that critical sections are non-preemptible and _irq operations really disable hardware interrupts. Note that you should use the normal primitives (e.g., spin_lock()) on raw_spinlock_t. That said, you shouldn't be using raw_spinlock_t -at- -all- except deep within architecture-specific code or low-level scheduling and synchronization primitives. Misuse of raw_spinlock_t will destroy the realtime aspects of PREEMPT_RT. You have been warned.

#### rwlock_t
Critical sections are preemptible. The _irq operations (e.g., write_lock_irqsave()) do -not- disable hardware interrupts. Priority inheritance is used to prevent priority inversion. In order to keep the complexity of priority inheritance down to a dull roar, only one task may read-acquire a given rwlock_t at a time, though that task may recursively read-acquire the lock.

#### RW_LOCK_UNLOCKED(mylock)
The RW_LOCK_UNLOCKED macro now takes the lock itself as an argument, which is required for priority inheritance. Unfortunately, this makes its use incompatible with the PREEMPT and non-PREEMPT kernels. Uses of RW_LOCK_UNLOCKED should therefore be changed to DEFINE_RWLOCK().

#### raw_rwlock_t （disappear in 4.x）
Special variant of rwlock_t that offers the traditional behavior, so that critical sections are non-preemptible and _irq operations really disable hardware interrupts. Note that you should use the normal primitives (e.g., read_lock()) on raw_rwlock_t. That said, as with raw_spinlock_t, you shouldn't be using raw_rwlock_t -at- -all- except deep within architecture-specific code or low-level scheduling and synchronization primitives. Misuse of raw_rwlock_t will destroy the realtime aspects of PREEMPT_RT.	You have once again been warned.

#### seqlock_t
Critical sections are preemptible. Priority inheritance has been applied to the update side (the read-side cannot be involved in priority inversion, since seqlock_t readers do not block writers).

#### SEQLOCK_UNLOCKED(name)
The SEQLOCK_UNLOCKED macro now takes the lock itself as an argument, which is required for priority inheritance. Unfortunately, this makes its use incompatible with the PREEMPT and non-PREEMPT kernels. Uses of SEQLOCK_UNLOCKED should therefore be changed to use DECLARE_SEQLOCK(). Note that DECLARE_SEQLOCK() defines the seqlock_t and initializes it.

#### struct semaphore
The struct semaphore is now subject to priority inheritance.

#### down_trylock()
This primitive can schedule, so cannot be invoked with hardware interrupts disabled or with preemption disabled. However, since almost all interrupts run in process context with both preemption and interrupts enabled, this restriction has no effect thus far.

#### struct compat_semaphore
A variant of struct semaphore that is -not- subject to priority inheritance. This is useful for cases when you need an event mechanism, rather than a sleeplock.

#### struct rw_semaphore
The struct rw_semaphore is now subject to priority inheritance, and only one task at a time may read-hold. However, that task may recursively read-acquire the rw_semaphore.

#### struct compat_rw_semaphore
A variant of struct rw_semaphore that is -not- subject to priority inheritance. Again, this is useful for cases when you need an event mechanism, rather than a sleeplock.


### Per-CPU Variables

#### def/decl_per_cpu
DEFINE_PER_CPU_LOCKED(type, name)
DECLARE_PER_CPU_LOCKED(type, name)
Define/declare a per-CPU variable with the specified type and name, but also define/declare a corresponding spinlock_t. If you have a group of per-CPU variables that you want to be protected by a spinlock, you can always group them into a struct.

#### get_per_cpu_locked(var, cpu)
Return the specified per-CPU variable for the specified CPU, but only after acquiring the corresponding spinlock.

#### put_per_cpu_locked(var, cpu)
Release the spinlock corresponding to the specified per-CPU variable for the specified CPU.

#### per_cpu_lock(var, cpu)
Returns the spinlock corresponding to the specified per-CPU variable for the specified CPU, but as an lvalue. This can be useful when invoking a function that takes as an argument a spinlock that it will release.

#### per_cpu_locked(var, cpu)
Returns the specified per-CPU variable for the specified CPU as an lvalue, but without acquiring the lock, presumably because you have already acquired the lock but need to get another reference to the variable. Or perhaps because you are making an RCU-read-side reference to the variable, and therefore do not need to acquire the lock.

#### rcu related
+#ifdef CONFIG_PREEMPT_RCU
+	return rcu_batches_completed();
+#else
 	return rcu_batches_completed_bh();
+#endif
 }
 
区别是？

### Interrupt Handlers

#### SA_NODELAY
Used in the struct irqaction to specify that the corresponding interrupt handler should be directly invoked in hardware-interrupt context rather than being handed off to an irq thread. The function redirect_hardirq() does the wakeup, and the interrupt-processing loop may be found in do_irqd().
Note that SA_NODELAY should -not- be used for normal device interrupts: (1) this will degrade both interrupt and scheduling latency and (2) SA_NODELAY interrupt handlers are much more difficult to code and maintain than are normal interrupt handlers. Use SA_NODELAY only for low-level interrupts (such as the timer tick) or for hardware interrupts that must be processed with extreme realtime latencies.

#### local_irq_* irqs_* local_*

local_irq_enable()
local_irq_disable()
local_irq_save(flags)
local_irq_restore(flags)
irqs_disabled()
irqs_disabled_flags()
local_save_flags(flags)

The local_irq*() functions do not actually disable hardware interrupts, instead, they simply disable preemption. These are suitable for use with normal interrupts, but not for SA_NODELAY interrupt handlers.
However, it is usually even better to use locks (possibly per-CPU locks) instead of these functions for PREEMPT_RT environments -- but please also consider the effects on SMP machines using non-PREEMPT kernels!

#### raw_local_irq* raw_irqs_* raw_local_*
raw_local_irq_enable()
raw_local_irq_disable()
raw_local_irq_save(flags)
raw_local_irq_restore(flags)
raw_irqs_disabled()
raw_irqs_disabled_flags()
raw_local_save_flags(flags)

These functions disable hardware interrupts, and are therefore suitable for use with SA_NODELAY interrupts such as the scheduler clock interrupt (which, among other things, invokes scheduler_tick()).
These functions are quite specialized, and should only be used in low-level code such as the scheduler, synchronization primitives, and so on. Keep in mind that you cannot acquire normal spinlock_t locks while under the effects of raw_local_irq*().


### Miscellaneous
#### wait_for_timer()
Wait for the specified timer to expire. This is required because timers run in process in the PREEMPT_RT environment, and can therefore be preempted, and can also block, for example during spinlock_t acquisition.

#### smp_send_reschedule_allbutself()
Sends reschedule IPI to all other CPUs. This is used in the scheduler to quickly find another CPU to run a newly awakened realtime task that is high priority, but not sufficiently high priority to run on the current CPU. This capability is necessary to do the efficient global scheduling required for realtime. Non-realtime tasks continue to be scheduled in the traditional manner per-CPU manner, sacrificing some priority exactness for greater efficiency and scalability.

#### INIT_FS(name)
This now takes the name of the variable as an argument so that the internal rwlock_t can be properly initialized (given the need for priority inheritance).

#### *_nort/NORT
local_irq_disable_nort()
local_irq_enable_nort()
local_irq_save_nort(flags)
local_irq_restore_nort(flags)
spin_lock_nort(lock)
spin_unlock_nort(lock)
spin_lock_bh_nort(lock)
spin_unlock_bh_nort(lock)
BUG_ON_NONRT()
WARN_ON_NONRT()

These do nothing (or almost nothing) in PREEMPT_RT, but have the normal effect in other environments. These primitives should not be used outside of low-level code (e.g., in the scheduler, synchronization primitives, or architecture-specific code).

#### *_rt/RT
spin_lock_rt(lock)
spin_unlock_rt(lock)
in_atomic_rt()
BUG_ON_RT()
WARN_ON_RT()

Conversely, these have the normal effect in PREEMPT_RT, but do nothing in other environments. Again, these primitives should not be used outside of low-level code (e.g., in the scheduler, synchronization primitives, or architecture-specific code).

#### smp_processor_id_rt(cpu)
This returns "cpu" in the PREEMPT_RT environment, but acts the same as smp_processor_id() in other environments. This is intended for use only in the slab allocator.




## PREEMPT_RT configuration options
### High-Level Preemption-Option Selection

- PREEMPT_NONE selects the traditional no-preemption case for server workloads.
- PREEMPT_VOLUNTARY enables voluntary preemption points, but not wholesale kernel preemption. This is intended for desktop use.
- PREEMPT_DESKTOP enables voluntary preemption points along with non-critical-section preemption (PREEMPT). This is intended for low-latency desktop use.
- PREEMPT_RT enables full preemption, including critical sections.

### Feature-Selection Configuration Options

- PREEMPT enables non-critical-section kernel preemption.
- PREEMPT_BKL causes big-kernel-lock critical sections to be preemptible.
- PREEMPT_HARDIRQS causes hardirqs to run in process context, thus making them preemptible. However, the irqs - marked as SA_NODELAY will continue to run in hardware interrupt context.
- PREEMPT_RCU causes RCU read-side critical sections to be preemptible.
- PREEMPT_SOFTIRQS causes softirqs to run in process context, thus making them preemptible.

### Debugging Configuration Options
These are subject to change, but give a rough idea of the sorts of debug features available within PREEMPT_RT.

- CRITICAL_PREEMPT_TIMING measures the maximum time that the kernel spends with preemption disabled.
- CRITICAL_IRQSOFF_TIMING measures the maximum time that the kernel spends with hardware irqs disabled.
- DEBUG_IRQ_FLAGS causes the kernel to validate the "flags" argument to spin_unlock_irqrestore() and similar primitives.
- DEBUG_RT_LOCKING_MODE enables runtime switching of spinlocks from preemptible to non-preemptible. This is useful to kernel developers who want to evaluate the overhead of the PREEMPT_RT mechanisms.
- DETECT_SOFTLOCKUP causes the kernel to dump the current stack trace of any process that spends more than 10 seconds in the kernel without rescheduling.
- LATENCY_TRACE records function-call traces representing long-latency events. These traces may be read out of the kernel via /proc/latency_trace. It is possible to filter out low-latency traces via /proc/sys/kernel/preempt_thresh.
  This config option is extremely useful when tracking down excessive latencies.

- LPPTEST enables a device driver that performs parallel-port based latency measurements, such as used by Kristian Benoit for measurements posted on LKML in June 2005.
  Use scripts/testlpp.c to actually run this test.

PRINTK_IGNORE_LOGLEVEL causes -all- printk() messages to be dumped to the console. Normally a very bad idea, but helpful when other debugging tools fail.
RT_DEADLOCK_DETECT finds deadlock cycles.
RTC_HISTOGRAM generates data for latency histograms for applications using /dev/rtc.
WAKEUP_TIMING measures the maximum time from when a high-priority thread is awakened to the time it actually starts running in microseconds. The result is accessed from /proc/sys/kernel/wakeup_timing. and the test may be restarted via:
	echo 0 > /proc/sys/kernel/preempt_max_latency


### some situations

### migrate_disable()
New mechanism that in some situations can
replace preempt_disable().

- get_cpu_var()  uses preempt_disable()
- get_local_var() uses migrate_disable()
- local_lock()  uses get_local_var()


### CPU Hotplug
Summary of the redesign/rework discussion is at:
https://lkml.org/lkml/2012/3/19/350


### Deadline Scheduler

A new scheduling class
Task registers:
- amount of cpu required to complete work
- when work must be completed
- how often task executes

Scheduler only allows task to register if there are
sufficient cpu resources to guarantee task will
complete work by deadline.

 EDF scheduling

### CPU Isolation
Dedicate a processor to a specific task (kernel
space or user space).
Eliminate all normal kernel interrupts and
overhead on the processor.

Goal:
- minimize latency
- maximize throughput

Early reactions were
- skeptical
- somewhat hostile
- suggesting different solutions

[git pull] CPU isolation extensions
From: Max Krasnyansky
https://lkml.org/lkml/2008/2/7/1

The patchset consist of 4 patches.
- Make cpu isolation configurable and export isolated map
- Do not route IRQs to the CPUs isolated at boot
- Do not schedule workqueues on the isolated CPUs
- Do not halt isolated CPUs with Stop Machine

### Virtualization
source (14 August 2009):
http://developer.novell.com/wiki/index.php/AlacrityVM

Development is continuing. One example is:
Using KVM as a Real-Time Hypervisor
Jan Kiszka
KVM Forum 2011
slides at:
http://www.linux-kvm.org/page/KVM_Forum_2011
video at:


### tools

rt-rests git repository is now at:
git.kernel.org/pub/scm/linux/kernel/git/clrkwllms/rt-tests.git


## rt-patchs

### spin_lock 

### Simple wait queues
https://lwn.net/Articles/577370/

引入的原因：
The end result is a data structure that is far larger and more complex than it was in the 2.0 days. It is the callback feature that was most problematic for the realtime tree, though; since those callbacks can sleep, they prevent the use of "raw" spinlocks to protect the wait queues themselves. To work around this problem, Thomas Gleixner created a new "simple wait queue" mechanism that would dispense with most of the added functionality and, thus, be suitable for use in the realtime kernel.

The code looks a lot like a return to the 2.0 kernel; much of the functionality that wait queues have gained in the meantime has been stripped away, leaving a familiar-looking linked list of waiting threads. There is no exclusive wakeup feature, no callback feature, and not much of anything else. What there is, though, is a wait queue mechanism that is sufficient for the needs of most wait queue users (of which there are many) in the kernel.

### cpu_chill
cpu_chill-->cpu_rest OR cpu_relax

 #ifdef CONFIG_PREEMPT_RT_FULL
 Use cpu_chill() after a spin_trylock_or_boost() which will boost the owner
 of the lock to the callers priority (if needed), and cpu_chill will
 act like a sched_yield() allowing the owner to proceed.

 Use cpu_rest() if there's no way to find out who the owner you are waiting
 for (like spinning on a status variable or bit). This is equivalent to
 a msleep(1) and you can hope that the status will change by the time
 you wake up.

##对抢占preempt的理解
抢占式内核实现的原理是在释放自旋锁时或从中断返回时，如果当前执行进程的 need_resched 被标记，则进行抢占式调度。Linux内核在线程信息结构上增加了成员preempt_count作为内核抢占锁，为0表示可以进行内核高度，它随spinlock和rwlock等一起加锁和解锁。
在抢占式内核中，认为如果内核不是在一个中断处理程序中，并且不在被 spinlock等互斥机制保护的临界代码中，就认为可以"安全"地进行进程切换。Linux内核将临界代码都加了互斥机制进行保护，同时，还在运行时间过长的代码路径上插入调度检查点，打断过长的执行路径，这样，任务可快速切换进程状态，也为内核抢占做好了准备。

禁止内核抢占的情况列出如下：

（1）内核执行中断处理例程时不允许内核抢占，中断返回时再执行内核抢占。

（2）当内核执行软中断或tasklet时，禁止内核抢占，软中断返回时再执行内核抢占。

（3）在临界区禁止内核抢占，临界区保护函数通过抢占计数宏控制抢占，计数大于0，表示禁止内核抢占。

### 内核抢占API函数

在中断或临界区代码中，线程需要关闭内核抢占，因此，互斥机制（如：自旋锁（spinlock）、RCU等）、中断代码、链表数据遍历等需要关闭内核抢占，临界代码运行完时，需要开启内核抢占。关闭/开启内核抢占需要使用内核抢占API函数preempt_disable和preempt_enable。

内核抢占API函数说明如下（在include/linux/preempt.h中）：

preempt_enable() //内核抢占计数preempt_count减1

preempt_disable() //内核抢占计数preempt_count加1

preempt_enable_no_resched()　 //内核抢占计数preempt_count减1，但不立即抢占式调度

preempt_check_resched () //如果必要进行调度

preempt_count() //返回抢占计数

preempt_schedule() //核抢占时的调度程序的入口点



## 对NO_HZ的理解

在打开NO_HZ前后，rt的performance如何？

## 对部分函数的理解

### get/put_cpu_var_locked v2.6.22

- in 2.6.22 get/put_cpu_var_locked 替换 get/put_cpu_var   in include/asm-generic/percpu.h

  是否都替换，还是替换一部分？

NON_RT

```
/*
 * Must be an lvalue. Since @var must be a simple identifier,
 * we force a syntax error here if it isn't.
 */
#define get_cpu_var(var) (*({				\
	extern int simple_identifier_##var(void);	\
	preempt_disable();				\
	&__get_cpu_var(var); }))
#define put_cpu_var(var) preempt_enable()
```



RT

```
+/*
+ * Per-CPU data structures with an additional lock - useful for
+ * PREEMPT_RT code that wants to reschedule but also wants
+ * per-CPU data structures.
+ *
+ * 'cpu' gets updated with the CPU the task is currently executing on.
+ *
+ * NOTE: on normal !PREEMPT_RT kernels these per-CPU variables
+ * are the same as the normal per-CPU variables, so there no
+ * runtime overhead.
+ */
+#define get_cpu_var_locked(var, cpuptr)			\
+(*({							\
+	int __cpu = raw_smp_processor_id();		\
+							\
+	*(cpuptr) = __cpu;				\
+	spin_lock(&__get_cpu_lock(var, __cpu));		\
+	&__get_cpu_var_locked(var, __cpu);		\
+}))
+
+#define put_cpu_var_locked(var, cpu) \
+	 do { (void)cpu; spin_unlock(&__get_cpu_lock(var, cpu)); } while (0)
```

### local_lock v4.11



### touch/stop_critical_timing

对tr的保护？ atomic_inc(&tr->disabled)  ....   atomic_dec(&tr->disabled) ; mcount();



### atomic_notifier_call_chain TO  raw_notifier_call_chain

atomic_notifier chains are note NMIsafe in rt

NMI context, NMI safe 的含义？？

```

Note that there already are several messages printed in NMI context:
WARN_ON(in_nmi()), BUG_ON(in_nmi()), anything being printed out from MCE
handlers.  These are not easy to avoid.
```

### workqueue, tasklet v.s. softirq
在通用linux中
workqueue和softirq、tasklet有本质的区别：workqueue运行在process context，而softirq和tasklet运行在interrupt context。因此，出现workqueue是不奇怪的，在有sleep需求的场景中，defering task必须延迟到kernel thread中执行，也就是说必须使用workqueue机制。

tasklet是基于softirq的。

bottom half机制的设计有两方面的需求，一个是性能，一个是易用性。设计一个通用的bottom half机制来满足这两个需求非常的困难，因此，内核提供了softirq和tasklet两种机制。softirq更倾向于性能，而tasklet更倾向于易用性。 


为了性能，同一类型的softirq有可能在不同的CPU上并发执行，这给使用者带来了极大的痛苦，因为驱动工程师在撰写softirq的回调函数的时候要考虑重入，考虑并发，要引入同步机制。但是，为了性能，我们必须如此。 

如果是tasklet的情况会如何呢？为何tasklet性能不如softirq呢？如果一个tasklet在processor A上被调度执行，那么它永远也不会同时在processor B上执行，也就是说，tasklet是串行执行的
