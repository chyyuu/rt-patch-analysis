## history format
```
PATCH_ITEM ::= * VERSIONS  PATCH_TITLE {CHARACTERISTIC::ASPECT} \n PATCH_CHANGS
VERSIONS ::= '['BEGIN_VERSION - END_VERSION']'|'['BEGIN_VERSION']'
BEGIN_VERSION|END_VERSION ::= [2..4].[0..18].[22..29]
PATCH_TITLE ::= TITLE.patch 
TITLE|DESCRIPT = ['a'..'z','A'..'Z']*|NULL //string or nothing
CHARACTERISTIC ::='C'
ASPECT ::= FEATURE|FIXBUG|PERFORMANCE|MAINTAIN
FEATURE ::= 'feature'::TITLE[::DESCRIPT]
FIXBUG ::= 'fixbug'::BUG_CONCREQUENCE::BUG_TYPE::FIX_METHOD [DESCRIPT]
BUG_CONSEQUENCE ::='corrupt'|'hang'|'crash'|'leak'|'irq'|'livelock'|'??'|...

BUG_TYPE ::= SEMANTIC|CONCURRENCY|MEMORY|ERRORCODE
SEMANTIC ::= 'hardware'|'softirq'|'migration'|'preempt'|'irq'|...
CONCURRENCY ::= 'atomicity'|'order'|'deadlock'|'livelock'|...
MEMORY ::= 'resource leak'|'uninit var'|'buf overflow'|...
ERRORCODE ::= 'compiling err'|'config err'|'runtime err'|'var type'|...
FIX_METHOD ::= 'hardware'|'lock'|'irq'|'preempt'|'migration'|'other'|...
PERFORMANCE ::= 'performance'::PERF_METHOD::DESCRIPT
PERF_METHOD ::= 'cache'|'msleep'|'softirq'|     ...
MAINTAIN ::='maintain'::MAINTAIN_METHOD
```

### bug consequence
- corrupt:: 系统破坏了保存的数据（主要与文件系统，存储系统相关）
- hang:: 系统长时间无反应
- deadlock::由于拥有资源且申请资源导致系统无法继续运行。死锁（deadlock）是无法解开的。
- livelock:: 如果事务T1封锁了数据R,事务T2又请求封锁R，于是T2等待。T3也请求封锁R，当T1释放了R上的封锁后，系统首先批准了T3的请求，T2仍然等待。然后T4又请求封锁R，当T3释放了R上的封锁之后，系统又批准了T的请求......T2可能永远等待，这就是活锁。活锁有一定几率解开。
- crash:: 系统崩溃，但没有破坏保存的数据
- leak:: 发生数据泄漏
- irq:: 无法响应/打开/关闭中断，导致系统工作不正确


### bug type
#### semantic
- hardware:: 硬件初始化/工作流控制逻辑错误
- softirq:: 在软中断工作范围内出现的错误
- migration:: 与线程/进程迁移处理中的错误
- preempt:: 与线程/进程能否抢占相关的错误
- irq:: 与设置中断相关的错误

#### concurrency
- atomicity:临界区没有保护好共享资源的互斥(mutex)访问
- order: 没有确保执行的顺序性(sync)
- deadlock: 形成了死锁
- livelock: 形成了活锁

#### memory
- resource leak:: 资源/动态分配的内存没有释放
- uninit var:: 资源/变量没有初始化
- buf overflow::缓冲区溢出

#### error code
- compiling err:: 编译错误
- config err:: 配置错误
 
### fix method
- hardware'|'lock'|'irq'|'preempt'|'migration

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
