# Preempt_RT patch 4.4.79 更新到 4.5.0 
记录了使用linux-4.4.79的Preempt_rt patch更新linux-4.5.0过程中出现的冲突和bug，对它们进行分析。

#### 1 /block/blk-iopoll.c

在linux-4.5.0中，找不到该文件。

从` https://patchwork.kernel.org/patch/7611921/ `可以看出iopoll被替换成了irq_poll。

从`https://lwn.net/Articles/346187/`可以看到iopoll建立的初衷。

#### 2 /drivers/cpuidle/coupled.c
在Linux-4.5.0中，此处修改已经加入了mainline，不需要打patch。

#### 3 /kernel/sched/cputime.c
在Linux-4.5.0中，这个文件的基础修改都加入了mainline，不需要打patch。

#### 4 /fs/dcache.c
patch failed.

通过源代码的对比可以看出，在linux-4.5中，这要修改的这一段代码做了做了一些改动，要做一些分析。



未完待续。。。

