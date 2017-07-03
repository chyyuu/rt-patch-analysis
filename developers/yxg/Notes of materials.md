* [Wikipedia Real-time computing](https://en.wikipedia.org/wiki/Real-time_computing#Hard)
- Real-time computing
  - Real-time computing (RTC), or reactive computing describes hardware and software systems subject to a "real-time constraint", for example from event to system response. Real-time programs must guarantee response within specified time constraints, often referred to as "deadlines". Real-time responses are often understood to be in the order of milliseconds, and sometimes microseconds.
  - A real-time system has been described as one which "controls an environment by receiving data, processing them, and returning the results sufficiently quickly to affect the environment at that time."
  - Definition: A system is said to be real-time if the total correctness of an operation depends not only upon its logical correctness, but also upon the time in which it is performed. Classified as:
    - Hard: missing a deadline is a total system failure.
    - Firm: infrequent deadline misses are tolerable, but may degrade the system's quality of service. The usefullness of a result is zero after its deadline.
    - Soft: the usefullness of a result degrades after its deadline, thereby degrading the system's performance.
> The difference of the latter two are the usefullness of a delayed result? Thus it is a definition of the demand made by applications.

* [Wikipedia Real-time operating system](https://en.wikipedia.org/wiki/Real-time_operating_system)
- RTOS
  - A real-time operating system (RTOS) is an operating system (OS) intended to serve real-time applications that process data as it comes in, typically without buffer delays. Processing time requirements (including any OS delay) are measured in tenths of seconds or shorter increments of time. They either are event driven or time sharing.
  - A key characteristic of an RTOS is the level of its consistency concerning the amount of time it takes to accept and complete an application's task; the variability is jitter.[1] A hard real-time operating system has less jitter than a soft real-time operating system.
  - The chief design goal is a guarantee of a soft or hard performance category.
  - Key factors in a real-time OS are minimal interrupt latency and minimal thread switching latency.

* [Wikipedia RTLinux](https://en.wikipedia.org/wiki/RTLinux)*(Saved for future reference)*
- RTLinux
  - Simple description: RTLinux is a hard realtime RTOS microkernel that runs the entire Linux operating system as a **fully preemptive process**. The hard real-time property makes it possible to control robots, data acquisition systems, manufacturing plants, and other time-sensitive instruments and machines from RTLinux applications.
  - Even with a similar name it is not related the "Real-Time Linux" project of the Linux Foundation.
- Background
  The key design objective was to add hard real-time capabilities to commodity OS to facilitate the development of complex control programs with both capabilities.

* [Wikipedia Scheduling analysis real-time systems](https://en.wikipedia.org/wiki/Scheduling_analysis_real-time_systems)

* [Attempted summary of "RT patch acceptance" thread, take2](https://old.lwn.net/Articles/143323/)
- Realtime operating system, especially hard-realtime, must be designed from ground up; Some exceptions:
  - **Many realtim eapplications use a very restricted subset of general-purpose OS.** Possible to provide very limited realtime support.
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
  - A situation that a low-priority threa is holding the resourse that a high-priority task needs, result in infinite delay of high-priority work.
  - Could happen in the following situation:
    - Low-priority thread A aquires a pthread_mutex
    - Mid-priority thread B preemptes A
    - High-priority thread attempts to aquires the pthread_mutex
    - And suppose thread B is a rt thread, who will never lower down its priority. Thus thread A will never execute again to release the mutex, permits thread C to continue proceeding.
  - Not only mutex, but also some similar resourses: memory, communications packets, signals or events, file data.
  - Solutions
    - Disable preemption while a resource is held. 
      - Impractice for some resourses, and degrade scheduling latencies.
    - Forbid resourses to be acquired by tasks of different priorities.
    - Priority inheritance

* To be read
- [https://old.lwn.net/Articles/146861/](https://old.lwn.net/Articles/146861/)
- [http://www2.rdrop.com/users/paulmck/realtime/paper/MV07_RTLdeepdive.2007.09.26a.pdf](http://www2.rdrop.com/users/paulmck/realtime/paper/MV07_RTLdeepdive.2007.09.26a.pdf)
- [https://events.linuxfoundation.org/sites/events/files/slides/linux-con-rt-into-mainline-2015.pdf](https://events.linuxfoundation.org/sites/events/files/slides/linux-con-rt-into-mainline-2015.pdf)
- [https://www.ibm.com/developerworks/linux/library/l-kprobes/index.html](https://www.ibm.com/developerworks/linux/library/l-kprobes/index.html)
- [https://lwn.net/Articles/132196/](https://lwn.net/Articles/132196/)
- [https://wiki.linuxfoundation.org/realtime/documentation/technical_details/start](https://wiki.linuxfoundation.org/realtime/documentation/technical_details/start)
- [https://wiki.linuxfoundation.org/realtime/documentation/technical_basics/start](https://wiki.linuxfoundation.org/realtime/documentation/technical_basics/start)
