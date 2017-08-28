# Preempt_RT patch 4.4.79 更新到 4.5.0 
记录了使用linux-4.4.79的Preempt_rt patch更新linux-4.5.0过程中出现的冲突和bug，对它们进行分析。

#### 1 /block/blk-iopoll.c
在linux-4.5.0中，找不到该文件。

从` https://patchwork.kernel.org/patch/7611921/ `可以看出iopoll被替换成了irq_poll。

从`https://lwn.net/Articles/346187/`可以看到iopoll建立的初衷。

**具体的代码分析后面再补**

#### 2 /drivers/cpuidle/coupled.c
在Linux-4.5.0中，此处修改已经加入了kernel代码，不需要打patch。

#### 3 /kernel/sched/cputime.c
在Linux-4.5.0中，这个文件的基础修改都加入了kernel代码，不需要打patch。

#### 4 /fs/dcache.c
patch failed.

通过源代码的对比可以看出，在linux-4.5中，这要修改的这一段代码做了做了一些改动，要做一些分析。

![linux-4.4.79_fs:dcache_vs_linux-4.5.0_fs:dcache](https://github.com/lighttime0/pictures/blob/master/linux-4.4.79_fs:dcache_vs_linux-4.5.0_fs:dcache.png)

linux-4.4.79的代码中，在`kill_it`标签下多了一个cond_resched()函数，这个函数将调度一个新程序投入运行，但是它只有在设置完need_resched标志后，才能生效。也就是说，该方法有效的条件是系统中存在更重要的任务需要执行。

在linux-4.5中没有这个函数，直接删掉patch中这一行即可。

#### 5 /mm/filemap.c
patch failed.

在linux-4.5中，代码位置偏移较多，可能patch自动检测不到，手动修改下patch文件中的行数即可。

#### 6 /kernel/fork.c
patch failed.

在linux-4.5中，此处修改已加入kernel代码，不需要打patch。

#### 7 /kernel/futex.c
（1）Hunk #3 FAILED.
Hunk #3的修改在linux-4.5.0中已经加入kernel代码，不需要打patch。

（2）Hunk #4 FAILED.
Hunk #4中修改了7处，其中前6处在linux-4.5.0中已经加入kernel代码，不需要打patch。在patch文件中将前6处删掉，第7处单独列出来即可。

（3）Hunk #7 FAILED.
Hunk #7的修改在linux-4.5.0中已经加入kernel代码，不需要打patch。

#### 8 /drivers/gpu/drm/i915/i915_gem_shrinker.c
Hunk #1 FAILED.

如下图，将patch文件中的old文件代码改一下即可。
![i915_gem_shrinker.c](https://github.com/lighttime0/pictures/blob/master/i915_gem_shrinker_c.png)

#### 9 /include/linux/init_task.h
Hunk #1 FAILED.

Hunk #1有两处修改，第一处增加了一些代码，可以正常打上；但第二处在linux-4.5.0中加入了kernel代码，不需要打patch。所以直接在patch文件中将第二处修改删除。

#### 10 /arch/arm/Kconfig
Hunk #1 FAILED.

kernel代码的差别和patch文件见下图。在linux-4.5中，此处的条件增加了`MMU`，具体的用法**先留个坑**，后面再填。patch文件的修改比较容易，把`MMU`加进去即可。
![arch/arm/Kconfig](https://github.com/lighttime0/pictures/blob/master/arch:arm:Kconfig.png)

#### 11 /mm/memcontrol.c
（1）Hunk #6 FAILED.

kernel代码有差别，如下图。但是patch文件修改的地方没差别，修改下patch文件的上下文就好，至于kernel代码的差别会不会需要其他的修改，就需要对语义的深入理解了，**留个坑先**。
![mm/memcontrol](https://github.com/lighttime0/pictures/blob/master/mm:memcontrol.png)

（2）Hunk #7 FAILED.

和Hunk #6类似的问题，kernel代码有区别，如下图。patch文件比较好改，但是同样的，kernel代码的差别会不会引起运行时的bug还需要更深入的分析。
![mm/memcontrol](https://github.com/lighttime0/pictures/blob/master/mm:memcontrol_Hunk#7.png)

（3）Hunk #10 FAILED.

和Hunk #6类似的问题，kernel代码有区别，如下图。patch文件比较好改，但是同样的，kernel代码的差别会不会引起运行时的bug还需要更深入的分析。
![mm/memcontrol](https://github.com/lighttime0/pictures/blob/master/mm:memcontrol_Hunk#10.png)

#### 12 /arch/x86/kernel/nmi.c
在Linux-4.5.0中，此处修改已经加入了kernel代码，不需要打patch。

#### 13 /drivers/net/wireless/orinoco/orinoco_usb.c
can't find file to patch.

在linux-4.5.0中，`/drivers/net/wireless/orinoco/`文件夹整体移动到了`/drivers/net/wireless/intersil/orinoco/`，orinoco_usb.c文件本身没改动，将patch中的文件位置修改一下即可。

#### 14 /mm/page_alloc.c
Hunk #6 FAILED.

Hunk #6有两处修改，第一处修改已经加入kernel代码，将该Hunk的第一处修改删去即可。




