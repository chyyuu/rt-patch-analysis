# 获取v4.12内核

```bash
wget https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git/snapshot/linux-stable-4.12.tar.gz
tar zxf linux-stable-4.12.tar.gz
```

# 获取v4.11.12-rt10版本的patch

```bash
wget https://www.kernel.org/pub/linux/kernel/projects/rt/4.11/patch-4.11.12-rt10.patch.gz
gunzip patch-4.11.12-rt10.patch.gz
```

# 给v4.12内核打v4.11.12-rt10的patch

```bash
cd linux-stable-4.12
patch -Np1 --ignore-whitespace -F3 < ../patch-4.11.12-rt10.patch
patching file Documentation/admin-guide/sysrq.rst
patching file Documentation/trace/events.txt
patching file MAINTAINERS
Reversed (or previously applied) patch detected!  Skipping patch.
1 out of 1 hunk ignored -- saving rejects to file MAINTAINERS.rej
patching file arch/Kconfig
Hunk #1 succeeded at 16 (offset 4 lines).
patching file arch/alpha/include/asm/spinlock_types.h
patching file arch/arm/Kconfig
Hunk #1 succeeded at 42 with fuzz 3.
patching file arch/arm/include/asm/irq.h
patching file arch/arm/include/asm/spinlock_types.h
patching file arch/arm/include/asm/switch_to.h
patching file arch/arm/include/asm/thread_info.h
patching file arch/arm/kernel/asm-offsets.c
patching file arch/arm/kernel/entry-armv.S
patching file arch/arm/kernel/entry-common.S
patching file arch/arm/kernel/hw_breakpoint.c
patching file arch/arm/kernel/patch.c
patching file arch/arm/kernel/process.c
patching file arch/arm/kernel/signal.c
patching file arch/arm/kernel/smp.c
patching file arch/arm/kernel/unwind.c
can't find file to patch at input line 938
Perhaps you used the wrong -p or --strip option?
The text leading up to this was:
--------------------------
|diff --git a/arch/arm/kvm/arm.c b/arch/arm/kvm/arm.c
|index 314eb6abe1ff..61369a7bb25c 100644
|--- a/arch/arm/kvm/arm.c
|+++ b/arch/arm/kvm/arm.c
--------------------------
File to patch: virt/kvm/arm/arm.c
patching file virt/kvm/arm/arm.c
Hunk #1 succeeded at 628 with fuzz 3 (offset -4 lines).
Hunk #2 succeeded at 656 (offset 3 lines).
Hunk #3 succeeded at 712 (offset 3 lines).
patching file arch/arm/mach-exynos/platsmp.c
patching file arch/arm/mach-hisi/platmcpm.c
patching file arch/arm/mach-omap2/omap-smp.c
patching file arch/arm/mach-prima2/platsmp.c
patching file arch/arm/mach-qcom/platsmp.c
patching file arch/arm/mach-spear/platsmp.c
patching file arch/arm/mach-sti/platsmp.c
patching file arch/arm/mm/fault.c
patching file arch/arm/mm/highmem.c
patching file arch/arm/plat-versatile/platsmp.c
patching file arch/arm/probes/kprobes/core.c
patching file arch/arm64/Kconfig
Hunk #2 succeeded at 754 (offset 11 lines).
patching file arch/arm64/include/asm/cpufeature.h
Reversed (or previously applied) patch detected!  Skipping patch.
4 out of 4 hunks ignored -- saving rejects to file arch/arm64/include/asm/cpufeature.h.rej
patching file arch/arm64/include/asm/insn.h
Hunk #1 succeeded at 433 (offset 30 lines).
patching file arch/arm64/include/asm/kvm_host.h
Reversed (or previously applied) patch detected!  Skipping patch.
2 out of 2 hunks ignored -- saving rejects to file arch/arm64/include/asm/kvm_host.h.rej
patching file arch/arm64/include/asm/spinlock_types.h
patching file arch/arm64/include/asm/thread_info.h
patching file arch/arm64/kernel/asm-offsets.c
patching file arch/arm64/kernel/cpufeature.c
Reversed (or previously applied) patch detected!  Skipping patch.
4 out of 4 hunks ignored -- saving rejects to file arch/arm64/kernel/cpufeature.c.rej
patching file arch/arm64/kernel/entry.S
patching file arch/arm64/kernel/insn.c
patching file arch/arm64/kernel/signal.c
patching file arch/arm64/kernel/smp.c
Hunk #1 succeeded at 961 (offset 46 lines).
patching file arch/blackfin/include/asm/spinlock_types.h
patching file arch/hexagon/include/asm/spinlock_types.h
patching file arch/ia64/include/asm/spinlock_types.h
patching file arch/ia64/kernel/mca.c
patching file arch/ia64/kernel/salinfo.c
Reversed (or previously applied) patch detected!  Skipping patch.
7 out of 7 hunks ignored -- saving rejects to file arch/ia64/kernel/salinfo.c.rej
patching file arch/ia64/kernel/topology.c
Reversed (or previously applied) patch detected!  Skipping patch.
1 out of 1 hunk ignored -- saving rejects to file arch/ia64/kernel/topology.c.rej
patching file arch/ia64/sn/kernel/sn2/sn_hwperf.c
Reversed (or previously applied) patch detected!  Skipping patch.
2 out of 2 hunks ignored -- saving rejects to file arch/ia64/sn/kernel/sn2/sn_hwperf.c.rej
patching file arch/m32r/include/asm/spinlock_types.h
patching file arch/metag/include/asm/spinlock_types.h
patching file arch/metag/kernel/smp.c
patching file arch/mips/Kconfig
Hunk #1 succeeded at 2516 (offset -4 lines).
patching file arch/mips/include/asm/spinlock_types.h
patching file arch/mips/include/asm/switch_to.h
patching file arch/mips/kernel/jump_label.c
patching file arch/mips/kernel/mips-mt-fpaff.c
patching file arch/mips/kernel/traps.c
patching file arch/mn10300/include/asm/spinlock_types.h
patching file arch/powerpc/Kconfig
Hunk #1 succeeded at 99 (offset 47 lines).
Hunk #2 succeeded at 205 (offset 50 lines).
Hunk #3 succeeded at 384 (offset 50 lines).
patching file arch/powerpc/include/asm/spinlock_types.h
patching file arch/powerpc/include/asm/thread_info.h
Hunk #1 succeeded at 35 (offset -8 lines).
Hunk #2 succeeded at 82 with fuzz 1 (offset -8 lines).
Hunk #3 succeeded at 101 (offset -7 lines).
Hunk #4 FAILED at 128.
1 out of 4 hunks FAILED -- saving rejects to file arch/powerpc/include/asm/thread_info.h.rej
patching file arch/powerpc/kernel/asm-offsets.c
patching file arch/powerpc/kernel/entry_32.S
Hunk #1 succeeded at 844 (offset -1 lines).
Hunk #2 succeeded at 862 (offset -1 lines).
Hunk #3 succeeded at 1189 (offset -1 lines).
Hunk #4 succeeded at 1210 (offset -1 lines).
patching file arch/powerpc/kernel/entry_64.S
Hunk #1 succeeded at 654 (offset -2 lines).
Hunk #2 succeeded at 716 (offset -2 lines).
Hunk #3 succeeded at 744 (offset -2 lines).
patching file arch/powerpc/kernel/irq.c
Hunk #1 succeeded at 597 (offset -41 lines).
Hunk #2 succeeded at 615 (offset -41 lines).
patching file arch/powerpc/kernel/misc_32.S
patching file arch/powerpc/kernel/misc_64.S
patching file arch/powerpc/kernel/smp.c
Hunk #1 succeeded at 97 (offset -1 lines).
Hunk #2 FAILED at 787.
Hunk #3 succeeded at 808 with fuzz 3 (offset -4 lines).
1 out of 3 hunks FAILED -- saving rejects to file arch/powerpc/kernel/smp.c.rej
patching file arch/powerpc/kvm/Kconfig
Hunk #1 succeeded at 176 (offset 1 line).
patching file arch/powerpc/kvm/book3s_hv.c
Hunk #1 succeeded at 3368 (offset 9 lines).
Hunk #2 succeeded at 3390 (offset 9 lines).
patching file arch/powerpc/platforms/cell/spufs/sched.c
patching file arch/powerpc/platforms/powernv/subcore.c
patching file arch/powerpc/platforms/ps3/device-init.c
patching file arch/s390/include/asm/spinlock_types.h
Hunk #1 succeeded at 1 with fuzz 2.
patching file arch/s390/kernel/jump_label.c
patching file arch/s390/kernel/kprobes.c
patching file arch/s390/kernel/time.c
Hunk #1 succeeded at 636 (offset 2 lines).
patching file arch/sh/include/asm/spinlock_types.h
patching file arch/sh/kernel/irq.c
patching file arch/sparc/Kconfig
patching file arch/sparc/include/asm/spinlock_types.h
patching file arch/sparc/kernel/irq_64.c
patching file arch/sparc/kernel/jump_label.c
patching file arch/sparc/kernel/sysfs.c
Reversed (or previously applied) patch detected!  Skipping patch.
4 out of 4 hunks ignored -- saving rejects to file arch/sparc/kernel/sysfs.c.rej
patching file arch/tile/include/asm/setup.h
patching file arch/tile/include/asm/spinlock_types.h
patching file arch/tile/kernel/hardwall.c
patching file arch/tile/kernel/jump_label.c
patching file arch/x86/Kconfig
Hunk #1 succeeded at 160 with fuzz 3.
Hunk #2 succeeded at 244 (offset 1 line).
Hunk #3 succeeded at 911 (offset 2 lines).
patching file arch/x86/crypto/aesni-intel_glue.c
patching file arch/x86/crypto/cast5_avx_glue.c
patching file arch/x86/crypto/glue_helper.c
Hunk #1 succeeded at 40 (offset 1 line).
Hunk #2 succeeded at 50 (offset 1 line).
Hunk #3 succeeded at 72 (offset 1 line).
Hunk #4 succeeded at 195 (offset 1 line).
Hunk #5 succeeded at 204 (offset 1 line).
Hunk #6 succeeded at 278 (offset 1 line).
Hunk #7 succeeded at 287 (offset 1 line).
Hunk #8 succeeded at 382 (offset 1 line).
Hunk #9 succeeded at 395 (offset 1 line).
patching file arch/x86/entry/common.c
Hunk #1 FAILED at 130.
1 out of 2 hunks FAILED -- saving rejects to file arch/x86/entry/common.c.rej
patching file arch/x86/entry/entry_32.S
Hunk #1 succeeded at 337 (offset -3 lines).
patching file arch/x86/entry/entry_64.S
Hunk #1 succeeded at 538 (offset -3 lines).
Hunk #2 succeeded at 902 (offset -3 lines).
Hunk #3 succeeded at 915 (offset -3 lines).
patching file arch/x86/events/core.c
patching file arch/x86/events/intel/core.c
Hunk #1 succeeded at 3410 (offset 21 lines).
Hunk #2 succeeded at 3486 (offset 21 lines).
Hunk #3 succeeded at 4112 (offset 22 lines).
patching file arch/x86/events/intel/cqm.c
patching file arch/x86/include/asm/preempt.h
patching file arch/x86/include/asm/signal.h
patching file arch/x86/include/asm/stackprotector.h
patching file arch/x86/include/asm/thread_info.h
Hunk #3 succeeded at 89 with fuzz 1 (offset -3 lines).
Hunk #4 succeeded at 115 with fuzz 1 (offset -1 lines).
Hunk #5 succeeded at 155 (offset 3 lines).
patching file arch/x86/include/asm/uv/uv_bau.h
Hunk #1 succeeded at 643 (offset 19 lines).
Hunk #2 succeeded at 847 (offset 32 lines).
patching file arch/x86/kernel/apic/io_apic.c
patching file arch/x86/kernel/asm-offsets.c
patching file arch/x86/kernel/cpu/mcheck/mce.c
Hunk #1 succeeded at 42 (offset 1 line).
Hunk #2 succeeded at 1309 (offset -8 lines).
Hunk #3 succeeded at 1318 (offset -8 lines).
Hunk #4 succeeded at 1353 (offset -8 lines).
Hunk #5 succeeded at 1365 (offset -8 lines).
Hunk #6 succeeded at 1380 with fuzz 1 (offset -8 lines).
Hunk #7 succeeded at 1383 with fuzz 2 (offset -15 lines).
Hunk #8 FAILED at 1455.
Hunk #9 succeeded at 1759 (offset -14 lines).
Hunk #10 succeeded at 1772 (offset -14 lines).
Hunk #11 succeeded at 2279 (offset -279 lines).
Hunk #12 succeeded at 2296 (offset -279 lines).
Hunk #13 succeeded at 2332 (offset -280 lines).
1 out of 13 hunks FAILED -- saving rejects to file arch/x86/kernel/cpu/mcheck/mce.c.rej
patching file arch/x86/kernel/cpu/mtrr/main.c
patching file arch/x86/kernel/irq_32.c
patching file arch/x86/kernel/jump_label.c
patching file arch/x86/kernel/process_32.c
Hunk #1 succeeded at 37 with fuzz 3.
Hunk #2 succeeded at 199 (offset 2 lines).
Hunk #3 succeeded at 303 (offset 2 lines).
patching file arch/x86/kernel/smpboot.c
patching file arch/x86/kvm/lapic.c
Hunk #1 succeeded at 2065 (offset 3 lines).
patching file arch/x86/kvm/x86.c
Hunk #1 succeeded at 6087 (offset -31 lines).
patching file arch/x86/mm/highmem_32.c
patching file arch/x86/mm/iomap_32.c
patching file arch/x86/platform/uv/tlb_uv.c
Hunk #1 succeeded at 759 (offset 12 lines).
Hunk #2 succeeded at 781 (offset 12 lines).
Hunk #3 succeeded at 804 (offset 12 lines).
Hunk #4 succeeded at 817 (offset 12 lines).
Hunk #5 succeeded at 880 (offset 12 lines).
Hunk #6 succeeded at 1013 (offset 12 lines).
Hunk #7 succeeded at 1025 (offset 12 lines).
Hunk #8 succeeded at 1961 (offset 23 lines).
patching file arch/x86/platform/uv/uv_time.c
patching file arch/xtensa/include/asm/spinlock_types.h
patching file block/blk-core.c
Hunk #3 succeeded at 692 with fuzz 2 (offset 14 lines).
Hunk #4 succeeded at 712 (offset 14 lines).
Hunk #5 succeeded at 784 (offset 18 lines).
Hunk #6 succeeded at 3160 (offset -29 lines).
Hunk #7 succeeded at 3208 (offset -29 lines).
Hunk #8 succeeded at 3227 (offset -29 lines).
Hunk #9 succeeded at 3239 (offset -29 lines).
Hunk #10 succeeded at 3266 (offset -29 lines).
patching file block/blk-ioc.c
patching file block/blk-mq.c
Hunk #1 succeeded at 101 (offset 22 lines).
Hunk #2 succeeded at 149 (offset 22 lines).
Hunk #3 succeeded at 195 (offset 22 lines).
Hunk #4 succeeded at 234 with fuzz 1 (offset 21 lines).
Hunk #5 succeeded at 420 (offset 22 lines).
Hunk #6 succeeded at 438 with fuzz 3 (offset 22 lines).
Hunk #7 succeeded at 458 with fuzz 1 (offset 29 lines).
Hunk #8 succeeded at 1163 with fuzz 1 (offset -4 lines).
patching file block/blk-mq.h
Hunk #1 succeeded at 101 (offset -29 lines).
patching file block/blk-softirq.c
patching file block/bounce.c
patching file crypto/algapi.c
patching file crypto/api.c
patching file crypto/internal.h
patching file drivers/acpi/acpica/acglobal.h
patching file drivers/acpi/acpica/hwregs.c
patching file drivers/acpi/acpica/hwxface.c
patching file drivers/acpi/acpica/utmutex.c
patching file drivers/acpi/pci_root.c
patching file drivers/acpi/processor_driver.c
Reversed (or previously applied) patch detected!  Skipping patch.
2 out of 2 hunks ignored -- saving rejects to file drivers/acpi/processor_driver.c.rej
patching file drivers/acpi/processor_throttling.c
Reversed (or previously applied) patch detected!  Skipping patch.
7 out of 7 hunks ignored -- saving rejects to file drivers/acpi/processor_throttling.c.rej
patching file drivers/ata/libata-sff.c
patching file drivers/base/node.c
patching file drivers/block/zram/zcomp.c
patching file drivers/block/zram/zcomp.h
patching file drivers/block/zram/zram_drv.c
Hunk #1 succeeded at 461 with fuzz 3.
Hunk #2 FAILED at 512.
Hunk #3 FAILED at 553.
Hunk #4 FAILED at 638.
Hunk #5 FAILED at 733.
Hunk #6 FAILED at 781.
Hunk #7 FAILED at 907.
6 out of 7 hunks FAILED -- saving rejects to file drivers/block/zram/zram_drv.c.rej
patching file drivers/block/zram/zram_drv.h
Hunk #2 succeeded at 119 (offset -4 lines).
patching file drivers/char/random.c
Hunk #6 succeeded at 1114 with fuzz 1 (offset 4 lines).
Hunk #7 succeeded at 2035 (offset 4 lines).
Hunk #8 succeeded at 2052 (offset 4 lines).
Hunk #9 succeeded at 2062 (offset 4 lines).
Hunk #10 succeeded at 2079 (offset 4 lines).
Hunk #11 succeeded at 2089 (offset 4 lines).
patching file drivers/clocksource/tcb_clksrc.c
patching file drivers/clocksource/timer-atmel-pit.c
patching file drivers/clocksource/timer-atmel-st.c
patching file drivers/connector/cn_proc.c
patching file drivers/cpufreq/Kconfig.x86
patching file drivers/cpufreq/cpufreq.c
patching file drivers/cpufreq/ia64-acpi-cpufreq.c
Reversed (or previously applied) patch detected!  Skipping patch.
8 out of 8 hunks ignored -- saving rejects to file drivers/cpufreq/ia64-acpi-cpufreq.c.rej
patching file drivers/cpufreq/loongson2_cpufreq.c
Reversed (or previously applied) patch detected!  Skipping patch.
1 out of 1 hunk ignored -- saving rejects to file drivers/cpufreq/loongson2_cpufreq.c.rej
patching file drivers/cpufreq/pasemi-cpufreq.c
patching file drivers/cpufreq/sh-cpufreq.c
Reversed (or previously applied) patch detected!  Skipping patch.
2 out of 2 hunks ignored -- saving rejects to file drivers/cpufreq/sh-cpufreq.c.rej
patching file drivers/cpufreq/sparc-us2e-cpufreq.c
Reversed (or previously applied) patch detected!  Skipping patch.
3 out of 3 hunks ignored -- saving rejects to file drivers/cpufreq/sparc-us2e-cpufreq.c.rej
patching file drivers/cpufreq/sparc-us3-cpufreq.c
Reversed (or previously applied) patch detected!  Skipping patch.
3 out of 3 hunks ignored -- saving rejects to file drivers/cpufreq/sparc-us3-cpufreq.c.rej
patching file drivers/crypto/n2_core.c
Reversed (or previously applied) patch detected!  Skipping patch.
2 out of 2 hunks ignored -- saving rejects to file drivers/crypto/n2_core.c.rej
patching file drivers/gpu/drm/i915/i915_gem_execbuffer.c
Hunk #1 FAILED at 1445.
1 out of 1 hunk FAILED -- saving rejects to file drivers/gpu/drm/i915/i915_gem_execbuffer.c.rej
patching file drivers/gpu/drm/i915/i915_gem_timeline.c
patching file drivers/gpu/drm/i915/i915_irq.c
Hunk #1 succeeded at 869 (offset 2 lines).
Hunk #2 succeeded at 921 (offset 2 lines).
patching file drivers/gpu/drm/i915/intel_display.c
Hunk #1 succeeded at 10484 (offset -1631 lines).
patching file drivers/gpu/drm/i915/intel_sprite.c
Hunk #2 succeeded at 68 with fuzz 2 (offset 2 lines).
Hunk #3 succeeded at 104 with fuzz 1 (offset 3 lines).
Hunk #4 succeeded at 134 (offset 3 lines).
Hunk #5 succeeded at 209 with fuzz 2 (offset 4 lines).
patching file drivers/gpu/drm/radeon/radeon_display.c
Hunk #1 succeeded at 1854 (offset 9 lines).
Hunk #2 succeeded at 1947 (offset 9 lines).
patching file drivers/hv/vmbus_drv.c
Hunk #1 succeeded at 968 (offset -2 lines).
Hunk #2 succeeded at 1013 (offset -2 lines).
patching file drivers/hwtracing/coresight/coresight-etm3x.c
patching file drivers/hwtracing/coresight/coresight-etm4x.c
patching file drivers/ide/alim15x3.c
patching file drivers/ide/hpt366.c
patching file drivers/ide/ide-io-std.c
patching file drivers/ide/ide-io.c
patching file drivers/ide/ide-iops.c
patching file drivers/ide/ide-probe.c
patching file drivers/ide/ide-taskfile.c
patching file drivers/infiniband/hw/hfi1/affinity.c
patching file drivers/infiniband/hw/hfi1/sdma.c
patching file drivers/infiniband/hw/qib/qib_file_ops.c
patching file drivers/infiniband/ulp/ipoib/ipoib_multicast.c
Hunk #1 succeeded at 898 (offset -4 lines).
Hunk #2 succeeded at 980 (offset -4 lines).
patching file drivers/input/gameport/gameport.c
patching file drivers/iommu/amd_iommu.c
patching file drivers/iommu/intel-iommu.c
Hunk #1 succeeded at 481 (offset 1 line).
Hunk #2 succeeded at 3725 (offset 5 lines).
Hunk #3 succeeded at 3759 (offset 5 lines).
Hunk #4 succeeded at 4311 (offset 5 lines).
Hunk #5 succeeded at 4561 (offset 5 lines).
patching file drivers/iommu/iova.c
Hunk #2 succeeded at 399 (offset -21 lines).
Hunk #3 succeeded at 728 (offset -21 lines).
Hunk #4 succeeded at 758 (offset -21 lines).
Hunk #5 succeeded at 791 (offset -21 lines).
Hunk #6 succeeded at 813 (offset -21 lines).
patching file drivers/leds/trigger/Kconfig
patching file drivers/md/bcache/Kconfig
patching file drivers/md/dm-rq.c
Hunk #1 succeeded at 674 (offset 7 lines).
patching file drivers/md/raid5.c
Hunk #1 succeeded at 2059 (offset 73 lines).
Hunk #2 succeeded at 2120 with fuzz 1 (offset 76 lines).
Hunk #3 succeeded at 6785 (offset 119 lines).
Hunk #4 succeeded at 6796 (offset 119 lines).
patching file drivers/md/raid5.h
Hunk #1 succeeded at 623 (offset -20 lines).
patching file drivers/misc/Kconfig
patching file drivers/mmc/host/mmci.c
Hunk #1 succeeded at 1200 (offset -4 lines).
Hunk #2 succeeded at 1245 (offset -4 lines).
patching file drivers/net/ethernet/3com/3c59x.c
patching file drivers/net/ethernet/realtek/8139too.c
patching file drivers/net/wireless/intersil/orinoco/orinoco_usb.c
patching file drivers/pci/pci-driver.c
patching file drivers/scsi/fcoe/fcoe.c
patching file drivers/scsi/fcoe/fcoe_ctlr.c
patching file drivers/scsi/libfc/fc_exch.c
patching file drivers/scsi/libsas/sas_ata.c
patching file drivers/scsi/qla2xxx/qla_inline.h
patching file drivers/thermal/x86_pkg_temp_thermal.c
patching file drivers/tty/serial/8250/8250_core.c
patching file drivers/tty/serial/8250/8250_port.c
patching file drivers/tty/serial/amba-pl011.c
Hunk #1 succeeded at 2227 (offset 5 lines).
Hunk #2 succeeded at 2265 (offset 5 lines).
patching file drivers/tty/serial/omap-serial.c
patching file drivers/usb/core/hcd.c
Hunk #1 succeeded at 1765 (offset 1 line).
patching file drivers/usb/gadget/function/f_fs.c
Hunk #1 succeeded at 1593 (offset -1 lines).
patching file drivers/usb/gadget/legacy/inode.c
Hunk #1 succeeded at 346 (offset 1 line).
Hunk #2 succeeded at 355 (offset 1 line).
patching file drivers/xen/manage.c
patching file fs/aio.c
patching file fs/autofs4/autofs_i.h
patching file fs/autofs4/expire.c
patching file fs/buffer.c
Hunk #1 succeeded at 302 (offset -1 lines).
Hunk #2 succeeded at 315 (offset -1 lines).
Hunk #3 succeeded at 327 (offset -1 lines).
Hunk #4 succeeded at 355 (offset -1 lines).
Hunk #5 succeeded at 367 (offset -1 lines).
Hunk #6 succeeded at 3406 (offset -12 lines).
patching file fs/cifs/readdir.c
patching file fs/dcache.c
Hunk #2 succeeded at 753 (offset 2 lines).
Hunk #4 succeeded at 2340 (offset -3 lines).
Hunk #5 succeeded at 2400 (offset -3 lines).
Hunk #6 succeeded at 2526 (offset -3 lines).
Hunk #7 succeeded at 3623 (offset -3 lines).
patching file fs/eventpoll.c
Hunk #1 succeeded at 587 (offset 77 lines).
patching file fs/exec.c
Hunk #1 succeeded at 1042 (offset -1 lines).
patching file fs/fuse/dir.c
patching file fs/jbd2/checkpoint.c
patching file fs/locks.c
patching file fs/namei.c
Hunk #2 succeeded at 3101 (offset 32 lines).
patching file fs/namespace.c
Hunk #2 succeeded at 353 (offset -4 lines).
patching file fs/nfs/delegation.c
patching file fs/nfs/dir.c
Hunk #1 succeeded at 452 (offset -39 lines).
Hunk #2 succeeded at 1437 (offset -56 lines).
Hunk #3 succeeded at 1757 (offset -56 lines).
Hunk #4 succeeded at 1771 (offset -56 lines).
patching file fs/nfs/inode.c
Hunk #1 succeeded at 1987 (offset 3 lines).
patching file fs/nfs/nfs4_fs.h
patching file fs/nfs/nfs4proc.c
Hunk #1 succeeded at 2609 (offset 1 line).
Hunk #2 succeeded at 2647 (offset 1 line).
patching file fs/nfs/nfs4state.c
patching file fs/nfs/unlink.c
patching file fs/ntfs/aops.c
patching file fs/proc/array.c
patching file fs/proc/base.c
Hunk #1 succeeded at 1833 (offset -3 lines).
patching file fs/proc/proc_sysctl.c
Hunk #1 succeeded at 661 (offset -21 lines).
patching file fs/timerfd.c
patching file include/acpi/platform/aclinux.h
patching file include/asm-generic/bug.h
Hunk #1 succeeded at 231 (offset 16 lines).
patching file include/linux/blk-mq.h
Hunk #1 succeeded at 227 (offset 9 lines).
patching file include/linux/blkdev.h
Hunk #1 succeeded at 133 (offset 5 lines).
Hunk #2 succeeded at 574 (offset 8 lines).
patching file include/linux/bottom_half.h
patching file include/linux/buffer_head.h
patching file include/linux/cgroup-defs.h
Hunk #1 succeeded at 18 (offset 1 line).
Hunk #2 succeeded at 141 with fuzz 3 (offset 1 line).
patching file include/linux/completion.h
patching file include/linux/cpu.h
patching file include/linux/cpuhotplug.h
Hunk #1 succeeded at 153 (offset 2 lines).
Hunk #2 succeeded at 176 (offset 2 lines).
Hunk #3 succeeded at 205 (offset 2 lines).
Hunk #4 succeeded at 240 (offset 2 lines).
Hunk #5 succeeded at 274 (offset 2 lines).
Hunk #6 succeeded at 306 (offset 2 lines).
patching file include/linux/dcache.h
patching file include/linux/delay.h
patching file include/linux/delayacct.h
patching file include/linux/highmem.h
patching file include/linux/hrtimer.h
Hunk #9 succeeded at 403 (offset -4 lines).
Hunk #10 succeeded at 434 (offset -4 lines).
patching file include/linux/idr.h
patching file include/linux/init_task.h
Hunk #1 succeeded at 168 (offset 1 line).
Hunk #2 succeeded at 188 with fuzz 3 (offset 1 line).
Hunk #3 succeeded at 247 (offset 15 lines).
Hunk #4 succeeded at 290 (offset 15 lines).
patching file include/linux/interrupt.h
patching file include/linux/irq.h
patching file include/linux/irq_work.h
patching file include/linux/irqdesc.h
patching file include/linux/irqflags.h
patching file include/linux/jbd2.h
patching file include/linux/kdb.h
patching file include/linux/kernel.h
Hunk #1 succeeded at 202 (offset 1 line).
Hunk #2 succeeded at 212 (offset 1 line).
Hunk #3 succeeded at 494 (offset 2 lines).
patching file include/linux/list_bl.h
patching file include/linux/locallock.h
patching file include/linux/mm_types.h
Hunk #2 succeeded at 497 (offset 5 lines).
patching file include/linux/module.h
Reversed (or previously applied) patch detected!  Skipping patch.
2 out of 2 hunks ignored -- saving rejects to file include/linux/module.h.rej
patching file include/linux/mutex.h
patching file include/linux/mutex_rt.h
patching file include/linux/netdevice.h
Hunk #2 succeeded at 2457 (offset 17 lines).
Hunk #3 succeeded at 2836 (offset 17 lines).
patching file include/linux/netfilter/x_tables.h
patching file include/linux/nfs_fs.h
Hunk #1 succeeded at 162 (offset 1 line).
patching file include/linux/nfs_xdr.h
Hunk #1 succeeded at 1515 (offset 2 lines).
patching file include/linux/notifier.h
patching file include/linux/padata.h
patching file include/linux/pci.h
Hunk #1 succeeded at 376 (offset 6 lines).
patching file include/linux/percpu-rwsem.h
patching file include/linux/percpu.h
Hunk #2 succeeded at 139 with fuzz 3.
patching file include/linux/perf_event.h
Hunk #1 succeeded at 801 (offset 7 lines).
patching file include/linux/pid.h
patching file include/linux/preempt.h
patching file include/linux/printk.h
patching file include/linux/radix-tree.h
patching file include/linux/random.h
patching file include/linux/rbtree.h
patching file include/linux/rbtree_augmented.h
patching file include/linux/rbtree_latch.h
patching file include/linux/rcu_assign_pointer.h
patching file include/linux/rcupdate.h
Hunk #2 succeeded at 183 (offset 5 lines).
Hunk #3 succeeded at 209 (offset 5 lines).
Hunk #4 succeeded at 271 (offset 5 lines).
Hunk #5 succeeded at 301 (offset 5 lines).
Hunk #6 succeeded at 487 (offset 10 lines).
Hunk #7 succeeded at 614 (offset 10 lines).
Hunk #8 succeeded at 892 (offset 10 lines).
Hunk #9 succeeded at 909 (offset 10 lines).
patching file include/linux/rcutree.h
Hunk #1 succeeded at 44 with fuzz 1.
Hunk #4 succeeded at 115 with fuzz 2 (offset 1 line).
patching file include/linux/ring_buffer.h
patching file include/linux/rtmutex.h
patching file include/linux/rwlock_rt.h
patching file include/linux/rwlock_types.h
patching file include/linux/rwlock_types_rt.h
patching file include/linux/rwsem.h
patching file include/linux/rwsem_rt.h
patching file include/linux/sched.h
Hunk #9 succeeded at 798 with fuzz 3.
Hunk #10 succeeded at 1057 (offset 2 lines).
Hunk #11 succeeded at 1249 (offset 9 lines).
Hunk #12 succeeded at 1273 (offset 9 lines).
Hunk #13 succeeded at 1307 (offset 9 lines).
Hunk #14 succeeded at 1445 (offset 5 lines).
Hunk #15 succeeded at 1518 (offset 5 lines).
Hunk #16 succeeded at 1626 (offset 5 lines).
patching file include/linux/sched/mm.h
patching file include/linux/sched/rt.h
Reversed (or previously applied) patch detected!  Skipping patch.
1 out of 1 hunk ignored -- saving rejects to file include/linux/sched/rt.h.rej
patching file include/linux/sched/task.h
patching file include/linux/sched/wake_q.h
patching file include/linux/seqlock.h
patching file include/linux/signal.h
patching file include/linux/skbuff.h
Hunk #2 succeeded at 1591 (offset 3 lines).
patching file include/linux/smp.h
Reversed (or previously applied) patch detected!  Skipping patch.
3 out of 3 hunks ignored -- saving rejects to file include/linux/smp.h.rej
patching file include/linux/spinlock.h
patching file include/linux/spinlock_api_smp.h
patching file include/linux/spinlock_rt.h
patching file include/linux/spinlock_types.h
patching file include/linux/spinlock_types_nort.h
patching file include/linux/spinlock_types_raw.h
patching file include/linux/spinlock_types_rt.h
patching file include/linux/spinlock_types_up.h
patching file include/linux/srcu.h
Hunk #1 FAILED at 84.
Hunk #2 FAILED at 119.
2 out of 2 hunks FAILED -- saving rejects to file include/linux/srcu.h.rej
patching file include/linux/stop_machine.h
patching file include/linux/suspend.h
patching file include/linux/swait.h
patching file include/linux/swap.h
patching file include/linux/swork.h
patching file include/linux/thread_info.h
Hunk #1 succeeded at 86 (offset 12 lines).
patching file include/linux/timer.h
patching file include/linux/trace_events.h
Hunk #2 succeeded at 300 (offset -9 lines).
Hunk #3 succeeded at 315 (offset -9 lines).
Hunk #4 succeeded at 327 (offset -9 lines).
Hunk #5 succeeded at 397 (offset -9 lines).
Hunk #6 succeeded at 423 (offset -9 lines).
patching file include/linux/tracepoint.h
Hunk #2 succeeded at 212 (offset 3 lines).
patching file include/linux/uaccess.h
Hunk #1 succeeded at 214 (offset 190 lines).
Hunk #2 succeeded at 231 (offset 190 lines).
patching file include/linux/vmstat.h
patching file include/linux/wait.h
patching file include/linux/workqueue.h
Reversed (or previously applied) patch detected!  Skipping patch.
1 out of 1 hunk ignored -- saving rejects to file include/linux/workqueue.h.rej
patching file include/net/gen_stats.h
patching file include/net/neighbour.h
Hunk #1 succeeded at 447 with fuzz 1 (offset 1 line).
Hunk #2 succeeded at 471 (offset 1 line).
Hunk #3 succeeded at 512 (offset 1 line).
patching file include/net/net_seq_lock.h
patching file include/net/netns/ipv4.h
Hunk #1 succeeded at 78 (offset -1 lines).
patching file include/net/sch_generic.h
Hunk #2 succeeded at 88 (offset 1 line).
Hunk #3 succeeded at 100 (offset 1 line).
Hunk #4 succeeded at 124 (offset 1 line).
Hunk #5 succeeded at 324 (offset 1 line).
patching file include/trace/events/sched.h
Reversed (or previously applied) patch detected!  Skipping patch.
7 out of 7 hunks ignored -- saving rejects to file include/trace/events/sched.h.rej
patching file init/Kconfig
Hunk #2 succeeded at 661 (offset 39 lines).
Hunk #3 succeeded at 688 (offset 39 lines).
Hunk #4 succeeded at 1091 (offset 39 lines).
Hunk #5 succeeded at 1865 (offset 39 lines).
Hunk #6 succeeded at 1886 (offset 39 lines).
Hunk #7 succeeded at 1905 (offset 39 lines).
patching file init/Makefile
patching file init/main.c
Hunk #4 succeeded at 1037 (offset 4 lines).
patching file kernel/Kconfig.locks
patching file kernel/Kconfig.preempt
patching file kernel/async.c
patching file kernel/cgroup/cgroup.c
patching file kernel/cgroup/cpuset.c
Hunk #14 succeeded at 2176 (offset -3 lines).
Hunk #15 succeeded at 2218 (offset -3 lines).
Hunk #16 succeeded at 2307 (offset -3 lines).
Hunk #17 succeeded at 2419 (offset -3 lines).
Hunk #18 succeeded at 2471 (offset -3 lines).
Hunk #19 succeeded at 2567 (offset -3 lines).
patching file kernel/cpu.c
Hunk #18 succeeded at 1127 with fuzz 2 (offset 2 lines).
Hunk #19 succeeded at 1415 (offset 2 lines).
Hunk #20 succeeded at 1457 (offset 2 lines).
Hunk #21 succeeded at 1482 (offset 2 lines).
Hunk #22 succeeded at 1538 (offset 2 lines).
Hunk #23 succeeded at 1546 (offset 2 lines).
Hunk #24 succeeded at 1575 (offset 2 lines).
Hunk #25 succeeded at 1596 (offset 2 lines).
Hunk #26 succeeded at 1647 (offset 2 lines).
Hunk #27 succeeded at 1856 with fuzz 3 (offset 2 lines).
patching file kernel/cpu_pm.c
patching file kernel/debug/kdb/kdb_io.c
patching file kernel/delayacct.c
patching file kernel/events/core.c
Hunk #1 succeeded at 389 (offset 3 lines).
Hunk #2 succeeded at 1047 (offset 3 lines).
Hunk #3 succeeded at 3814 (offset 3 lines).
Hunk #4 succeeded at 7718 (offset 132 lines).
Hunk #5 succeeded at 7740 (offset 132 lines).
Hunk #6 succeeded at 7748 (offset 132 lines).
Hunk #7 succeeded at 7756 (offset 132 lines).
Hunk #8 succeeded at 8620 (offset 132 lines).
Hunk #9 succeeded at 8935 (offset 132 lines).
Hunk #10 succeeded at 8944 (offset 132 lines).
Hunk #11 succeeded at 9074 (offset 132 lines).
Hunk #12 succeeded at 9898 (offset 139 lines).
Hunk #13 succeeded at 10087 (offset 139 lines).
Hunk #14 succeeded at 10193 (offset 139 lines).
Hunk #15 succeeded at 10226 (offset 139 lines).
Hunk #16 succeeded at 10280 (offset 139 lines).
Hunk #17 succeeded at 10962 (offset 139 lines).
Hunk #18 succeeded at 10979 (offset 139 lines).
Hunk #19 succeeded at 10992 (offset 139 lines).
Hunk #20 succeeded at 11009 (offset 139 lines).
Hunk #21 succeeded at 11032 (offset 139 lines).
patching file kernel/exit.c
patching file kernel/extable.c
patching file kernel/fork.c
Hunk #1 succeeded at 87 with fuzz 3.
Hunk #2 succeeded at 409 (offset 19 lines).
Hunk #3 succeeded at 437 (offset 19 lines).
Hunk #4 succeeded at 586 (offset 24 lines).
Hunk #5 succeeded at 599 (offset 24 lines).
Hunk #6 succeeded at 920 (offset 24 lines).
Hunk #7 succeeded at 1501 with fuzz 3 (offset 24 lines).
Hunk #8 succeeded at 1513 (offset 25 lines).
Hunk #9 succeeded at 1672 (offset 25 lines).
patching file kernel/futex.c
Reversed (or previously applied) patch detected!  Skipping patch.
46 out of 46 hunks ignored -- saving rejects to file kernel/futex.c.rej
patching file kernel/irq/handle.c
patching file kernel/irq/manage.c
Hunk #9 succeeded at 1395 (offset 2 lines).
Hunk #10 succeeded at 2130 (offset 9 lines).
patching file kernel/irq/settings.h
patching file kernel/irq/spurious.c
patching file kernel/irq_work.c
patching file kernel/jump_label.c
patching file kernel/kprobes.c
Hunk #1 succeeded at 483 (offset -3 lines).
Hunk #2 succeeded at 490 (offset -3 lines).
Hunk #3 succeeded at 513 (offset -3 lines).
Hunk #4 succeeded at 538 (offset -3 lines).
Hunk #5 succeeded at 562 (offset -3 lines).
Hunk #6 succeeded at 588 (offset -3 lines).
Hunk #7 succeeded at 652 (offset -3 lines).
Hunk #8 succeeded at 792 (offset 4 lines).
Hunk #9 succeeded at 814 (offset 4 lines).
Hunk #10 succeeded at 829 (offset 4 lines).
Hunk #11 succeeded at 837 (offset 4 lines).
Hunk #12 succeeded at 856 (offset 4 lines).
Hunk #13 succeeded at 865 (offset 4 lines).
Hunk #14 succeeded at 1017 (offset 4 lines).
Hunk #15 succeeded at 1031 (offset 4 lines).
Hunk #16 succeeded at 1304 (offset 4 lines).
Hunk #17 succeeded at 1355 (offset 4 lines).
Hunk #18 succeeded at 1558 (offset 7 lines).
Hunk #19 succeeded at 1576 (offset 7 lines).
patching file kernel/ksysfs.c
Hunk #1 succeeded at 140 with fuzz 2 (offset 4 lines).
Hunk #2 succeeded at 239 (offset 6 lines).
patching file kernel/locking/Makefile
patching file kernel/locking/lockdep.c
Reversed (or previously applied) patch detected!  Skipping patch.
8 out of 8 hunks ignored -- saving rejects to file kernel/locking/lockdep.c.rej
patching file kernel/locking/locktorture.c
patching file kernel/locking/rt.c
patching file kernel/locking/rtmutex-debug.c
Reversed (or previously applied) patch detected!  Skipping patch.
1 out of 1 hunk ignored -- saving rejects to file kernel/locking/rtmutex-debug.c.rej
patching file kernel/locking/rtmutex-debug.h
Reversed (or previously applied) patch detected!  Skipping patch.
1 out of 1 hunk ignored -- saving rejects to file kernel/locking/rtmutex-debug.h.rej
patching file kernel/locking/rtmutex.c
Hunk #4 succeeded at 242 with fuzz 2 (offset 6 lines).
Hunk #5 FAILED at 256.
Hunk #6 FAILED at 340.
Hunk #7 succeeded at 402 (offset -32 lines).
Hunk #8 succeeded at 417 (offset -32 lines).
Hunk #9 succeeded at 554 (offset -32 lines).
Hunk #10 FAILED at 637.
Hunk #11 succeeded at 718 with fuzz 3 (offset -15 lines).
Hunk #12 succeeded at 754 (offset -13 lines).
Hunk #13 FAILED at 796.
Hunk #14 FAILED at 812.
Hunk #15 succeeded at 865 with fuzz 3 (offset -13 lines).
Hunk #16 succeeded at 907 (offset -11 lines).
Hunk #17 FAILED at 940.
Hunk #18 FAILED at 990.
Hunk #19 succeeded at 1002 with fuzz 2 (offset -10 lines).
Hunk #20 FAILED at 1027.
Hunk #21 FAILED at 1049.
Hunk #22 succeeded at 1083 (offset -9 lines).
Hunk #23 FAILED at 1102.
Hunk #24 FAILED at 1119.
Hunk #25 succeeded at 1138 with fuzz 2 (offset 3 lines).
Hunk #26 FAILED at 1158.
Hunk #27 FAILED at 1197.
Hunk #28 succeeded at 1237 (offset 12 lines).
Hunk #29 succeeded at 1247 (offset 12 lines).
Hunk #30 FAILED at 1284.
Hunk #31 succeeded at 1320 (offset 10 lines).
Hunk #32 FAILED at 1361.
Hunk #33 FAILED at 1373.
Hunk #34 FAILED at 1420.
Hunk #35 FAILED at 1436.
Hunk #36 succeeded at 1510 (offset 8 lines).
Hunk #37 FAILED at 1517.
Hunk #38 succeeded at 1559 (offset 3 lines).
Hunk #39 succeeded at 1577 (offset 3 lines).
Hunk #40 FAILED at 1596.
Hunk #41 succeeded at 1669 (offset 26 lines).
Hunk #42 FAILED at 1667.
Hunk #43 FAILED at 1690.
Hunk #44 FAILED at 1713.
Hunk #45 FAILED at 1764.
Hunk #46 succeeded at 1828 with fuzz 3 (offset 26 lines).
24 out of 46 hunks FAILED -- saving rejects to file kernel/locking/rtmutex.c.rej
patching file kernel/locking/rtmutex.h
Reversed (or previously applied) patch detected!  Skipping patch.
1 out of 1 hunk ignored -- saving rejects to file kernel/locking/rtmutex.h.rej
patching file kernel/locking/rtmutex_common.h
Hunk #2 succeeded at 29 with fuzz 3.
Hunk #3 FAILED at 101.
1 out of 3 hunks FAILED -- saving rejects to file kernel/locking/rtmutex_common.h.rej
patching file kernel/locking/rwlock-rt.c
patching file kernel/locking/rwsem-rt.c
patching file kernel/locking/spinlock.c
patching file kernel/locking/spinlock_debug.c
patching file kernel/module.c
Reversed (or previously applied) patch detected!  Skipping patch.
4 out of 4 hunks ignored -- saving rejects to file kernel/module.c.rej
patching file kernel/padata.c
Hunk #1 succeeded at 933 (offset -5 lines).
Hunk #2 succeeded at 940 (offset -5 lines).
Hunk #3 succeeded at 954 (offset -5 lines).
Hunk #4 succeeded at 977 (offset -5 lines).
Hunk #5 succeeded at 991 (offset -5 lines).
patching file kernel/panic.c
patching file kernel/power/hibernate.c
patching file kernel/power/suspend.c
patching file kernel/printk/printk.c
Hunk #1 succeeded at 400 (offset -1 lines).
Hunk #2 succeeded at 1234 (offset -1 lines).
Hunk #3 succeeded at 1408 (offset -1 lines).
Hunk #4 succeeded at 1421 (offset -1 lines).
Hunk #5 succeeded at 1441 (offset -1 lines).
Hunk #6 succeeded at 1460 (offset -1 lines).
Hunk #7 succeeded at 1506 (offset -1 lines).
Hunk #8 succeeded at 1656 (offset -1 lines).
Hunk #9 succeeded at 1677 (offset -1 lines).
Hunk #10 succeeded at 1797 (offset -1 lines).
Hunk #11 succeeded at 1860 (offset -1 lines).
Hunk #12 succeeded at 1985 (offset -1 lines).
Hunk #13 succeeded at 2331 (offset 4 lines).
Hunk #14 succeeded at 2393 (offset 4 lines).
patching file kernel/ptrace.c
patching file kernel/rcu/rcutorture.c
patching file kernel/rcu/tree.c
Hunk #1 succeeded at 57 with fuzz 3.
Hunk #2 succeeded at 268 (offset 1 line).
Hunk #3 succeeded at 290 with fuzz 2 (offset 1 line).
Hunk #4 succeeded at 606 (offset 30 lines).
Hunk #5 succeeded at 632 (offset 30 lines).
Hunk #6 succeeded at 641 (offset 30 lines).
Hunk #7 succeeded at 665 (offset 30 lines).
Hunk #8 succeeded at 684 (offset 30 lines).
Hunk #9 succeeded at 741 (offset 30 lines).
Hunk #10 succeeded at 3063 (offset -85 lines).
Hunk #11 succeeded at 3085 (offset -85 lines).
Hunk #12 succeeded at 3322 (offset -86 lines).
Hunk #13 succeeded at 3331 (offset -86 lines).
Hunk #14 succeeded at 3423 (offset -86 lines).
Hunk #15 succeeded at 3450 (offset -86 lines).
Hunk #16 succeeded at 3792 (offset -121 lines).
Hunk #17 succeeded at 3801 (offset -121 lines).
Hunk #18 succeeded at 4327 (offset -114 lines).
patching file kernel/rcu/tree.h
Hunk #1 succeeded at 457 (offset -132 lines).
Hunk #2 succeeded at 468 with fuzz 2 (offset -131 lines).
Hunk #3 succeeded at 491 (offset -131 lines).
patching file kernel/rcu/tree_plugin.h
patching file kernel/rcu/update.c
Hunk #2 succeeded at 331 (offset 33 lines).
Hunk #3 succeeded at 358 (offset 33 lines).
patching file kernel/sched/Makefile
patching file kernel/sched/clock.c
patching file kernel/sched/completion.c
patching file kernel/sched/core.c
Hunk #2 succeeded at 346 (offset -10 lines).
Hunk #3 succeeded at 427 (offset -10 lines).
Hunk #4 succeeded at 457 (offset -10 lines).
Hunk #5 succeeded at 518 (offset -10 lines).
Hunk #6 succeeded at 583 (offset -10 lines).
Hunk #7 succeeded at 609 (offset -10 lines).
Hunk #8 succeeded at 1050 with fuzz 1 (offset -2 lines).
Hunk #14 succeeded at 1365 (offset 6 lines).
Hunk #15 succeeded at 1409 (offset 6 lines).
Hunk #16 succeeded at 1422 (offset 6 lines).
Hunk #17 succeeded at 1478 (offset 6 lines).
Hunk #18 succeeded at 1493 (offset 6 lines).
Hunk #19 succeeded at 1569 (offset 6 lines).
Hunk #20 succeeded at 1609 (offset 6 lines).
Hunk #21 succeeded at 1661 (offset 6 lines).
Hunk #22 succeeded at 1671 (offset 6 lines).
Hunk #23 succeeded at 1683 (offset 6 lines).
Hunk #24 succeeded at 1749 (offset 6 lines).
Hunk #25 succeeded at 2081 (offset 3 lines).
Hunk #26 FAILED at 2194.
Hunk #27 succeeded at 2265 (offset 1 line).
Hunk #28 succeeded at 2553 (offset 1 line).
Hunk #29 succeeded at 2682 (offset 1 line).
Hunk #30 succeeded at 2885 (offset 1 line).
Hunk #31 succeeded at 3541 (offset 4 lines).
Hunk #32 succeeded at 3547 (offset 1 line).
Hunk #36 succeeded at 3726 (offset 25 lines).
Hunk #37 succeeded at 3764 (offset 25 lines).
Hunk #38 succeeded at 3792 (offset 25 lines).
Hunk #39 succeeded at 3817 (offset 25 lines).
Hunk #40 FAILED at 3847.
Hunk #41 FAILED at 3858.
Hunk #42 FAILED at 3888.
Hunk #43 succeeded at 3882 with fuzz 3 (offset -30 lines).
Hunk #44 succeeded at 4018 with fuzz 2 (offset 69 lines).
Hunk #45 FAILED at 4200.
Hunk #46 succeeded at 4521 (offset 68 lines).
Hunk #47 FAILED at 4490.
Hunk #48 succeeded at 5115 (offset 68 lines).
Hunk #49 succeeded at 5234 (offset 72 lines).
Hunk #50 succeeded at 5248 (offset 72 lines).
Hunk #51 succeeded at 5633 (offset 72 lines).
Hunk #52 succeeded at 5683 (offset 72 lines).
Hunk #53 succeeded at 5739 (offset 72 lines).
Hunk #54 succeeded at 5778 (offset 72 lines).
Hunk #55 succeeded at 5794 (offset 72 lines).
Hunk #56 succeeded at 5883 (offset 69 lines).
Hunk #57 succeeded at 6124 (offset 70 lines).
Hunk #58 succeeded at 6411 (offset 70 lines).
Hunk #59 succeeded at 6446 (offset 70 lines).
Hunk #60 succeeded at 7582 (offset 72 lines).
6 out of 60 hunks FAILED -- saving rejects to file kernel/sched/core.c.rej
patching file kernel/sched/cpudeadline.c
patching file kernel/sched/cpupri.c
patching file kernel/sched/deadline.c
patching file kernel/sched/debug.c
patching file kernel/sched/fair.c
Hunk #1 succeeded at 1547 (offset -6 lines).
Hunk #2 succeeded at 1657 (offset -6 lines).
Hunk #3 succeeded at 3765 (offset 23 lines).
Hunk #4 succeeded at 3789 (offset 23 lines).
Hunk #5 succeeded at 3931 (offset 23 lines).
Hunk #6 succeeded at 4113 (offset 23 lines).
Hunk #7 succeeded at 4742 (offset 24 lines).
Hunk #8 succeeded at 5485 (offset 25 lines).
Hunk #9 succeeded at 5605 (offset 25 lines).
Hunk #10 succeeded at 5744 with fuzz 2 (offset 62 lines).
Hunk #11 succeeded at 5778 (offset 62 lines).
Hunk #12 succeeded at 5830 with fuzz 3 (offset 62 lines).
Hunk #13 succeeded at 5985 (offset 62 lines).
Hunk #14 succeeded at 6256 (offset 62 lines).
Hunk #15 succeeded at 6718 (offset 62 lines).
Hunk #16 succeeded at 6745 (offset 62 lines).
Hunk #17 succeeded at 7287 (offset 70 lines).
Hunk #18 succeeded at 7862 (offset 71 lines).
Hunk #19 succeeded at 8249 (offset 73 lines).
Hunk #20 succeeded at 9047 (offset 78 lines).
Hunk #21 succeeded at 9071 (offset 78 lines).
patching file kernel/sched/features.h
patching file kernel/sched/rt.c
patching file kernel/sched/sched.h
Hunk #2 succeeded at 1481 (offset 4 lines).
patching file kernel/sched/swait.c
patching file kernel/sched/swork.c
patching file kernel/signal.c
patching file kernel/softirq.c
patching file kernel/stop_machine.c
patching file kernel/time/hrtimer.c
Hunk #11 succeeded at 1593 (offset -3 lines).
Hunk #12 succeeded at 1646 (offset -3 lines).
Hunk #13 FAILED at 1667.
Hunk #14 succeeded at 1678 with fuzz 3 (offset -3 lines).
Hunk #15 succeeded at 1705 (offset -3 lines).
Hunk #16 succeeded at 1727 with fuzz 1 (offset -1 lines).
Hunk #17 succeeded at 1758 (offset -1 lines).
Hunk #18 succeeded at 1799 (offset -1 lines).
Hunk #19 succeeded at 1840 (offset -1 lines).
1 out of 19 hunks FAILED -- saving rejects to file kernel/time/hrtimer.c.rej
patching file kernel/time/itimer.c
patching file kernel/time/jiffies.c
patching file kernel/time/ntp.c
patching file kernel/time/posix-cpu-timers.c
Hunk #4 succeeded at 1030 (offset 13 lines).
Hunk #5 succeeded at 1119 (offset 13 lines).
Hunk #6 succeeded at 1179 (offset 13 lines).
patching file kernel/time/posix-timers.c
Hunk #3 succeeded at 831 (offset 2 lines).
Hunk #4 succeeded at 924 (offset 4 lines).
Hunk #5 succeeded at 933 with fuzz 2 (offset 4 lines).
Hunk #6 succeeded at 977 (offset 5 lines).
Hunk #7 succeeded at 1011 (offset 5 lines).
patching file kernel/time/tick-broadcast-hrtimer.c
patching file kernel/time/tick-common.c
patching file kernel/time/tick-sched.c
Hunk #7 succeeded at 1203 (offset 12 lines).
patching file kernel/time/timekeeping.c
Hunk #1 succeeded at 2322 (offset -1 lines).
patching file kernel/time/timekeeping.h
patching file kernel/time/timer.c
Hunk #6 succeeded at 1110 with fuzz 2.
patching file kernel/trace/ring_buffer.c
Hunk #8 succeeded at 509 (offset 1 line).
Hunk #9 succeeded at 1404 (offset 1 line).
Hunk #10 succeeded at 2244 (offset 1 line).
Hunk #11 succeeded at 2296 (offset 1 line).
Hunk #12 succeeded at 2486 (offset 1 line).
Hunk #13 succeeded at 2517 (offset 1 line).
Hunk #14 succeeded at 2534 (offset 1 line).
Hunk #15 succeeded at 2718 (offset 1 line).
Hunk #16 succeeded at 2796 (offset 1 line).
Hunk #17 succeeded at 3482 (offset 1 line).
Hunk #18 succeeded at 3511 (offset 1 line).
Hunk #19 succeeded at 3740 (offset 1 line).
Hunk #20 succeeded at 3778 (offset 1 line).
Hunk #21 succeeded at 3813 (offset 1 line).
Hunk #22 succeeded at 3868 (offset 1 line).
patching file kernel/trace/trace.c
Hunk #1 succeeded at 1170 (offset 6 lines).
Hunk #2 succeeded at 2031 (offset 89 lines).
Hunk #3 succeeded at 2042 (offset 89 lines).
Hunk #4 succeeded at 2183 (offset 89 lines).
Hunk #5 succeeded at 3239 (offset 118 lines).
Hunk #6 succeeded at 3275 (offset 118 lines).
Hunk #7 succeeded at 6019 (offset 122 lines).
Hunk #8 succeeded at 6099 (offset 122 lines).
Hunk #9 succeeded at 8105 (offset 180 lines).
patching file kernel/trace/trace.h
Hunk #3 succeeded at 283 (offset 3 lines).
Hunk #4 succeeded at 1274 (offset 80 lines).
Hunk #5 succeeded at 1318 (offset 80 lines).
Hunk #6 succeeded at 1351 (offset 80 lines).
Hunk #7 succeeded at 1531 (offset 80 lines).
Hunk #8 succeeded at 1576 (offset 80 lines).
Hunk #9 succeeded at 1744 (offset 80 lines).
patching file kernel/trace/trace_events.c
patching file kernel/trace/trace_events_hist.c
patching file kernel/trace/trace_events_trigger.c
patching file kernel/trace/trace_hwlat.c
patching file kernel/trace/trace_kprobe.c
Hunk #1 succeeded at 898 (offset 25 lines).
Hunk #2 succeeded at 1424 (offset 25 lines).
Hunk #3 succeeded at 1446 (offset 25 lines).
Hunk #4 succeeded at 1517 (offset 25 lines).
patching file kernel/trace/trace_output.c
Hunk #1 succeeded at 437 (offset -1 lines).
Hunk #2 succeeded at 468 (offset -1 lines).
Hunk #3 succeeded at 479 (offset -1 lines).
patching file kernel/trace/trace_probe.c
patching file kernel/trace/trace_probe.h
patching file kernel/trace/trace_uprobe.c
patching file kernel/trace/tracing_map.c
patching file kernel/trace/tracing_map.h
patching file kernel/tracepoint.c
patching file kernel/user.c
patching file kernel/watchdog.c
patching file kernel/watchdog_hld.c
patching file kernel/workqueue.c
Hunk #35 succeeded at 3299 (offset -1 lines).
Hunk #36 succeeded at 3353 (offset -1 lines).
Hunk #37 succeeded at 3461 (offset -1 lines).
Hunk #38 succeeded at 4122 (offset -1 lines).
Hunk #39 succeeded at 4215 (offset -1 lines).
Hunk #40 succeeded at 4227 (offset -1 lines).
Hunk #41 succeeded at 4254 (offset -1 lines).
Hunk #42 succeeded at 4451 (offset -1 lines).
Hunk #43 succeeded at 4504 (offset -1 lines).
Hunk #44 succeeded at 4778 with fuzz 3 (offset -1 lines).
Hunk #45 succeeded at 4888 (offset 22 lines).
Hunk #46 succeeded at 5087 (offset 22 lines).
Hunk #47 succeeded at 5096 (offset 22 lines).
patching file kernel/workqueue_internal.h
patching file lib/Kconfig
patching file lib/debugobjects.c
patching file lib/irq_poll.c
patching file lib/locking-selftest.c
patching file lib/percpu_ida.c
patching file lib/radix-tree.c
patching file lib/scatterlist.c
patching file lib/smp_processor_id.c
patching file localversion-rt
patching file mm/Kconfig
Hunk #1 succeeded at 409 (offset -1 lines).
patching file mm/backing-dev.c
Hunk #1 succeeded at 482 (offset 23 lines).
patching file mm/compaction.c
Hunk #1 succeeded at 1634 (offset 33 lines).
patching file mm/filemap.c
patching file mm/highmem.c
patching file mm/memcontrol.c
Hunk #3 succeeded at 1690 (offset 5 lines).
Hunk #4 succeeded at 1713 (offset 5 lines).
Hunk #5 succeeded at 1721 (offset 5 lines).
Hunk #6 succeeded at 1748 (offset 5 lines).
Hunk #7 succeeded at 1766 (offset 5 lines).
Hunk #8 succeeded at 1775 (offset 5 lines).
Hunk #9 succeeded at 1791 (offset 5 lines).
Hunk #10 succeeded at 1808 (offset 5 lines).
Hunk #11 succeeded at 4550 (offset 11 lines).
Hunk #12 succeeded at 5437 (offset 11 lines).
Hunk #13 FAILED at 5485.
Hunk #14 succeeded at 5663 (offset 16 lines).
Hunk #15 succeeded at 5858 (offset 16 lines).
Hunk #16 succeeded at 5899 (offset 16 lines).
1 out of 16 hunks FAILED -- saving rejects to file mm/memcontrol.c.rej
patching file mm/mmu_context.c
patching file mm/page_alloc.c
Hunk #2 succeeded at 288 (offset 1 line).
Hunk #3 succeeded at 1100 (offset 1 line).
Hunk #4 FAILED at 1110.
Hunk #5 succeeded at 1135 (offset -3 lines).
Hunk #6 succeeded at 1143 (offset -3 lines).
Hunk #7 succeeded at 1156 with fuzz 3 (offset -4 lines).
Hunk #8 succeeded at 1164 (offset -8 lines).
Hunk #9 succeeded at 1250 (offset -8 lines).
Hunk #10 succeeded at 2325 (offset 39 lines).
Hunk #11 succeeded at 2352 (offset 39 lines).
Hunk #12 succeeded at 2401 (offset 39 lines).
Hunk #13 succeeded at 2415 (offset 39 lines).
Hunk #14 succeeded at 2486 (offset 39 lines).
Hunk #15 succeeded at 2501 (offset 39 lines).
Hunk #16 succeeded at 2563 (offset 39 lines).
Hunk #17 succeeded at 2589 (offset 39 lines).
Hunk #18 succeeded at 2756 (offset 39 lines).
Hunk #19 succeeded at 2764 (offset 39 lines).
Hunk #20 succeeded at 2791 (offset 39 lines).
Hunk #21 succeeded at 2811 (offset 39 lines).
Hunk #22 succeeded at 6786 (offset 38 lines).
Hunk #23 succeeded at 7652 (offset 38 lines).
Hunk #24 succeeded at 7661 (offset 38 lines).
1 out of 24 hunks FAILED -- saving rejects to file mm/page_alloc.c.rej
patching file mm/percpu.c
Reversed (or previously applied) patch detected!  Skipping patch.
2 out of 2 hunks ignored -- saving rejects to file mm/percpu.c.rej
patching file mm/slab.h
patching file mm/slub.c
patching file mm/swap.c
Hunk #3 succeeded at 255 (offset 10 lines).
Hunk #4 succeeded at 309 (offset 10 lines).
Hunk #5 succeeded at 342 (offset 10 lines).
Hunk #6 succeeded at 364 (offset 10 lines).
Hunk #7 succeeded at 406 (offset 10 lines).
Hunk #8 succeeded at 616 (offset 17 lines).
Hunk #9 succeeded at 656 (offset 17 lines).
Hunk #10 FAILED at 659.
Hunk #11 succeeded at 698 (offset 17 lines).
Hunk #12 FAILED at 709.
2 out of 12 hunks FAILED -- saving rejects to file mm/swap.c.rej
patching file mm/swap_slots.c
Hunk #1 succeeded at 272 (offset 5 lines).
Hunk #2 succeeded at 296 (offset 5 lines).
patching file mm/truncate.c
patching file mm/vmalloc.c
patching file mm/vmscan.c
Hunk #1 succeeded at 3652 (offset -2 lines).
patching file mm/vmstat.c
patching file mm/workingset.c
Hunk #4 succeeded at 478 with fuzz 2 (offset -1 lines).
Hunk #5 succeeded at 497 (offset -1 lines).
Hunk #6 succeeded at 537 (offset -1 lines).
Hunk #7 succeeded at 545 (offset -1 lines).
patching file mm/zsmalloc.c
patching file net/Kconfig
patching file net/core/dev.c
Hunk #1 succeeded at 191 (offset 2 lines).
Hunk #2 succeeded at 214 (offset 2 lines).
Hunk #3 succeeded at 892 (offset 2 lines).
Hunk #4 succeeded at 1162 (offset 2 lines).
Hunk #5 succeeded at 1185 (offset 2 lines).
Hunk #6 succeeded at 1211 (offset 2 lines).
Hunk #7 succeeded at 1225 (offset 2 lines).
Hunk #8 succeeded at 2412 (offset 2 lines).
Hunk #9 succeeded at 2475 (offset 2 lines).
Hunk #10 succeeded at 3089 (offset 5 lines).
Hunk #11 succeeded at 3156 (offset 5 lines).
Hunk #12 succeeded at 3399 (offset 5 lines).
Hunk #13 succeeded at 3409 (offset 5 lines).
Hunk #14 succeeded at 3792 (offset 6 lines).
Hunk #15 succeeded at 3811 (offset 6 lines).
Hunk #16 succeeded at 3821 (offset 6 lines).
Hunk #17 succeeded at 3862 (offset 6 lines).
Hunk #18 succeeded at 4470 (offset 140 lines).
Hunk #19 succeeded at 4480 (offset 140 lines).
Hunk #20 succeeded at 5000 with fuzz 1 (offset 153 lines).
Hunk #21 succeeded at 5007 (offset 146 lines).
Hunk #22 succeeded at 5037 (offset 146 lines).
Hunk #23 succeeded at 5047 (offset 146 lines).
Hunk #24 succeeded at 5087 (offset 146 lines).
Hunk #25 succeeded at 5124 (offset 146 lines).
Hunk #26 succeeded at 5136 (offset 146 lines).
Hunk #27 FAILED at 5092.
Hunk #28 succeeded at 5490 with fuzz 2 (offset 142 lines).
Hunk #29 succeeded at 5534 (offset 142 lines).
Hunk #30 succeeded at 8288 with fuzz 3 (offset 172 lines).
Hunk #31 succeeded at 8605 (offset 172 lines).
1 out of 31 hunks FAILED -- saving rejects to file net/core/dev.c.rej
patching file net/core/filter.c
Hunk #1 succeeded at 1667 (offset 15 lines).
Hunk #2 succeeded at 1675 (offset 15 lines).
patching file net/core/gen_estimator.c
patching file net/core/gen_stats.c
patching file net/core/skbuff.c
patching file net/core/sock.c
Hunk #1 succeeded at 2642 (offset 101 lines).
patching file net/ipv4/icmp.c
Hunk #6 succeeded at 662 (offset -17 lines).
Hunk #7 succeeded at 751 (offset -17 lines).
Hunk #8 succeeded at 914 (offset -17 lines).
Hunk #9 succeeded at 965 (offset -17 lines).
patching file net/ipv4/sysctl_net_ipv4.c
Hunk #1 succeeded at 763 (offset 77 lines).
patching file net/ipv4/tcp_ipv4.c
Hunk #2 succeeded at 580 (offset -4 lines).
Hunk #3 succeeded at 709 (offset -4 lines).
Hunk #4 succeeded at 719 (offset -4 lines).
Hunk #5 succeeded at 797 (offset -4 lines).
Hunk #6 succeeded at 806 (offset -4 lines).
patching file net/mac80211/rx.c
Hunk #1 succeeded at 4255 (offset 26 lines).
patching file net/netfilter/core.c
patching file net/packet/af_packet.c
patching file net/rds/ib_rdma.c
patching file net/rxrpc/security.c
patching file net/sched/sch_api.c
Hunk #1 succeeded at 991 (offset 11 lines).
patching file net/sched/sch_generic.c
patching file net/sunrpc/svc_xprt.c
patching file samples/trace_events/trace-events-sample.c
patching file scripts/mkcompile_h
patching file sound/core/pcm_native.c
```

