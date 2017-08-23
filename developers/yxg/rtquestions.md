## Q1 
preempt_disable: 通过给preempt计数加一来关闭抢占，避免该进程被调度  

### 何时需要添加或取消preempt_disable/disable[_rt]
[2.6.26]ppc-tlbflush-preempt.patch
[2.6.26]send-nmi-all-preempt-disable.patch
[2.6.29]preempt-realtime-x86_64.patch
[2.6.29]preempt-realtime-ipc.patch
[2.6.29]x86-pae-preempt-realtime-fix.patch
[4.1]0011-arm-futex-UP-futex_atomic_op_inuser-relies-on-disabl.patch
[4.9]fs-namespace-preemption-fix.patch
- 保护访问或修改per cpu var的代码段，例如`write_cr3()`
- 保护同步互斥，比如`[4.1]0011-arm-futex-UP-futex_atomic_op_inuser-relies-on-disabl.patch`，当然，这种方法是不是实时性最好值得商榷
- 最后一个patch恰好相反，是打开抢占，避免在循环中抢占一直关闭，使得部分循环可抢占

### 何时需要把XXX替换为preempt_disable/disable[_rt]
用preempt_disable替换的只有barrier，且只有一处
- barrier() -> preempt_disable()   
[4.9]peterz-percpu-rwsem-rt.patch

缩小了关闭抢占的区域，注释中说，用preempt_disable保护临界区代码，其余的修改基本就是重构

### 何时需要把preempt_enable替换为preempt_enable_nort
_nort的实现就是一个barrier()，保护执行顺序。

[4.8]lglocks-rt.patch
[4.8]lockinglglocks_Use_preempt_enabledisable_nort.patch
[4.9]mm--rt--Fix-generic-kmap_atomic-for-RT.patch
[4.9]arm-enable-highmem-for-rt.patch

- 该区域中的函数自己关闭抢占，或者可以保护好per cpu var，替换后往往可以缩小临界区。例如1中，使用per_cpu_ptr关闭抢占获得值，就不需要在外部使用preempt_disable关闭抢占了。
- 还有的是修改了部分函数，使得某些函数（pagefault_disable)自带preempt_disable/enable，那么额外的preempt_disable降低了效率。这种修改均和pagefault_disable相关。

## Q2
### 何时需要添加或取消migrate_disable/disable
关闭迁移但是依然可以抢占，可以保护per cpu var，抢占进来的进程不会修改该进程的per cpu var，所以该进程只需要保证不被迁移出去即可 
有大量的关闭迁移用于替代关闭抢占，但是patch中只找到以下两例：
[3.0]console-make-rt-friendly.patch
[3.18]printk-rt-aware.patch

- 两个都应该是保护per cpu var：con，因为con这个变量是cpu独占的，避免迁移保证其正确性

### migrate_disable() -> local_bh_disable()
[3.10]net-netif-rx-ni-use-local-bh-disable.patch

这个是因为内部的调用的函数被删去，不在需要migrate_disable

### 何时需要把XXX替换为migrate_disable/disable
- preempt_disable() -> migrate_disable()
关闭抢占改为关闭迁移，使得保护变得“轻量”，同时减少了优先级反转的可能

之后的patch基本上都是只需要将thread绑定在cpu上，保证正确性即可，不需要完全关闭抢占

如果只是为了保护per CPU var 的存取，那么只需要关闭迁移，抢占依然是可以允许的。这样可以提高实时性。
[3.0]hotplug-use-migrate-disable.patch
[3.10]upstream-net-rt-remove-preemption-disabling-in-netif_rx.patch
[3.18]block-mq-drop-preempt-disable.patch
[3.18]printk-rt-aware.patch
[4.4]dump-stack-don-t-disable-preemption-during-trace.patch
[4.6]KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch

## Q3
### 何时需要添加或取消local_irq_disable/enable, local_irq_save/restore[_nort]
关闭中断，或者将FLAG保存后关闭中断

以下的patch打开了中断，使得这一部分代码运行时接收可能的IPI中断

这个和函数的设计实现相关，并没有特殊的意义
[2.6.24]sched-enable-irqs-in-preempt-in-notifier-call.patch

### Enclose with irq_save
[2.6.25]radix-percpu-hack-fix.patch

该patch关中断是为了互斥保护，注释中说也可以使用一个rt sleeping spinlock来达到相同目的

[2.6.26]rwlock-protect-reader_lock_count.patch
同样也是互斥保护，在该语句下接了一个spinlock，事实上就是一个spinlock_irqsave


### Remove irq-save
在rt内核下，该函数是在一个线程中，就不再需要关闭中断了
[3.10]mmci-remove-bogus-irq-save.patch

### local_irq_save() -> raw_local_irq_save()
[2.6.22]arm-fix-atomic-cmpxchg.patch
[2.6.25]i386-mark-atomic-irq-ops-raw.patch
[2.6.26]generic-cmpxchg-use-raw-local-irq-variant.patch

### local_irq_disable() -> local_irq_save(flags)
[2.6.25]rcu-hrt-fixups.patch

### local_irq_save() -> local_irq_save_nort()
关闭中断变为空操作；

有很多这样的修改，部分是不再需要关闭中断来保证原子性，由于锁变为了“sleeping”的，或者内部有其他的手段保证原子性，或者里面的函数在rt中可以被抢占，不再需要额外的关中断，其余的和死锁或者crash相关

[2.6.24]local_irq_save_nort-in-swap.patch
[2.6.24]user-no-irq-disable.patch
[3.0]ata-disable-interrupts-if-non-rt.patch
[3.0]drivers-net-gianfar-make-rt-aware.patch
[3.0]drivers-net-vortex-fix-locking-issues.patch
[3.0]fs-ntfs-disable-interrupt-non-rt.patch
[3.0]ide-use-nort-local-irq-variants.patch
[3.0]infiniband-mellanox-ib-use-nort-irq.patch
[3.0]inpt-gameport-use-local-irq-nort.patch
[3.0]mm-scatterlist-dont-disable-irqs-on-RT.patch
[3.0]signal-fix-up-rcu-wreckage.patch
[3.14]user-use-local-irq-nort.patch
[4.11]mm-bounce-local-irq-save-nort.patch

以下的替换均是bugfix
[2.6.24]ntfs-local-irq-save-nort.patch
[3.0]resource-counters-use-localirq-nort.patch
[4.1]sas-ata-isci-dont-t-disable-interrupts-in-qc_issue-h.patch