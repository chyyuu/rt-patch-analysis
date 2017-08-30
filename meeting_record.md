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


## 2017.7.24 patch analysis job alloct
```
各个版本的patch数量
~/kernel-test/rt-patch-analysis/developers/chy$ grep "^* \[" ./history.org  | cut -b 1-9 | uniq -c
    374 * [2.6.22
    120 * [2.6.23
    126 * [2.6.24
     47 * [2.6.25
     92 * [2.6.26
     92 * [2.6.29
    217 * [   3.0
     76 * [   3.2
     19 * [   3.4
     30 * [   3.6
     51 * [   3.8
     28 * [  3.10
     21 * [  3.12
     47 * [  3.14
     19 * [  3.18
     47 * [   4.0
     10 * [   4.1
     16 * [   4.4
     41 * [   4.6
     22 * [   4.8
     17 * [   4.9
    114 * [  4.11

总共patch数量	
~/kernel-test/rt-patch-analysis/developers/chy$ grep "^* \[" ./history.org  | cut -b 1-9 | wc -l
1626
一共有1626个ptach



1626-374=1252 还剩1252个patch没有看
1252/4=313	 每人大概看313个

任务分工情况
    120 * [2.6.23 zw
    126 * [2.6.24 zw
     47 * [2.6.25 zw
     92 * [2.6.26 mym
     92 * [2.6.29 mym
    217 * [   3.0 yxg
     76 * [   3.2 yxg
     19 * [   3.4 yxg
     30 * [   3.6 yxg
     51 * [   3.8 mym
     28 * [  3.10 mym 
     21 * [  3.12 mym
     47 * [  3.14 mym
     19 * [  3.18 zzm
     47 * [   4.0 zzm
     10 * [   4.1 zzm
     16 * [   4.4 zzm
     41 * [   4.6 zzm
     22 * [   4.8 zzm
     17 * [   4.9 zzm
    114 * [  4.11 zzm

zw:293
mym:331
yxg:342
zzm:286
```

## 2017.8.7 rt patches analysis

### zw 重复度
#### 分析重复度

简述分析patch重复度的方法（即如何根据位于24个版本的9k个rt patch形成 history.org的）

需要分析出这些patchs中相同的部分，形成实际的patch重复度分析图

patch的重复度：

x axis:  重复出现数（）

y axis:  patch 个数

比如 x=2, y=59 表示只出现了2次(4.1, 4.2 OR 4.9,4.11)的patch个数为59个

并对此图进行分析，给出对此图的个人理解/观点

#### 形成不同版本的patch独特度的分析图

x axis:  kernel 版本号

y axis:  只在这个版本才出现的patch 个数

并对此图进行分析，给出对此图的个人理解/观点



#### 分析rt patch中修改的文件在内核源码中的分布，即分析 kernel componenet(基于 kernel src目录)的分布情况图

x axis:  内核的目录（arch,drivers+sound, fs, net, mm, kernel+init, block, ipc, other(include+lib+crypto +virt )）

y axis:  只在这个目录下才出现的patch中位于x标识的目录中的修改的文件个数

并对此图进行分析，给出对此图的个人理解/观点


为了形成第三个图，需要生成更加完整的history.org . 应该用你的detect-modules.py就可以了。

然后在用gnuplot or matlab等你顺手的工具形成图。

### yxg  patch type

We classify patches into four categories (Table 1): bug fixes (bug), performance improvements (performance),  new features (feature), and maintenance and refactoring (maintenance). Each patch usually belongs to a single category.

#### 1 Table 1: Patch Type. This table describes the classification and definition of RT patches.

raw : TYPE  ,  DESCRIPTION

column:

#### 2 Figure X patch type

shows the number and relative percentages of patch types for each rt-linux. Note that even though
rt-linux exhibit significantly different levels of patch activity (shown by the total number of patches), the percentage breakdowns of patch types are relatively similar.

x axis:  内核版本号

y axis:  不同type的patchs的百分比，顶部是这个内核版本的patch个数
并对此图进行分析，给出对此图的个人理解/观点

