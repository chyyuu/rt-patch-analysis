## 开会时间：2017.7.22
与毛英明，肖络元，杨兴杲交流
1 肖络元可以在qemu上运行git pull+compile+run，也可在物理机器上运行，但无法通过host 把内核传到target，并把log放到host中
2 初步完成了2.6.22的rt-patch分析，形成history.org， history-format.md文档。杨兴杲，毛英明等需要进一步分析
3 张蔚在茅俊杰指导下完成了org-check, org-merge的脚本，方便了我们的分析。
4 2017.7.22～23在微信群中加入了各位kernel hacker和爱好者，希望得到大家的帮助并进行充分的交流。

下周将让多个学生分工分析和理解其余的rt-patch.

## 开会时间：2017.6.23

本周计划：一周以后（6月30号）能让lkp从代码更新到运行测试用例，整个流程能够运行起来。

1. 检测git更新触发后续动作 (张蔚负责）
   1.  能够检测https://github.com/chyyuu/linux.git上面的以rt结尾的分支的更新动作。传递git_url git_branch_name 参数到compile.sh脚本
   1.  可以测试git tree中指定的commit。传递git_url commitID 参数到compile.sh脚本（两种方案：通过配置文件或者队列来实现）


2. 编译代码（毛英明和杨兴杲负责）
   1.  需要挑选和下载3.x,4.x中各个版本的rt-linux patch，然后打patch形成完整版本的rt-linux
   1.  需要试一下各个版本的rt-linux需要使用什么版本的gcc和binutils编译。并且安装各个版本的gcc和binutils。
   1.  将编译脚本和git自动更新检测脚本接到一起。能够通过git_url和git_branch_name下载对应分支最新的代码
   1.  开始编译内核生成vmlinuz。并且调用lkp qemu  传递-kernel /path/to/vmlinuz   -initrd=/path/to/initrd-lkp.img -append "git_commitid  bencmark_name"  

>> chyyuu 基于 git://git.kernel.org/pub/scm/linux/kernel/git/rt/linux-rt-devel.git 中的rt-liux branch即可，不用挑选下载3.x,4.x的patch。且从高版本到低版本一个一个实验。

3. 分支(版本）名字和编译规则的映射关系（毛英明和杨兴杲负责，茅俊杰提供帮助）

   1.  根据commit能够查询到brantch或者tagname从而知道其对应的内核版本
   1.  知道该使用哪个版本的gcc和binutils编译代码
   1.  知道该使用什么.config文件(config文件中需要打开RT相关选项，并且将需要的内核ko编译进vmlinuz，从而不需要考虑ko文件安装的事情）

4. lkp qemu测试（肖络元主要负责）

   1.  利用lkp运行rtlinux的cycletest测试用例
   1.  原本计划使用基于ubuntu的虚拟磁盘rootfs，在虚拟磁盘中运行rt-linux内核和lkp的全部代码（包括rt相关benchmark），这样的方式虚拟磁盘体积比较大。
   1.  肖络元和茅俊杰建议：使用lkp qemu命令，比较方便：
   1.  不使用虚拟磁盘rootfs，而是将lkp测试用例封装到initrd.img文件(initrd-lkp.img)中。
   1.  将内核版本的commit和需要测试的benchmakr_name通过-append传递给lkp
   1.  毛英明和肖络元约定-append传递参数问题。

5. 后续计划： patch的人工分析和归类


## 开会时间：2017.6.28

LKP RTLINUX测试部分：
1. git update test，不能只focus github，需要能对任何git都能检测。最好使用已有的代码实现。（参考茅俊杰和肖络元之前写的代码）
1. 需要在真实系统上面利用LKP测试一下，RTLINUX的性能，写程序能够分析出测试结果中比较大的差异，如果问题搞不明白可以跟吴峰光发邮件寻求帮助。（肖络元主要负责，毛英明提供帮助）
1. SMI会影响实时性，可以通过hwlat detecter来检查SMI是否产生了干扰，如果是的关闭SMI 
1. GPU driver里面的阻塞函数可能会影响实时性，用户态的图形应用程序，可能会触发gpu dirver的执行，导致影响实时性。后续可以测试一下opengl和mesa应用。

inside the RTpatch的学习记录：
1. kernel config里面提供了不同程度的抢占级别。不同时间的抢占，和不同地点的抢占。
   1.  3个层次：关中断，关闭抢占，关闭进程迁移
1. 需要看一下might_sleep的源代码实现，在原子操作里面是不允许调用might_sleep的（会发生睡眠和进程切换，破坏原子操作)
   1.  但是存在一个疑问？（原子操作不就是临界区里面的代码吗？其不是已经有锁来保护了吗？即使发生了进程切换，其他进程仍然不能获得锁，依然无法执行临界区里面的内容啊？）

1. RTLINUX补丁，会将一部分spinlock（自旋锁）替换成了mutex_lock（睡眠锁），如果想继续使用自旋锁需要使用raw_spin_lock
   1.  但是不是所有原来使用spinlock的地方都可以换成mutex_lock，例如使用了percpu变量的进程，使用了mutex_lock会被迁移到别的进程上面去执行，这个时候percpu变量会出错。

1. get_cpu不会抢占，不会进程迁移。get_cpu_light会抢占，但是不允许进程迁移

1. IRQ_NO_THREAD的中断例程里面不可以调用spin_lock（语义已经被替换为了mutex_lcok)会导致睡眠。如果driver里面的ISR例程，想要实现IRQ_THREAD,需要将原来使用spin_lock的地方，替换为raw_spin_lock。

1. 查一下：in atomic path到底是什么意思？
1. 查一下：PREEMPT_COUNT 实现机制。


## 2017.7.24 patch分析分工
```
2.6.23 patch number:  zw
397
2.6.24 patch number:  mym
484
2.6.25 patch number:  yxg
369
2.6.26 patch number:  zzm
403
2.6.29 patch number:  zw
267
3.0 patch number:     mym
235
3.10 patch number:   yxg
276
3.12 patch number:    zzm
281
3.14 patch number:    zw
314
3.18 patch number:   mym
311
3.2 patch number:   yxg
250
3.4 patch number:   zzm
245
3.6 patch number:  zw
254
3.8 patch number:   mym
283
4.0 patch number:  yxg
346
4.1 patch number:   zzm
267
4.11 patch number:  zw
388
4.4 patch number:  mym
256
4.6 patch number:   yxg
286
4.8 patch number:   zzm
291
4.9 patch number:    yxg
288
```
