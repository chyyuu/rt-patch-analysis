
# rt-linux-lkp使用文档


## 各个文件的作用
* git-polling.sh 

负责检查git各个分支是否有更新，如果有更新，把更新过的分支的最新的giturl和commitid传递给rt-linux-lkp.sh。

* build_bat.sh 

给定一些giturl和commitid/tagname/branchname(不推荐不能唯一标定源代码版本）调用rt-linux-lkp.sh进行测试。


* rt-linux-lkp.sh 

通过giturl和commitid/tagname 来检出对应版本的源代码，并进行编译和启动测试，和lkp测试。

* initrd_lkp.img 

一个简单的initrd.img用来进行新编译的内核启动测试。

* run_lkp.sh 

通过指定新编译的内核的bzImage文件和commitid，还有benchmarkname来运行lkp测试。


## 使用方法
*  自动回归测试 

修改git-polling.sh中url="https://github.com/chyyuu/linux-rt-devel.git" 为想要测试的giturl 

执行./git-polling.sh

*  自动批量测试指定版本代码

修改build_bat.sh中url="https://github.com/chyyuu/linux-rt-devel.git" 为想要测试的giturl tagename为想要测试的版本号码或者commitid 

执行./build_bat.sh

*  查看测试结果

/build/${REPO_NAME}/${COMMITID}/$(date)/build_dir/目录中存放了内核源代码的编译结果。和编译日志make.log和简单的启动测试日志boot_run.log
可以通过查看这两个文件从而知道是否编译或者启动成功。

