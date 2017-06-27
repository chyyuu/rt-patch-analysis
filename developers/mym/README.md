your work

have finished  a script to auto download kernel sourcecode, compile kernel sourcecode 
install kernel vmlinuz and kernel module to  qemu_img disk. then boot the qemu_img disk use the new compiled kernel.


rt-linux-lkp.sh    https://github.com/chyyuu/linux-rt-devel.git  3ae7b241a0f49035e5b99b6b86c27fea5e49ef1c

需要传递两个参数GIT_URL和commitID



需要做的事情： 
1. 目前对于monitor部分的ftrace，需要把config中对应的内核的配置打开
1. 检查不同的内核版本使用什么版本的gcc
1. 检查不同的内核版本使用什么配置选项打开RT和把关心的KO编译到vmlinuz里面。

````
修改
build_bat.sh
其中每行第一列表示GIT_URL  第2列表上GIT_COMMITID或者tagname或者branch_name(不推荐)

然后运行
./build_bat.sh即可批量测试指定版本的内核。

其中
./build/${GIT_REPO_NAME}/
表示内核源代码目录
./build/${GIT_REPO_NAME}/${commitID/tagname}/ 
表示编译的中间结果。

./build/${GIT_REPO_NAME}/${commitID/tagname}/make.log
表示编译日志

./build/${GIT_REPO_NAME}/${commitID/tagname}/boot_run_log.txt
表示QEMU启动内核的运行日志（输出了当前的内核版本号）如果在boot_run_log.txt中能够看到内核版本号码，说明编译、运行都正确。

e.g
 ./linux-rt-devel/
./build/linux-rt-devel/v4.9-rt1/
./build/linux-rt-devel/v4.9-rt1/make.log
./build/linux-rt-devel/v4.9-rt1/boot_run_log.txt 
```
