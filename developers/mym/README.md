your work

have finished  a script to auto download kernel sourcecode, compile kernel sourcecode 
install kernel vmlinuz and kernel module to  qemu_img disk. then boot the qemu_img disk use the new compiled kernel.


rt-linux-lkp.sh    https://github.com/chyyuu/linux-rt-devel.git  3ae7b241a0f49035e5b99b6b86c27fea5e49ef1c

需要传递两个参数GIT_URL和commitID



需要做的事情： 
1. 目前对于monitor部分的ftrace，需要把config中对应的内核的配置打开
1. 检查不同的内核版本使用什么版本的gcc
1. 检查不同的内核版本使用什么配置选项打开RT和把关心的KO编译到vmlinuz里面。
