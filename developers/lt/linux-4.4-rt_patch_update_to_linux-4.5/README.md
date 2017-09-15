# README

###项目说明

​	使用Linux-4.4.79-rt92.patch更新Linux-4.5.0。Porting后的代码放在github上了：[https://github.com/chyyuu/linux/tree/v4.5-rt](https://github.com/chyyuu/linux/tree/v4.5-rt)。

###项目进度

[*]	手动更改好patch；

[*]	处理编译过程中的bug；

[*]	本机测试bzImage，在KVM中运行到shell；

[*]	192.168.0.127服务器，进行rt-linux-lkp测试。

###文件说明

​	patch_log.txt：将patch打到kernel代码上时的信息。

​	patch_rej：打patch时出现冲突的Hunk。

​	patch-4.4.79-rt92.patch：patch文件

​	patch-4.4.79-rt92_after_change.patch：手动修改了冲突之后的patch。

​	Preempt_RT patch 4.4.79 更新到 4.5.0.md：自己对出现冲突的Hunk做的分析，未完待续。

###关键操作命令

（1）打patch：`patch -Np1 --ignore-whitespace -F3 < ../patch-4.4.79-rt92.patch`

（2）编译内核：

```
make defconfig
make menuconfig
# Processor type and features  --->
#     Preemption Model (Voluntary Kernel Preemption (Desktop))  --->
#     ( ) Fully Preemptible Kernel (RT)
make -j4
```

（3）本机测试bzImage
    下载initrd：`wget http://boot.ipxe.org/demo/initrd.img`；
    启动内核：
    
    ​```
    qemu-system-x86_64 -kernel arch/x86_64/boot/bzImage -initrd initrd.img -serial stdio -append "root=/dev/ram0 console=ttyAMA0  console=ttyS0"
     ```

（4）服务器端测试

​	首先上传porting后的代码到github；

​	然后在实验室的192.168.0.127服务器上修改配置文件后，运行rt-linux-lkp测试，结果放在[服务器端rt-linux-lkp测试结果](https://github.com/chyyuu/rt-patch-analysis/blob/master/developers/lt/linux-4.4-rt_patch_update_to_linux-4.5/服务器端rt-linux-lkp测试结果.md)。

​	rt-linux的porting没有完备性的证明，测试结果也表明，在一些架构的某些Kconfig配置情况下会有编译错误，包括x86架构下的某些配置。

