## history format
```
PATCH_ITEM ::= * VERSIONS  PATCH_TITLE {CHARACTERISTIC::ASPECT} \n PATCH_CHANGS
VERSIONS ::= '['BEGIN_VERSION - END_VERSION']'|'['BEGIN_VERSION']'
BEGIN_VERSION|END_VERSION ::= [2..4].[0..18].[22..29]
PATCH_TITLE ::= TITLE.patch 
TITLE|DESCRIPT = ['a'..'z','A'..'Z']*|NULL //string or nothing
CHARACTERISTIC ::='C'
ASPECT ::= FEATURE|BUG|PERFORMANCE|MAINTAIN

FEATURE ::= 'feature'::FEATURE_METHOD::DESCRIPT
FEATURE_METHOD::= 'hardware'|'debuginfo'|'idle'|'hrtimer'|'statistics'|'delay'

BUG ::= 'bug'::BUG_CONSEQUENCE::BUG_TYPE::FIX_METHOD::DESCRIPT
BUG_CONSEQUENCE ::='corrupt'|'hang'|'crash'|'leak'|'irq'|'livelock'|'na'|'??'|...
BUG_TYPE ::= SEMANTIC|CONCURRENCY|MEMORY|ERRORCODE
SEMANTIC ::= 'hardware'|'softirq'|'migration'|'preempt'|'irq'|'na'|...
CONCURRENCY ::= 'atomicity'|'order'|'deadlock'|'livelock'|...
MEMORY ::= 'resource leak'|'uninit var'|'buf overflow'|...
ERRORCODE ::= 'compiling err'|'config err'|'runtime err'|'var type'|...
FIX_METHOD ::= 'hardware'|'lock'|'irq'|'preempt'|'migration'|'other'|...

PERFORMANCE ::= 'performance'::PERF_METHOD::DESCRIPT
PERF_METHOD ::= 'cache'|'msleep'|'softirq'|'barrier'|'idle'|'mm'|'hrtimer'|...

MAINTAIN ::='maintain'::MAINTAIN_METHOD
MAINTAIN_METHOD ::='refactor'|'donothing'|...
```

## bug related info
### bug consequence
- corrupt:: 系统破坏了保存的数据（主要与文件系统，存储系统相关）
- hang:: 系统长时间无反应
- deadlock::由于拥有资源且申请资源导致系统无法继续运行。死锁（deadlock）是无法解开的。scheduling in atomic, or nested lock
- livelock:: 如果事务T1封锁了数据R,事务T2又请求封锁R，于是T2等待。T3也请求封锁R，当T1释放了R上的封锁后，系统首先批准了T3的请求，T2仍然等待。然后T4又请求封锁R，当T3释放了R上的封锁之后，系统又批准了T的请求......T2可能永远等待，这就是活锁。活锁有一定几率解开。
- crash:: 系统崩溃，但没有破坏保存的数据， 比如有在log中有关键字 break machine, ARM, WARNING...
- leak:: 发生数据泄漏 
- data_err:: 数据处理/显示错误 （有warning信息也算）
- ctrl_err:: kernel thread, app can not run
- rtlatency:: unexpected realtime latencies
- irq/softirq:: not-irq/softirq-safe 无法响应/打开/关闭中断(包括nmi)，softirq执行延迟/挂起，产生大量irq,  导致系统工作不正确
- compile:: compiling/build error
- idle:: idle OR suspend/resume相关错误
- hwerr:: hardware malfunction. 硬件/外设/watchdog不能正常工作  e.g.  i386-pit-stop-only-when-in-periodic-or-oneshot-mode.patch
- na|??:: Not Available OR Not Applicable 无从得知或不适用


### bug type
#### semantics
- hardware:: 硬件初始化/工作流控制逻辑错误 
- time:: 时间处理相关的错误
_ err_access:: 用户态访问内核态等类似的程序访问错误，执行错误指令
- semantics:: 编程逻辑有误，对函数语义理解有误 
- na: Not Available OR Not Applicable 无从得知或不适用

* semantics+na 都可归于other类

#### concurrency
- migration:: 与线程/进程迁移处理中的错误
- preempt:: 与线程/进程能否抢占相关的错误
- sched:: 与线程/进程调度相关的错误 （主要集中在kernel/sched*.c）
- irq/softirq:: 与设置中断/软中断相关的错误 如 change die_chain from atomic to raw notifiers   atomic_notifier_call_chain --> raw_notifier_call_chain ???
- atomicity:临界区没有保护好/过度保护共享资源的互斥(mutex)访问. 
- order: 没有确保执行的顺序性(sync,barrier),或者barrier工作无效了。如  [2.6.24 - 2.6.26] rt: PI-workqueue: fix barriers
- deadlock: 形成了死锁   e.g. BUG: sleeping function called from invalid context at kernel/locking/rtmutex.c:914 |in_atomic(): 1, irqs_disabled(). 一个进程获得了spinlock之后它就进入了这里所谓的atomic context，或者是在一个irq-handler，也就是一个中断上下文中。这两种上下文中理论上不应该让当前的execution path进入sleep状态(虽然不是强制规定，换句话说，一个拥有spinlock的进程进入sleep并不必然意味着系统就一定会deadlock 等，但是对内核编程而言，还是应该尽力避开这个雷区)。
- livelock: 一个线程在不确定的长时间范围内得不到执行，导致活锁

* atomicity 在文中用mutual exclusive（mutex）表示更好，因为她主要表示共享数据/资源的mutex相关bug

