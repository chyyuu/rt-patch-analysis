
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


