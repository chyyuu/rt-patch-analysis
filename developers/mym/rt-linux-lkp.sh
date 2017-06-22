#!/bin/bash -x
   
#############################
#   WORK_DIR=/home/elwin/rt-linux
#   QEMU_IMG=${WORK_DIR}/ubuntu_img.img
#   dd if=/dev/zero of=${QEMU_IMG}  bs=1 count=0 seek=60G
#    
#   #install ubuntu to  ${QEMU_IMG}
#   qemu-system-x86_64 -enable-kvm -hda ${QEMU_IMG}   -m 2048 -cdrom ./ubuntu.iso  -boot d 
#   ##update grub entry info add rtlinux kernel grub entry
#############################   


 
   
#############################
##  define  some dir name
#############################      

  WORK_DIR=/home/elwin/rt-linux

  #KERNEL_SRC_DIR=${WORK_DIR}/linux
  BUILD_DIR=${WORK_DIR}/build
  FK_ROOTFS=${WORK_DIR}/fkroot

 
  
  
  
  
#############################
##  make or clear  dir
#############################   
  
if [ ! -d ${WORK_DIR} ]
then

    mkdir -p  ${WORK_DIR}
fi
 
cd ${WORK_DIR}
  
  
if [ -d ${BUILD_DIR} ]
then

   rm -rf ${BUILD_DIR}

fi
    mkdir -p  ${BUILD_DIR}

	
if [ -d ${FK_ROOTFS} ]
then
   rm -rf ${FK_ROOTFS}
fi
   mkdir -p  ${FK_ROOTFS}/boot/
   

#############################
## git  pull or clone kernel source code
############################# 
  
  cd  ${WORK_DIR}
  
  if [ -d  ${WORK_DIR}/linux/.git ]
then

   cd  ${WORK_DIR}/linux
   git pull
   
else

    git clone https://github.com/chyyuu/linux.git  -b v4.10-rc1-rt  --depth 1
fi
  

  
#############################
## compile kernel 
#############################  
  
  
  cd  ${WORK_DIR}/linux
  
  make   ARCH=x86_64  O=${BUILD_DIR}   defconfig
  make   ARCH=x86_64  O=${BUILD_DIR}   -j10  V=1  >${BUILD_DIR}/make.log 2>&1
  make   ARCH=x86_64  O=${BUILD_DIR}   INSTALL_MOD_PATH=${FK_ROOTFS}  modules_install  V=1  >${BUILD_DIR}/md_install.log 2>&1
  make   ARCH=x86_64  O=${BUILD_DIR}   INSTALL_PATH=${FK_ROOTFS}/boot/  install  V=1  >${BUILD_DIR}/kn_install.log 2>&1
  

#############################
## install vmlinuz and ko to qemu img
#############################  
QEMU_IMG=${WORK_DIR}/ubuntu_img.img
if [ !  -f ${QEMU_IMG} ]
then
   echo " error no   ${QEMU_IMG} " >&2
   exit 1
fi
 sudo losetup -f 
 sudo losetup  -d /dev/loop4
 sudo losetup -P /dev/loop4 ${QEMU_IMG}
 
 

 QEMU_IMG_MNT=${WORK_DIR}/qemu_img_mnt


##############
#need to make sure QEMU_IMG_MNT is a mount point 
#if QEMU_IMG_MNT is not mount and is not empty
#then rm -rf it
######### 

if [ ! -d ${QEMU_IMG_MNT} ]
then

    mkdir -p  ${QEMU_IMG_MNT}
fi 
 
sudo umount  ${QEMU_IMG_MNT}  
sleep 2
sudo mount /dev/loop4p1   ${QEMU_IMG_MNT} 


if [ -d ${QEMU_IMG_MNT}/lib/modules/4.10.0-rc1-rt ]
then

 sudo   rm -rf ${QEMU_IMG_MNT}/lib/modules/4.10.0-rc1-rt
fi


sudo cp  -a  ${FK_ROOTFS}/boot/*    ${QEMU_IMG_MNT}/boot/
sudo cp  -a   ${FK_ROOTFS}/lib/modules/*    ${QEMU_IMG_MNT}/lib/modules/

sudo umount  ${QEMU_IMG_MNT}  
sudo losetup  -d /dev/loop4

##update grub entry info

########################
## run qemu with qemu img 
#############################   
 
#qemu-system-x86_64 -enable-kvm -hda ${QEMU_IMG}  -kernel ${FK_ROOTFS}/boot/vmlinuz-4.10.0-rc1-rt  -append  "root=/dev/sda1" -m 2048
qemu-system-x86_64 -enable-kvm -hda ${QEMU_IMG}  -m 2048