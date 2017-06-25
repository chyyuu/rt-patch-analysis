# A Study of Real-Time Linux Evolution

这个报告的基本目标是：

- 理解rt-linux的特征（设计特点，使用规则）和容易发生的错误
- 让linux developer开发中减少错误和提供实时确定性
- 使得rt-linux的演化更加容易

Challenge：

如何静态/动态分析bug/determinism  deadlock/livelock, race condition, long latency, jitter

## Abstract

我们对Real-Time Linux based on rt-patch的演进进行了全面深入的分析。通过研究XX年的
XXXX个patches来分析Real-Time Linux的变化，我们得到了很多对Real-Time Linux开发的新
的理解。我们的结果对于Real-Time Linux的进一步开发和改进bug-finding工具都会提供帮助。



## 1 Introduction

RT-PATCH的起源，开发和广泛应用情况

Real-time together with GNU/Linux seems to be on the rise, but there is no “one-fits-it-all” solution to bring real-time capabilities to it.  The reason is that there is no silver bullet to make something as big and complex as GNU/Linux 100% real-time aware since this is extremely costly in terms of maintenance. Just keep in mind that, as noted above,  one needs to keep up with the fast development cycle of 2 months practiced by the GNU/Linux kernel community.  

it is clear that Linux can support significant realtime requirements, as it is already being used heavily in the realtime arena.

The following general approaches to Linux realtime have been proposed,
along with many variations on each of these themes:

1.  non-CONFIG_PREEMPT
    2.CONFIG_PREEMPT
    3.CONFIG_PREEMPT_RT
    4.Nested OS
    5.Dual-OS/Dual-Core (Xenomai, RTAI)

    6.Migration Between OSes
    7.Migration Within OS

The idea of PREEMPT_RT is to make the Linux kernel preemptive e.g. by replacing spinlocks by preemptible objects as well as making interrupts preemptible. By enabling PREEMPT_RT on a single processor SMP bugs can be uncovered, which is an indicator that PREEMPT_RT acts as a warning mechanism for future mainline kernel problems.  It is very well suited for applications, where it’s difficult to separate the real-time from the non real-time part. The standard programming model is POSIX which allows reuse of mainline drivers. The PREEMPT_RTpatch is more than 80% mainline and there are high hopes that some time around the near future it will be fully mainline.

But how far should Linux extend its realtime support, and what is the best way to extend Linux in this direction?  Can one approach to realtime satisfy all reasonable requirements, or would it be better to support multiple approaches, each with its area of applicability?



The CONFIG_PREEMPT_RT patch by Ingo Molnar introduces additional preemption, allowing most spinlock (now "mutexes") critical sections, RCU read-side critical sections, and interrupt handlers to be preempted. Preemption of spinlock critical sections requires that priority inheritance be added to prevent the "priority inversion" problem where
a low-priority task holding a lock is preempted by a medium-priority task, while a high-priority task is blocked waiting on the lock.

The key point of the PREEMPT_RT patch is to minimize the amount of kernel code that is non-preemptible, while also minimizing the amount of code that must be changed in order to provide this added preemptibility. In particular, critical sections, interrupt handlers, and interrupt-disable code sequences are normally preemptible. The PREEMPT_RT patch leverages the SMP capabilities of the Linux kernel to add this extra preemptibility without requiring a complete kernel rewrite. In a sense, one can loosely think of a preemption as the addition of a new CPU to the system, and then use the normal locking primitives to synchronize with any action taken by the preempting task.



RT-PATCH的问题
1 here is little quantitative understanding of their code bases.
一些具体的问题

Where does the complexity of such systems lie?

what are most patches for?

What types of bugs are common?

Which performance features exist? Which reliability features are utilized?

如果解决的这些问题，会带来的好处

for developers, so that they can improve current designs and implementations
and create better systems;

for tool builders, so that they can improve their tools to match reality (e.g.,
by finding the types of bugs that plague existing systems).

解决方法

1 comprehensive study of the evolution of RT-Linux, focusing on 2.6.x
3.x, 4.x

