统计的结果我放在了同目录下的log文件中  
对于每一个统计结果我都有相应的说明

# patch type
![patch type](/developers/yxg/3.2assignment/image/patch-type.png)

- 首先，percentage breaks down to similar range这句话有误，虽然，feature和bug占到了绝大多数，但是比例变化很大，考虑到分类时，performance和feature区别不大，将二者合并后，估计标准差会变小。
- 此外，由于有大量的回滚被放到了feature中，把这部分从拿出来，单考虑其他的feature，feature的振荡没有这么大

# bug, performance, feature
- 后两者我没有画图
  - performance是由于数量很少但是分类很多，柱状图基本不存在连续性，图画出来很乱，不如直接做成表格
  - feature的话，则是，rtsupport在绝大多数的版本中占到了绝大多数，其他的则是分类太多，每种只有很少的几个，画图完全没有意义
- 对于bug
![bug](/developers/yxg/3.2assignment/image/bug-type.png)

粗略的分类可以看到semantic和concurrency占到了绝大多数
![bug-detail](/developers/yxg/3.2assignment/image/bug-type-other.png)

细分之后，占比较大的依次是semantics，compiling_err，deadlock和irq/softirq，分别位于semantics，concurrency和error code中。  
但是同样，分类太细，就算是选出了5个最多的种类，图依然很乱  
在FAST'13中对细分的bug/bugtype做了图，我仿照那个对于semantic做了一下  
![semantic](/developers/yxg/3.2assignment/image/semantics.png)

好了一点  

另一个问题是，有很多的bug分类数量很少考虑是不是可以合并掉
na, config_err, overflow, err_access, typo_var, resourse_leak

现在的问题就是
- 如果想让图看起来不那么乱，最好是能够合并performance和feature中的子类，合并到4-5个最好
- bug中一些出现较少的type我挑着看了一下，可能有分类有问题或者不是很必要额外多一个子类的情况