#### 3 Figure X Bug patches

x axis:  内核版本号

y axis:  不同type的bug patchs的百分比，顶部是这个内核版本的bug patch的个数

挑选数量最多的4 or 5类bug patch，其他的用 other 表示
并对此图进行分析，给出对此图的个人理解/观点
#### 4 Figure X performance patches

x axis:  内核版本号

y axis:  不同type的perf patchs的百分比，顶部是这个内核版本的perf patch的个数

挑选数量最多的4 or 5类perf patch，其他的用 other 表示
并对此图进行分析，给出对此图的个人理解/观点
#### 5 Figure X  feature patches

x axis:  内核版本号

y axis:  不同type的feature patchs的百分比，顶部是这个内核版本的feature patch的个数

挑选数量最多的4 or 5类feature patch，其他的用 other 表示
并对此图进行分析，给出对此图的个人理解/观点


### zzm Patch Size

Patch size is one approximate way to quantify the complexity of a patch, and is defined here as the sum of linesof added and deleted by a patch. Figure X displays the size distribution of bug, performance, maintain, and feature patches. Most bug patches are small; XX% are less than 10 lines of code. However,  feature patches are significantly larger than other patch types. Over XX% of these patches have more than 100 lines of code; XX% have over 1000 lines of code.

#### 1 Figure X: Patch Size.

This figure shows the size distribution for different patch types (bug, performance, maintain, and feature), in terms of lines of modifications.

x axis:  Lines of modified Code  标注点：1, 10, 100, 1000, 1000

y axis:  4 types的patchs的百分比 标注点：0.0, 0.2, 0.4, 0.6, 0.8, 1.0

## 2017.8.9 rt-questions
```
https://github.com/chyyuu/rt-patch-analysis/blob/master/developers/chy/rt-questions.txt

yxg 
Q1  3
Q2  2
Q3  4

zzm
Q4  2
Q5  6
Q12 1

zw
Q6  5
Q7  2
Q8  2

mym
Q9  7
Q10 1
Q11 1

help info
grep -w -E "migrate_disable|migrate_enable" ./* -Rn

make O=../v4.11.5-rt1/ CFLAGS_KERNEL=-g3 ./kernel/locking/rtmutex.i

https://github.com/chyyuu/rt-patch-analysis/blob/master/rt-linux-lkp/how_to_get_compile_rt_linux_kernel.txt

```

## 2017.8.15 rt-bug-analysis
```
## semantics
- migration 14   yxg
- preempt   29   zzm
- sched     10   zw
- irq/softirq 57+7  mym

## concurrency
- atomicity: 43  yxg
- order:     17  zzm
- deadlock:  67  zw
- livelock:  10  mym


yxg:57
zzm:46
zw:77
mym:74


grep -A 1 -E "C::bug::[^:]*::irq::" ./history.org  >bug_irq.txt


grep  -E  "C::bug::[^:]*::irq::"  ./history.org  | wc -l


"C::bug::[^:]*::irq::"
"C::bug::[^:]*::softirq::"
"C::bug::[^:]*::livelock::"

"C::bug::[^:]*::migration::"
"C::bug::[^:]*::preempt::"
"C::bug::[^:]*::sched::"
"C::bug::[^:]*::atomicity::"
"C::bug::[^:]*::order::"
"C::bug::[^:]*::deadlock::"
```
## 2017.8.18 job_to_do
1. 毛英明  
接下来需要细化相关内容。
请把你的分析的api进行进一步整理
   1.  是完善 chy/api-analysis.md ，把没有添加的api添加到表格中，并填写相关属性。
   1.  建立api的调用关系层次结构，可以形成一个格（lattice）结构；
   1.  茅俊杰生成了一个api替换表，请理解在什么情况下某些api要换成另外一些api， 
   1.  建立api的使用pattern，比如对于per_cpu var，大致的访问patter是...，对于global var,大致的访问pattern是...。（可基于前面同学的api分析）
