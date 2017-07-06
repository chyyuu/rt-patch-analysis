#### Table of Contents
- [Wikipedia Real-time computing](#Wikipedia-Real-time-computing)
- [Wikipedia Real-time operating system](#Wikipedia-Real-time-operating-system)
- [Wikipedia RTLinux](#Wikipedia-RTLinux)
- [Wikipedia Scheduling analysis real-time systems](#Wikipedia-Scheduling-analysis-real-time-systems)
- [Attempted summary of "RT patch acceptance" thread, take2](#Attempted-summary-of-"RT-patch-acceptance"-thread,-take2)
- [Spinlock](#Spinlock)
    - [A Revise of RW Problem](#A-Revise-of-RW-Problem)
    - [The comment in ```linux/arch/x86/include/asm/spinlock.h```](#The-comment-in-```linux/arch/x86/include/asm/spinlock.h```)
- [RCU](#RCU)
    - [Basic concepts](#Basic-concepts)
    - [Usage](#Usage)
- [The Design of Preemptible read-copy-update](#The-Design-of-Preemptible-read-copy-update)
- [A Realtime Preemption Overview](#A-Realtime-Preemption-Overview)
- [To be read](#To-be-read)

# Wikipedia Real-time computing
[wiki](https://en.wikipedia.org/wiki/Real-time_computing#Hard)
- Real-time computing
  - Real-time computing (RTC), or reactive computing describes hardware and software systems subject to a "real-time constraint", for example from event to system response. Real-time programs must guarantee response within specified time constraints, often referred to as "deadlines". Real-time responses are often understood to be in the order of milliseconds, and sometimes microseconds.
  - A real-time system has been described as one which "controls an environment by receiving data, processing them, and returning the results sufficiently quickly to affect the environment at that time."
  - Definition: A system is said to be real-time if the total correctness of an operation depends not only upon its logical correctness, but also upon the time in which it is performed. Classified as:
    - Hard: missing a deadline is a total system failure.
    - Firm: infrequent deadline misses are tolerable, but may degrade the system's quality of service. The usefullness of a result is zero after its deadline.
    - Soft: the usefullness of a result degrades after its deadline, thereby degrading the system's performance.
> The difference of the latter two are the usefullness of a delayed result? Thus it is a definition of the demand made by applications.

# Wikipedia Real-time operating system
[wiki](https://en.wikipedia.org/wiki/Real-time_operating_system)
- RTOS
  - A real-time operating system (RTOS) is an operating system (OS) intended to serve real-time applications that process data as it comes in, typically without buffer delays. Processing time requirements (including any OS delay) are measured in tenths of seconds or shorter increments of time. They either are event driven or time sharing.
  - A key characteristic of an RTOS is the level of its consistency concerning the amount of time it takes to accept and complete an application's task; the variability is jitter. A hard real-time operating system has less jitter than a soft real-time operating system.
  - The chief design goal is a guarantee of a soft or hard performance category.
  - Key factors in a real-time OS are minimal interrupt latency and minimal thread switching latency.

# Wikipedia RTLinux
[wiki](https://en.wikipedia.org/wiki/RTLinux)*(Saved for future reference)*
- RTLinux
  - Simple description: RTLinux is a hard realtime RTOS microkernel that runs the entire Linux operating system as a **fully preemptive process**. The hard real-time property makes it possible to control robots, data acquisition systems, manufacturing plants, and other time-sensitive instruments and machines from RTLinux applications.
  - Even with a similar name it is not related the "Real-Time Linux" project of the Linux Foundation.
- Background
  The key design objective was to add hard real-time capabilities to commodity OS to facilitate the development of complex control programs with both capabilities.

# Wikipedia Scheduling analysis real-time systems
[wiki](https://en.wikipedia.org/wiki/Scheduling_analysis_real-time_systems)

# Attempted summary of "RT patch acceptance" thread, take2
[lwn](https://old.lwn.net/Articles/143323/)
- Realtime operating system, especially hard-realtime, must be designed from ground up; Some exceptions:
  - **Many realtime applications use a very restricted subset of general-purpose OS.** Possible to provide very limited realtime support.
  - **Dramatic increase in performance.**
- Desires
  - Quality of Service
    - Reliability of hardware to meet he deadline
    - timeframe
      - Some applications have definite response-time.
      - A few of services of a os is needed: interrupt handling, process scheduling, disk I/O, network I/O, process creation/distruction, VM operations and so on.
      - Many popular RTOSes provide **very little** in the way of services, leaving the complex stuff to general-purpose os, which raise the possibility **providing a single Linux os instance that provides some services with realtime guarantees and other services in a non-realtime fashion.**
      - Performance penalty for realtime support must be paid, but the less the better. > How comes these penalty?
  - Amount of code Inspection Required **!!!Very Important**
    - How much of the rest of system should you inspect to be able to guarantee that the new feature provide the required level of realtime response. **More codes sometimes means more realtime "bugs".**
    - Following are the categories of cods need to be inspected:
      - the low-level interrupt-handing code
      - the realtime process scheduler
      - any code that disables interrupts
      - any code that disables preemption
      - any code that holds a lock, mutex, semaphore, or other resource that is needed by the code implementing your new feature, as well as the code that actually implements the lock, mutex, semaphore, or other resource.
      - any code that manipulates hardware that can stall the bus, delay interrupts, or otherwise interfere with forward progress. Note that it is also necessary to inspect user-level code that directly manipulates such hardware.
    - The last point has no way to be found other than exhaustive testing. Some driver bugs may resulted in hardware stalls.
  - API Provided
  - Relative Complexity
    - Trade off between complexity of application and the realtime capability.
  - Fault Isolation
    > Cannot understand the definition or effect of fault isolation.
    - Following sorts of faults need isolating
      - Excessive disabling of interrupts
      - Excessive disabling of preemption
      - Holding a lock, mutex, or semaphore for too long, when that resource must be acquired by realtime code
      - Memory corruption, either via wild pointers or via wild DMA
  - Hardware and Software Configurations
    - Some applications choose to restrict the software or the hardware configurations of the platform to meet the realtime deadlines.
- Linux Realtime Approaches
> Maybe useful but too much irrelevant info. Check this part when needed, I think the comparison here is very useful.
  - CONFIG_PREEMPT_RT *I think this is what we use now*
    - Allowing most spinlock(?now mutex) critical sections, RCU read-side critical sections, and interrupt handlers to be preempted.
    - Preemption of spinlock critical sections requires that priority inheritance
    - Desires(Check this part in the future)
    - Amount of code to be inspected
      - The low--level interrupt-handing code
      - The process scheduler.
      - And the latter four sorts described above.
- Priority Inversion Problem
  - A situation that a low-priority thread is holding the resourse that a high-priority task needs, result in infinite delay of high-priority work.
  - Could happen in the following situation:
    - Low-priority thread A acquires a pthread_mutex
    - Mid-priority thread B preemptes A
    - High-priority thread attempts to acquires the pthread_mutex
    - And suppose thread B is a rt thread, who will never lower down its priority. Thus thread A will never execute again to release the mutex, permits thread C to continue proceeding.
  - Not only mutex, but also some similar resourses: memory, communications packets, signals or events, file data.
  - Solutions
    - Disable preemption while a resource is held. 
      - Impractice for some resourses, and degrade scheduling latencies.
    - Forbid resourses to be acquired by tasks of different priorities.
    - Priority inheritance

# Spinlock
- References:
  - [wiki](https://en.wikipedia.org/wiki/Spinlock)
  - [makelinux.net](http://www.makelinux.net/ldd3/chp-5-sect-5)
  - [ececs.uc](gauss.ececs.uc.edu/Courses/c4029/code/pthreads/spinlock.c)
  - [spinlocks linux documentation](https://github.com/XingGaoY/linux/blob/master/Documentation/locking/spinlocks.txt)
- Spinlock is a lock which causes a thread trying to acquire it **simply wait in a loop wile repeatedly checking if the lock is available**, a kind of busy waiting.
- Offer higher performance than semaphores, when properly implemented. Usually implemented as a single integer bit value. And TS is used to set the bit.
- When a spinlock is acquired, and the thread loses the processor, the other threads may need to wait for a long time for the spinlock to be released or deadlock entirely. Thus the critical section protected by spinlock must be atomic, preemption is disabled, no interrupt is allowed. However, sleep can happen in surprising places, operation of swapping in from the disk when copying data from user space requires a sleep. 
- Spinlock must always be held for the minimum time possible.
- Once you start using spinlocks they tend to expand to areas you might not have noticed before, because you have to make sure the spinlocks correctly protect the shared data structures _everywhere_ they are used. The spinlocks are most easily added to places that are completely independent of other code (for example, internal driver data structures that nobody else ever touches).
- NOTE! The spin-lock is safe only when you _also_ use the lock itself to do locking across CPU's, which implies that EVERYTHING that touches a shared variable has to agree about the spinlock they want to use.
- The irq-versions of the spinlocks only need to disable the _local_ interrupts - it's ok to use spinlocks in interrupts on other CPU's, because an interrupt on another CPU doesn't interrupt the CPU that holds the lock, so the lock-holder can continue and eventually releases the lock.
- Functions:
  - ```spin_lock_irqsave``` and ```spin_lock_irq``` acquire the spinlock and disable interrupt, the former one saves the previous interrupt state in ```flags```.
  - ```spin_lock_bh``` disables software interrups, leaves hardware interrupts enabled.
- Reader/Writer Spinlocks
[Detailed implementation in linux](https://www.ibm.com/developerworks/cn/linux/l-rwlock_writing/index.html)
  - A reader/writer form of spinlocks that is directly analogous to reader/writer semaphores, allows any number of readers into a critical section simutaneously, but writers must have exculsive access.
  - The form is similar with normal spinlock, except that they are identified with ```read``` or ```write```.
## A Revise of RW Problem
- RW allows multiple readers to be in the same critical region at once, but if somebody wants to change the variables it has to get an exclusive write lock.
- Two kinds of locks: reader's and writer's, ensure that only a single writer can enter the critical section and no writer can acquire the writer's lock when any reader is still looking up the list.
- When a reader acquires a read lock, it will increment the readers variable which tracks how many readers are currently inside the data structure.
- Thus the first reader acquires the writelock, and all the readers are able to enter the critical section(there is a ```sem``` with large initial number, thus easy for readers to acquire readlock). The last reader releases the writelock.
## The comment in ```linux/arch/x86/include/asm/spinlock.h```
```
    NOTE! it is quite common to have readers in interrupts but no interrupt writers. For those circumstances we can "mix" irq-safe locks - any writer needs to get a irq-safe write-lock, but readers can get non-irqsafe read-locks.
    On x86, we implement read-write locks using the generic qrwlock with x86 specific optimization.
```

# RCU
## Basic concepts
- References
  - LWN series about RCU
    - [What is RCU, Fundamentally?](http://lwn.net/Articles/262464/)
    - [What is RCU? Part 2: Usage](http://lwn.net/Articles/263130/)
    - [RCU part 3: the RCU API](http://lwn.net/Articles/264090/)
    - [The RCU API, 2010 Edition](http://lwn.net/Articles/418853/)
    - [The RCU API, 2014 Edition](http://lwn.net/Articles/609904/)
- A synchronization mechanism achieves scalability improvements by allowing reads  to occur concurrently with updates.
- RCU ensures that reads are coherent by maintaining multiple versions of objects and ensuring that they are not freed up until all pre-existing read-side critical sections complete. RCU defines and uses efficient and scalable mechanisms for publishing and reading new versions of an object, and also for deferring the collection of old versions. These mechanisms distribute the work among read and update paths in such a way as to make read paths extremely fast. In some cases (non-preemptable kernels), RCU's read-side primitives have zero overhead. 
- Advantages of RCU include performance, deadlock immunity, and realtime latency.
- Publish-Subscribe Mechanism
  - Concurrent modify, if there are several operations to init ```gp```, ```rcu_assign-pointer(gp, p)``` will create a barrier to make sure ```p``` is set after all assignments.
    - Sometimes(~I guess I don't need to know the details for now~), ```p->a``` may be fetched before the value of ```p```. So guarrenteeing subsequent operations will see any initialization that occurred **before the corresponding publish operation** with ```rcu_dereference```
    - In practice, these two primitives are used in some higher implementation, like ```list_add_rcu()``` and ```list_for_each_entry_rcu``` to protect executing sequence.
    > **Quiz 2** is interesting.
- Wait for Pre-Existing RCU Readers to Complete
  - The great advantage of RCU is that it can wait for each of (say) 20,000 different things without having to explicitly track each and every one of them, and without having to worry about the performance degradation, scalability limitations, complex deadlock scenarios, and memory-leak hazards that are inherent in schemes using explicit tracking. 
  - The things waited on are "RCU read-side critical sections", start with an ```rcu_read_lock()``` primitive and ends with an ```rcu_read_unlock()``.
  - The read-copy procedure: while permit concurrent _reads_, line 16 _copies_ and line 17-19 do an _update_; ```synchronize_rcu``` is used to wait all prior RCU read-side critical sections are guarranteed to have completed. 
```
    ...
    15 q = kmalloc(sizeof(*p), GFP_KERNEL);
    16 *q = *p;
    17 q->b = 2;
    18 q->c = 3;
    19 list_replace_rcu(&p->list, &q->list);
    20 synchronize_rcu();
```
  - And ```synchronize_rcu()``` can conceptually be:
```
    1 for_each_online_cpu(cpu)
    2   run_on(cpu);           
\\ Switch the current thread to the specified CPU, which forces a context switch on that CPU. 
\\ And the for loop does this on each CPU, guaranteeing all prior RCU read-side critical sections
\\ have been completed.
```
  - **Although this simple approach works for kernels in which preemption is disabled across RCU read-side critical sections, in other words, for non-CONFIG_PREEMPT and CONFIG_PREEMPT kernels, it does not work for CONFIG_PREEMPT_RT realtime (-rt) kernels. Therefore, realtime RCU uses a different approach based loosely on reference counters. **
- Maitain Multiple Versions of Recently Updated Objects
  - No readers will hold reference to the instance which has been deleted or replaced after the operation '''synchronize_rcu()```
## Usage
- RCU as a Reader-Writer Lock Replacement
  - RCU's most common use is as a replacement for rwlocking in reading intensive situations.
  - RCU provide a significant performance advantages than rwlock.
  - Some comparison of performence between rwlock and rcu. Check them if a visual sense is needed.
- Deadlock Immunity
  - For the fact that RCU read-side primitives do not block, spin, or even do backwards branches, so their execution time is deterministic, making it impossible to participate in a deadlock cycle.
  - Another interesting thing is RCU's readside deadlock immunity is that it is possible to unconditionally upgrade an RCU reader to an RCU updater.
  - And it has immunity to a large class of priority inversion problems.
- Realtime Latency
  - Excellent realtime latencies, because of no spin nor block.
- RCU Readers and Updaters Run Concurrently
  - RCU readers and updaters do not block each other, which permits the RCU readers to see the updated values sooner.
  - Because their execution overlap with RCU updater, all of the RCU readers might well see updated values.
  - Comparison:
    - rwlock guarantees any reader that begins after the writer starts executing to see new values. Readers attempt to start while the writer is spinning might or might not see new values, depending on the r/w preference of rwlock implementation.
    - rcu guarantees any reader that begins after the updater completes to see new values. Readers that end after the updater begins might or might not see new values, depending on timing.
    - some consistency problems **Maybe future check is necessary**
- Low-Priority RCU Readers Can Block High-Priority Reclaimers
> Details are in rt-RCU, may be vital to check.
- RCU Grace Periods Extend for Many Milliseconds
> Pay attention to this feature!!!
- RCU is a Bulk Reference-Counting Mechanism
  - A mechanism to reduce cache line bouncing, or so called false sharing
- RCU is a Poor Man's Garbage Collector
  - Partially true, manually indication to collect and manually mark RCU read-side critical sections where references might legitimately be held.
- RCU is a Way of Providing Existence Guarantees
  - If any RCU-protected data element is accessed within an RCU read-side critical section, that data element is guaranteed to remain in existence for the duration of that RCU read-side critical section. 
- RCU is a Way of Waiting for Things to Finish
> Didn't skim.

# The Design of Preemptible read-copy-update
[lwn](https://lwn.net/Articles/253651/)

# A Realtime Preemption Overview
[lwn](https://old.lwn.net/Articles/146861/)
- Philosophy
  - Minimize the amount of kernel code that is non-preemptible and the amount of code that must be changed.
  - Particularly, critical sections, interrupt handlers, interrupt-disable code sequences are normally preemptible.
> Check this paragraph again, not that understand the metaphore here.
- Features
  - Preemptible critical sections  
    - Able to block while acquiring a spinlock and illegal to acquire a spinlock with either preemption or interrupts disabled, even ```spin_lock_irqsave()``` is cannot disable hardware interrupts when used on spinlock_t.
    - Normal spinlocks(```spinlock_t``` and ```rwlock_t```), RCU read-side sections(```rcu_read_lock()``` and ```rcu_read_unlock()```) and Semaphore critical sections are preemptible
    > Does this "illegal" right? Unable because of correctness or intrinsic design? I prefer the latter.
    - Use ```raw_spinlock_t``` to acquire a lock when interrupts or preemption are disabled. A kind of "overload" is used in PREEMPT_RT.
    - Critical section can be preempted leading it move to a different CPU, and the per-CPU variables need to be especially dealt with:
      - explicitly disable preemption, through use of ```get_cpu_var()```, ```preempt_disable()``` or disabling hardware interrupts.
      - Use a per-CPU lock variables, by using primitive ```DEFINE_PER_CPU_LOCKED()```
      - Preemptible interrupt handlers *(Thread are caused by interrupt or normal? lead to the difference between interrupt context and process context)*
    - Almost all interrupt handlers run in process context.
    - ```SA_NODELAY``` can be used to let it run in interrupt context, only ```fpu_irq```*(floating-point co-processor interrupts)*, ```irq0```*(per-CPU timer interrupt)*, ```irq2``` and ```lpptest```*(interrupt-latency benchmarking)* is specified with it, and only ```irq0``` is normally used.
    - Software times do not run in hardware interrupt context, in process context and are fully preemptible instead.
    - ```SA_NODELAY``` is not meant to be frequent use for performance degradation. And it should be used carefully.
    - Per-CPU timer interrupt runs in hardware-interrupt context, any locks shared with process-context code must be raw spinlocks, and ```_irq``` variants must be used.
  - Preemptible "interrupt disable" code sequences
    - **Any code that interacts with an interrupt handler must be prepared to deal with that interrupt handler running concurrently on some other CPU.**
    - ```spin_lock_irqsave``` and related need not disable preemption, if the interrupt handler runs, even if it preempts code hold the lock, it will block as soon as attempt to acquire the lock.
    > It was designed to prevent deadlock caused by priority inversion. However, no busy waiting any more, it will block when trying to fetch the lock???
    - ```local_irq_save()``` still disables preemption, no corresponding lock to rely on.
    - Code must interact with ```SA_NODELAY``` interrupts connot use ```local_irq_save()```, instead, ```raw_local_irq_save()``` should be used.
  - Priority inheritance for in-kernel spinlocks and semaphores
    - Piority inheritance is used to prevent priority inheritance. Higher priority task give their priority to lower priority tasks that are holding critical locks.
    - Transitive. And time is limited, as the lock is released, the enhanced priority is given up.
    - *Too much detail, check here again when necessary*

# To be read
- [https://old.lwn.net/Articles/146861/](https://old.lwn.net/Articles/146861/)
- [http://www2.rdrop.com/users/paulmck/realtime/paper/MV07_RTLdeepdive.2007.09.26a.pdf](http://www2.rdrop.com/users/paulmck/realtime/paper/MV07_RTLdeepdive.2007.09.26a.pdf)
- [https://events.linuxfoundation.org/sites/events/files/slides/linux-con-rt-into-mainline-2015.pdf](https://events.linuxfoundation.org/sites/events/files/slides/linux-con-rt-into-mainline-2015.pdf)
- [https://www.ibm.com/developerworks/linux/library/l-kprobes/index.html](https://www.ibm.com/developerworks/linux/library/l-kprobes/index.html)
- [https://lwn.net/Articles/132196/](https://lwn.net/Articles/132196/)
- [https://wiki.linuxfoundation.org/realtime/documentation/technical_details/start](https://wiki.linuxfoundation.org/realtime/documentation/technical_details/start)
- [https://wiki.linuxfoundation.org/realtime/documentation/technical_basics/start](https://wiki.linuxfoundation.org/realtime/documentation/technical_basics/start)
- [Memory Ordering in Modern Microprocessors](http://www.rdrop.com/users/paulmck/scalability/paper/ordering.2007.09.19a.pdf)
- [Priority Boosting RCU Read-Side Critical Sections](https://lwn.net/Articles/220677/)
- [Using Promela and Spin to verify parallel algorithms](https://lwn.net/Articles/243851/)
- [Sleepable RCU](https://lwn.net/Articles/202847/)
- [Tornado: Maximizing Locality and Concurrency in a Shared Memory Multiprocessor Operating System](https://www.usenix.org/legacy/events/osdi99/full_papers/gamsa/gamsa.pdf)
