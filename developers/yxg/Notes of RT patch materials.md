#### Table of Contents
- [Wikipedia Real-time computing](#Wikipedia-Real-time-computing)
- [Wikipedia Real-time operating system](#Wikipedia-Real-time-operating-system)
- [Wikipedia RTLinux](#Wikipedia-RTLinux)
- [Wikipedia Scheduling analysis real-time systems](#Wikipedia-Scheduling-analysis-real-time-systems)
- [Attempted summary of "RT patch acceptance" thread, take2](#Attempted-summary-of-"RT-patch-acceptance"-thread,-take2)
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
- [lrt ibm(1)](https://www.ibm.com/developerworks/cn/linux/l-lrt/part1/index.html)
- [lrt ibm(2)](https://www.ibm.com/developerworks/cn/linux/l-lrt/part2/#icomments)