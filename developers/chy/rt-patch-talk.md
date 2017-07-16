title: rt-patch intro
speaker: Yu Chen
url: https://github.com/ksky521/nodePPT
transition: zoomin
theme: light
files: /js/demo.js,/css/demo.css

[slide]

# RT-PATCH Intro
## Yu Chen

[slide]

# RT patch  {:&.flexbox.vleft}
## Web Site
 * https://rt.wiki.kernel.org/index.php/Main_Page


## Stable Repository
 * git://git.kernel.org/pub/scm/linux/kernel/git/rt/linux-stable-rt.git

## Patches
 * http://www.kernel.org/pub/linux/kernel/projects/rt/


[slide]

# Hardware Effect on RT  {:&.flexbox.vleft}

* Dependent on the system
 * SMI
 * Cache
 * Bus Contention
* hwlat detector
 * monitor kernel module


[slide]
# The Goal of PREEMPT_RT
----
* 100% Preemptible kernel {:&.fadeIn}
 * Not actually possible, but lets try regardless
 * Remove disabling of interrupts
 * Removal of disabling other forms of preemption

* Quick reaction times!
  * bring latencies down to a minimum


[slide]
# Some layer of RT
----
* No Preemption　{:&.fadeIn}
 * Server, Long latency syscall
 * Never schedule unless a function explicitly calls schedule()
* Voluntary Preemption
 * might_sleep(); -> might_resched() -> _cond_resched
 * need_resched, schedule only at “preemption points”
 * Used as a debugging aid to catch functions that might schedule called from atomic operations.

[slide]
# Some layer of RT
----
* Preemptible Kernel　{:&.fadeIn}
 * Robert Love's CONFIG_PREEMPT
 * SMP machines must protect the same critical sections as a preemptible kernel
 * Preempt anywhere except within spin_locks and some minor other areas (preempt_disable).
 * Every spin_lock acts like a single “global lock” WRT preemption.

[slide]
# Some layer of RT
----
* Fully Preemptible Kernel　{:&.fadeIn}
 * PREEMPT_RT_FULL
 * Preempt everywhere! (except from preempt_disable and interrupts disabled).
 * spin_locks are now mutexes.
 * Interrupts as threads, interrupt handlers can schedule
 * Priority inheritance inside the kernel (not just for user mutexes)


[slide]
# Implemtation of RT
----
* Sleeping spin_lock
 * sleeping spin_locks contains critical sections that are localized to tasks
 * Must have threaded interrupts
 * Must not be in atomic paths (preempt_disable or local_irq_save)
 * Uses priority inheritance, Not just for futexes

 
[slide]
# Implemtation of RT
----
* PREEMPT_LAZY
 * RT can preempt almost anywhere
 * Spinlocks that are now mutexes can be preempted, Much more likely to cause contention
 * Do not preempt on migrate_disable(), which os used by sleepable spinlocks
 * Increases throughput on non-RT tasks

 
[slide]
# Implemtation of RT
----

 
[slide]
# Implemtation of RT
----

 
[slide]
# Implemtation of RT
----
 
[slide]
# Implemtation of RT
----

 
[slide]
# Implemtation of RT
----

 
[slide]
# Implemtation of RT
----
 
[slide]
# Implemtation of RT
----

 
[slide]
# Implemtation of RT
----

 
[slide]
# Implemtation of RT
----
 
[slide]
# Implemtation of RT
----

 
[slide]
# Implemtation of RT
----

 
[slide]
# Implemtation of RT
----
 
[slide]
# Implemtation of RT
----

 
[slide]
# Implemtation of RT
----

 
[slide]
# Implemtation of RT
---- 
