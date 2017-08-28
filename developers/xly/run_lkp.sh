#!/bin/bash

#Jobs:ebizzy cyclictest

if [ $# -lt 4 ]; then
	echo -e "Usage: $0 kernel commit modules job job job ..."
	echo -e "\t$0 boot/vmlinuz-4.8.0-58-generic 5218ea982c5d78259175b4ec3737d80fa68444f0 boot/modules.tar.gz ebizzy cyclictest "
	exit
fi

root_img="ubuntu-16.04.2-amd64.img"
kernel_img="boot/vmlinuz-4.8.0-58-generic"
initrd_img="boot/initrd.img-4.8.0-58-generic"

result_root="/result/QEMU"

jobs=""
argc=1
for i in $@
do
	if   [ $argc -eq 1 ];then
	kernel_img=$i
	elif [ $argc -eq 2 ];then
	commit_id=$i
	elif [ $argc -eq 3 ];then
	modules_img=$i
	else
	jobs="$jobs,$i"
	fi

	let argc++
done
echo -e "\033[32mJobs: $jobs\033[0m"

qemu-system-x86_64 -enable-kvm -m 3G -nographic \
-fsdev local,id=test_dev,path=$result_root,security_model=none \
-device virtio-9p-pci,fsdev=test_dev,mount_tag=9p/virtfs_mount \
-kernel $kernel_img \
-initrd $initrd_img \
-append "root=/dev/sda1 ro text user=lkp job=$jobs ARCH=x86_64 kconfig=x86_64-rhel branch=master commit=$commit_id BOOT_IMAGE=$kernel_img max_uptime=3300 RESULT_ROOT=$result_root LKP_SERVER=localhost earlyprintk=ttyS0,115200 systemd.log_level=err debug apic=debug sysrq_always_enabled rcupdate.rcu_cpu_stall_timeout=100 panic=-1 softlockup_panic=1 nmi_watchdog=panic oops=panic load_ramdisk=2 prompt_ramdisk=0 console=ttyS0,115200 vga=normal ip=dhcp result_service=9p/virtfs_mount" \
-hda $root_img \
-no-reboot -watchdog i6300esb -rtc base=localtime -device e1000,netdev=net0 -netdev user,id=net0 


#qemu-system-x86_64 -enable-kvm -fsdev local,id=test_dev,path=/result/ebizzy/200%-4x-10s/chy-KVM/debian-x86_64.cgz/x86_64-rhel/gcc-4.9/c13dcf9f2d6f5f06ef1bf79ec456df614c5e058b/16,security_model=none -device virtio-9p-pci,fsdev=test_dev,mount_tag=9p/virtfs_mount -kernel /lkp-cache/lkp-qemu-downloads/pkg/linux/x86_64-rhel/gcc-4.9/c13dcf9f2d6f5f06ef1bf79ec456df614c5e058b/vmlinuz-4.2.0-rc8 -append root=/dev/ram0 user=lkp job=/lkp/scheduled/kvm/ebizzy.yaml ARCH=x86_64 kconfig=x86_64-rhel branch=master commit=c13dcf9f2d6f5f06ef1bf79ec456df614c5e058b BOOT_IMAGE=/pkg/linux/x86_64-rhel/gcc-4.9/c13dcf9f2d6f5f06ef1bf79ec456df614c5e058b/vmlinuz-4.2.0-rc8 max_uptime=3300 RESULT_ROOT=/result/ebizzy/200%-4x-10s/chy-KVM/debian-x86_64.cgz/x86_64-rhel/gcc-4.9/c13dcf9f2d6f5f06ef1bf79ec456df614c5e058b/16 LKP_SERVER=localhost earlyprintk=ttyS0,115200 systemd.log_level=err debug apic=debug sysrq_always_enabled rcupdate.rcu_cpu_stall_timeout=100 panic=-1 softlockup_panic=1 nmi_watchdog=panic oops=panic load_ramdisk=2 prompt_ramdisk=0 console=ttyS0,115200 vga=normal rw  ip=dhcp result_service=9p/virtfs_mount -initrd /tmp/initrd-5798 -smp 2 -m 0M -no-reboot -watchdog i6300esb -rtc base=localtime -device e1000,netdev=net0 -netdev user,id=net0 -display none -monitor null -serial stdio -drive file=/tmp/vdisk-root/disk0-chy-KVM,media=disk,if=virtio -drive file=/tmp/vdisk-root/disk1-chy-KVM,media=disk,if=virtio -drive file=/tmp/vdisk-root/disk2-chy-KVM,media=disk,if=virtio -drive file=/tmp/vdisk-root/disk3-chy-KVM,media=disk,if=virtio -drive file=/tmp/vdisk-root/disk4-chy-KVM,media=disk,if=virtio -drive file=/tmp/vdisk-root/disk5-chy-KVM,media=disk,if=virtio -vnc localhost:1


