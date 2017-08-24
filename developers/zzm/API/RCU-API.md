- ` rcu_read_lock/unlock `

	- 源代码

			Rcu_read_lock()和rcu_read_unlock()的实现如下: 
			#define rcu_read_lock() __rcu_read_lock() 
			#define rcu_read_unlock() __rcu_read_unlock() 
			
			#define __rcu_read_lock() 
			do { 
			preempt_disable(); 
			__acquire(RCU); 
			rcu_read_acquire(); 
			} while (0) 
			#define __rcu_read_unlock() 
			do { 
			rcu_read_release(); 
			__release(RCU); 
			preempt_enable(); 
			} while (0) 

		- 从源代码可以看出rcu_read_lock(),rcu_read_unlock()只是禁止和启用抢占.因为在读者临界区,不允许发生上下文切换.
		- RCU使用在读者多而写者少的情况.RCU和读写锁相似.但RCU的读者占锁没有任何的系统开销.写者与写者之间必须要保持同步,且写者必须要等它之前的读者全部都退出之后才能释放之前的资源.
		- RCU保护的是指针.这一点尤其重要.因为指针赋值是一条单指令.也就是说是一个原子操作.因它更改指针指向没必要考虑它的同步.只需要考虑cache的影响. 
		- 读者是可以嵌套的.也就是说rcu_read_lock()可以嵌套调用. 
		- 读者在持有rcu_read_lock()的时候,不能发生进程上下文切换.否则,因为写者需要要等待读者完成,写者进程也会一直被阻塞. 
		- 它既允许多个读者同时访问被保护的数据，又允许多个读者和多个写者同时访问被保护的数据（注意：是否可以有多个写者并行访问取决于写者之间使用的同步机制），读者没有任何同步开销，而写者的同步开销则取决于使用的写者间同步机制。但RCU不能替代rwlock，因为如果写比较多时，对读者的性能提高不能弥补写者导致的损失。

				critical section（N）：没有持有锁，不能保护临界区，对于rcu_read,可以嵌套读写，没有必要保护。
				uninterrupt（N）:
				nopreempt （Y）：在获取lock（）需要禁止抢占，否则写着会等待读者一直阻塞
				nomigrate （Y）：
				nosfotirq （N）： 
				sleep/sched（N）：抢占禁止的原子上下文禁止调度和睡眠。

