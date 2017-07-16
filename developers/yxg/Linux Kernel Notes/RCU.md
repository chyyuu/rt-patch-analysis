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
