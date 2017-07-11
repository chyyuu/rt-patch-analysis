# Memeory barriers
## Memory access model
  - Prerequisite: Multi-CPU may perform their own memory operations, and overall orders are arbitrary. Mainwhile, compiler may arrange instructions it emit in any order, provided that it doesn't affect the apparent operation of program.
  - Thus, the CPU may get different return value when it load the value others may store simutaneously.

### Guarantees
  - On any given CPU, dependent memory accesses will be issued in order.
  - Overlapping loads and stores(means visit the same memory address somehow) within a particular CPU will appear to be ordered within that CPU.
  - It **MUST NOT** be assumed that the compiler will do what you want with memory references that are not protected by ```READ_ONCE``` and ```WRITE_ONCE```.
  - It **MUST NOT** be assumed that independent loads and stores will be issued in that order given.
  - It **MUST** be assumed that overlapping memory accesses may be merged or discarded.(Access once as a bulk)  
Some anti-guarrantees
  - These guarantees do not apply to bitfields, **because compilers often generate code to modify these using non-atomic read-modify-write sequences**. Do not attempt to use bitfields to synchronize parallel algorithms.
  - Even when bitfields are protected by locks, all fields in a given bitfield must be protected by **one** lock.
  - These guarantees apply only to properly aligned and sized scalar variables.

## What Are Memory Barriers
  - Memory Barriers is used as a way of intervening to instruct the compiler and the CPU to restrict the order.
  - Memory barriers are only required when there 's a possibility of interaction between two CPUs or between a CPU and a device.
  - There are minimal guarrantees provided by architectures.
### Varies of Memory Barrier
  - Write (or store) memory barriers
    - Guarantee all the STORE operations specified before the barrier to happen before the barrier(or to say concisely, before the store after the barrier).
    - Partial ordering on stores only, have nothing to do with loads.
    - **NOTE**: write barriers should normally be paired with read or data dependence barriers.
    > Not quite understand the note.
  - Data dependency barriers
    - Weaker form of read barrier.
    - Partial ordering on interdependent loads only; not  required to have any effect on stores, independent loads or overlapping loads.
    - Guarrantee that for any load preceding it, if that load touches one of the sequence of stores from another CPU, then by the time the barrier completes, the effects of all the store prior to that touched by the load will be perticible to any loads issued after the data dependency barrier.
    - **NOTE**: The first load really has to have a data dependenty and not a control dependency. If the second load 's address is dependent on the first, but is through a conditional then a control dependency and a full read barrier or beter is required.
    - **NOTE**: The data dependency barriers should normally be paired with write barriers.
  - Read (or load) memory barriers
    - Read barrier is a data dependency barrier plus a guarantee that all the LOAD operations specified before the barrier will appear to happen before the barrier.
    - Partial ordering on loads only.
    - **NOTE**: normally be paired with write barriers
  - General memory barriers
    - Guarrantee that all the LOAD and STORE operations happen before barrier.

Implicit varieties:
  - ACQUIRE operations
    - Act as a one-way permeable barrier: all memory operations after the it will apear to happen after it.
    - Include LOCK operations, both ```smp_load_acquire``` and ```smp_cond_acquire```.
    - Memory operations before it may happen after ACQUIRE.
    - Should always be paired with RELEASE operation.
  - RELEASE operations
    - One-way barrier as well.
    - Include UNLOCK operations and ```smp_store_release```.
    - Memroy operations after it may happen before it.
  - The use of them generally precludes the need for other sorts of memory barrier(excepts exist).
  - The ACQUIRE-RELEASE pair is not guaranteed to act as a full memory barrier.

