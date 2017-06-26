#!/bin/bash -x

if [ $# -ne 2 ]
then 

cat <<EOF
Usage: $(basename $0) git_repo_url  commitid
e.g
rt-linux-lkp.sh    https://github.com/chyyuu/linux-rt-devel.git  3ae7b241a0f49035e5b99b6b86c27fea5e49ef1c
EOF
exit 1
fi
  


  cd $(pwd)
  GIT_URL=$1
  #https://github.com/chyyuu/linux-rt-devel.git  
  COMMITID=$2
  
  ##GET REPO_NAME
  REPO_NAME_T=${GIT_URL##*/}
  ###linux-rt-devel.git
  REPO_NAME=${REPO_NAME_T%.git}
  ###linux-rt-devel
  WORK_DIR=$(pwd)


  BUILD_DIR=${WORK_DIR}/build/${REPO_NAME}/${COMMITID}

#exit 
#############################
##  make or clear  dir
#############################   
  
# if [ ! -d ${WORK_DIR} ]
# then

    # mkdir -p  ${WORK_DIR}
# fi
 
cd ${WORK_DIR}
  
  
if [ -d ${BUILD_DIR} ]
then

   rm -rf ${BUILD_DIR}

fi

mkdir -p  ${BUILD_DIR}

	
#############################
## git  pull or clone kernel source code
############################# 
  
  cd  ${WORK_DIR}
  
  if [ -d  ${WORK_DIR}/${REPO_NAME}/.git ]
then

   cd  ${WORK_DIR}/${REPO_NAME}
   git checkout master
   git pull
   
else
    git clone ${GIT_URL}  
fi

cd ${WORK_DIR}/${REPO_NAME}
  
git checkout ${COMMITID}
##can we checkout files to anothoer dir?

  
#############################
## compile kernel 
#############################  
  
  
  cd ${WORK_DIR}/${REPO_NAME}
  make   ARCH=x86_64  O=${BUILD_DIR}   defconfig
  make   ARCH=x86_64  O=${BUILD_DIR}   -j10  V=1  >${BUILD_DIR}/make.log 2>&1


if [ !  -f ${BUILD_DIR}/arch/x86/boot/bzImage ]
then
   echo " error no ${BUILD_DIR}/arch/x86/bzImage " >&2
   echo "  compile error!!! " >&2
   exit 1
fi
   
#############################
## test kernel via lkp
#############################  
echo "FOR TEST!"
   

INITRD_IMG=${WORK_DIR}/ubuntu_img.img
if [ !  -f ${INITRD_IMG} ]
then
   echo " error no   ${INITRD_IMG} " >&2
   exit 1
fi

########################
## run qemu with qemu img 
#############################   
 
qemu-system-x86_64 -enable-kvm   -kernel ${BUILD_DIR}/arch/x86/boot/bzImage -initrd ${INITRD_IMG} -append  "commitid=${COMMITID} benchmark=abench" -m 2048

##lkp qemu
