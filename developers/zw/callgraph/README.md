# might_sleep的作用

[include/linux/kernel.h](https://github.com/torvalds/linux/blob/master/include/linux/kernel.h)中对`might_sleep`的注释如下

> this macro will print a stack trace if it is executed in an atomic context (spinlock, irq-handler, ...).
>
> This is a useful debugging help to be able to catch problems early and not be bitten later when the calling function happens to sleep when it is not supposed to.

正常编译时，`might_sleep`宏展开为`do { do { } while (0); } while (0)`，只有在`make menuconfig`时选择

```
Kernel Hacking  --->
  Lock Debugging (spinlocks, mutexes, etc..)  --->
    [*] Sleep inside atomic section checking
```

才能展开为`do { __might_sleep(__FILE, __LINE__, 0); do { } while (0); } while (0)`，`__might_sleep`会在atomic context中输出调试信息。因此`might_sleep`宏只能作为*annotation for functions that can sleep*，本身没有任何作用。

# 使用egypt获取callgraph

首先安装[egypt](https://www.gson.org/egypt/)

```bash
curl https://www.gson.org/egypt/download/egypt-1.10.tar.gz | tar -x
cd egypt-1.10
perl Makefile.PL
make
make install
```

`make menuconfig`后修改Makefile，并在各个`CFLAGS`和`CXXFLAGS`中加入`-fdump-rtl-expand`选项，编译完成后，使用以下命令生成DOT文件

```bash
egypy `find . -name "*.expand"` --include-external > callgraph.dot
```

# 构造callgraph

* [NetworkX](https://networkx.github.io/)

# 静态分析

* LLVM
    - 需要给RT Linux打[LLVM Patch](http://llvm.linuxfoundation.org/index.php/Main_Page)
* [GCC plugins](https://gcc.gnu.org/wiki/plugins)
    - [GCC Python plugin](https://gcc-python-plugin.readthedocs.io/en/latest/)

TODO