2.6.22/23/24/25/26/29/31/33   8 vers.

3.0/2/4/6/8/10/12/14/18   9 vers

4.0/1/4/6/8/9/11   7 vers

total 24 vers.

需要分析出这些patchs中相同的部分，形成实际的patch分析

2 examine every rt-patch in the Linux over a period of XX years including XXXX patches. By carefully studying each patch to understand its intention, and then labeling the patch accordingly along numerous important axes,  we can gain deep quantitative insight into the rt-linux development process.

一些分析的结论

1  A large number of patches (nearly XX%) are XXX( e.g. maintenance) patches. The remaining dominant category is XXX(e.g. bugs)



2 breaking down the bug category further,  we find that semantic bugs, which require an understanding of rt-linux semantics to find or fix, are the dominant
bug category (over XX% of all bugs).  Most of them are hard to detect via generic bug detection tools.

3 while bug patches comprise most of our study, performance and reliability patches are also prevalent, accounting for XX% and XX% of patches respectively.

4 the study consequence of bugs.

5 Beyond these results, another outcome of our work is an annotated dataset of rt-linux patches, which we make publicly available for further study

The contributions of our work are as follows:

-  We provide a repeatable methodology for finding faults in Linux code, based on open source tools, and a publicly available archive containing our complete results.
-  Although fault-finding tools are now being used regularly in Linux development, they seem to have only had a small impact on the kinds of faults we consider. Research is thus needed on how such tools can be better integrated into the development process.

## 2 Methodology

### 2.1 Target: rt-patch

### 2.2 the degree of **determinism** on rt-linux

In the PREEMPT_RT kernel there are 4 essential types of contexts: "hard interrupt context", "interrupt context", "soft interrupt context" and "process context". The hard interrupt context is an extremely small shim in essence - a few tens of lines total, per arch - it just deals with the interrupt controller, masks the IRQ line, acks the controller and returns. The "interrupt context" is a separate per-IRQ interrupt thread, which behaves like a process and is fully preemptible. "Soft interrupt context" is a separate per-softirq system-thread too, fully preemptible. "Process context" is what it used to be, and fully preemptible too. ['fully preemptible' means it's preemptible for in essence everything but the scheduler code and the basic RT-mutex/PI code]

considering the above description, your comment about "the lesser we run in interrupt context, the better" is indeed correct: in PREEMPT_RT the hardirq context execution time and complexity has been reduced to an absolute physical minimum. It is a fundamentally good and important thing to achieve determinism. Everything else is a "thread", as far as the scheduler is concerned, and is as preemptible as possible. You can then use individual thread priorities to make some interrupts more important than others.

There is (inevitably) some scheduling overhead due to having more contexts, i've measured it to be 3-5%, worst-case [80 thousand irqs/sec], and near zero for the common case [couple of thousand irqs/sec], which is pretty good.

1) PREEMPT_NONE*. That's the default scheduler of a vanilla GNU/Linux kernel. It's geared towards maximum raw processing power and throughput. Every process gets it's fair share of  the CPU as it is  typical for a classical Unix multi-user environment. By default processes can not be preempted while they execute system calls and since, among other things, the timing behavior of some kernel services is non deterministic the whole thing is not deterministic as well.

*2) PREEMPT_VOLUNTARY\**.*** Around 2001 Ingo Molnar and later on Andrew Morton introduced preemption points in long running pieces of code, which is widely known as “low-latency patches”. This  reduces the latency at the cost of slightly lower throughput. This enables reacting to interactive events by allowing a low priority process to voluntarily preempt itself even if it is in kernel mode executing a system call.[4]

*3) PREEMPT_(DESKTOP).* Explicit preemption points are hard to find, so Robert Love and others went out to seek for implicit preemption points. Among other things spinlocks and interrupt return code were modified to implement implicit preemption points.

 

A spinlock is, similar to a mutex, used to protect access to shared resources. It's usually implemented by a hardware test and set operation. When a process attempts to access a resource that is in use by another process, the “blocked” process(es) will “spin” (busy wait) until the resource becomes available. 

 