1. 张之敏 
接下来需要细化对bug的分析内容，请也看看其他同学（包括我修改的）bug分析内容，进一步总结其中的bug pattern。
请注意 chy/api-analysis.md中列出的属性来进行归类总结，考虑为了在critical section（分为 per cpu var, global var, 
might_sleep等情况）中进行正确且实时性高的保护，应该如何设置lock/unclok (有各种变种)，写critical section需要关注的点是啥？

1. 张蔚 
 我们已经发现might_sleep类的bug是最多的，但内核中其实还有大量调用了might_sleep的函数，比如linux 4.11 with preempt-rt 
大约有372个调用了might_sleep的函数，我们能否用某种方法（也许基于call graph等方法）可以找到类似的新的bug？建议用比较轻量和准确的静态分析方法。

1. 杨兴杲  
 继续抓紧完成还没有完成的分析工作

1. 肖络元
 请把preempt-rt的kvm实验环境在实验室搭好，便于下周同学们可以进行编译rt kernel，并进行动态测试。

1. 陈老师
 开始修改和写技术报告，有问题随时交流。


## 2017.8.24 some_questions
 我们看到有一类bug（数量不少）与might_sleep相关。请思考问题 
*   问题1：对于直接或间接调用了might_sleep的函数有何特点？为何要在这些函数中调用might_sleep? 如果不调用，会如何？在Kernel没有config  hacking的情况下，其实might_sleep是空函数。 

*   问题2：preempt中的另外一类bug是order, deadlock, livelock，它们有何特点？是否有一些共性的特征？

*   问题3：对于内核中的Preempt_RT开发，特别是使用相关的RT API，是否有一些比较好的API usage rule/pattern，可保证没有bug的情况下，还有RT性能。 

*   希望晚上大家就此思考和讨论一下。当然，不限于这些问题。

## 2017.8.24 交流记录
1. might_sleep这个API的问题，它的语义是什么。
 
1. performance和feature的区别。 patch的分类需要一些调整。
   其中fix methord里面属于semantic的类型很多，需要再分。可以看看推荐的文献里面分类是怎么分的。

    
1. 关于互斥和原子类型的bug，有可能会用到多种方式（API）来保护一个percpu变量。   
   例如使用migrate_disable和local_lock组合来保护一个percpu变量。其中local_lock里面的锁的
   来说还是一个per_cpu类型的变量。
1. 关于同步、order类型的bug。分析一下rt kernel里常用哪种发式来实现同步？是否有找到了livelock问题(ABBA) 
```
   lockdep 是一种死锁检测机制
   while(1)
   {
    cpu_chill()/cpu_relax();
	if(condition)
	  break;
   }
   上面的代码是一种同步形式。
    有一个order类型的bug。
   [  3.14 -   4.11] net: sched: Use msleep() instead of yield(){C::bug::deadlock::deadlock::semantics::sched: Use msleep() instead of yield()}
  + [[file:3.14/net-sched-dev_deactivate_many-use-msleep-1-instead-o.patch][3.14]]
```
1. 使用rt kernel内核编程的时候，会有什么类型的编程错误，例如cpuhotplug部分支持的不太好。
   写内核模块，或者升级的时候，是否会出现内核编程错误。
    当vanilla打上rt patch以后，内核的驱动需要改吗?
    linux desktop换上rt kernel是否可以继续运行?
	可以升级一下内核看看会碰到什么问题（例如4.9升级到4.10或者4.11升级到4.12，总结过程中的错误）
1. 如何从静态的call graph里面找到一些错误的函数调用路径（例如preempt_disable, might_sleep, preempt_enable)
    矛俊杰建议可以采用给每个statment着色的方法(preempt_disable开始，以后开始着色，然后找了preempt_enable以后停止着色）
    还可以看哪些函数调用了might_sleep，然后再看第2级调用了might_sleep的函数，倒着推（好像是这样，没有记清楚）	

## 2017.8.26 rt内核版本升级
```
4.2 yxg
4.3 mym
4.5 lt
4.7 zzm
4.12 zw
```
