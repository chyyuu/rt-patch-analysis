cr以linux 4.11-rt为参考对象
1 分析 mainline Linux v.s. Linux-rt-full locl/mutex/sync api
在SMP下，理解每对api的含义，使用场景，特征


| API name                                 | kernel  | critical section | uninterrupt | nopreempt | nomigrate | nosfotirq | sleep/sched |
| :--------------------------------------- | :------ | :--------------: | :---------: | :-------: | :-------: | :-------: | :---------: |
| local_irq_disable/enable                 | vanilla |         N        |      Y      |     Y     |     Y     |    y      |      N      |
|                                          | rt-full |         N        |      Y      |     Y     |     Y     |    Y      |      N      |
| local_irq_save/restore                   | vanilla |         N        |      Y      |     Y     |     Y     |    Y      |      N      |
|                                          | rt-full |         N        |      Y      |     Y     |     Y     |     Y     |      N      |
| local_bh_disable/enable                  | vanilla |         N        |      N      |     Y     |     Y     |     Y     |             |
|                                          | rt-full |                  |             |           |     Y     |     Y     |             |
| spin_lock/unlock                         | vanilla |        Y         |      N      |     Y     |     Y     |     N     |      N      |
|                                          | rt-full |        Y         |             |           |     Y     |           |             |
| spin_lock/unlock_irqsave/restore         | vanilla |        Y         |      Y      |     Y     |           |           |             |
|                                          | rt-full |        Y         |             |           |     Y     |           |             |
| spin_lock/unlock_bh                      | vanilla |        Y         |             |     Y     |           |     Y     |             |
|                                          | rt-full |        Y         |             |           |     Y     |     Y     |             |
| preempt_disable/enable                   | vanilla |        N         |             |     Y     |           |           |             |
|                                          | rt-full |                  |             |     Y     |     Y     |           |             |
| mutex_lock/unlock                        | vanilla |        Y         |             |           |           |           |             |
|                                          | rt-full |        Y         |             |           |           |           |             |
| rcu_read_lock/unlock                     | vanilla |                  |             |     *     |           |           |             |
|                                          | rt-full |                  |             |           |           |           |             |
| get/put_cpu                              | vanilla |                  |             |     Y     |           |           |             |
|                                          | rt-full |                  |             |     Y     |     Y     |           |             |
| local_irq_disable/enable_nort            | vanilla |                  |      Y      |     Y     |           |           |             |
|                                          | rt-full |                  |             |           |           |           |             |
| local_irq_disable/enable_rt              | vanilla |                  |             |           |           |           |             |
|                                          | rt-full |                  |      Y      |     Y     |     Y     |           |             |
| local_irq_save/restore_nort              | vanilla |                  |      Y      |     Y     |           |           |             |
|                                          | rt-full |                  |             |           |           |           |             |
| local_irq_save/restore_rt                | vanilla |                  |             |           |           |           |             |
|                                          | rt-full |                  |      Y      |     Y     |     Y     |           |             |
| get/put_cpu                              | vanilla |                  |      Y      |           |           |           |             |
|                                          | rt-full |                  |      Y      |     Y     |           |           |             |
| local_lock/unlock[_irq]                  | rt-full |        *         |             |           |     Y     |           |             |
| cpu_relax                                | vanilla |                  |             |           |           |           |             |
|                                          | rt-full |                  |             |           |           |           |             |
| cpu_chill                                | rt-full |                  |             |           |           |           |      Y      |
| get/put_cpu                              | rt-full |                  |             |           |     Y     |     Y     |             |
| get/put_cpu_light                        | rt-full |                  |             |           |           |     Y     |             |
| migrate_disable/enable                   | rt-full |                  |             |           |           |           |             |
| spin_lock/unlock_ _no_mg                 | rt-full |                  |             |           |           |           |             |
| wake_futex                               | vanilla |                  |             |           |           |           |             |
| WAKE_Q\|wake_up_q\|wake_q_add\|mark_wake_futex | rt-full |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |
| pagefault_disabled_inc/dec               | rt-full |                  |             |           |           |           |             |
| pagefault_disable/enable\|pagefault_disabled\|might_fault | rt-full |                  |             |           |           |           |             |
| in_atomic                                | vanilla |                  |             |           |           |           |             |
| faulthandler_disabled                    | rt-full |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |
| lock/unlock_fpu_owner                    | rt-full |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |
| local_lock_irqsave                       | rt-full |       Y          |             |           |     Y     |           |             |
| spin_lock_irq                            | vanilla |       Y          |    Y        |    Y      |     Y     |           |             |
| spin_lock_irq                            | rt-full |       Y          |             |           |     Y     |           |             |
|                                          |         |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |
|                                          |         |                  |             |           |           |           |             |

* "*" determined by CONFIG_PREEMPT_RCU
* uninterruptible > no preempt
* Preemption (along with some other context info) are maintained by the preempt_count(). Possible
* contexts include task, hardirq, softirq and nmi.
* Mainline Linux has no specific way to disable migration while enable preemption.
* With preemption enabled in the configuration, do not allow preemption = unsleepable.
* Softirq handlers are always invoked in a separate thread with preemption disabled.