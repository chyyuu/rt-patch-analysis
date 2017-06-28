#!/bin/bash

function conv_ascii() {
    iconv -f iso-8859-1 -t ASCII -o tmp -c $1 && mv tmp $1
}

# Some patches in 2.6.x has the same subjects
sed "s/i386: prepare sharing the hpet code with x86_64/i386: add x8664 specific hpet bits/g" -i 2.6.23/i386-hpet-add-x8664-hpet-bits.patch
sed "s/i386: prepare sharing the PIT code/x86_64: use i386 i8253.h/g" -i 2.6.23/x86_64-use-i386-i8253-h.patch

sed "s/Fix TASKLET_STATE_SCHED WARN_ON()/More Fixes to TASKLET_STATE_SCHED WARN_ON()/g" -i 2.6.22/tasklet-more-fixes.patch
sed "s/Fix TASKLET_STATE_SCHED WARN_ON()/More Fixes to TASKLET_STATE_SCHED WARN_ON()/g" -i 2.6.23/tasklet-more-fixes.patch
sed "s/Fix TASKLET_STATE_SCHED WARN_ON()/More Fixes to TASKLET_STATE_SCHED WARN_ON()/g" -i 2.6.24/tasklet-more-fixes.patch
sed "s/Fix TASKLET_STATE_SCHED WARN_ON()/More Fixes to TASKLET_STATE_SCHED WARN_ON()/g" -i 2.6.25/tasklet-more-fixes.patch

sed "s/handle accurate time keeping over long/Fixup merge between xtime_cache and timekeeping starvation fix/g" -i 2.6.24/time-accumulate-offset-fix.patch
sed "s/    delays//g" -i 2.6.24/time-accumulate-offset-fix.patch

sed "s/Subject:/Subject: x86:/g" -i 2.6.24/mcount-add-time-notrace-annotations.patch

sed "s/rt\.fix/lockdep: fix compat_sema_init/g" -i 2.6.29/lockdep-compat-sema-fix.patch
sed "s/rt\.fix/x86: fix sparse irq vector/g" -i 2.6.29/x86-vector-sparse-irq-fix.patch

# Duplicate patches

rm -f 2.6.24/rt-powerpc-workarounds.patch                   # Duplicate of ppc-hacks-to-allow-rt-to-run-kernbench.patch
rm -f 2.6.24/sched-root-domain-backport.patch               # Duplicate of dynamically-update-root-domain-span-online-maps.patch
rm -f 2.6.24/local-irq-enable-safe-for-irqs-disabled.patch  # Duplicate of no-warning-for-irqs-disabled-in-local-bh-enable.patch
rm -f 2.6.24/time-accumulate-ppc.patch                      # Duplicate of time-accumulate-over-delay.patch
rm -f 2.6.24/timekeeping-add-cycle-monotonic.patch          # Duplicate of timekeeping-add-cycle-raw-for-actual-incrementation.patch
rm -f 2.6.29/origin.patch                                   # The merge of all the other patches

# Drop non-ascii characters
conv_ascii 2.6.25/timer-warning-fix.patch
conv_ascii 2.6.26/timer-warning-fix.patch
conv_ascii 2.6.29/preempt-realtimer-timer-non-rt-warning-fixes.patch

conv_ascii 3.2/tasklist-lock-fix-section-conflict.patch
conv_ascii 3.4/tasklist-lock-fix-section-conflict.patch
conv_ascii 3.6/tasklist-lock-fix-section-conflict.patch
conv_ascii 3.8/tasklist-lock-fix-section-conflict.patch
conv_ascii 3.10/tasklist-lock-fix-section-conflict.patch

# 'futex_atomic_cmpxchg_inatomic' mistakenly written as 'futex_atomic_op_inuser'
sed "s/futex_atomic_op_inuser/futex_atomic_cmpxchg_inatomic/g" -i 4.1/0009-futex-UP-futex_atomic_cmpxchg_inatomic-relies-on-dis.patch

# 'uaccess' mistakenly written as 'futex'
sed "s/futex/uaccess/g" -i 4.1/0003-uaccess-clarify-that-uaccess-may-only-sleep-if-pagef.patch

# 'pid.h: include atomic.h' mistakenly written as 'wait.h: include atomic.h'
sed "s/wait\.h/pid\.h/g" -i 4.4/pid.h-include-atomic.h.patch
sed "s/wait\.h/pid\.h/g" -i 4.6/pid.h-include-atomic.h.patch
