- **获取linux-stable-4.7.tar**

	- 访问 https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git/refs/tags

	- 找到内核版本v4.7，鼠标指向linux-stable-4.7.tar.gz复制URL

	- 终端命令行：root@zzm-Inspiron-3421:/home/zzm/linux_source# wget https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git/snapshot/linux-stable-4.7.tar.gz
	

	- 解压kernel：root@zzm-Inspiron-3421:/home/zzm/linux_source# tar -xzvf linux-stable-4.7.tar.gz 

- **获取patch-4.6.7-rt14.patch.gz**

	- 访问 https://www.kernel.org/pub/linux/kernel/projects/rt/

	- 找到patch-4.6.7-rt14.patch.gz对应的补丁文件下载URL

	- 终端命令行：root@zzm-Inspiron-3421:/home/zzm/linux_source# wget https://www.kernel.org/pub/linux/kernel/projects/rt/4.6/patch-4.6.7-rt14.patch.gz

	- 解压patch：root@zzm-Inspiron-3421:/home/zzm/linux_source# gunzip patch-4.6.7-rt14.patch 

	
- **patch过程处理**
	- 执行以下命令
		
			root@zzm-Inspiron-3421:/home/zzm/linux_source# cd linux-stable-4.7
			root@zzm-Inspiron-3421:/home/zzm/linux_source/linux-stable-4.7# patch -Np1 < ../patch-4.6.7-rt14.patch 

	- patch相关信息处理
		- Hunk #* succeeded at *** (offset * lines).
			- 查看相关文件，发现对于v4.6 kernel来说，v4.7 kernel修改了一些内容，因此patch-4.6.7-rt14.patch中修改的行并不完全匹配v4.7 kernel,但是patch一般都成功了。
		- Reversed (or previously applied) patch detected!  Skipping patch.(13 个)
				
				patching file arch/arm/mach-imx/Kconfig
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file arch/arm/mach-imx/Kconfig.rej
	
				patching file drivers/crypto/ccp/ccp-dev.c
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file drivers/crypto/ccp/ccp-dev.c.rej
	
				patching file drivers/gpu/drm/i915/i915_drv.h
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file drivers/gpu/drm/i915/i915_drv.h.rej
	
				patching file drivers/gpu/drm/i915/intel_uncore.c
				Reversed (or previously applied) patch detected!  Skipping patch.
				7 out of 7 hunks ignored -- saving rejects to file drivers/gpu/drm/i915/intel_uncore.c.rej
	
				patching file drivers/i2c/busses/i2c-omap.c
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file drivers/i2c/busses/i2c-omap.c.rej
				
				patching file drivers/infiniband/ulp/ipoib/ipoib_ib.c
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file drivers/infiniband/ulp/ipoib/ipoib_ib.c.rej
	
				patching file drivers/net/ethernet/chelsio/cxgb/sge.c
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file drivers/net/ethernet/chelsio/cxgb/sge.c.rej
	
				patching file drivers/net/ethernet/neterion/s2io.c
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file drivers/net/ethernet/neterion/s2io.c.rej
	
				patching file drivers/net/rionet.c
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file drivers/net/rionet.c.rej
	
				patching file include/asm-generic/preempt.h
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file include/asm-generic/preempt.h.rej
	
				patching file kernel/sched/cpudeadline.c
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file kernel/sched/cpudeadline.c.rej
	
				patching file kernel/sched/cpupri.c
				Reversed (or previously applied) patch detected!  Skipping patch.
				1 out of 1 hunk ignored -- saving rejects to file kernel/sched/cpupri.c.rej
	
				patching file kernel/sched/deadline.c
				Reversed (or previously applied) patch detected!  Skipping patch.
				14 out of 14 hunks ignored -- saving rejects to file kernel/sched/deadline.c.rej
	
			- arch/arm/mach-imx/Kconfig：通过diff v4.6 v4.7（v4.7与patch文件相同，因此Skipping patch）
				
					root@zzm-Inspiron-3421:/home/zzm/linux_source# diff linux-stable-4.6/arch/
					arm/mach-imx/Kconfig linux-stable-4.7/arch/arm/mach-imx/Kconfig
					529c529
						<       select HAVE_ARM_TWD if SMP
						---
						>       select HAVE_ARM_TWD
			
			- drivers/crypto/ccp/ccp-dev.c：通过diff v4.6 v4.7（v4.7与patch文件相同，因此Skipping patch）
	
					root@zzm-Inspiron-3421:/home/zzm/linux_source# diff linux-stable-4.6/
					drivers/crypto/ccp/ccp-dev.c linux-stable-4.7/drivers/crypto/ccp/ccp-dev.c
					19c19
					< #include <linux/rwlock_types.h>
					---
					> #include <linux/spinlock_types.h>
	
			- drivers/gpu/drm/i915/i915_drv.h：通过diff v4.6 v4.7（v4.7与patch文件相同，因此Skipping patch）
				
					717c684
					<               struct timer_list timer;
					---
					>               struct hrtimer timer; 
		
			- 通过同样的方法查看其它Skipping patch 的文件，同样是该patch已经进入mainline。
	
		- 对于Hunk #* FAILED at*** 需要查看*.rej文件做手动修改。（37处FAILED）
	
				patching file arch/x86/include/asm/uv/uv_hub.h  
				Hunk #1 FAILED at 492.    //此处结构体已改变，新结构体重补丁增加的内容已进入主体
				1 out of 1 hunk FAILED -- saving rejects to file arch/x86/include/asm/uv/uv_hub.h.rej
				patching file arch/x86/kernel/apic/x2apic_uv_x.c  
				Hunk #3 FAILED at 950.    //结构发生了变化，不能加入
				1 out of 3 hunks FAILED -- saving rejects to file arch/x86/kernel/apic/x2apic_uv_x.c.rej
				patching file arch/x86/kernel/dumpstack_64.c     
				Hunk #1 FAILED at 152.  //手动添加get/put_cpu_light()
				Hunk #2 FAILED at 241.  //手动添加get/put_cpu_light()
				2 out of 4 hunks FAILED -- saving rejects to file arch/x86/kernel/dumpstack_64.c.rej
				patching file drivers/crypto/ccp/ccp-dev.c    
				Hunk #1 FAILED at 16.  //手动删除头文件
				1 out of 1 hunk FAILED -- saving rejects to file drivers/crypto/ccp/ccp-dev.c.rej
				patching file drivers/net/ethernet/atheros/atl1c/atl1c_main.c 
				Hunk #1 FAILED at 2217. //手动添加spin_lock_irqsave(&adapter->tx_lock, flags);
				1 out of 1 hunk FAILED -- saving rejects to file drivers/net/ethernet/atheros/atl1c/atl1c_main.c.rej
				patching file drivers/net/ethernet/atheros/atl1e/atl1e_main.c   
				Hunk #1 FAILED at 1880.  //手动添加spin_lock_irqsave(&adapter->tx_lock, flags);
				1 out of 1 hunk FAILED -- saving rejects to file drivers/net/ethernet/atheros/atl1e/atl1e_main.c.rej
				patching file drivers/net/ethernet/oki-semi/pch_gbe/pch_gbe_main.c  
				Hunk #1 FAILED at 2137. //手动添加spin_lock_irqsave(&adapter->tx_lock, flags);
				1 out of 1 hunk FAILED -- saving rejects to file drivers/net/ethernet/oki-semi/pch_gbe/pch_gbe_main.c.rej
				patching file drivers/net/ethernet/tehuti/tehuti.c
				Hunk #1 FAILED at 1629. //手动添加spin_lock_irqsave(&adapter->tx_lock, flags);
				1 out of 1 hunk FAILED -- saving rejects to file drivers/net/ethernet/tehuti/tehuti.c.rej
				patching file fs/dcache.c  
				Hunk #3 FAILED at 786.  //手动修改代码
				1 out of 4 hunks FAILED -- saving rejects to file fs/dcache.c.rej  
				patching file include/linux/rcutree.h   
				Hunk #3 FAILED at 93.   //手动去除几处定义
				1 out of 4 hunks FAILED -- saving rejects to file include/linux/rcutree.h.rej
				patching file include/linux/sched.h   
				Hunk #11 FAILED at 1916. //手动添加代码
				Hunk #18 FAILED at 2677. //手动添加代码
				2 out of 22 hunks FAILED -- saving rejects to file include/linux/sched.h.rej
				patching file include/linux/timer.h   
				Hunk #6 FAILED at 156.  //手动添加定义代码
				1 out of 8 hunks FAILED -- saving rejects to file include/linux/timer.h.rej
				patching file kernel/sched/core.c
				Hunk #14 FAILED at 1656.    //已进入mainline
				Hunk #17 FAILED at 2138.   // 手动删除
				Hunk #22 FAILED at 3434.	//手动删除
				Hunk #36 FAILED at 5737.	//找不到对应的函数
				4 out of 37 hunks FAILED -- saving rejects to file kernel/sched/core.c.rej
				patching file kernel/sched/rt.c
				Hunk #3 FAILED at 336.  //mainline
				Hunk #4 FAILED at 353.  //mainline
				Hunk #5 FAILED at 1326. //mainline
				Hunk #6 FAILED at 1415.  // mainline
				Hunk #7 FAILED at 1439.  //mainline
				Hunk #8 FAILED at 1447.  // mainline
				Hunk #9 FAILED at 1581.  //mainline
				Hunk #10 FAILED at 1631. //mainline
				Hunk #11 FAILED at 1764.  //mainline
				Hunk #12 FAILED at 2124.  //mainline
				Hunk #13 FAILED at 2199.  //mainline
				11 out of 13 hunks FAILED -- saving rejects to file kernel/sched/rt.c.rej
				patching file mm/page_alloc.c  
				Hunk #4 FAILED at 840. //手动添加或删除代码（注意有些变量发生变化添加或删除代码时更改相关变量）
				Hunk #6 FAILED at 875.  //（同上）
				Hunk #15 FAILED at 2396. //（同上）
				Hunk #17 FAILED at 2430. //（同上）
				4 out of 22 hunks FAILED -- saving rejects to file mm/page_alloc.c.rej
				patching file mm/swap.c  
				Hunk #11 FAILED at 709.   //手动添加代码
				1 out of 11 hunks FAILED -- saving rejects to file mm/swap.c.rej
				patching file mm/truncate.c  
				Hunk #1 FAILED at 63.  //手动添加代码
				1 out of 1 hunk FAILED -- saving rejects to file mm/truncate.c.rej
				patching file net/ipv4/tcp_ipv4.c 
				Hunk #3 FAILED at 691.  // mainline 中添加的是local_bh_disable/enable(),需要替换为local_lock/unlock(tcp_sk_lock);
				Hunk #4 FAILED at 776.  //(同上)
				2 out of 4 hunks FAILED -- saving rejects to file net/ipv4/tcp_ipv4.c.rej


					
