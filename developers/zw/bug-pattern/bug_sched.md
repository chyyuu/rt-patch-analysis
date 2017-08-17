* [2.6.25         ] disable-sched-rt-groups.patch {C::bug::hang::sched::sched::temporary disable sched_rt groups}
  + [[file:2.6.25/disable-sched-rt-groups.patch][2.6.25]]
--
* [2.6.26 - 2.6.29] sched-fix-dequeued-race.patch {C::bug::crash::sched::sched::sched-fix-dequeued-race}
  + [[file:2.6.26/sched-fix-dequeued-race.patch][2.6.26]]
--
* [2.6.29         ] cpu-hotplug: cpu_down vs preempt-rt{C::bug::crash::sched::idle:: using mmdrop_delayed_drop fun}
  + [[file:2.6.29/cpuhotplug-idle.patch][2.6.29]]

  防止idle thread被调度走，会引发"curious problems"
--
* [   3.8 -   3.12] sched: Adjust sched_reset_on_fork when nothing else changesC::bug::data_err::sched::sched::sched: Adjust sched_reset_on_fork when nothing else changes}
  + [[file:3.8/sched-adjust-reset-on-fork-always.patch][3.8]]

  在某个特定路径下sched_reset_on_fork没有被修改
--
* [   3.8 -   3.12] sched: Consider pi boosting in setscheduler{C::bug::rtlatency::sched::sched::sched: Consider pi boosting in setscheduler}
  + [[file:3.8/sched-consider-pi-boosting-in-setscheduler.patch][3.8]]

  调度引起同优先级的任务顺序重排
--
* [   3.8 -   3.14] sched: Init idle->on_rq in init_idle(){C::bug::crash::sched::sched::Init idle->on_rq in init_idle()}
  + [[file:3.8/idle-state.patch][3.8]]

  初始化变量
--
* [   3.8 -   3.14] sched: Queue RT tasks to head when prio drops{C::bug::rtlatency::sched::sched::sched: Queue RT tasks to head when prio drops}
  + [[file:3.8/sched-enqueue-to-head.patch][3.8]]

  调度引起同优先级的任务顺序重排，修改为若一个任务的优先级上升则加入高优先级队列的尾部，若优先级下降则加入低优先级队列的头部的原则，以防止任务顺序错乱
--
* [  3.14         ] sched: Adjust p->sched_reset_on_fork when nothing else changes{C::bug::data_err::sched::sched::sched: Adjust p->sched_reset_on_fork when nothing else changes}
  + [[file:3.14/sched-Adjust-p-sched_reset_on_fork-when-nothing-else.patch][3.14]]

  在某个特定路径下sched_reset_on_fork没有被修改
--
* [  3.14 -   3.18] sched: Fix broken setscheduler(){C::bug::rtlatency::sched::sched::sched: Fix broken setscheduler()}
  + [[file:3.14/sched-Fix-broken-setscheduler.patch][3.14]]
--
* [   4.8 -   4.11] mm: perform lru_add_drain_all() remotely{C::bug::hang::sched::semantics::grabbing swapvec_lock}
  + [[file:4.8/mm-perform-lru_add_drain_all-remotely.patch][4.8]]

  lru_add_drain_all()可能永远不被调度
