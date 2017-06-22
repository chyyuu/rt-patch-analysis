6.22
-TODO
用busybox做了一个文件系统，不知道是不是提到的那个ubunturootfs
- 编译过程
```
    cd linux  
  //内核
    make   ARCH=x86_64 defconfig  
    make   ARCH=x86_64 -j10
    make   ARCH=x86_64 modules_install
    make   ARCH=x86_64 install

    cd ..
  //文件系统，busybox
    curl https://busybox.net/downloads/busybox-1.26.2.tar.bz2 | tar xjf -
    cd busybox-1.26.2
    make menuconfig
  //BusyboxSettings->Build options->Build Busybox as a static binary
    make
    cd ..
    dd if=/dev/zero of=rootfs.img bs=1M count=10
    mkfs.ext3 rootfs.img
    mkdir rootdisk
    mount -t ext3 -o loop rootfs.img rootdisk
    cd rootdisk 
    mkdir dev proc sys
    cd ..
    cd busybox
    make install CONFIG_PREFIX=..rootdisk

    cd ..
    umount rootdisk
    rmdir rootdisk

    qemu-system-x86_64 -enable-kvm -kernel fkroot/boot/vmlinuz-4.10.0-rc1-rt+ -hda rootfs.img -append "root=/dev/sda" -m 2048

```
早上爬起来之后运行了一下学长的脚本，loop出了些问题没解决，也没有按照当时讨论的说什么把XXX放在一个文件夹里，具体的我忘了
- 遇到的问题  
遇到了一次prepare3报错，```make distclean```解决
- 参考
	- http://blog.csdn.net/hejinjing_tom_com/article/details/46770559
	- https://github.com/chyyuu/rt-patch-analysis/blob/master/developers/mym/rt-linux-lkp.sh
	- https://www.linux.com/learn/kernel-newbie-corner-building-and-running-new-kernel
	- http://mgalgs.github.io/2015/05/16/how-to-build-a-custom-linux-kernel-for-qemu-2015-edition.html
