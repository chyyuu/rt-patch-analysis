开会时间：2017.6.23

本周计划：一周以后（6月30号）能让lkp从代码更新到运行测试用例，整个流程能够运行起来。

1. 检测git更新触发后续动作 (张蔚负责）
   1.  能够检测https://github.com/chyyuu/linux.git上面的以rt结尾的分支的更新动作。传递git_url git_branch_name 参数到compile.sh脚本
   1.  可以测试git tree中指定的commit。传递git_url commitID 参数到compile.sh脚本（两种方案：通过配置文件或者队列来实现）


1. 编译代码（毛英明和杨兴杲负责）
   1.  需要挑选和下载3.x,4.x中各个版本的rt-linux patch，然后打patch形成完整版本的rt-linux
   1.  需要试一下各个版本的rt-linux需要使用什么版本的gcc和binutils编译。并且安装各个版本的gcc和binutils。
   1.  将编译脚本和git自动更新检测脚本接到一起。能够通过git_url和git_branch_name下载对应分支最新的代码
   1.  开始编译内核生成vmlinuz。并且调用lkp qemu  传递-kernel /path/to/vmlinuz   -initrd=/path/to/initrd-lkp.img -append "git_commitid  bencmark_name"  

>> chyyuu 基于 git://git.kernel.org/pub/scm/linux/kernel/git/rt/linux-rt-devel.git 中的rt-liux branch即可，不用挑选下载3.x,4.x的patch。且从高版本到低版本一个一个实验。

1. 分支(版本）名字和编译规则的映射关系（毛英明和杨兴杲负责，茅俊杰提供帮助）
   1.  根据commit能够查询到brantch或者tagname从而知道其对应的内核版本
   1.  知道该使用哪个版本的gcc和binutils编译代码
   1.  知道该使用什么.config文件(config文件中需要打开RT相关选项，并且将需要的内核ko编译进vmlinuz，从而不需要考虑ko文件安装的事情）

1. lkp qemu测试（肖络元主要负责）
   1.  利用lkp运行rtlinux的cycletest测试用例
   1.  原本计划使用基于ubuntu的虚拟磁盘rootfs，在虚拟磁盘中运行rt-linux内核和lkp的全部代码（包括rt相关benchmark），这样的方式虚拟磁盘体积比较大。
   1.  肖络元和茅俊杰建议：使用lkp qemu命令，比较方便：
   1.  不使用虚拟磁盘rootfs，而是将lkp测试用例封装到initrd.img文件(initrd-lkp.img)中。
   1.  将内核版本的commit和需要测试的benchmakr_name通过-append传递给lkp
   1.  毛英明和肖络元约定-append传递参数问题。

1. 后续计划： patch的人工分析和归类


