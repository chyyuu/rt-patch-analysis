# Preempt_RT patch 4.4.79 更新到 4.5.0 
记录了使用linux-4.4.79的Preempt_rt patch更新linux-4.5.0过程中出现的冲突和bug，对它们进行分析。

#### 1 /block/blk-iopoll.c 
错误信息：`Can't find file to patch. Skipping patch. 3 out of 3 hunks ignored.`

从[https://patchwork.kernel.org/patch/7611921/](https://patchwork.kernel.org/patch/7611921/)可以看出`block/blk-iopoll.c`被替换成了`lib/irq_poll.c`，目的是让这个机制更general的使用。但是给修改带来了**很大的隐患**，这个patch是在三个地方各增加一句`preempt_check_resched_rt()`，目前暂时将这个patch修改为在`lib/irq_poll.c`中对应的地方增加一句`preempt_check_resched_rt()`。

从`https://lwn.net/Articles/346187/`可以看到iopoll建立的初衷。

**具体的代码分析后面再补**

#### 2 /drivers/cpuidle/coupled.c
错误信息：`Reversed (or previously applied) patch detected! Skipping patch. 1 out of 1 hunk ignored.`

在Linux-4.5.0中，此处修改已经加入了kernel代码，不需要打patch。

#### 3 /kernel/sched/cputime.c
错误信息：`Reversed (or previously applied) patch detected! Skipping patch. 8 out of 8 hunks ignored.`

在Linux-4.5.0中，这个文件的几处修改都加入了kernel代码，不需要打patch。

#### 4 /fs/dcache.c
错误信息：`Hunk #3 FAILED.`

通过源代码的对比可以看出，在linux-4.5.0中，这要修改的这一段代码做了做了一些改动，要做一些分析。

![linux-4.4.79_fs:dcache_vs_linux-4.5.0_fs:dcache](https://github.com/lighttime0/pictures/blob/master/linux-4.4.79_fs:dcache_vs_linux-4.5.0_fs:dcache.png)

linux-4.4.79的代码中，在`kill_it`标签下多了一个cond_resched()函数，这个函数将调度一个新程序投入运行，但是它只有在设置完need_resched标志后，才能生效。也就是说，该方法有效的条件是系统中存在更重要的任务需要执行。

在linux-4.5.0中没有这个函数，直接删掉patch中这一行即可。

#### 5 /mm/filemap.c
错误信息：`Hunk #2 FAILED.`

在linux-4.5中，代码位置偏移较多，可能patch自动检测不到，手动修改下patch文件中的行数即可。

#### 6 /kernel/fork.c
错误信息：`Hunk #6 FAILED.`

在linux-4.5.0中，此处修改已加入kernel代码，不需要打patch。

#### 7 /kernel/futex.c
（1）`Hunk #3 FAILED.`
Hunk #3的修改在linux-4.5.0中已经加入kernel代码，不需要打patch。

（2）`Hunk #4 FAILED.`
Hunk #4中修改了7处，其中前6处在linux-4.5.0中已经加入kernel代码，不需要打patch。在patch文件中将前6处删掉，第7处单独列出来即可。

（3）`Hunk #7 FAILED.`
Hunk #7的修改在linux-4.5.0中已经加入kernel代码，不需要打patch。

#### 8 /drivers/gpu/drm/i915/i915_gem_shrinker.c
错误信息：`Hunk #1 FAILED.`

如下图，将patch文件中的old文件代码改一下即可。可能存在一些语义上的隐患，**留坑**。
![i915_gem_shrinker.c](https://github.com/lighttime0/pictures/blob/master/i915_gem_shrinker_c.png)

#### 9 /include/linux/init_task.h
错误信息：`Hunk #1 FAILED.`

Hunk #1有两处修改，第一处增加了一些代码，可以正常打上；但第二处在linux-4.5.0中加入了kernel代码，不需要打patch。所以直接在patch文件中将第二处修改删除。

#### 10 /arch/arm/Kconfig
错误信息：`Hunk #1 FAILED.`

kernel代码的差别和patch文件见下图。在linux-4.5.0中，此处的条件增加了`MMU`，具体的语义**先留个坑**，后面再填。patch文件的修改比较容易，把`MMU`加进去即可。
![arch/arm/Kconfig](https://github.com/lighttime0/pictures/blob/master/arch:arm:Kconfig.png)

#### 11 /mm/memcontrol.c
（1）`Hunk #6 FAILED.`

kernel代码有差别，如下图。但是patch文件修改的地方没差别，修改下patch文件的上下文就好，至于kernel代码的差别会不会需要其他的修改，就需要对语义的深入理解了，**留个坑先**。
![mm/memcontrol](https://github.com/lighttime0/pictures/blob/master/mm:memcontrol.png)

（2）`Hunk #7 FAILED.`

和Hunk #6类似的问题，kernel代码有区别，如下图。patch文件比较好改，但是同样的，kernel代码的差别会不会引起运行时的bug还需要更深入的分析。
![mm/memcontrol](https://github.com/lighttime0/pictures/blob/master/mm:memcontrol_Hunk%237.png)

（3）`Hunk #10 FAILED.`

和Hunk #6类似的问题，kernel代码有区别，如下图。这个地方代码变化比较多。所以在修改上暂时删除这一对`local_lock_irqsave`和`local_unlock_irqrestore`。
![mm/memcontrol](https://github.com/lighttime0/pictures/blob/master/mm:memcontrol_Hunk%2310.png)

#### 12 /arch/x86/kernel/nmi.c
错误信息：`Can't find file to patch. Skipping patch. 3 out of 3 hunks ignored.`

在Linux-4.5.0中，此处修改已经加入了kernel代码，不需要打patch。

#### 13 /drivers/net/wireless/orinoco/orinoco_usb.c
错误信息：`Can't find file to patch. Skipping patch. 1 out of 1 hunk ignored.`

在linux-4.5.0中，`/drivers/net/wireless/orinoco/`文件夹整体移动到了`/drivers/net/wireless/intersil/orinoco/`，orinoco_usb.c文件本身没改动，将patch中的文件位置修改一下即可。

#### 14 /mm/page_alloc.c
错误信息：`Hunk #6 FAILED.`

patch好修改，语义问题**留坑**。

#### 15 /kernel/panic.c
错误信息：`Hunk #2 FAILED.`
错误信息：`Hunk #3 FAILED.`

这两处修改在linux-4.5.0中已经加入kernel代码，不需要打这两个Hunk。

#### 16 /arch/x86/kernel/reboot.c
错误信息：`Can't find file to patch. Skipping patch. 3 out of 3 hunks ignored.`

前两个Hunk在linux-4.5.0已经加入到kernel代码中，不用patch。

第三个Hunk情况比较复杂。patch本来要增加一个在linux-4.4.79中没有的函数，linux-4.5.0中有这个函数，但是和patch中的该函数有些不同。暂时将linux-4.5.0中的这个函数改为patch中的代码，具体的语义**留坑，以后再看**。

#### 17 /kernel/locking/rtmutex.c
这个patch有60个Hunk FAILED。全部都是比较简单的问题，比如位置移动，或者有些改动已经加入kernel代码，手动改起来比较繁琐，但是没有语义上的问题，不会出现运行时的bug。

#### 18 /include/linux/sched.h
错误信息：`Hunk #8 FAILED.`

在Linux-4.5.0中，此处修改已经加入了kernel代码，不需要打patch。

#### 19 /kernel/stop_machine.c
错误信息：`Hunk #2 FAILED.`
错误信息：`Hunk #5 FAILED.`
错误信息：`Hunk #6 FAILED.`
错误信息：`Hunk #7 FAILED.`
错误信息：`Hunk #8 FAILED.`

语义都有些小隐患。**留坑**。

#### 20 /mm/swap.c
（1）错误信息：`Hunk #9 FAILED.`
    在linux-4.5.0中，Hunk #9的这两个函数中间加了一段代码，解决方法是将Hunk #9拆成两个Hunk。

（2）错误信息：`Hunk #10 FAILED.`
    linux-4.5.0在这处修改中增加了一个if的判断条件，可能存在一些语义上的隐患，**留坑**。
    
#### 21 /kernel/rcu/tree.c
错误信息：`Hunk #28 FAILED.`

linux-4.5.0在这里代码有些差别，可能存在一些语义上的隐患，**留坑**。

    
#### 22 /mm/truncate.c
错误信息：`Hunk #1 FAILED.`

linux-4.5.0中，这一大段代码前加了一个判断条件，可能存在语义上的隐患。 

#### 23 /drivers/hv/vmbus_drv.c
错误信息：`Hunk #1 FAILED.`

linux-4.5.0在这处修改上有一些代码变化，可能存在一些语义上的隐患，**留坑**。

#### 24 /drivers/media/platform/vsp1/vsp1_video.c
错误信息：`Can't find file to patch. Skipping patch. 1 out of 1 hunk ignored.`

在Linux-4.5.0中，此处修改已经加入了kernel代码，不需要打patch。

#### 25 /kernel/watchdog.c
错误信息：`Hunk #3 FAILED.`

Hunk #3的两处修改，一处已经加入到linux-4.5.0的代码中，另一处没有语义隐患。