### Things not to be assumed about memory barriers
  - Linux kernel memory barriers do not guarantee:
    - No guarantee that any of the memory accesses specified before a memory barrier will be complete by the completion of a memeory barrier instructions. Just a guarantee that the operations separated by the barrier will not interleave.
    - No guarantee that memory barrier on one CPU will have any direct effect on another CPU or any other hardware in the system.
    - No guarantee that a CPU will see the correct order of effects from a second CPU's accesses, even if the second CPU uses a memory barrier, unless the first CPU also uses a matching memory barrier.
    > I thing it's vital!
    - No guarantee that some interveneing piece of off-the-CPU hardware will not reorder the memory accesses. **CPU cache coherency mechanisms should propagate the indirect effects of a memory barrier between CPUs, but might not do so in order** 

### Barriers Details
  - Data Dependency Barriers
    > I think it as a good example:
```
	CPU 1		      CPU 2  
	===============	      ===============  
	{ A == 1, B == 2, C == 3, P == &A, Q == &C }  
  1.    B = 4;  
  2.    <write barrier>  
  3.    WRITE_ONCE(P, &B);  
  4.                          Q = READ_ONCE(P);  
  5.                          <data dependency barrier>  
  6.                          D = *Q;  
```
    - If there is no ```<data dependency barrier>```, **the value of B may be update after updating D, and the execute sequence is thus 3->4->6->1**. Notice that the ```<write barrier>``` could not guarrantee the load operation to execute after the write barrier.
    - And thus, the ```<data dependency barrier>``` is inserted to make sure any store operation become effective before the barrier.
    - **This is very important to the RCU system**
    > However I find no barrier API used in the linux/include/linux/rcupdate.h
  - Control Dependencies
  > I think it is interesting, and the linux documentation provide us a lot of details
  > Read the [documentation](https://github.com/torvalds/linux/blob/master/Documentation/memory-barriers.txt#L640) carefully, I just take down some of my thoughts
    - ?Current compilers do not understand them, some optimization is taken, leading to wrong order.
    > I think it is false of compiler? and should not happen anyway?
    - First, a definition of control dependencies: a store operation and a condition statement with the value updated with that operation. The code below is a load-load control sequence:
```
    q = READ_ONCE(a);
    if(q){
        p = READ_ONCE(b);
    }
```
  - Problems:
    - The CPU may short-circuit by attempting to predict the outcome in advance, so the other CPUs see the load from b having happened before the load from a.
      - Thus a ```<read_barrier>``` is put before the load from b.
    - Then there is something I don't know what does it explain about load-store sequence
      - Two-legged if control ordering is used to garrantee the order, but the compiler may move the store operation out of the if statement and thus violate the order
      - If the two legs are loading different, the load operation will not be moved out of the if statement.
      - If you need to order the sequence of load-store, use the explicit mb like ```smp_store_release()``` to prevent compiler optimization.
  - Control dependencies apply only to the then & else clause of the if-statement, doesn't necessarily apply to code following the if-statement.
  - Control dependencies do not guarrantee transitivity, use ```smp_mb()``` if necessary
### SMP barrier pairing
  - Barriers can pair all other kinds of barriers, with some exceptions that read and write may not pair with themselves.
  - The [Note](https://github.com/torvalds/linux/blob/master/Documentation/memory-barriers.txt#L974) should be careful, because I don't get the reason why it is mentioned.
### Examples of Memory Barrier Sequences
  - As the example mentioned before, the ```<data_dependency_barrier>``` is used to combine the sequence of update of perception on both CPU. Without it, although the update in the second CPU is expected to execute the Load operation after the Store operation in the first CPU, there is no guarrantee that it will happen.
  - Another example is trying to emphasis that the barrier is a *partial* barrier, but the picture of the sequence is *wrong*.


## Ref
  - [Linux Document](https://github.com/torvalds/linux/blob/master/Documentation/memory-barriers.txt)
  - [A formal kernel memory-ordering model (part 1)](https://lwn.net/Articles/718628/)
  - [A formal kernel memory-ordering model (part 2)](https://lwn.net/Articles/720550/)

## TODOS
  - Linux ```READ_ONLY``` & ```WRITE_ONLY```
  - C bitfield