This option further reduces the latency of the kernel by making all kernel code that is executing in a critical section preemptible.  The latency is further reduced at the cost of slightly lower throughput and a slight runtime overhead to kernel code.[4]

 

*4) PREEMPT_RT[GR-2].* The goal of the real-time preemption patch is to make fixed priority preemptive scheduling (i.e. POSIX SCHED_FIFO and SCHED_RR classes) as close as possible to their ideal behavior and all this with no impact for users/processes not interested in real-time. 

> [Mao] Shall we discuss the difference among PREEMPT_RT_BASE, PREEMPT_RT_FULL
> and PREEMPT_LAZY?



####  Comparing Priority Inversion

spinlock related

...

 preempt_disable

Note that preempt_disable() causes priority inversion:

- Task 0 at priority 0 disables preemption on single-CPU system
- Task 1 at priority 1 awakens, and is “born preempted” due to task 0's disabling of preemption

 migration_disable

Note that migration_disable() causes priority inversion:

-  Task 1 at priority 1 running on CPU 0 disables migration
- Task 2 at priority 2 awakens and runs on CPU 1
- Task 3 at priority 3 awakens and preempts task 0 on CPU 0
-  Task 3 disables migration
-  Task 2 blocks, but neither task 1 nor task 3 can be migrated to CPU 1
- This is a priority inversion involving the idle loop
- Similar sequences result in more typical priority-inversion situations

Disabling migration produces order-of-magnitude reductions in probability of priority inversion

 Lesson: If you disable long enough, bad things are probable

Disabling migration produces better results than does disabling preemption in all scenarios analyzed
=======



### 2.3 Classification of RT patches

we conduct a comprehensive study of its evolution by examining all RT patches from Linux 2.6.22
(Jul ’07) to 4.11 (Jun ’17).

To better understand the evolution of different RT-linux, we conduct a broad study to answer three categories
of fundamental questions:

- Overview: What are the common types of patches in rt-linux and how do patches change as linux evolve? Do patches of different types have different sizes?
- Bugs: What types of bugs appear in rt-linux? Do some components of rt-linux contain more bugs than others? What types of consequences do different bugs have?
- Performance and Reliability: What techniques are used by rtlinux to improve real-time performance? What common reliability enhancements are proposed in rt-linux?

To answer these questions, we manually analyzed each patch to understand its purpose and functionality, examining XXXX patches from the selected Linux 2.6.22-4.11.

rt-linux generally have similar logical components, such as scheduling, locking, and waiting. To enable precise analysis, we partition each rt-linux into  X logical components (Table X).



| Name                             | Begin Version | Description |
| -------------------------------- | ------------- | ----------- |
| Deterministic Scheduler          | 2.6.22        |             |
| Preemption Support               | 2.6.24        |             |
| PI Mutexes                       | OoM           |             |
| High-Resolution Timer            | 2.6.24        |             |
| Preemptive Read-Copy Update      | 2.6.25        |             |
| IRQ Threads                      | 2.6.30        |             |
| Raw Spinlock Annotation          | 2.6.33        |             |
| Forced IRQ Threads               | 2.6.39        |             |
| R/W Semaphore Cleanup            | 2.6.39        |             |
| Full Realtime Preemption Support | OoM           |             |

Table 2: Logical Components of rt-linux. This table shows the classification and definition of rt-linux logical components. (OoM: Out of Mainline Kernel)



Each of the following categories of code might need to be inspected:

a.	The low-level interrupt-handing code.

b.	The realtime process scheduler.

c.	Any code that disables interrupts.

d.	Any code that disables preemption.

e.	Any code that holds a lock, mutex, semaphore, or other resource
	that is needed by the code implementing your new feature, as
	well as the code that actually implements the lock, mutex,
	semaphore, or other resource.

f.	Any code that manipulates hardware that can stall the bus,
	delay interrupts, or otherwise interfere with forward progress.
	Note that it is also necessary to inspect user-level code that
	directly manipulates such hardware.
