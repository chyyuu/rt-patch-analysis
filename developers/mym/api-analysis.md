cr以linux 4.11-rt为参考对象
1 分析 mainline Linux v.s. Linux-rt-full locl/mutex/sync api
在SMP下，理解每对api的含义，使用场景，特征


| API name                                 | kernel  | critical section | uninterrupt | nopreempt | nomigrate | nosfotirq | sleep/sched |
| :--------------------------------------- | :------ | :--------------: | :---------: | :-------: | :-------: | :-------: | :---------: |
| local_irq_disable/enable                 | vanilla |         N        |      Y      |     Y     |     Y     |    y      |      N      |
|                                          | rt-full |         N        |      Y      |     Y     |     Y     |    Y      |      N      |
| local_irq_save/restore                   | vanilla |         N        |      Y      |     Y     |     Y     |    Y      |      N      |
|                                          | rt-full |         N        |      Y      |     Y     |     Y     |     Y     |      N      |
| local_irq_disable/enable_nort            | rt-full |        N         |      N      |     N     |     N     |     N     |      Y      |
| local_irq_disable/enable_rt              | rt-full |        N         |      Y      |     Y     |     Y     |     Y     |      Y      |
| local_irq_save/restore_nort              | rt-full |        N         |      N      |     N     |     N     |     N     |      Y      |
| local_bh_disable/enable                  | vanilla |         N        |      N      |     Y     |     Y     |     Y     |      N      |
|                                          | rt-full |         N        |      N      |     N     |     Y     |     Y     |      Y?     |
| spin_lock/unlock                         | vanilla |        Y         |      N      |     Y     |     Y     |     N     |      N      |
|                                          | rt-full |        Y         |      N      |     N     |     Y     |     N     |      Y?     |
| spin_lock/unlock_irqsave/restore         | vanilla |        Y         |      Y      |     Y     |     Y     |     Y     |      N      |
|                                          | rt-full |        Y         |      N      |     N     |     Y     |     N     |      Y?     |
| spin_lock/unlock_bh                      | vanilla |        Y         |      N      |     Y     |     Y     |     Y     |      N      |
|                                          | rt-full |        Y         |      N      |     Y     |     Y     |     Y     |      Y?     |
| spin_lock_irq                            | vanilla |       Y          |    Y        |    Y      |     Y     |           |             |
|                                          | rt-full |       Y          |             |           |     Y     |           |             |
| spin_lock/unlock_ _no_mg                 | rt-full |       Y          |      N      |     N     |     N     |     N     |      Y      |
| preempt_disable/enable                   | vanilla |        N         |      N      |     Y     |     Y     |     N     |      N?     |
|                                          | rt-full |        N         |      N      |     Y     |     Y     |     N     |      N?     |
| mutex_lock/unlock                        | vanilla |        Y         |      N      |     N     |     N     |     N     |      Y      |
|                                          | rt-full |        Y         |      N      |     N     |     N     |     N     |      Y      |
| rcu_read_lock/unlock                     | vanilla |        N         |      N      |     *     |           |           |             |
|                                          | rt-full |                  |             |           |           |           |             |
| get/put_cpu                              | vanilla |        N         |      N      |     Y     |     Y     |     N?    |      N      |
|                                          | rt-full |        N         |      N      |     Y     |     Y     |     N??   |      N      |
| get/put_cpu_light                        | rt-full |        N         |      N      |     N     |     Y     |     N     |      Y?     |
| local_lock/unlock                        | rt-full |        N         |      N      |     N     |     N     |     N?    |      Y?     |
| local_lock/unlock_irq                    | rt-full |        *         |      N      |     N     |     Y     |     N     |      Y?     |
| local_lock_irqsave                       | rt-full |        *         |      N      |     N     |     Y     |     N     |      Y?     |
| cpu_relax                                | vanilla |                  |             |           |           |           |      N      |
|                                          | rt-full |                  |             |           |           |           |      N      |
| cpu_chill                                | rt-full |                  |             |           |           |           |      Y      |
| migrate_disable/enable                   | rt-full |       N          |     N       |     N     |     Y     |     N?    |     Y?      |
| futex_wait/wake                          | vanilla |       Y          |     N       |     N     |     N     |     N     |     Y       |
| WAKE_Q\|wake_up_q\|wake_q_add\|mark_wake_futex | rt-full |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |
| pagefault_disabled_inc/dec               | rt-full |                  |             |           |           |           |             |
| pagefault_disable/enable\|pagefault_disabled\|might_fault | rt-full |                  |             |         |    Y     |           |             |
|                                          | vanilla |                  |             |         |     N     |           |             |
| in_atomic                                | vanilla |                  |             |           |           |           |             |
|                                          | rt-full |                  |             |           |           |           |             |
| faulthandler_disabled                    | vanilla |                  |             |           |    N      |           |             |
|                                          | rt-full |                  |             |           |    Y      |           |             |
| lock/unlock_fpu_owner                    | rt-full |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |

* "*" determined by CONFIG_PREEMPT_RCU
* uninterruptible > no preempt
* Preemption (along with some other context info) are maintained by the preempt_count(). Possible
* contexts include task, hardirq, softirq and nmi.
* Mainline Linux has no specific way to disable migration while enable preemption.
* With preemption enabled in the configuration, do not allow preemption = unsleepable.
* Softirq handlers are always invoked in a separate thread with preemption disabled.