#### memory
- resource_leak:: 资源/动态分配的内存没有释放
- uninit_var:: 资源/变量没有初始化
- typo_var:: 变量类型错误
- overflow::缓冲区溢出 OR 栈溢出 buf/stack overflow刘明明 <eva980636@126.com>, eva980636 <eva980636@163.com>

- err_var:: 数据处理/比较错误 use after free


#### error code
- compiling_err:: 编译错误
- config_err:: 配置错误
 
### fix method
- hardware:: 硬件相关的修复
- mutex:: 互斥相关的修复
- sync/order:: order OR 同步相关的修复
- irq/softirq:: 中断/软中断相关的修复 
- preempt:: 抢占相关的修复 如 handle accurate time keeping over long delays NEED TO READ， 修改方法之一：  用preempt_disable() friendly swork 代替work_struct 或 preempt_disable --> migration_disable
- migration:: 迁移相关的修复
- idle:: idle OR suspend/resume相关的修复
- memory:: type of var, init var, var<-->ptr  percpu var -->pertask var, use after free相关的修复
- sched:: 调度相关的修复（主要集中在kernel/sched*.c）
- config:: 修复config相关的bug，特别是直接!PREEMPT_RT_*的方式，在有rt的情况下，就不支持这个feature了
- syntax:: 修复编译语法错误
- runtime:: add might_sleep() function to find bug on os running.
- semantics:: 修复语义错误(修改代码，删除代码) 如  Don't call mcount from vsyscall_fn's OR PowerPC: remove broken vsyscall cod


## feature related info
### feature method
- hardware:: 添加/删除硬件相关特性
- debuginfo:: 添加/减少调试/warning信息
- idle:: 添加idle OR suspend/resume OR power management相关功能
- hrtimer:添加采用高精度时钟相关功能
- statistics:: 添加统计信息
- delay:: 添加workqueue/softirq相关功能
- sched:: 对调度的修改改进
- mm:: 对内存的修改改进
- hotplug:: 对hotplug的rt改进
- timer:: clock_event，time of day, 等与时钟通知机制有关的功能添加
- lockless:: 无锁设计
- capability:: 与rt相关的权限设置
- net:: 对net的修改（hash） inet_hash_bits.patch
- rtsupport:: 与rt相关的lock添加设计/回滚设计,包括 migration_eanble/disable, preempt_enable/disable, trylock, rcu, bh, sched, atomic op, anon sem, seqlock, get/put_cpu_light, local_lock...。也包括添加/减少 CONFIG等。对于这样的patch, 如果不这样实现，会出现rt错误，但并没有在log中说明有错误，所以归类为rtsupport  .  e.g.  preempt: rt no slub  swait_*
- check:: add runtime check to make it more stable/rt latency detect. e.g. hw_latency SMI detector
- arch:: add new architecture support for RT
- power:: 节能
- testcase:: e.g. v2.6.26-rwlock-torture.patch  add a kernel module to test rwlock
- other:: 不太好归类的， e.g. dont stop box in panic function 或 highmem: revert mainline 即恢复到mainline/upstream

## performance related info
### performance method
- hardware:: 硬件相关优化
- cache:: 优化cache访问
- msleep:: msleep优化
- irq/softirq:: irq/softirq相关优化
- mutex:: 与lock/mutex相关的优化，比如去掉多余的lock/unlock， 减少cirtical section的范围等
- preempt:: sched/preempt/rcu (also process preempt)相关的优化
- migration:: 与migration/load balance相关的优化
- barrier:: barrier相关优化
- idle:: 缩短idle OR suspend/resume时间的正确计算与优化
- hrtimer:采用高精度时钟的优化
- mm: memory management/kmem_cache相关优化
- percpu_var:: percpu var设计优化
- smallsize:: 减少不必要的代码执行/执行次数等，以优化执行时间
- config:: use config to disable some feature when enable preempt_rt_full

## maintain related info
### maintain method
- refactor:: 重构软件相关,包括调整位置，删除无用代码(unused code)
- donothing:: 什么也没做，包括增加注释、和修改文档或者增加文档。

### PATCH_CHANGES
```
      + [[file:2.6.22/new-softirq-code.patch][2.6.22]]  {MOD::KER_MOD}
      M [[file:2.6.23/new-softirq-code.patch][2.6.23]]
        [[file:2.6.24/new-softirq-code.patch][2.6.24]]
      M [[file:2.6.25/new-softirq-code.patch][2.6.25]]
        [[file:2.6.26/new-softirq-code.patch][2.6.26]]
      - 2.6.29

   Meaning of the first character:

      [+]        This patch is introduced in this version (not seen in previous ones).
      [-]        This patch appears in the previous version but disappears in this one.
      [ ]        This patch is seen in both the previous and current version.
                 This patch is identical in the two versions.
      [m]        This patch is seen in both the previous and current version.
                 The changed lines in the patches are identical, but the contexts are not.
      [M]        This patch is seen in both the previous and current version.
                 The changed lines in the patches are different.

      KER_MOD    The 1~2 level directories(means kernel modules) of kernel src code, such as  kernel, 
                 mm, fs, net, drivers/acpi, drivers, lib, include/linux ... 
```

### example
```
* [2.6.22         ] slob-scale-break-out-caches.patch {C::performance::cache::use kmem_cache,remove global slobfree}
  + [[file:2.6.22/slob-scale-break-out-caches.patch][2.6.22]]  {MOD::mm}
