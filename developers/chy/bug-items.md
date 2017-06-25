## #bug items

RCU and Real Time: History
 2005: Preemptible RCU take 1 (in -rt)
 2007: Preemptible RCU take 2: nonatomic (in mainline)
 2009: Preemptible RCU take 3: scalable (in mainline)
 2012: Bug report claiming 200-microsecond latency spikes from RCU grace-period initialization

  – Which came as quite a surprise given ~30-microsecond latencies from
the entire kernel, not just RCU...
  – But further down in the email, there was a kernel-configuration
parameter that fully explained the difference in latency

  – NR_CPUS=4096!!!
​     • At which point: “You mean it only took 200 microseconds???” 
​     • Therefore...