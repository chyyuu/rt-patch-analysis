- i386-pit-stop-only-when-in-periodic-or-oneshot-mode.patch 
  > I don't think this patch necessary, actually it doesn't change anything
  - 8253
    - [8253](https://en.wikipedia.org/wiki/Intel_8253)
      - programmable interval timers, used in x86 systems
      - 8254: superset of 8323 with higher clock speed ratings
      - Has three counters(0, 1 and 2), called channels, able to be programmed to operate in one of six modes. They can perform independently.
      - Assigned to IRQ-0(highest priority hardware interrupt).
      - Each has two input pins - "CLK" and "GATE", and one output pins - "OUT"
      - *More information about modes and program hints*

- clockevents-fix-device-replacement.patch
  > Confused of the type, add an "else" statement, maybe bugfix?
  - The only change in the patch is ```tick_broadcast_mask```, it is cleared.
  - ```tick_broadcast_mask``` is the bitmap which represents list of processors that are in a sleeping mode.
  - Ref
    - [Linux时间子系统（十四）tick broadcast framework(中文)](http://www.wowotech.net/timer_subsystem/tick-broadcast-framework.html)
    - [Tick broadcast framework and dyntick](https://0xax.gitbooks.io/linux-insides/content/Timers/timers-3.html)
    - Sometimes, a idle cpu could not wake itself up with its timer, so a outside tick broadcast mechanism is needed.

- barrier.patch
  > I used to learned it in Parallel Computing, it is quite different here.
  > I think it is a new feature rather than perf, as no change but add some functions
  - check ```smp_rmb/wmb``` especially
  - Ref
    - [Linux Document](https://github.com/torvalds/linux/blob/master/Documentation/memory-barriers.txt)
    - //TODO linux ```READ_ONCE()``` & ```WRITE_ONCE()``` macros
    - //TODO C bitfield
      - [C language Ref in msdn](https://msdn.microsoft.com/en-us/library/yszfawxh(VS.80).aspx)
      > A good doc for many languages and compiler

- cpuidle_last_measured_004.patch
  > Here we need to determine what is performance? in RT.
  > This patch add a cnt to record the breakout time when wakeup shorter than idle state's target_residency.
  - CPU idle configuration. A driver to decide which state going into.
  - Ref  
Didn't find much ref in linux documentation
    - cpuidle framework
      - [wowotech cpuidle](http://www.wowotech.net/pm_subsystem/cpuidle_overview.html)
    - c state

- cpuidle_add_support_for_max_cstate_limit.patch
  - move the max cstate set in acpi.h to osl.c, the other change seems to get or set the max_cstate, and make it available for some setup.
  > It are quite many things about cpuidle framework in 2.6.22, and never show up again in the following versions.

- use-write_trylock_irqsave-in-ptrace_attach.patch
  - Use ```write_trylock_irqsave``` instead of ```write_trylock```. And remove ```local_irq_disable``` things.
  > The first patch relevant with preempt qaq
  > Actually no change, the irqsave will disable interrupt even in mainline.
  - REF
    - [Linux man page](https://linux.die.net/man/2/ptrace)
    - [Wikipedia](https://en.wikipedia.org/wiki/Ptrace)
    - [Linux journal](http://www.linuxjournal.com/article/6100)

- hrtimer-no-getnstimeofday.patch
  - [high resolution timer](https://github.com/torvalds/linux/blob/master/Documentation/timers/hrtimers.txt)
  > The function ```getnstimeofday``` is replaced by some other functions. I don't know the reason why replace it, just sort this patch as performance.

- nohz-fix-nohz-x86-dyntick-idle-handling.patch
  - nohz in cpuidle

- slob-scale-break-out-caches.patch
  - The first part of linux I learned and moved to ucore+ one year ago, so familiar with the code
  - The kmem_cache is reintroduced, and of course the way to trace the list of it

- preempt-realtime-gtod-fixups.patch
  > Not quite sure it is a perf patch, as maybe something malfunction when irqsaved
  - gtod: generic time-of-day

- lockstat-core.patch
  > Maybe I need to read the detail someday.

- cdrom-use-mdelay-instead-of-jiffies-loop.patch
  > I doubt whether it should be put in perf

- s_files-per_cpu-fluch-fix.patch
  > just add a function and don't know why data lose is mentioned

- lockstat_bounce.patch
  - seems inportant, relevant with both lock and cache bouncing

- export symbol details

- lockdep in linux

- softlockup

- mm-lockless-preempt-rt-fixup.patch
> Maybe very important I think, need to config PREEMPT_RT on

- fastcall cplusplus

- mightsleep

- check all ? and null

- resched
  - preempt-rt resched delay

- IRQF_NODELAY

- preempt-irqs-x86-64.patch
  - irqf_nodelay
    - https://stackoverflow.com/questions/16982703/where-can-i-find-irqf-nodelay-flag-in-linux-kernel

- fix-migrating-softirq.patch
  - migration

- preempt-realtime-powerpc-b4.patch

- preempt-irqs-ppc-fix-b5.patch