对于`Hunk #N FAILED at XXXX.`，需要查看相应的.rej文件并手动合并，解决冲突。


# 编译v4.12内核

```bash
make O=../4.12 defconfig
make O=../4.12 menuconfig
# Processor type and features  --->
#     Preemption Model (Voluntary Kernel Preemption (Desktop))  --->
#     ( ) Fully Preemptible Kernel (RT)
make O=../4.12
```

# 测试bzImage

```bash
cd ../4.12
qemu-system-x86_64 -kernel arch/x86_64/boot/bzImage -serial stdio -append "root=/dev/ram0 console=ttyAMA0  console=ttyS0"
warning: TCG doesn't support requested feature: CPUID.01H:ECX.vmx [bit 5]
[    0.000000] Linux version 4.12.0-rt10 (zhangwei@zhangwei-B85M-D3H) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #3 SMP PREEMPT RT Sat Aug 26 13:20:31 CST 2017
[    0.000000] Command line: root=/dev/ram0 console=ttyAMA0  console=ttyS0
[    0.000000] x86/fpu: x87 FPU will use FXSAVE
[    0.000000] e820: BIOS-provided physical RAM map:
[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
[    0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x0000000007fdffff] usable
[    0.000000] BIOS-e820: [mem 0x0000000007fe0000-0x0000000007ffffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff] reserved
[    0.000000] NX (Execute Disable) protection: active
[    0.000000] SMBIOS 2.8 present.
[    0.000000] DMI: QEMU Standard PC (i440FX + PIIX, 1996), BIOS Ubuntu-1.8.2-1ubuntu1 04/01/2014
[    0.000000] tsc: Fast TSC calibration using PIT
[    0.000000] e820: last_pfn = 0x7fe0 max_arch_pfn = 0x400000000
[    0.000000] x86/PAT: Configuration [0-7]: WB  WC  UC- UC  WB  WC  UC- WT  
[    0.000000] found SMP MP-table at [mem 0x000f6640-0x000f664f] mapped at [ffff9af2800f6640]
[    0.000000] Scanning 1 areas for low memory corruption
[    0.000000] ACPI: Early table checksum verification disabled
[    0.000000] ACPI: RSDP 0x00000000000F6460 000014 (v00 BOCHS )
[    0.000000] ACPI: RSDT 0x0000000007FE16EE 000034 (v01 BOCHS  BXPCRSDT 00000001 BXPC 00000001)
[    0.000000] ACPI: FACP 0x0000000007FE0C14 000074 (v01 BOCHS  BXPCFACP 00000001 BXPC 00000001)
[    0.000000] ACPI: DSDT 0x0000000007FE0040 000BD4 (v01 BOCHS  BXPCDSDT 00000001 BXPC 00000001)
[    0.000000] ACPI: FACS 0x0000000007FE0000 000040
[    0.000000] ACPI: SSDT 0x0000000007FE0C88 0009B6 (v01 BOCHS  BXPCSSDT 00000001 BXPC 00000001)
[    0.000000] ACPI: APIC 0x0000000007FE163E 000078 (v01 BOCHS  BXPCAPIC 00000001 BXPC 00000001)
[    0.000000] ACPI: HPET 0x0000000007FE16B6 000038 (v01 BOCHS  BXPCHPET 00000001 BXPC 00000001)
[    0.000000] No NUMA configuration found
[    0.000000] Faking a node at [mem 0x0000000000000000-0x0000000007fdffff]
[    0.000000] NODE_DATA(0) allocated [mem 0x07fdc000-0x07fdffff]
[    0.000000] Zone ranges:
[    0.000000]   DMA      [mem 0x0000000000001000-0x0000000000ffffff]
[    0.000000]   DMA32    [mem 0x0000000001000000-0x0000000007fdffff]
[    0.000000]   Normal   empty
[    0.000000] Movable zone start for each node
[    0.000000] Early memory node ranges
[    0.000000]   node   0: [mem 0x0000000000001000-0x000000000009efff]
[    0.000000]   node   0: [mem 0x0000000000100000-0x0000000007fdffff]
[    0.000000] Initmem setup node 0 [mem 0x0000000000001000-0x0000000007fdffff]
[    0.000000] ACPI: PM-Timer IO Port: 0x608
[    0.000000] ACPI: LAPIC_NMI (acpi_id[0xff] dfl dfl lint[0x1])
[    0.000000] IOAPIC[0]: apic_id 0, version 17, address 0xfec00000, GSI 0-23
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 5 global_irq 5 high level)
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 9 global_irq 9 high level)
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 10 global_irq 10 high level)
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 11 global_irq 11 high level)
[    0.000000] Using ACPI (MADT) for SMP configuration information
[    0.000000] ACPI: HPET id: 0x8086a201 base: 0xfed00000
[    0.000000] smpboot: Allowing 1 CPUs, 0 hotplug CPUs
[    0.000000] PM: Registered nosave memory: [mem 0x00000000-0x00000fff]
[    0.000000] PM: Registered nosave memory: [mem 0x0009f000-0x0009ffff]
[    0.000000] PM: Registered nosave memory: [mem 0x000a0000-0x000effff]
[    0.000000] PM: Registered nosave memory: [mem 0x000f0000-0x000fffff]
[    0.000000] e820: [mem 0x08000000-0xfffbffff] available for PCI devices
[    0.000000] clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1910969940391419 ns
[    0.000000] setup_percpu: NR_CPUS:64 nr_cpumask_bits:64 nr_cpu_ids:1 nr_node_ids:1
[    0.000000] percpu: Embedded 37 pages/cpu @ffff9af287c00000 s112384 r8192 d30976 u2097152
[    0.000000] Built 1 zonelists in Node order, mobility grouping on.  Total pages: 32105
[    0.000000] Policy zone: DMA32
[    0.000000] Kernel command line: root=/dev/ram0 console=ttyAMA0  console=ttyS0
[    0.000000] PID hash table entries: 512 (order: 0, 4096 bytes)
[    0.000000] Memory: 110304K/130552K available (9752K kernel code, 1369K rwdata, 2944K rodata, 1184K init, 852K bss, 20248K reserved, 0K cma-reserved)
[    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=1, Nodes=1
[    0.000000] Preemptible hierarchical RCU implementation.
[    0.000000]  RCU debugfs-based tracing is enabled.
[    0.000000]  RCU restricting CPUs from NR_CPUS=64 to nr_cpu_ids=1.
[    0.000000]  RCU kthread priority: 1.
[    0.000000] RCU: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=1
[    0.000000] NR_IRQS:4352 nr_irqs:256 16
[    0.000000] Console: colour VGA+ 80x25
[    0.000000] console [ttyS0] enabled
[    0.000000] clocksource: hpet: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604467 ns
[    0.000000] tsc: Fast TSC calibration using PIT
[    0.002000] tsc: Detected 3990.696 MHz processor
[    0.003170] Calibrating delay loop (skipped), value calculated using timer frequency.. 7981.39 BogoMIPS (lpj=3990696)
[    0.003239] pid_max: default: 32768 minimum: 301
[    0.003315] ACPI: Core revision 20170303
[    0.017252] ACPI: 2 ACPI AML tables successfully acquired and loaded
[    0.017805] Security Framework initialized
[    0.017884] SELinux:  Initializing.
[    0.018541] Dentry cache hash table entries: 16384 (order: 6, 262144 bytes)
[    0.018807] Inode-cache hash table entries: 8192 (order: 4, 65536 bytes)
[    0.019053] Mount-cache hash table entries: 512 (order: 0, 4096 bytes)
[    0.019071] Mountpoint-cache hash table entries: 512 (order: 0, 4096 bytes)
[    0.026748] mce: CPU supports 10 MCE banks
[    0.027292] Last level iTLB entries: 4KB 0, 2MB 0, 4MB 0
[    0.027298] Last level dTLB entries: 4KB 0, 2MB 0, 4MB 0, 1GB 0
[    0.185690] Freeing SMP alternatives memory: 32K
[    0.191702] smpboot: Max logical packages: 1
[    0.196000] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1
[    0.206000] smpboot: CPU0: AMD QEMU Virtual CPU version 2.5+ (family: 0x6, model: 0x6, stepping: 0x3)
[    0.213531] Performance Events: PMU not available due to virtualization, using software events only.
[    0.229143] Huh? What family is it: 0x6?!
[    0.231083] smp: Bringing up secondary CPUs ...
[    0.231238] smp: Brought up 1 node, 1 CPU
[    0.231361] smpboot: Total of 1 processors activated (7981.39 BogoMIPS)
[    0.233785] sched_clock: Marking stable (233000000, 0)->(338812373, -105812373)
[    0.239049] devtmpfs: initialized
[    0.247004] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1911260446275000 ns
[    0.247366] futex hash table entries: 256 (order: 3, 32768 bytes)
[    0.248650] RTC time:  6:26:17, date: 08/26/17
[    0.251854] NET: Registered protocol family 16
[    0.259946] kworker/u2:0 (20) used greatest stack depth: 14360 bytes left
[    0.271976] kworker/u2:1 (27) used greatest stack depth: 13848 bytes left
[    0.273900] cpuidle: using governor menu
[    0.274165] PCCT header not found.
[    0.274833] ACPI: bus type PCI registered
[    0.276888] PCI: Using configuration type 1 for base access
[    0.393918] BUG: unable to handle kernel NULL pointer dereference at 0000000000000068
[    0.394203] IP: __try_to_take_rt_mutex+0x16a/0x1f0
[    0.394227] PGD 0 
[    0.394244] P4D 0 
[    0.394254] 
[    0.394287] Oops: 0000 [#1] PREEMPT SMP
[    0.394341] Modules linked in:
[    0.394449] CPU: 0 PID: 287 Comm: kworker/u2:1 Not tainted 4.12.0-rt10 #3
[    0.394457] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS Ubuntu-1.8.2-1ubuntu1 04/01/2014
[    0.394487] task: ffff9af287218000 task.stack: ffffbb26c0650000
[    0.394508] RIP: 0010:__try_to_take_rt_mutex+0x16a/0x1f0
[    0.394515] RSP: 0018:ffffbb26c0653d00 EFLAGS: 00000002
[    0.394529] RAX: ffffbb26c065be18 RBX: ffff9af287218000 RCX: 0000000000000000
[    0.394535] RDX: 0000000000000078 RSI: 0000000000000078 RDI: ffffbb26c0653d50
[    0.394542] RBP: ffffbb26c0653d60 R08: 0000000000000001 R09: ffffffff92c050d8
[    0.394548] R10: 0000000000000001 R11: ffffbb26c0653e1e R12: ffffffff92c050c0
[    0.394554] R13: ffffbb26c0653dc0 R14: 0000000000000286 R15: ffff9af287218000
[    0.394599] FS:  0000000000000000(0000) GS:ffff9af287c00000(0000) knlGS:0000000000000000
[    0.394608] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[    0.394623] CR2: 0000000000000068 CR3: 000000000421a000 CR4: 00000000000006f0
[    0.394663] Call Trace:
[    0.394952]  rt_spin_lock_slowlock_locked+0x32/0x2d0
[    0.395006]  ? __d_lookup+0x82/0x140
[    0.395015]  ? preempt_count_add+0x99/0xb0
[    0.395023]  rt_spin_lock_slowlock+0x43/0x60
[    0.395041]  ? _raw_spin_lock+0x12/0x40
[    0.395062]  ? task_rq_lock+0x53/0xe0
[    0.395081]  __rt_spin_lock+0x20/0x30
[    0.395088]  rt_read_lock+0x15/0x20
[    0.395094]  rt_write_lock+0x9/0x10
[    0.395102]  release_task+0x44/0x470
[    0.395113]  do_exit+0x6a4/0xbc0
[    0.395119]  ? kfree+0x19e/0x1b0
[    0.395129]  call_usermodehelper_exec_async+0x137/0x140
[    0.395135]  ? umh_complete+0x40/0x40
[    0.395142]  ret_from_fork+0x22/0x30
[    0.395177] Code: 4c 3b 60 38 48 89 4d e8 0f 85 96 00 00 00 48 39 f0 0f 84 1e ff ff ff 8b 70 44 39 f2 0f 8c 13 ff ff ff 85 d2 78 71 45 85 c0 74 20 <83> 3c 25 68 00 00 00 63 7e 16 39 f2 75 12 85 d2 0f 89 f4 fe ff 
[    0.395338] RIP: __try_to_take_rt_mutex+0x16a/0x1f0 RSP: ffffbb26c0653d00
[    0.395351] CR2: 0000000000000068
```