Limitations:

 Our study is limited by the rt-linux we chose, which may not reflect the characteristics of other real-time implementations based on Linux or  other non-Linux RTOS.   As for bug representativeness, we only studied the bugs reported and fixed in patches, which is a biased subset; there may be (many) other bugs not yet reported.



## 3 PATCH Overview

rt-linux evolve through patches. A large number of patches are discussed and submitted to mailing lists, bug report websites, and other forums. Some are used to implement new features, while others fix existing bugs. In this section, we investigate three general questions regarding rt-linux patches. First, what are rt-linux patch types? Second, how do patches change over time? Lastly, what is the distribution of patch sizes?

### 3.1 patch type

We classify patches into five categories (Table 1): bug fixes (bug), performance improvements (performance), reliability enhancements (reliability), new features (feature), and maintenance and refactoring (maintenance). Each patch usually belongs to a single category.

Figure X shows the number and relative percentages of patch types for each rt-linux. Note that even though
rt-linux exhibit significantly different levels of patch activity (shown by the total number of patches), the percentage breakdowns of patch types are relatively similar.

Maintenance patches

Bug patches

performance patches

Summary:


> [Mao] RTL consists of patchsets based on some Linux versions and thus does not
> have a linear history. Do we need to discuss how many similar patches there
> are in the patchsets for different versions? How many patches are merged into
> mainline in each patchset? Looking into these may also reduce the total amount
> of patches we need to inspect if quite a lot of the older patches are simply
> re-applied to newer kernels.

### 3.2 Patch Size

Patch size is one approximate way to quantify the complexity of a patch, and is defined here as the sum of linesof added and deleted by a patch. Figure X displays the size distribution of bug, performance, reliability, and feature patches. Most bug patches are small; XX% are less than 10 lines of code. However,  feature patches are significantly larger than other patch types. Over XX% of these patches have more than 100 lines of code; XX% have over 1000 lines of code.

Summary:



## 4 rt-linux bugs

In this section, we study rt-linux bugs in detail to understand their patterns and consequences comprehensively. First, we show the distribution of bugs in rt-linux logical components. Second, we describe our bug pattern classification, bug trends, and bug consequences.  Finally, we analyze each type of bug with a more detailed classification and a number of real examples.


> [Mao] Which bugs are going to be studied? If we only consider those explicitly
> fixed in the patchset, I doubt if we have an adequate amount of bugs to
> support our claim (25 patches w/ Call Trace in 4.9-rt1, mostly fixing
> preemptible spin locks in preempt_disabled sections).

### 4.0 some rules on RT-patch

an overview of the features/rules that the PREEMPT_RT patch provides.

1. Preemptible critical sections
2. Preemptible interrupt handlers
3. Preemptible "interrupt disable" code sequences
4. Priority inheritance for in-kernel spinlocks and semaphores
5. Deferred operations
6. Latency-reduction measures

#### Preemptible critical sections

- In PREEMPT_RT, normal spinlocks (spinlock_t and rwlock_t) are preemptible, as are RCU read-side critical sections (rcu_read_lock() and rcu_read_unlock()). 
- This preemptibility means that you can block while acquiring a spinlock, which in turn means that it is illegal to acquire a spinlock with either preemption or interrupts disabled (the one exception to this rule being the _trylock variants, at least as long as you don't repeatedly invoke them in a tight loop).
- This preemptibility also means that spin_lock_irqsave() does -not- disable hardware interrupts when used on a spinlock_t.
- what to do if you need to acquire a lock when either interrupts or preemption are disabled? You use a raw_spinlock_t instead of a spinlock_t, but continue invoking spin_lock() and friends on the raw_spinlock_t. 
- These raw locks(raw_spinlock_t,raw_rwlock_t)) should not be needed outside of a few low-level areas, such as the scheduler, architecture-specific code, and RCU.
- Since critical sections can now be preempted, you cannot rely on a given critical section executing on a single CPU -- it might move to a different CPU due to being preempted. 
- when you are using per-CPU variables in a critical section, you must separately handle the possibility of preemption: (1) Explicitly disable preemption, either through use of get_cpu_var(), preempt_disable(), or disabling hardware interrupts. (2) Use a per-CPU lock to guard the per-CPU variables. One way to do this is by using the new DEFINE_PER_CPU_LOCKED() primitive

