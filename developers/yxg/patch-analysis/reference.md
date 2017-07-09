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
    