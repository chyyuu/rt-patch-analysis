# 服务器端rt-linux-lkp测试结果

[https://github.com/chyyuu/linux/](https://github.com/chyyuu/linux/) v4.5-rt

f963c13d4b9b6903f7f50b15afe7e77a441e099c lt: linux-4.5 porting. Patch linux-4.5.0 with modefied linux-4.4.79-rt92.patch.



crypto/algapi.c:721: undefined reference to `srcu_notifier_chain_register'
crypto/algapi.c:727: undefined reference to `srcu_notifier_chain_unregister'
crypto/api.c:239: undefined reference to `srcu_notifier_call_chain'
crypto/built-in.o:(.data+0x44): undefined reference to `process_srcu'
crypto/internal.h:146: undefined reference to `srcu_notifier_call_chain'
drivers/hv/vmbus_drv.c:820:2: error: implicit declaration of function 'add_interrupt_randomness' [-Werror=implicit-function-declaration]
drivers/misc/hwlat_detector.c:344:1: warning: the frame size of 1272 bytes is larger than 1024 bytes [-Wframe-larger-than=]
mm/slub.c:3518:16: error: passing argument 1 of 'spin_lock_irq' from incompatible pointer type [-Werror=incompatible-pointer-types]
mm/slub.c:3518:16: warning: passing argument 1 of 'spin_lock_irq' from incompatible pointer type
mm/slub.c:3518:2: warning: passing argument 1 of 'spin_lock_irq' from incompatible pointer type
mm/slub.c:3518:2: warning: passing argument 1 of 'spin_lock_irq' from incompatible pointer type [enabled by default]
mm/slub.c:3528:18: error: passing argument 1 of 'spin_unlock_irq' from incompatible pointer type [-Werror=incompatible-pointer-types]
mm/slub.c:3528:18: warning: passing argument 1 of 'spin_unlock_irq' from incompatible pointer type
mm/slub.c:3528:2: warning: passing argument 1 of 'spin_unlock_irq' from incompatible pointer type
mm/slub.c:3528:2: warning: passing argument 1 of 'spin_unlock_irq' from incompatible pointer type [enabled by default]
sound/soc/codecs/rt5659.c:1233:14: note: in expansion of macro 'SOC_VALUE_ENUM_SINGLE_DECL'

Error ids grouped by kconfigs:

recent_errors
├── alpha-defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm64-alldefconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm64-allmodconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ ├── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
│ └── sound-soc-codecs-rt5659.c:note : in-expansion-of-macro-SOC_VALUE_ENUM_SINGLE_DECL
├── arm64-allnoconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm64-defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-allmodconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ ├── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
│ └── sound-soc-codecs-rt5659.c:note : in-expansion-of-macro-SOC_VALUE_ENUM_SINGLE_DECL
├── arm-allnoconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-arm5
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-arm67
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-efm32_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-exynos_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-imx_v6_v7_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-ixp4xx_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-multi_v5_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-multi_v7_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-sa1100
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-samsung
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-sh
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── arm-sunxi_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── blackfin-allmodconfig
│ └── sound-soc-codecs-rt5659.c:note : in-expansion-of-macro-SOC_VALUE_ENUM_SINGLE_DECL
├── c6x-evmc6678_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── cris-etrax-100lx_v2_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── frv-defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── i386-allmodconfig
│ └── sound-soc-codecs-rt5659.c:note : in-expansion-of-macro-SOC_VALUE_ENUM_SINGLE_DECL
├── i386-randconfig-i0-201736
│ ├── mm-slub.c:warning : passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:warning : passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── ia64-alldefconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── ia64-allmodconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── ia64-allnoconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── ia64-defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── m68k-m5475evb_defconfig
│ ├── mm-slub.c:warning : passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:warning : passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── nios2-10m50_defconfig
│ ├── crypto-algapi.c:undefined-reference-to-srcu_notifier_chain_register
│ ├── crypto-algapi.c:undefined-reference-to-srcu_notifier_chain_unregister
│ ├── crypto-api.c:undefined-reference-to-srcu_notifier_call_chain
│ ├── crypto-built-in.o:(.data):undefined-reference-to-process_srcu
│ └── crypto-internal.h:undefined-reference-to-srcu_notifier_call_chain
├── parisc-allnoconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── parisc-c3000_defconfig
│ └── drivers-misc-hwlat_detector.c:warning : the-frame-size-of-bytes-is-larger-than-bytes
├── powerpc-allnoconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── powerpc-defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── powerpc-ppc64_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── s390-default_defconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── sh-allnoconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── sparc64-allnoconfig
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── tile-tilegx_defconfig
│ ├── mm-slub.c:warning : passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:warning : passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── x86_64-allmodconfig
│ ├── drivers-hv-vmbus_drv.c:error:implicit-declaration-of-function-add_interrupt_randomness
│ ├── mm-slub.c:error:passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ ├── mm-slub.c:error:passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
│ └── sound-soc-codecs-rt5659.c:note : in-expansion-of-macro-SOC_VALUE_ENUM_SINGLE_DECL
├── x86_64-allyesdebian
│ └── drivers-hv-vmbus_drv.c:error:implicit-declaration-of-function-add_interrupt_randomness
├── x86_64-randconfig-i0-201736
│ ├── mm-slub.c:warning : passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:warning : passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
├── xtensa-common_defconfig
│ ├── mm-slub.c:warning : passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
│ └── mm-slub.c:warning : passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type
└── xtensa-iss_defconfig
├── mm-slub.c:warning : passing-argument-of-spin_lock_irq-from-incompatible-pointer-type
└── mm-slub.c:warning : passing-argument-of-spin_unlock_irq-from-incompatible-pointer-type

elapsed time: 160m

configs tested: 145

i386 randconfig-x019-201736
i386 randconfig-x013-201736
i386 randconfig-x012-201736
i386 randconfig-x016-201736
i386 randconfig-x018-201736
i386 randconfig-x010-201736
i386 randconfig-x011-201736
i386 randconfig-x015-201736
i386 randconfig-x014-201736
i386 randconfig-x017-201736
i386 randconfig-n0-201736
i386 allmodconfig
arm omap2plus_defconfig
arm sa1100
arm allmodconfig
arm samsung
arm mvebu_v7_defconfig
arm ixp4xx_defconfig
arm imx_v6_v7_defconfig
arm64 allmodconfig
arm tegra_defconfig
arm arm5
arm64 alldefconfig
arm sh
arm arm67
i386 randconfig-a0-201736
i386 randconfig-a1-201736
mn10300 asb2364_defconfig
openrisc or1ksim_defconfig
um x86_64_defconfig
um i386_defconfig
frv defconfig
tile tilegx_defconfig
parisc c3000_defconfig
parisc b180_defconfig
parisc defconfig
alpha defconfig
parisc allnoconfig
cris etrax-100lx_v2_defconfig
blackfin TCM-BF537_defconfig
blackfin BF561-EZKIT-SMP_defconfig
blackfin BF533-EZKIT_defconfig
blackfin BF526-EZBRD_defconfig
x86_64 randconfig-x016-201736
x86_64 randconfig-x011-201736
x86_64 randconfig-x012-201736
x86_64 randconfig-x014-201736
x86_64 randconfig-x019-201736
x86_64 randconfig-x013-201736
x86_64 randconfig-x018-201736
x86_64 randconfig-x015-201736
x86_64 randconfig-x010-201736
x86_64 randconfig-x017-201736
m68k sun3_defconfig
m68k multi_defconfig
m68k m5475evb_defconfig
i386 randconfig-s1-201736
i386 randconfig-s0-201736
i386 tinyconfig
mips jz4740
mips malta_kvm_defconfig
mips 64r6el_defconfig
mips 32r2_defconfig
mips allnoconfig
mips fuloong2e_defconfig
mips txx9
x86_64 randconfig-i0-201736
i386 randconfig-i1-201736
i386 randconfig-i0-201736
x86_64 allmodconfig
microblaze mmu_defconfig
microblaze nommu_defconfig
sh titan_defconfig
sh rsk7269_defconfig
sh sh7785lcr_32bit_defconfig
sh allnoconfig
sparc defconfig
sparc64 allnoconfig
sparc64 defconfig
ia64 allnoconfig
ia64 defconfig
ia64 alldefconfig
powerpc defconfig
s390 default_defconfig
powerpc ppc64_defconfig
powerpc allnoconfig
arm at91_dt_defconfig
arm allnoconfig
arm efm32_defconfig
arm64 defconfig
arm multi_v5_defconfig
arm sunxi_defconfig
arm64 allnoconfig
arm exynos_defconfig
arm shmobile_defconfig
arm multi_v7_defconfig
c6x evmc6678_defconfig
xtensa common_defconfig
m32r m32104ut_defconfig
score spct6600_defconfig
xtensa iss_defconfig
m32r opsput_defconfig
m32r usrv_defconfig
m32r mappi3.smp_defconfig
nios2 10m50_defconfig
h8300 h8300h-sim_defconfig
i386 randconfig-x076-201736
i386 randconfig-x075-201736
i386 randconfig-x071-201736
i386 randconfig-x070-201736
i386 randconfig-x074-201736
i386 randconfig-x079-201736
i386 randconfig-x072-201736
i386 randconfig-x078-201736
i386 randconfig-x073-201736
i386 randconfig-x077-201736
x86_64 acpi-redef
x86_64 allyesdebian
x86_64 nfsroot
x86_64 randconfig-x001-201736
x86_64 randconfig-x007-201736
x86_64 randconfig-x000-201736
x86_64 randconfig-x006-201736
x86_64 randconfig-x003-201736
x86_64 randconfig-x009-201736
x86_64 randconfig-x004-201736
x86_64 randconfig-x008-201736
x86_64 randconfig-x005-201736
x86_64 randconfig-x002-201736
x86_64 kexec
x86_64 rhel
x86_64 rhel-7.2
i386 randconfig-x003-201736
i386 randconfig-x000-201736
i386 randconfig-x004-201736
i386 randconfig-x009-201736
i386 randconfig-x005-201736
i386 randconfig-x001-201736
i386 randconfig-x008-201736
i386 randconfig-x007-201736
i386 randconfig-x006-201736
i386 randconfig-x002-201736
i386 allnoconfig
i386 defconfig
i386 alldefconfig