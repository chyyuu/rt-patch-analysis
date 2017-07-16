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