#### Preemptible "interrupt disable" code sequences

- Code that must interact with SA_NODELAY interrupts cannot use local_irq_save(), since this does not disable hardware interrupts. Instead, raw_local_irq_save() should be used.
- Similarly, raw spinlocks (raw_spinlock_t, raw_rwlock_t, and raw_seqlock_t) need to be used when interacting with SA_NODELAY interrupt handlers.
- However, raw spinlocks and raw interrupt disabling should -not- be used outside of a few low-level areas, such as the scheduler, architecture-dependent code, and RCU.

#### Preemptible "interrupt disable" code sequences

The concept of preemptible interrupt-disable code sequences may seem to be a contradiction in terms, but it is important to keep in mind the PREEMPT_RT philosophy. This philosophy relies on the SMP capabilities of the Linux kernel to handle races with interrupt handlers, keeping in mind that most interrupt handlers run in process context. Any code that interacts with an interrupt handler must be prepared to deal with that interrupt handler running concurrently on some other CPU.

- spin_lock_irqsave() and related primitives need not disable preemption.  The reason this is safe is that if the interrupt handler runs, even if it preempts the code holding the spinlock_t, it will block as soon as it attempts to acquire that spinlock_t. The critical section will therefore still be preserved.
- local_irq_save() still disables preemption, since there is no corresponding lock to rely on.
- Using locks instead of local_irq_save() therefore can help reduce scheduling latency, but substituting locks in this manner can reduce SMP performance, so be careful.
- Code that must interact with SA_NODELAY interrupts cannot use local_irq_save(), since this does not disable hardware interrupts. Instead, raw_local_irq_save() should be used. 
- Note that SA_NODELAY should -not- be used for normal device interrupts: (1) this will degrade both interrupt and scheduling latency and (2) SA_NODELAY interrupt handlers are much more difficult to code and maintain than are normal interrupt handlers.

#### Deferred operations

- Since spin_lock() can now sleep, it is no longer legal to invoke it while preemption (or interrupts) are disabled.  In some cases, this has been solved by deferring the operation requiring the spin_lock() until preemption has been re-enabled: put_task_struct_delayed() queues up a put_task_struct() to be executed at a later time when it is legal to acquire (for example) the spinlock_t alloc_lock in task_struct. mmdrop_delayed() queues up an mmdrop() to be executed at a later time, similar to put_task_struct_delayed() above. In all of these situations, the solution is to defer an action until that action may be more safely or conveniently performed.

### 4.1 correlation between using modules and bug

内核那部分使用 rt feature容易出现bug



### 4.2 Bug Patterns

To build a more reliable rt-linux, it is important to  understand the type of bugs that are most prevalent and the typical patterns across rt-linux. Since different  types of bugs require different approaches to detect and fix, these fine-grained bug patterns provide useful information to developers and tool builders alike.

We partition rt-linux bugs into X categories based on their root causes as shown in Table X.

Figure 2(b) (page 4) shows the total number and per-centage of each type of bug across rt-linux. There are about 1800 total bugs, providing a great opportunity to explore bug patterns at scale. Semantic bugs dominate other  types . Most semantic bugs require rt-linux domain knowledge to understand, detect, and fix; generic bug-finding tools (e.g., Coverity [9]) may have a hard time finding these bugs.

in Linux 2.6.33, away from the Big Kernel Lock (BKL), which introduced a large number of concurrency bugs.



### 4.3 Bug Trends

rt-linux mature from the initial development stage to the stable stage over time, by applying bug-fixing, performance and reliability patches. Various bug detection and testing tools are also proposed to improve rt-linux stability. A natural question arises: do rt-linux bug patterns change over time, and in what way?

趋势与版本相关，需要分析各个版本之间的bug pattern的问题。

### 4.4  Bug Consequences

data corruption, system crashes, unexpected errors, deadlocks,system hangs and resource leaks

