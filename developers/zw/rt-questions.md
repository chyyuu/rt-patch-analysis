# Q6

## 内核的哪些地方一定要把spin_lock/unlock[_irqsave/restore|irq]换成raw_spin_lock/unlock[_irqsave/restore|irq]，这里面的规律是什么？

PREEMPT_RT配置下spin_lock是可睡眠的，因此凡是不可睡眠的地方一定要把spin_lock替换为raw_spin_lock。

1. 抢占或中断被关闭的区域不能使用spin_lock，相关patch有
  * arm-kprobe-replace-patch_lock-to-raw-lock.patch
  * arm-unwind-use_raw_lock.patch
  * cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
2. 另外，虽然PREEMPT_RT配置下进行了中断线程化，但一些硬件中断（如per-CPU timer interrupt）未线程化，这类中断没有进程上下文，因此也不能睡眠。相关patch有
  * timer-make-the-base-lock-raw.patch //That means the lock can be made raw and held in IRQ context.

3. 此外，spin_lock会带来额外的上下文切换开销，如果要保护的代码段较短可以用raw_spin_lock提高吞吐量，且对实时性影响很小，相关patch有
  * cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
  * delayacct-use-raw_spinlocks.patch。
  * mm-enable-slub.patch

>>chyyuu
4. （对3的补充）在某些非官方的atomic region或下面的片段，由于不属于hardirq handler区域，所以是有进程上下文的，临界区中不能有sleepable 函数，否则会死锁
注意：skbufhead-raw-lock.patch
```
Use the rps lock as rawlock so we can keep irq-off regions. It looks low
latency. However we can't kfree() from this context therefore we defer this
to the softirq and use the tofree_queue list for it (similar to process_queue).
```
这里的context为何不能执行kfree? 
原因是这一块rps lock算是irq-off region，即属于atomic context，不能有睡眠

```
-			kfree_skb(skb);
+			__skb_queue_tail(&sd->tofree_queue, skb);
 			input_queue_head_incr(sd);
 		}
 	}
+	if (!skb_queue_empty(&sd->tofree_queue))
+		raise_softirq_irqoff(NET_RX_SOFTIRQ);
```


补充：
用 
```
$ cd ../linux-rt-devel/; ag '\braw_spin_lock\('|wc; cd - 

284     615   17715

$ cd ../linux-tuna/;ag '\braw_spin_lock\('|wc;cd -
251     509   15543

``` 
可以看出，rt patch可能大致修改了33个spin_lock 为raw_spin_lock

From paper "The evolution of real-time linux" 可看到
```
Not every spinlock in the Linux Kernel, can be con-
verted to a mutex. Certain critical sections of low-
level code are not preemptible, and must be pro-
tected by the legacy non-preemptible spinlock.
Examples of non-preemptible critical sections
are:
 - short-held locks, where a context switch would require greater overhead
 - locks protecting hardware registers that must be non-preemptible for correct system operation
 - locks nested within other non-preemptible spinlocks
 - The scheduler’s runqueue locks, as well as the synchronization code that 
   synchronizes access to the real-time mutexes, are examples of non-
   preemptable code.

```


## 何时需要把spin_lock替换为spin_lock_irq?

spin_lock_irq的定义见rt-add-rt-locks.patch，可见不需要将spin_lock替换为spin_lock_irq。

```diff
+#define spin_lock_irq(lock)		spin_lock(lock)
+#define spin_unlock_irq(lock)		spin_unlock(lock)
```

将spin_lock替换为spin_lock_irq的patch有

* workqueue-use-rcu.patch
* block-shorten-interrupt-disabled-regions.patch

在非PREEMPT_RT配置下这种替换可以避免显式地使用local_irq_save，可能减小关中断区域的长度，在PREEMPT_RT配置下无影响。

## 何时需要把XXX替换为spin_lock_irqsave/spin_unlock_irqrestore

```diff
+#define spin_lock_irqsave(lock, flags)			 \
+	do {						 \
+		typecheck(unsigned long, flags);	 \
+		flags = 0;				 \
+		spin_lock(lock);			 \
+	} while (0)

+#define spin_unlock_irqrestore(lock, flags)		\
+	do {						\
+		typecheck(unsigned long, flags);	\
+		(void) flags;				\
+		spin_unlock(lock);			\
+	} while (0)
```

发生替换的patch有两类

1. spin_lock/unlock替换为spin_lock_irqsave/spin_unlock_irqrestore，避免显式地使用local_irq_save，可能减小关中断区域的长度，在PREEMPT_RT配置下无影响。
  * drivers-tty-fix-omap-lock-crap.patch
  * drivers-tty-pl011-irq-disable-madness.patch
  * workqueue-use-rcu.patch