- **编译内核过程：**
	
		
	- 编译环境：
	
			Linux version 4.10.0-33-generic (buildd@lgw01-22) (gcc version 5.4.0 20160609 
			(Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #37~16.04.1-Ubuntu SMP Fri Aug 11 14:07:24 UTC 2017
	- make O=../v4.7-rt defconfig 	

		- make defconfig:按照默认的配置文件arch/i386/defconfig对内核进行配置，生成.config可以用作初始化配置，然后再使用make menuconfig进行定制化配置
			 
		- make oldconfig：但是它的作用是在现有的内核设置文件基础上建立一个新的设置文件，只会向用户提供有关新内核特性的问题，在新内核升级的过程 中，make oldconfig非常有用，用户将现有的配置文件.config复制到新内核的源码中，执行make oldconfig，此时，用户只需要回答那些针对新增特性的问题
		- make silentoldconfig : Like above, but avoids cluttering the screen with questions already answered.和上面oldconfig一样，但在屏幕上不再出现已在.config中配置好的选项。




	- make  O=../v4.7-rt/ menuconfig

			 Processor type and features  --->
			      Preemption Model (Voluntary Kernel Preemption (Desktop))  --->
				  (*) Fully Preemptible Kernel (RT) 

	- make O=../v4.7-rt/
	
		- **错误1---重定义（redefinition）：**
			- **错误代码**

					/home/zzm/linux_source/work/linux-stable-4.7/include/linux/sched.h:3476:19:
	       			 error: redefinition of ‘tsk_nr_cpus_allowed’
					 static inline int tsk_nr_cpus_allowed(struct task_struct *p)
					                   ^
					/home/zzm/linux_source/work/linux-stable-4.7/include/linux/sched.h:1985:19:
					 note: previous definition of ‘tsk_nr_cpus_allowed’ was here
					 static inline int tsk_nr_cpus_allowed(struct task_struct *p)
				
			- **错误原因**：这里是重定义了‘tsk_nr_cpus_allowed’，查看v4.6和v4.7的源码发现，在v4.6的mainline并没有该函数，在v4.7的mainline中加入了该函数，而patch-4.6.7-rt12.patch中定义了该函数，因此patch过程中该函数重复加入到v4.7中。
			- **改正方法**：解决的方法是将v4.7的mainline中的该函数屏蔽掉。

		- **错误2---函数声明（-Werror=implicit-function-declaration）（该错误存在多处）**：
			- **错误代码（列举几例）**

					/home/zzm/linux_source/work/linux-stable-4.7/arch/x86/entry/vdso/vma.c: In
					 function ‘map_vdso’:
					/home/zzm/linux_source/work/linux-stable-4.7/arch/x86/entry/vdso/
					vma.c:166:6: error: implicit declaration of function 
					‘down_write_killable’ [-Werror=implicit-function-declaration]
					  if (down_write_killable(&mm->mmap_sem))
						      ^
					cc1: some warnings being treated as errors

					../kernel/fork.c: In function ‘dup_mmap’:
					../kernel/fork.c:430:6: error: implicit declaration of function
					 ‘down_write_killable’ [-Werror=implicit-function-declaration]
					  if (down_write_killable(&oldmm->mmap_sem)) {
					      ^
					cc1: some warnings being treated as errors

					../kernel/sys.c: In function ‘SYSC_prctl’:
					../kernel/sys.c:2249:7: error: implicit declaration of function
					‘down_write_killable’ [-Werror=implicit-function-declaration]
				   	if (down_write_killable(&me->mm->mmap_sem))
				       ^
					cc1: some warnings being treated as errors

					../mm/util.c: In function ‘vm_mmap_pgoff’:
					../mm/util.c:300:7: error: implicit declaration of function 
					‘down_write_killable’ [-Werror=implicit-function-declaration]
					   if (down_write_killable(&mm->mmap_sem))
					       ^
					cc1: some warnings being treated as errors
			- **错误原因**：此处是在vma.c的map_vdso函数中调用`down_write_killable`函数，但该函数并没有声明。通过`grep -w -E "down_write_killable()" ./* -Rn`查看内核,发现该函数的声明在/include/linux/rwsem.h中，查看该文件和patch发现，patch增加了这段代码：

							#ifdef CONFIG_PREEMPT_RT_FULL
							#include <linux/rwsem_rt.h>
							#else /* PREEMPT_RT_FULL */
			查看<linux/rwsem_rt.h>，该函数中并未对down_write_killable()声明，因此产生了这个错误。



						
			- **改正方法**：在rwsem_rt.h中对该函数声明。我再此处是参考了patch-4.8中增加了一个`rt_down_write_killable()`,声明`down_write_killable()调用rt_down_write_killable()`问题得以解决。
			- **同类相关错误**：同样存在该错误的还有`up_read_non_owner(sem)和down_read_non_owner(sem)`。这里我的解决办法是将mainline中对这两个宏的声明加入到以下代码中。

							#ifdef CONFIG_PREEMPT_RT_FULL
							#include <linux/rwsem_rt.h>
							# define down_read_non_owner(sem)		down_read(sem)
							# define up_read_non_owner(sem)			up_read(sem)
							#else /* PREEMPT_RT_FULL */	

					
		- **错误3---强制转换类型（-Werror=incompatible-pointer-types）**

			- **错误代码**

					/home/zzm/linux_source/work/linux-stable-4.7/kernel/sched/core.c: In function ‘migrate_me’:
					/home/zzm/linux_source/work/linux-stable-4.7/kernel/sched/core.c:1213:23:
					 error: passing argument 2 of ‘task_rq_lock’ from incompatible pointer type
					 [-Werror=incompatible-pointer-types]
					  rq = task_rq_lock(p, &flags);
					                       ^
					/home/zzm/linux_source/work/linux-stable-4.7/kernel/sched/core.c:204:12:
					note: expected ‘struct rq_flags *’ but argument is of type ‘long unsigned int *’
					 struct rq *task_rq_lock(struct task_struct *p, struct rq_flags *rf)
					            ^
					/home/zzm/linux_source/work/linux-stable-4.7/kernel/sched/core.c:1222:25:
					 error: passing argument 3 of ‘task_rq_unlock’ from incompatible pointer
					 type [-Werror=incompatible-pointer-types]
					   task_rq_unlock(rq, p, &flags);
					                         ^
					In file included from /home/zzm/linux_source/work/linux-stable-4.7/kernel/
					sched/core.c:86:0:
					/home/zzm/linux_source/work/linux-stable-4.7/kernel/sched/sched.h:1490:1:
					 note: expected ‘struct rq_flags *’ but argument is of type ‘long unsigned int *’
					 task_rq_unlock(struct rq *rq, struct task_struct *p, struct rq_flags *rf)
					 ^
					/home/zzm/linux_source/work/linux-stable-4.7/kernel/sched/core.c:1232:24: 
					error: passing argument 3 of ‘task_rq_unlock’ from incompatible pointer type
					[-Werror=incompatible-pointer-types]
					  task_rq_unlock(rq, p, &flags);
					                        ^
					In file included from /home/zzm/linux_source/work/linux-stable-4.7/kernel/
					sched/core.c:86:0:
					/home/zzm/linux_source/work/linux-stable-4.7/kernel/sched/sched.h:1490:1: 
					note: expected ‘struct rq_flags *’ but argument is of type ‘long unsigned
					int *’task_rq_unlock(struct rq *rq, struct task_struct *p, struct rq_flags
					*rf)  ^
	
			
					
			- **错误原因**：`task_rq_lock(rq, p, &flags);task_rq_unlock(rq, p, &flags);`这两函数第三个参数是`(struct rq_flag *)`类型，但这里flags定义的是unsigned long类型;因此产生错误。
			- **修改方法**：根据`task_rq_lock/unlock()`的参数类型可以用强制类型转换将flags转换为	(struct rq_flag *)型指针类型。即：`task_rq_unlock(rq, p, (struct rq_flag *)flags);`
			
				
		- **错误4---缺少头文件**
	
			- **错误代码--unknown type name**

					In file included from ../fs/nfs/nfs4namespace.c:10:0:
					../include/linux/dcache.h:103:3: error: unknown type name ‘wait_queue_head_t’
					   wait_queue_head_t *d_wait; /* in-lookup ones only */
					   ^
					../include/linux/dcache.h:234:6: error: unknown type name ‘wait_queue_head_t’
		     		 wait_queue_head_t *);
		 
			
				- **错误原因：**缺少头文件。
				- **修改方法：**增加#include<linux/wait.h>
			

	
	- 编译成功，qemu测试bzImage---成功

			cd v4.7-rt/
			qemu-system-x86_64  -kernel arch/x86_64/boot/bzImage -serial stdio -append "root=/dev/sda init=/bin/ash"

	- qemu启动linux内核

		
		- 获取根文件系统 initrd.img
		- 启动：qemu-system-x86_64  -kernel arch/x86_64/boot/bzImage -initrd ../../initrd.img -serial stdio -append "root=/dev/sda init=/bin/ash" 成功。

			![](http://i.imgur.com/EC78bIf.png)

				