rt-linux bugs cause severe consequences; corruptions and crashes are most common; wrong behavior is uncommon; semantic bugs can lead to significant amounts of corruptions, crashes, errors, and hangs; all bug types have severe consequences.

### 4.5  Bug Pattern Examples and Analysis



## 5  determinism of Real-Time Performance

A small but important set of patches improve performance and reliability, which are quantitatively different than bug
patches (Figure X). Performance and reliability patches account for X% and X% of patches respectively.


> [Mao] If we want to collect RT performance metrics, we have to test the kernel
> on bare metal (not in VMs) to remove the interference of the VMM. We need to
> start this early next week so that the lkp-related stuff can be finished as
> planned.

###  5.1  determinism related Performance Patches

 There are a few changes in PREEMPT_RT whose primary purpose is to reduce scheduling or interrupt latency.

The first such change involves the x86 MMX/SSE hardware. This hardware is handled in the kernel with preemption disabled, and this sometimes means waiting until preceding MMX/SSE instructions complete. Some MMX/SSE instructions are no problem, but others take overly long amounts of time, so PREEMPT_RT refuses to use the slow ones.

The second change applies per-CPU variables to the slab allocator, as an alternative to the previous wanton disabling of interrupts.

### 5.2  determinism  & throughput experiments




## 6 Related work

## 7 Conclusions

## References

- [PREEMPT_RT](http://rt.wiki.kernel.org/index.php/Main_Page)

- [RTAI](https://www.rtai.org/)

- [xenomai](http://www.xenomai.org/index.php/Main_Page)

- [dual-core RTLINUX](http://www.windriver.com/products/platforms/real-time_core/)

- [xtratum](http://www.xtratum.org/)

- [A realtime preemption overview](https://old.lwn.net/Articles/146861/)

- [Different approaches to Linux realtime](http://lwn.net/Articles/143323/)

- [Per-CPU variables and the realtime tree](https://lwn.net/Articles/452884)

- [The return of simple wait queues](https://lwn.net/Articles/661424/)

- [Realtime mainlining](https://lwn.net/Articles/662833/)

- [PREEMPT_RT patchset](https://www.kernel.org/pub/linux/kernel/projects/rt/)

- [Realtime preemption and read-copy-update](https://lwn.net/Articles/129511/)

- [rationale for timer/hrtimer split](http://lwn.net/Articles/152363/)

- [deferrable timers](http://lwn.net/Articles/228143/)

- [high-resolution timer API – dated](http://lwn.net/Articles/167897/)

- [Threaded Interrupts Approaches, October 2004](http://lwn.net/Articles/106010/) 

- [Threaded Interrupts Debate, June 2005](http://lwn.net/Articles/138174/)

  ​

- [• http://en.wikipedia.org/wiki/RCU
  • http://lwn.net/Articles/128228/ (early realtime-RCU attempt)
  • http://www.rdrop.com/users/paulmck/RCU/OLSrtRCU.2006.08.11a.pdf
  (realtime-RCU OLS paper)
  • http://www.rdrop.com/users/paulmck/RCU/ (More RCU papers)
  • http://www.rdrop.com/users/paulmck/RCU/linuxusage.html (Graphs)
  • http://lwn.net/Articles/201195/ (Jon Corbet realtime-RCU writeup)
  • http://lwn.net/Articles/220677/ (RCU priority boosting)
  • http://lwn.net/Articles/220677/ (patch for higher-performance RCU)

- Threaded Interrupts softirq splitting, June 2005](http://lwn.net/Articles/139062/)




## QA

### 分析real-time的性能层次？

### 支持的cpu的情况？

### 为了支持新内核，需要增加的新patch的情况如何？这说明了upate的困难度， 是否也可看看seda的支持能力？

### concurrency bug都应该与rt-linux相关？如何统计linux kernel的concurrency bug?

### definitions/types of the bugs/faults

### What code is analyzed?  rt-patch在内核不同模块中的分布，这说明了linux对rt的支持程度，特别是在driver方面

### How many faults are there?

### Where are the faults?
