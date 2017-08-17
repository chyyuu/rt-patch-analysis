总结：
从现有分析的history.org中得到bug_preempt和bug_order一共47个，其中一直持续到目前版本的补丁有10个（1-10），其已经进入主线或被去除替换掉的补丁（11-47）

当前仍在持续的补丁中，可总结出的pattern


 

- 对Per_cpu var 的保护或增强实时性的改变：
	 

	- 增加可抢占区域:增加`preempt_disable/enable()`来减少原来不可抢占的区域。例如 patches（2）。
	 

	- 替换不可抢占API：将`preempt_disable/enable()->migration_disable/enable()`,对于以前的`get_cpu_*()`替换为`get_cpu_light_*()`或者替换为get_local_*(),后者是将前者的
	`preempt_disable/enable()->migration_disable/enable()`，但是这样的替换，需要后边对`per_cpu `  var 操作时需要加spin_lock 做互斥保护（好像有些patch并没有加保护，可能有规律）。例如 patch（6、10）
	

	- 修复在 RT中，`preempt_disable/enable()->migration_disable/enable()`修复在不可抢占区域调用睡眠锁造成在原子上下文进行重新调度，这是有问题的。例如 patch（6、10）



- 在空操作任务中一般需要将`spin_lock->raw_spin_lock`,因为空任务时，调度队列为空，如果在获取锁上阻塞，将不能重新唤醒（不知道对不对）。例如 patch（9、12）



- 使用`cpu_chill()`函数（其中的睡眠函数`__hrtimer_nanosleep（）`（原来使用sleep（1），存在bug）），来避免retry loops forever when modifying side was preempted。例如 patch（7、8）



- 系统初始化时，需要增加相应的原语和锁保护sch->tick*的准确性。例如patch（1、18）



- 对于软中断（bottom half），避免在中断结束，`raise_softirq_irqoff()`(禁用中断，唤醒软中断)以后，重新启用中断`local_irq_enable/restore`以后，被抢占，造成bottom half 无线延迟。因此，在RT中，需要增加preempt_check_resched_rt（）检查是否有抢占。例如 patch（5）。patch（29）此处通过增加检查（或循环检查）避免tasklet在上锁之后，增加到队列之前被竞争.




对于已经进入主线或被去除替换掉的补丁，可以总结出的pattern：




- 有些补丁可能已经被替换掉了，例如patch（18、19、21、22、23、32、41、42），这些补丁大多修复的是通过`preempt_disable/enable()`来对`per_CPU` var 进行保护，但目前的RT补丁为了增加可抢占区域，替换为`migration_disable/enable()`,因此，这些可能已经被替换掉。


- 有一些补丁是修复执行顺序的，例如patch（15）增加了clock event mode 用来在系统处于空模式的C-states状态恢复过程中的恢复顺序，确保clockevent devices在tick之前被重新启动，避免定时器中断产生，而clock event devices还没有恢复。但在mainline并没有看到这种方式的存在。patch（34）确保在文件之前释放inode。
patch（44）确保:clear `nmi_show_regs 在 show_regs()`之后。patch(29) patch（26、43、44、45）。



- 还有一些是修复引入mutex后，由于`spin_lock->raw_spin_lock`带来的问题。例如 patch（11、12、14、21、24、27、33）

- 其他的有一些是增加实时性，替换`preempt_disable()`,如patch（13、28）；有一些是增加功能，造成系统hang，如 patch(16)