检查`__try_to_take_rt_mutex`函数，并未发现异常，将v4.11.12-rt10和v4.12代码进行对比，发现

```diff
--- linux-stable-4.12/kernel/locking/rtmutex.c
+++ linux-stable-4.11.12/kernel/locking/rtmutex.c
-#define task_to_waiter(p) \
-   &(struct rt_mutex_waiter){ .prio = (p)->prio, .deadline = (p)->dl.deadline }
+#define task_to_waiter(p) &(struct rt_mutex_waiter) \
+   { .prio = (p)->prio, .deadline = (p)->dl.deadline, .task = (p) }
```

很可能是由于v4.12中未设置`.task = (p)`导致的NULL pointer dereference，修改后重新编译运行，问题消失

```bash
qemu-system-x86_64 -kernel arch/x86_64/boot/bzImage -initrd ~/rt-patch-analysis/rt-linux-lkp/initrd_lkp.img -serial stdio -append "root=/dev/ram0 console=ttyAMA0  console=ttyS0" 
warning: TCG doesn't support requested feature: CPUID.01H:ECX.vmx [bit 5]
[    0.000000] Linux version 4.12.0-rt10 (zhangwei@zhangwei-B85M-D3H) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #5 SMP PREEMPT RT Sat Aug 26 14:38:05 CST 2017
[    0.000000] Command line: root=/dev/ram0 console=ttyAMA0  console=ttyS0
[    0.000000] x86/fpu: x87 FPU will use FXSAVE
[    0.000000] e820: BIOS-provided physical RAM map:
[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
[    0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x0000000007fdffff] usable
[    0.000000] BIOS-e820: [mem 0x0000000007fe0000-0x0000000007ffffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff] reserved
[    0.000000] NX (Execute Disable) protection: active
[    0.000000] SMBIOS 2.8 present.
[    0.000000] DMI: QEMU Standard PC (i440FX + PIIX, 1996), BIOS Ubuntu-1.8.2-1ubuntu1 04/01/2014
[    0.000000] tsc: Fast TSC calibration using PIT
[    0.000000] e820: last_pfn = 0x7fe0 max_arch_pfn = 0x400000000
[    0.000000] x86/PAT: Configuration [0-7]: WB  WC  UC- UC  WB  WC  UC- WT  
[    0.000000] found SMP MP-table at [mem 0x000f6640-0x000f664f] mapped at [ffffa041000f6640]
[    0.000000] Scanning 1 areas for low memory corruption
[    0.000000] RAMDISK: [mem 0x07e85000-0x07fdffff]
[    0.000000] ACPI: Early table checksum verification disabled
[    0.000000] ACPI: RSDP 0x00000000000F6460 000014 (v00 BOCHS )
[    0.000000] ACPI: RSDT 0x0000000007FE16EE 000034 (v01 BOCHS  BXPCRSDT 00000001 BXPC 00000001)
[    0.000000] ACPI: FACP 0x0000000007FE0C14 000074 (v01 BOCHS  BXPCFACP 00000001 BXPC 00000001)
[    0.000000] ACPI: DSDT 0x0000000007FE0040 000BD4 (v01 BOCHS  BXPCDSDT 00000001 BXPC 00000001)
[    0.000000] ACPI: FACS 0x0000000007FE0000 000040
[    0.000000] ACPI: SSDT 0x0000000007FE0C88 0009B6 (v01 BOCHS  BXPCSSDT 00000001 BXPC 00000001)
[    0.000000] ACPI: APIC 0x0000000007FE163E 000078 (v01 BOCHS  BXPCAPIC 00000001 BXPC 00000001)
[    0.000000] ACPI: HPET 0x0000000007FE16B6 000038 (v01 BOCHS  BXPCHPET 00000001 BXPC 00000001)
[    0.000000] No NUMA configuration found
[    0.000000] Faking a node at [mem 0x0000000000000000-0x0000000007fdffff]
[    0.000000] NODE_DATA(0) allocated [mem 0x07e81000-0x07e84fff]
[    0.000000] Zone ranges:
[    0.000000]   DMA      [mem 0x0000000000001000-0x0000000000ffffff]
[    0.000000]   DMA32    [mem 0x0000000001000000-0x0000000007fdffff]
[    0.000000]   Normal   empty
[    0.000000] Movable zone start for each node
[    0.000000] Early memory node ranges
[    0.000000]   node   0: [mem 0x0000000000001000-0x000000000009efff]
[    0.000000]   node   0: [mem 0x0000000000100000-0x0000000007fdffff]
[    0.000000] Initmem setup node 0 [mem 0x0000000000001000-0x0000000007fdffff]
[    0.000000] ACPI: PM-Timer IO Port: 0x608
[    0.000000] ACPI: LAPIC_NMI (acpi_id[0xff] dfl dfl lint[0x1])
[    0.000000] IOAPIC[0]: apic_id 0, version 17, address 0xfec00000, GSI 0-23
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 5 global_irq 5 high level)
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 9 global_irq 9 high level)
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 10 global_irq 10 high level)
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 11 global_irq 11 high level)
[    0.000000] Using ACPI (MADT) for SMP configuration information
[    0.000000] ACPI: HPET id: 0x8086a201 base: 0xfed00000
[    0.000000] smpboot: Allowing 1 CPUs, 0 hotplug CPUs
[    0.000000] PM: Registered nosave memory: [mem 0x00000000-0x00000fff]
[    0.000000] PM: Registered nosave memory: [mem 0x0009f000-0x0009ffff]
[    0.000000] PM: Registered nosave memory: [mem 0x000a0000-0x000effff]
[    0.000000] PM: Registered nosave memory: [mem 0x000f0000-0x000fffff]
[    0.000000] e820: [mem 0x08000000-0xfffbffff] available for PCI devices
[    0.000000] clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1910969940391419 ns
[    0.000000] setup_percpu: NR_CPUS:64 nr_cpumask_bits:64 nr_cpu_ids:1 nr_node_ids:1
[    0.000000] percpu: Embedded 37 pages/cpu @ffffa04107c00000 s112384 r8192 d30976 u2097152
[    0.000000] Built 1 zonelists in Node order, mobility grouping on.  Total pages: 32105
[    0.000000] Policy zone: DMA32
[    0.000000] Kernel command line: root=/dev/ram0 console=ttyAMA0  console=ttyS0
[    0.000000] PID hash table entries: 512 (order: 0, 4096 bytes)
[    0.000000] Memory: 108916K/130552K available (9752K kernel code, 1369K rwdata, 2944K rodata, 1184K init, 852K bss, 21636K reserved, 0K cma-reserved)
[    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=1, Nodes=1
[    0.000000] Preemptible hierarchical RCU implementation.
[    0.000000]  RCU debugfs-based tracing is enabled.
[    0.000000]  RCU restricting CPUs from NR_CPUS=64 to nr_cpu_ids=1.
[    0.000000]  RCU kthread priority: 1.
[    0.000000] RCU: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=1
[    0.000000] NR_IRQS:4352 nr_irqs:256 16
[    0.000000] Console: colour VGA+ 80x25
[    0.000000] console [ttyS0] enabled
[    0.000000] clocksource: hpet: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604467 ns
[    0.000000] tsc: Fast TSC calibration using PIT
[    0.002000] tsc: Detected 3990.955 MHz processor
[    0.003368] Calibrating delay loop (skipped), value calculated using timer frequency.. 7981.91 BogoMIPS (lpj=3990955)
[    0.003430] pid_max: default: 32768 minimum: 301
[    0.003514] ACPI: Core revision 20170303
[    0.016038] ACPI: 2 ACPI AML tables successfully acquired and loaded
[    0.016730] Security Framework initialized
[    0.016837] SELinux:  Initializing.
[    0.017669] Dentry cache hash table entries: 16384 (order: 6, 262144 bytes)
[    0.017878] Inode-cache hash table entries: 8192 (order: 4, 65536 bytes)
[    0.018133] Mount-cache hash table entries: 512 (order: 0, 4096 bytes)
[    0.018149] Mountpoint-cache hash table entries: 512 (order: 0, 4096 bytes)
[    0.025030] mce: CPU supports 10 MCE banks
[    0.025645] Last level iTLB entries: 4KB 0, 2MB 0, 4MB 0
[    0.025651] Last level dTLB entries: 4KB 0, 2MB 0, 4MB 0, 1GB 0
[    0.186349] Freeing SMP alternatives memory: 32K
[    0.192433] smpboot: Max logical packages: 1
[    0.196000] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1
[    0.206000] smpboot: CPU0: AMD QEMU Virtual CPU version 2.5+ (family: 0x6, model: 0x6, stepping: 0x3)
[    0.211494] Performance Events: PMU not available due to virtualization, using software events only.
[    0.227063] Huh? What family is it: 0x6?!
[    0.229083] smp: Bringing up secondary CPUs ...
[    0.229210] smp: Brought up 1 node, 1 CPU
[    0.229325] smpboot: Total of 1 processors activated (7981.91 BogoMIPS)
[    0.231862] sched_clock: Marking stable (231000000, 0)->(331552293, -100552293)
[    0.237629] devtmpfs: initialized
[    0.243674] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1911260446275000 ns
[    0.243933] futex hash table entries: 256 (order: 3, 32768 bytes)
[    0.245221] RTC time:  6:39:23, date: 08/26/17
[    0.248298] NET: Registered protocol family 16
[    0.259585] kworker/u2:1 (21) used greatest stack depth: 14728 bytes left
[    0.259847] kworker/u2:0 (20) used greatest stack depth: 14360 bytes left
[    0.266949] cpuidle: using governor menu
[    0.267334] PCCT header not found.
[    0.267976] ACPI: bus type PCI registered
[    0.269826] PCI: Using configuration type 1 for base access
[    0.279675] kworker/u2:1 (50) used greatest stack depth: 14256 bytes left
[    0.280391] kworker/u2:1 (55) used greatest stack depth: 13848 bytes left
[    0.422414] HugeTLB registered 2 MB page size, pre-allocated 0 pages
[    0.426730] ACPI: Added _OSI(Module Device)
[    0.426837] ACPI: Added _OSI(Processor Device)
[    0.426933] ACPI: Added _OSI(3.0 _SCP Extensions)
[    0.427295] ACPI: Added _OSI(Processor Aggregator Device)
[    0.442586] ACPI: Interpreter enabled
[    0.443250] ACPI: (supports S0 S3 S4 S5)
[    0.443349] ACPI: Using IOAPIC for interrupt routing
[    0.443881] PCI: Using host bridge windows from ACPI; if necessary, use "pci=nocrs" and report a bug
[    0.499428] ACPI: PCI Root Bridge [PCI0] (domain 0000 [bus 00-ff])
[    0.499750] acpi PNP0A03:00: _OSC: OS supports [ASPM ClockPM Segments MSI]
[    0.500454] acpi PNP0A03:00: _OSC failed (AE_NOT_FOUND); disabling ASPM
[    0.500809] acpi PNP0A03:00: fail to add MMCONFIG information, can't access extended PCI configuration space under this bridge.
[    0.502624] PCI host bridge to bus 0000:00
[    0.502804] pci_bus 0000:00: root bus resource [io  0x0000-0x0cf7 window]
[    0.502937] pci_bus 0000:00: root bus resource [io  0x0d00-0xffff window]
[    0.503197] pci_bus 0000:00: root bus resource [mem 0x000a0000-0x000bffff window]
[    0.503312] pci_bus 0000:00: root bus resource [mem 0x08000000-0xfebfffff window]
[    0.503481] pci_bus 0000:00: root bus resource [bus 00-ff]
[    0.511595] pci 0000:00:01.1: legacy IDE quirk: reg 0x10: [io  0x01f0-0x01f7]
[    0.511764] pci 0000:00:01.1: legacy IDE quirk: reg 0x14: [io  0x03f6]
[    0.511882] pci 0000:00:01.1: legacy IDE quirk: reg 0x18: [io  0x0170-0x0177]
[    0.512172] pci 0000:00:01.1: legacy IDE quirk: reg 0x1c: [io  0x0376]
[    0.513753] pci 0000:00:01.3: quirk: [io  0x0600-0x063f] claimed by PIIX4 ACPI
[    0.513892] pci 0000:00:01.3: quirk: [io  0x0700-0x070f] claimed by PIIX4 SMB
[    0.535654] ACPI: PCI Interrupt Link [LNKA] (IRQs 5 *10 11)
[    0.536624] ACPI: PCI Interrupt Link [LNKB] (IRQs 5 *10 11)
[    0.537865] ACPI: PCI Interrupt Link [LNKC] (IRQs 5 10 *11)
[    0.538811] ACPI: PCI Interrupt Link [LNKD] (IRQs 5 10 *11)
[    0.539552] ACPI: PCI Interrupt Link [LNKS] (IRQs *9)
[    0.542326] ACPI: Enabled 16 GPEs in block 00 to 0F
[    0.545663] pci 0000:00:02.0: vgaarb: setting as boot VGA device
[    0.545810] pci 0000:00:02.0: vgaarb: VGA device added: decodes=io+mem,owns=io+mem,locks=none
[    0.546257] pci 0000:00:02.0: vgaarb: bridge control possible
[    0.546360] vgaarb: loaded
[    0.548562] SCSI subsystem initialized
[    0.550878] ACPI: bus type USB registered
[    0.551829] usbcore: registered new interface driver usbfs
[    0.552683] usbcore: registered new interface driver hub
[    0.553177] usbcore: registered new device driver usb
[    0.556882] pps_core: LinuxPPS API ver. 1 registered
[    0.557196] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
[    0.557516] PTP clock support registered
[    0.558794] EDAC MC: Ver: 3.0.0
[    0.561635] Advanced Linux Sound Architecture Driver Initialized.
[    0.562572] PCI: Using ACPI for IRQ routing
[    0.573479] NetLabel: Initializing
[    0.573610] NetLabel:  domain hash size = 128
[    0.573697] NetLabel:  protocols = UNLABELED CIPSOv4 CALIPSO
[    0.574478] NetLabel:  unlabeled traffic allowed by default
[    0.575765] HPET: 3 timers in total, 0 timers will be used for per-cpu timer
[    0.576152] hpet0: at MMIO 0xfed00000, IRQs 2, 8, 0
[    0.576296] hpet0: 3 comparators, 64-bit 100.000000 MHz counter
[    0.580708] clocksource: Switched to clocksource hpet
[    0.770488] VFS: Disk quotas dquot_6.6.0
[    0.770895] VFS: Dquot-cache hash table entries: 512 (order 0, 4096 bytes)
[    0.776903] pnp: PnP ACPI init
[    0.786392] pnp: PnP ACPI: found 6 devices
[    0.845754] clocksource: acpi_pm: mask: 0xffffff max_cycles: 0xffffff, max_idle_ns: 2085701024 ns
[    0.847059] NET: Registered protocol family 2
[    0.850545] TCP established hash table entries: 1024 (order: 1, 8192 bytes)
[    0.850981] TCP bind hash table entries: 1024 (order: 3, 57344 bytes)
[    0.851207] TCP: Hash tables configured (established 1024 bind 1024)
[    0.851980] UDP hash table entries: 256 (order: 3, 32768 bytes)
[    0.852261] UDP-Lite hash table entries: 256 (order: 3, 32768 bytes)
[    0.853406] NET: Registered protocol family 1
[    0.858337] RPC: Registered named UNIX socket transport module.
[    0.858512] RPC: Registered udp transport module.
[    0.858599] RPC: Registered tcp transport module.
[    0.858772] RPC: Registered tcp NFSv4.1 backchannel transport module.
[    0.858947] pci 0000:00:00.0: Limiting direct PCI/PCI transfers
[    0.859092] pci 0000:00:01.0: PIIX3: Enabling Passive Release
[    0.859288] pci 0000:00:01.0: Activating ISA DMA hang workarounds
[    0.859554] pci 0000:00:02.0: Video device with shadowed ROM at [mem 0x000c0000-0x000dffff]
[    0.866539] Unpacking initramfs...
[    0.999517] Freeing initrd memory: 1388K
[    1.003159] Scanning for low memory corruption every 60 seconds
[    1.012043] audit: initializing netlink subsys (disabled)
[    1.014954] audit: type=2000 audit(1503729563.012:1): state=initialized audit_enabled=0 res=1
[    1.017495] workingset: timestamp_bits=56 max_order=15 bucket_order=0
[    1.076471] NFS: Registering the id_resolver key type
[    1.077220] Key type id_resolver registered
[    1.077320] Key type id_legacy registered
[    1.096279] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 250)
[    1.096490] io scheduler noop registered
[    1.096591] io scheduler deadline registered
[    1.098126] io scheduler cfq registered (default)
[    1.098236] io scheduler mq-deadline registered
[    1.098324] io scheduler kyber registered
[    1.106579] input: Power Button as /devices/LNXSYSTM:00/LNXPWRBN:00/input/input0
[    1.107378] ACPI: Power Button [PWRF]
[    1.115378] Serial: 8250/16550 driver, 4 ports, IRQ sharing enabled
[    1.137882] 00:05: ttyS0 at I/O 0x3f8 (irq = 4, base_baud = 115200) is a 16550A
[    1.148599] Non-volatile memory driver v1.3
[    1.149480] Linux agpgart interface v0.103
[    1.191623] loop: module loaded
[    1.208546] scsi host0: ata_piix
[    1.213143] scsi host1: ata_piix
[    1.214091] ata1: PATA max MWDMA2 cmd 0x1f0 ctl 0x3f6 bmdma 0xc040 irq 14
[    1.214231] ata2: PATA max MWDMA2 cmd 0x170 ctl 0x376 bmdma 0xc048 irq 15
[    1.217453] e100: Intel(R) PRO/100 Network Driver, 3.5.24-k2-NAPI
[    1.217575] e100: Copyright(c) 1999-2006 Intel Corporation
[    1.217993] e1000: Intel(R) PRO/1000 Network Driver - version 7.3.21-k8-NAPI
[    1.218116] e1000: Copyright (c) 1999-2006 Intel Corporation.
[    1.378797] ata2.00: ATAPI: QEMU DVD-ROM, 2.5+, max UDMA/100
[    1.379883] ata2.00: configured for MWDMA2
[    1.400588] scsi 1:0:0:0: CD-ROM            QEMU     QEMU DVD-ROM     2.5+ PQ: 0 ANSI: 5
[    1.420795] sr 1:0:0:0: [sr0] scsi3-mmc drive: 4x/4x cd/rw xa/form2 tray
[    1.420880] cdrom: Uniform CD-ROM driver Revision: 3.20
[    1.425328] sr 1:0:0:0: Attached scsi generic sg0 type 5
[    1.974147] ACPI: PCI Interrupt Link [LNKC] enabled at IRQ 11
[    2.016804] tsc: Refined TSC clocksource calibration: 3990.981 MHz
[    2.017011] clocksource: tsc: mask: 0xffffffffffffffff max_cycles: 0x730e299016d, max_idle_ns: 881590412744 ns
[    2.259322] e1000 0000:00:03.0 eth0: (PCI:33MHz:32-bit) 52:54:00:12:34:56
[    2.259874] e1000 0000:00:03.0 eth0: Intel(R) PRO/1000 Network Connection
[    2.260316] e1000e: Intel(R) PRO/1000 Network Driver - 3.2.6-k
[    2.260423] e1000e: Copyright(c) 1999 - 2015 Intel Corporation.
[    2.261257] sky2: driver version 1.30
[    2.265185] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
[    2.265339] ehci-pci: EHCI PCI platform driver
[    2.266369] ohci_hcd: USB 1.1 'Open' Host Controller (OHCI) Driver
[    2.266577] ohci-pci: OHCI PCI platform driver
[    2.268261] uhci_hcd: USB Universal Host Controller Interface driver
[    2.269128] usbcore: registered new interface driver usblp
[    2.269475] usbcore: registered new interface driver usb-storage
[    2.270940] i8042: PNP: PS/2 Controller [PNP0303:KBD,PNP0f13:MOU] at 0x60,0x64 irq 1,12
[    2.275014] serio: i8042 KBD port at 0x60,0x64 irq 1
[    2.275223] serio: i8042 AUX port at 0x60,0x64 irq 12
[    2.280066] rtc_cmos 00:00: RTC can wake from S4
[    2.281279] input: AT Translated Set 2 keyboard as /devices/platform/i8042/serio0/input/input1
[    2.284991] rtc_cmos 00:00: rtc core: registered rtc_cmos as rtc0
[    2.289629] rtc_cmos 00:00: alarms up to one day, 114 bytes nvram, hpet irqs
[    2.294047] device-mapper: ioctl: 4.35.0-ioctl (2016-06-23) initialised: dm-devel@redhat.com
[    2.294948] hidraw: raw HID events driver (C) Jiri Kosina
[    2.308542] usbcore: registered new interface driver usbhid
[    2.309377] usbhid: USB HID core driver
[    2.319085] Netfilter messages via NETLINK v0.30.
[    2.322408] nf_conntrack version 0.5.0 (1024 buckets, 4096 max)
[    2.324249] ctnetlink v0.93: registering with nfnetlink.
[    2.326939] ip_tables: (C) 2000-2006 Netfilter Core Team
[    2.328109] Initializing XFRM netlink socket
[    2.329814] NET: Registered protocol family 10
[    2.336548] Segment Routing with IPv6
[    2.337485] ip6_tables: (C) 2000-2006 Netfilter Core Team
[    2.339155] sit: IPv6, IPv4 and MPLS over IPv4 tunneling driver
[    2.341587] NET: Registered protocol family 17
[    2.342180] Key type dns_resolver registered
[    2.349340] registered taskstats version 1
[    2.355632]   Magic number: 13:732:671
[    2.356316] console [netcon0] enabled
[    2.356421] netconsole: network logging started
[    2.358222] ALSA device list:
[    2.358299]   No soundcards found.
[    2.396358] Freeing unused kernel memory: 1184K
[    2.396502] Write protecting the kernel read-only data: 14336k
[    2.400818] Freeing unused kernel memory: 468K
[    2.416969] Freeing unused kernel memory: 1152K
Linux (none) 4.12.0-rt10 #5 SMP PREEMPT RT Sat Aug 26 14:38:05 CST 2017 x86_64 GNU/Linux
[    2.930013] input: ImExPS/2 Generic Explorer Mouse as /devices/platform/i8042/serio1/input/input3
[    3.026118] clocksource: Switched to clocksource tsc
Sat Aug 26 06:39:30 UTC 2017
root=/dev/ram0 console=ttyAMA0  console=ttyS0
Sat Aug 26 06:39:32 UTC 2017
PID   USER     TIME   COMMAND
    1 0          0:01 {init} /sh /init
    2 0          0:00 [kthreadd]
    3 0          0:00 [kworker/0:0]
    4 0          0:00 [kworker/0:0H]
    5 0          0:00 [kworker/u2:0]
    6 0          0:00 [mm_percpu_wq]
    7 0          0:00 [ksoftirqd/0]
    8 0          0:00 [ktimersoftd/0]
    9 0          0:00 [rcu_preempt]
   10 0          0:00 [rcu_sched]
   11 0          0:00 [rcub/0]
   12 0          0:00 [rcuc/0]
   13 0          0:00 [kswork]
   14 0          0:00 [posixcputmr/0]
   15 0          0:00 [migration/0]
   16 0          0:00 [cpuhp/0]
   17 0          0:00 [kdevtmpfs]
   18 0          0:00 [netns]
   19 0          0:00 [kworker/u2:1]
   33 0          0:00 [kworker/0:1]
  417 0          0:00 [oom_reaper]
  418 0          0:00 [writeback]
  420 0          0:00 [kcompactd0]
  421 0          0:00 [crypto]
  422 0          0:00 [bioset]
  424 0          0:00 [kblockd]
  426 0          0:00 [irq/9-acpi]
  505 0          0:00 [ata_sff]
  525 0          0:00 [md]
  528 0          0:00 [edac-poller]
  540 0          0:00 [cfg80211]
  633 0          0:00 [rpciod]
  634 0          0:00 [xprtiod]
  650 0          0:00 [kauditd]
  656 0          0:00 [kswapd0]
  730 0          0:00 [bioset]
  745 0          0:00 [nfsiod]
  792 0          0:00 [acpi_thermal_pm]
  819 0          0:00 [bioset]
  822 0          0:00 [bioset]
  825 0          0:00 [bioset]
  828 0          0:00 [bioset]
  831 0          0:00 [bioset]
  834 0          0:00 [bioset]
  837 0          0:00 [bioset]
  840 0          0:00 [bioset]
  850 0          0:00 [irq/14-ata_piix]
  851 0          0:00 [irq/15-ata_piix]
  860 0          0:00 [scsi_eh_0]
  861 0          0:00 [scsi_tmf_0]
  864 0          0:00 [scsi_eh_1]
  865 0          0:00 [scsi_tmf_1]
  868 0          0:00 [kworker/u2:2]
  869 0          0:00 [kworker/u2:3]
  876 0          0:00 [bioset]
  881 0          0:00 [kworker/0:1H]
  882 0          0:00 [kworker/0:2]
  908 0          0:00 [irq/12-i8042]
  909 0          0:00 [irq/1-i8042]
  922 0          0:00 [irq/8-rtc0]
  964 0          0:00 [kworker/0:3]
  970 0          0:00 [ipv6_addrconf]
  980 0          0:00 [irq/4-ttyS0]
  998 0          0:00 ps aux
[   12.722696] ps (998) used greatest stack depth: 13736 bytes left
Sat Aug 26 06:39:34 UTC 2017
[   13.445367] ACPI: Preparing to enter system sleep state S5
[   13.446120] reboot: Power down
```
