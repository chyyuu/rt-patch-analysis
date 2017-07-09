- Our problem is not the same with FAST'13. A bigger scope than fs.
  - A concise definition of problem sort is needed, or different and more detail whatever.
 
 >> chyyuu: yes, we need read&understand patches first, then define the problems/questions.
 
  - e.g. Does the performance patch a RT relevant performance enhancement, or the whole system, as the 2.6.22-cpuidle_last_measured_004.patch. This leads to the other two problems below.
  
- Some patches change I find irrelevant with RT features directly. Not all the patches are about preempte, I guess, most of them are not.
  - The problem is do we need to find the connection? Does it a normal patch or something specific in RT? The second question is beyond our discuss currently.
  
>> chyyuu: no, we need not to find the connections between RT & NON-RT. But we should to know how to implementation RT linux.

  - Although I just read few patches, I think it is necessary. Should we isolate preempte things from the other patches we don't yet know the relation with RT? 
  
>> chyyuu: performance&some fixbug type patches are more related with RT.

  - From some material I read, as it is a system, some changes seem irrelevant with RT do affect RT performance. Do we need to investigate the mechanism？
  
>> chyyuu: Maybe. We should read all rt patches in one kernel, then maybe we know whether we need to do. 