2. bit_spin_lock/unlock替换为spin_lock_irqsave/spin_unlock_irqrestore，可以提高PREEMPT_RT配置下的实时性，见问题5。
  * fs-replace-bh_uptodate_lock-for-rt.patch

## 何时需要把XXX（如bit_spin_lock.etc.）替换为spin_lock

```c
/*
 *  bit-based spin_lock()
 *
 * Don't use this unless you really need to: spin_lock() and spin_unlock()
 * are significantly faster.
 */
static inline void bit_spin_lock(int bitnum, unsigned long *addr)
{
	/*
	 * Assuming the lock is uncontended, this never enters
	 * the body of the outer loop. If it is contended, then
	 * within the inner loop a non-atomic test is used to
	 * busywait with less bus contention for a good time to
	 * attempt to acquire the lock bit.
	 */
	preempt_disable();
#if defined(CONFIG_SMP) || defined(CONFIG_DEBUG_SPINLOCK)
	while (unlikely(test_and_set_bit_lock(bitnum, addr))) {
		preempt_enable();
		do {
			cpu_relax();
		} while (test_bit(bitnum, addr));
		preempt_disable();
	}
#endif
	__acquire(bitlock);
}
```

发生此类替换的patch有

* drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
* fs-jbd-replace-bh_state-lock.patch

在PREEMPT_RT下使用能睡眠的spin_lock替换与raw_spin_lock类似的bit_spin_lock以提高实时性，并且根据[Avoid more bit_spin_lock usage on RT kernels](http://www.spinics.net/lists/linux-rt-users/msg10127.html)，bit_spin_lock在PREEMPT_RT配置下可能引发诸多问题。

## 何时需要把XXX（如 local_irq_save; bit_spin_lock())）替换为bh_uptodate_lock_irqsave/bh_uptodate_unlock_irqrestore

```diff
+static inline unsigned long bh_uptodate_lock_irqsave(struct buffer_head *bh)
+{
+	unsigned long flags;
+
+#ifndef CONFIG_PREEMPT_RT_BASE
+	local_irq_save(flags);
+	bit_spin_lock(BH_Uptodate_Lock, &bh->b_state);
+#else
+	spin_lock_irqsave(&bh->b_uptodate_lock, flags);
+#endif
+	return flags;
+}
```

发生此类替换的patch有

* fs-replace-bh_uptodate_lock-for-rt.patch

在PREEMPT_RT下使用能睡眠的spin_lock_irqsave/spin_unlock_irqrestore替换与raw_spin_lock/unlock类似的bit_spin_lock/unlock以提高实时性。

# Q7

## 何时需要添加rcu_read_lock/unlock？

在需要保证同步且需要读取操作保持高效能时应当使用rcu_read_lock/unlock。

## 何时需要把XXX替换为rcu_read_lock/unlock？这里面有规律吗？

发生此类替换的patch有

* workqueue-use-rcu.patch

通过使用rcu_read_lock减小了关中断代码段的长度，提高实时性。

```diff
-	local_irq_disable();
+	rcu_read_lock();
 	pool = get_work_pool(work);
 	if (!pool) {
-		local_irq_enable();
+		rcu_read_unlock();
 		return false;
 	}
```
local_irq_disable 屏蔽了中断，而rcu_read_lock disable preempt

# Q8

## 何时需要添加或取消migrate_disable/enable？

由于critical sections在PREEMPT_RT下是可抢占，因此进程可能被迁移到另一个CPU上运行，此时per-CPU variables可能为错误值。要解决这个问题，要么使用per-CPU lock，要么直接禁止迁移，此时我们可以使用migrate_disable/enable。

## 何时需要把XXX替换为migrate_disable/enable？

发生此类替换的patch有

* hotplug-use-migrate-disable.patch
* KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch
* upstream-net-rt-remove-preemption-disabling-in-netif_rx.patch

观察到的替换均为以下形式

```diff
--- a/net/core/dev.c
+++ b/net/core/dev.c
@@ -3798,7 +3798,7 @@ static int netif_rx_internal(struct sk_b
 		struct rps_dev_flow voidflow, *rflow = &voidflow;
 		int cpu;
 
-		preempt_disable();
+		migrate_disable();
 		rcu_read_lock();
 
 		cpu = get_rps_cpu(skb->dev, skb, &rflow);
@@ -3808,14 +3808,14 @@ static int netif_rx_internal(struct sk_b
 		ret = enqueue_to_backlog(skb, cpu, &rflow->last_qtail);
 
 		rcu_read_unlock();
-		preempt_enable();
+		migrate_enable();
 	} else
```
对于upstream-net-rt-remove-preemption-disabling-in-netif_rx.patch，感觉如果加了rcu_read_lock其实就是preempt_disable, 如果这样，还需migrate_disable吗???


使用preempt_disable/enable也是为了防止迁移，但效果过强，换成语义较弱的migrate_disable/enable可以提高性能。
