#  A Study of Real-Time Linux Kernel with Preempt-RT Evolution

这个报告的基本目标是：

- 理解rt-linux的特征（设计特点，使用规则）和容易发生的错误
- 让linux developer开发中减少错误和提供实时确定性
- 使得rt-linux的演化更加容易

Challenge：

如何静态/动态分析bug/determinism  deadlock/livelock, race condition, long latency, jitter

## Abstract

我们对Linux Kernel with Preempt-RT的演进进行了全面深入的分析。通过研究2007~2017年的22个kernel版本中的
6900个patches来分析Linux Kernel with Preempt-RT的变化，我们得到了很多对Linux Kernel with Preempt-RT开发的新
的理解。我们的结果对于推动Linux Kernel with Preempt-RT的进一步开发，加强Linux Kernel的实时性和改进bug-finding工具都会提供帮助。

## 1 Introduction

RT-PATCH的起源，开发和广泛应用情况

对于通用Linux操作系统而言，对其实时性能的需求越来越强烈，为此出现了多种对Linux操作系统的实时改进方案，但其主要的改进方案包括：CONFIG_PREEMPT_RT(Preempt_RT)，Dual-OS/Dual-Core (Xenomai, RTAI)，Nested OS（L4Linux）等。由于CONFIG_PREEMPT方案直接与在官方内核主线同步发展，而基于CONFIG_PREEMPT的Preempt_RT也能基于内核 LTS版同步发展，确保了有更广泛社区支持，其patches也在不断地进入官方内核，可支持更广泛的硬件平台，更容易开发支持基于实时POSIX标准的应用。

但是，尽管基于基于PREEMPT_RT方案的实时Linux占据了主流，不少Preempt_RT的patches已经被官方Linux kernel采纳，且有部分CONFIG_PREEMPT方案的实时性能分析，但还缺少对此方案的更深入和广泛的定量理解与分析。比如，对与官方Linux kernel而言，需要多少的代码移植工作才能把Preempt_RT移植/改进到新的内核版本上？相对于官方内核版本，把Preempt_RT的移植/改进会对Linux kernel中的API语义带来哪些变化，是否容易误导内核开发者对相关API的使用？具有Preempt_RT属性的Linux Kernel存在哪些类型的Bug，存在哪些实时性能特征。这些问题 的答案对于不同的社区会很重要：对于内核开发人员，他们可提高移植Preempt_RT的效率，减少犯错的可能性；对于内核测试人员，他们可知道如何设计有效的测试用例来测试Preempt_RT属性的Linux Kernel；对于工具设计人员，他们可知道如何设计开发工具/检查bug工具来提高Preempt_RT属性的Linux Kernel的可靠性；对于实时应用开发/使用人员，可以更好地理解Preempt_RT属性的Linux Kernel的实时性能，从而更好地在Preempt_RT属性的Linux Kernel上开发和使用各种类型的实时应用。最终可让Preempt_RT属性的Linux Kernel被内核社区和实时应用领域得到更快捷和广泛的认可与采纳。

对上述问题的分析与解答可通过研究Preempt_RT的开发历史来了解。由于Preempt_RT的开发代码/补丁相对比较完整地保存在[内核主网址][1]和[内核主开发网址][2]中，所以我们可以对源码和每个patchesf记录，包括log信息，代码修改处，开发时间等，进行详细的分析。

在本文中，我们第一次对Preempt_RT的演化过程进行了全面的研究，时间跨度为10年，涉及22个内核版本，包括6900个patches。我们仔细检查了每个patches来理解其意图，并从不同的维度来定量地了解Preempt_RT的开发过程。从而能够回答诸如“patches/bugs有哪些分类”，“哪些patch很跨了多个内核版本，具有较高的重复性？”，“哪些类型的bug最普遍？”，“新的API与被其替换的API的语义一同是什么？”，从而能够从新的角度来理解Preempt_RT的演化。

我们得到了如下一些高层的观察结果（Sec. 3)。有较大部分的patches是跨越多个版本的，在22个内核中6900个patches中，具有唯一性的patches数量为1625个，冗余度（uniqueness patches/total patches ）高达76.4%。在这些具有唯一性的patches中，较大部分的patches属于feature patches，占了大约45%，大部分集中在与同步互斥相关的部分，反映了Preempt_RT的开发过程中在改动Linux kernel，并设计和实现real-time能力方面做了大量的工作。另外处于第二位的是fix-bug patches，占了大约29.7%，这也说明了由于Preempt_RT的引入，触发或带来了更多的内核bug，且某些fix-bug patches在多个版本存在，有着比较长的生命周期。

通过把bug类的patches进行进一步分析和划分，我们发现semantic bug和concurrency bug占了大部分（Sec. 4)。对于语义bug，占了bug数量的48.3%。这类bug需要能够对相关的上下文，比如硬件特性，时钟，irq/softirq等，有比较清楚的了解，才能修改，所以修复的难度较大。但其中的有较大部分的此类bug还是与concurrency有直接和间接的关系。对于concurrency bug，则是另外一大类bug，占了bug数量的28.2%，在这里面，might_sleep，atomicity violation和deadlock/livelock类占了大部分。其他类型的bug主要属于memory bugs和error_code bugs。在memory bugs中，变量未初始化，数据处理错误，资源/动态分配的内存没有释放等问题依然存在；而对于error _code bugs，编译错误和配置错误占了主要部分，这方面的修改相对比较容易一些。

通过分析，我们发现为了提高Linux的实时响应能力，以及修复由于实现real-time的能力而与已有kernel实现冲突引入的bug，Preempt_RT的内核设计与开发人员对与scheduling/Concurrency等相关的API进行了两个层面的修改（Sec. 5)。第一层面是保持API的接口，但修改了内部实现的语义，使得与原有API在具体功能上有区别；第二个层面是增加了新的API接口和实现。对于这两种层面的API，并替换了在官方Linux中相对的老的API接口和调用方式。以最新的Linux 4.11 Preempt-RT为例，符合这样特征的API替换有127对。在API替换中，有两个特点需要注意：

1. 部分替换：新API只是替换部分老API，对于哪些老API需要替换，取决于Preempt_RT内核开发者对老API的使用场景的理解。比如在官方内核中的cpu_relax函数有1117处存在，但Preempt_RT的patch中，只在12处用了cpu_chill函数替换了cpu_relax函数。
2. 1对N替换：有15对API替换存在1:2或1:3的情况，即同一个API在不同的semantic context下，会替换/被替换为不同类型的API。比如preempt_disable函数，会在不同的semantic context下，被local_lock函数，migrate_disable函数或preempt_disable_nort替换。

这使得其他内核开发者在移植/定制Preempt_RT到新的内核版本或新的平台上时，容易产生混淆，不清楚在那种semantic context下应该使用具有那种特征的Kernel API，在确保没有bug的情况下，还能提升实时性能。

除了上述的高层结论，我们工作的另外一个成果是对这6900个patch的注释数据集Preempt_RT_DB，已经生成相关数据和统计的脚本，我们把它们公布在了github上。我们展示了如何通过Preempt_RT_DB来进行case study(Sec. 6)。通过这个演示实例，我们可以看到对于某个与Preempt_RT相关的函数，应该在哪类semantic context下使用，需要注意和规避的关键点在哪里，是否可进一步提升实时性能等。这样，可便于内核开发者，bug-finding tools开发者，实时应用开发者进行进一步的研究，开发，升级，改进和使用基于Preempt_RT的Linux Kernel。

## 2 Methodology

在这一节中，我们首先将简要描述Preempt_RT的设计与实现，然后用一个例子来介绍我们是如何分析Preempt_RT patech的。最后，我们介绍一下我们方法的局限性。

### 2.1 Overview of Preempt_RT 

我们的目标是理解Preempt_RT的设计与实现。由于Preempt_RT的演进过程大致从2006年开始，一直持续到现在，有不少起源于Preempt_RT的patches已经合并到了官方Linux中，但依然还有大约近300个左右的Preempt_RT的patches需要移植到不同版本的Linux kernel中。为此，我们需要分析针对Linux kernel 2.6.33～4.11，共22个版本的Preempt_RT patches，理解其变化规律和一些不变的属性。

通过Preempt_RT来实现Linux实时性的关键点是减少内核中非抢占性（non-preemptible）的代码量，且要尽量减少对实际的代码的修改量。为了减少内核中非抢占性（non-preemptible）的代码量，需要实现对临界区（critical secitons），中断处理例程（interrupt handlers），中断屏蔽代码段（interrupt-disable code sequences）的可抢占性。为了减少对实际的代码的修改量，Preempt_RT patches 充分重用了LInux  kernel对SMP的支持能力，从而避免了对Linux kernel的大量重写。

### 2.2 Classification of Preempt_RT  patches

我们对2007~2017年的22个kernel版本中的6900个Preempt_RT patches进行了全面的研究（comprehensive study）。这些pathces由增加new feature，fix bug，提升性能，代码维护（maintenance）等大类组成。味蕾更好地理解Preempt_RT的演化过程，我们进行比较广泛的研究（conduct a broad study）来回答下面三类基础问题（three categories of fundamental questions）：

- Overview: Preempt_RT  patches最常见的类型是什么？Preempt_RT  patches的冗余程度如何？Preempt_RT  patches是如何随着官方Linux kernel演进的?
- Bugs:加了 Preempt_RT  patches后，在内核中会出现哪些类型的bugs？内核中的哪些子系统存在更多的bugs？不同类型的bug会带来哪些类型的后果（consequences）?
- Performance: 哪些技术可以用于提高LInux kernel的实时性能？
- API usage: 对于具有 Preempt_RT能力的Linux kernel，如何理解名字未变/语义改变的RT相关API，如何理解新增加的RT相关API？在具有 Preempt_RT能力的Linux kernel中，应该如何使用这些API来避免bug，提高试试性能？

为了回答这些问题，我们手动分析了每个patch来理解其目的和功能（purpose and functionality），并对每个patch进行了分类，形成具有annotation的patch iterm，其格式如下：

```
PATCH_ITEM ::= * VERSIONS  PATCH_TITLE {CHARACTERISTIC::ASPECT} \n PATCH_CHANGS
VERSIONS ::= '['BEGIN_VERSION - END_VERSION']'|'['BEGIN_VERSION']'
BEGIN_VERSION|END_VERSION ::= [2..4].[0..18].[22..29]
PATCH_TITLE ::= TITLE.patch 
TITLE|DESCRIPT = ['a'..'z','A'..'Z']*|NULL //string or nothing
CHARACTERISTIC ::='C'
ASPECT ::= FEATURE|BUG|PERFORMANCE|MAINTAIN
FEATURE ::= 'feature'::FEATURE_METHOD::DESCRIPT
FEATURE_METHOD::= 'hardware'|'debuginfo'|'idle'|'hrtimer'|'statistics'|'delay'
BUG ::= 'bug'::BUG_CONSEQUENCE::BUG_TYPE::FIX_METHOD::DESCRIPT
BUG_CONSEQUENCE ::='corrupt'|'hang'|'crash'|'leak'|'irq'|'livelock'|'na'|'??'|...
BUG_TYPE ::= SEMANTIC|CONCURRENCY|MEMORY|ERRORCODE
SEMANTIC ::= 'hardware'|'softirq'|'migration'|'preempt'|'irq'|'na'|...
CONCURRENCY ::= 'atomicity'|'order'|'deadlock'|'livelock'|...
MEMORY ::= 'resource leak'|'uninit var'|'buf overflow'|...
ERRORCODE ::= 'compiling err'|'config err'|'runtime err'|'var type'|...
FIX_METHOD ::= 'hardware'|'lock'|'irq'|'preempt'|'migration'|'other'|...
PERFORMANCE ::= 'performance'::PERF_METHOD::DESCRIPT
PERF_METHOD ::= 'cache'|'msleep'|'softirq'|'barrier'|'idle'|'mm'|'hrtimer'|...
MAINTAIN ::='maintain'::MAINTAIN_METHOD
MAINTAIN_METHOD ::='refactor'|'donothing'|...
```

我们通过分析，发现有属于不同内核版本的不少patches是相同或近似的，为此我们把这些patches合并为一个，用PATCH_CHANGS来表示他们的关系，一个例子如下

```
      + [[file:2.6.22/new-softirq-code.patch][2.6.22]]  {MOD::arch/i386}
      M [[file:2.6.23/new-softirq-code.patch][2.6.23]]
      m [[file:2.6.24/new-softirq-code.patch][2.6.24]]
        [[file:2.6.25/new-softirq-code.patch][2.6.25]]
      - 2.6.26
   Meaning of the first character:
      [+]        This patch is introduced in this version (not seen in previous ones).
      [-]        This patch appears in the previous version but disappears in this one.
      [ ]        This patch is seen in both the previous and current version.
                 This patch is identical in the two versions.
      [m]        This patch is seen in both the previous and current version.
                 The changed lines in the patches are identical, but the contexts are not.
      [M]        This patch is seen in both the previous and current version.
                 The changed lines in the patches are different.
      KER_MOD    The 1~2 level directories(means kernel modules) of kernel src code
```
Limitations: 我们的研究仅局限在我们分析的这22个版本的Preempt_RT patches。对于不属于这22个版本的Linux kernel，	由于缺少相应的Preempt_RT patches，使得不能反映Linux对Preempt_RT能力支持的所有演化过程。且对于与Real-Time Linux kernel有关，但不属于Preempt_RT patches的其他patches，我们没有分析到。另外，我们并没有研究属于其他实现方式的Real-Time Linux方案，如RTAI，Xenomai，L4Linux等。这将是我们未来的工作。

## 3 PATCH Overview 

### 3.1 patch overview

针对我们分析的每个内核版本，大约有300个左右的patches组成了Preempt_RT的功能。这些patches在kernel maillist，bug report websites， [lwn website][3]等地方被大量讨论。在本节中，我们将调查有关这些patches的普遍问题：(1) Preempt_RT的patches的冗余度如何？(2) (3)

### 3.2 redundancy and uniqueness  of patches

####  redundancy 

我们分析的Preempt_RT的patches横跨22个版本，一共有6900个，其中针对每个版本的patche数量在200～400之间，通过分析，我们发现这些patches中存在大量的冗余，通过分析我们得到的出现Preempt_RT的patches的冗余度分布图如下

![Patch Frequency](chy_figs/patch_frequency.png)

可以看出整张图像类似长尾分布，虽然大部分patch出现的次数较少，只有少量patch出现多次。特别是出现了22次的两个feature类型的patch，在分析的各个内核版本中都有出现，一个与网络驱动相关，一个与屏蔽中断相关。然而，在上述分布图中，由于分析的patch对应的内核版本为从2.6.22~4.11，因此凡是4.11中引入的patch只可能出现一次，同样，在4.9中引入的patch出现次数也不会超过两次，以此类推，我们可以认为patches的冗余程度可能更高。

####  uniqueness

由于Preempt_RT的patches的冗余度较大，所以我们进一步分析了在不同内核版本中独有的Preempt_RT patches的数量，Preempt_RT的patches的唯一性分布图如下所示：

![Patch Uniqueness](chy_figs/patch_uniqueness.png)

对应某个内核版本的patch如果没有在其他版本出现过则被认为是独有的，由于在分析中2.6.22版本没有前驱，4.11版本没有后继，因而二者独有的patch数目最多。为了看的更加清楚，我们可以考虑新引入的patch，即在某一版本前都不存在，在该版本新引入的patch的分布。不同内核版本中新引入的RT patch的数量分布如下图：

![New Patch Frequency](chy_figs/new_patch_frequency.png)

从图中可以看出在除了2.6.22由于是第一次引入Preempt_RT patches，不具有参考性。内核2.6x中新patch数量平均小于100个，其中2.625的patch数量小于50个。在3.x以后的版本中，除了3.0和4.11，新引入的patch数量也小于50个。3.0和4.11的新patches数量相对多的原因是由于增加和改进了irq/softirq的thread化能力，已经从新实现和改进对hotplug的real-time能力的支持。总体而言，我们可以认为将Linux改进为实时操作系统的工作量较大，但如果不增加新real-time功能或对内核模块进行real-time改造，那完善后在各个版本间升级维护的代价相对较小。

### 3.2  patch type

对Preempt_RT patches的分类描述如表一所示。我们把patches分为new features(feature)，bug fixes(bug)，performance improvements(performance)，maintenance and refactoring(maintenance)四类。对于每一类还可进行细分到二级分类（feature，performance，maintenance）或三级分类(bug)，比如对于bug类patches，还可细分为：semantics，concurrency，memory，error_code等四个二级类，每个二级bug分类有4～5个三级分类。每一个patches通常属于单个分类中。为了分析的准确性，我们在统计patches的分类时，只考虑unique的patches。

表一：Patch Type：对Preempt_RT patches的分类描述

|    Type     |               Description                |
| :---------: | :--------------------------------------: |
|   Feature   | 实现新的RT Feature，确保新添加的功能不影响non-RT config下Linux Kernel的语义 |
|     Bug     |                 修复已有bugs                 |
| Performance |    通过语义/IRQ/Concurrency等方面修改，提高实时响应能力    |
| Maintenance |           维护文档和维护/重构代码（不改变语义）            |

如果不考虑从6900个Preempt_RT patches的冗余度，那么大约有76.4%的patches可以可参考上一个一个内核版本中几乎相同的修改内容完成对当前版本的修改。所以，其实从某种程度上来讲，这些patches都可归类于Maintenance 类型，这样Maintenance 类型的patches占了绝大多数。但如果只考虑unique patches，那么情况有所不同，下图显示了unique Preempt_RT patches在不同内核版本中的数量，以及不同类型的patches所占的百分比。在这些具有唯一性的patches中，较大部分的patches属于feature patches，占了大约45%，大部分集中在与同步互斥相关的部分。另外处于第二位的是fix-bug patches，占了大约29.7%，这也说明了由于Preempt_RT的引入，容易触发更多的内核bug。

![patch type](chy_figs/patch-type.png)

对于占大多数的feature patches，我们可进一步把它们细分了“trace/statistics”、“hardware/architecture”、“rt_suppor/kernel_subsystem”类型。rt_support/kernel_subsystem patches实现了Linux kernel中与硬件无关的Preempt_RT核心能力，主要体现在对spin_lock的基于rt_mutex的实时改造，full preempt支持，irq/softirq的强制内核线程化支持等，并进一步修改内核中的核心子系统lock/mutex/synchronization/shceduling/memory menagement/network等，从而形成了Linux with Preempt_RT的核心框架 。

hardware/architecture patches是在Linux with Preempt_RT核心框架的基础上，完成对不同硬件体系结构和外设的支持。当前主要支持的体系结构包括x86/arm/mips/powerpc/68knommu，但68knommu的支持越来越少，可能说明这类硬件在逐步消失。另外一个重要的外设支持是High-Resolution Timer，这是Preempt_RT的重要feature之一。而cpu_hog_plug 子系统的real-time支持相对而言持续时间很长，且改动较大，在kerner 4.11中，有多达近10%的patches与cpu_hog_plug子系统real-time支持相关。

trace/statistics patches给Linux kernel添加了动态检查bug和分析性能异常的能力，考虑到由于Preempt_RT patches极大提高了Linux kernel的实时抢占能力的同时，也引入了不确定性，从而使得分析kerne with Preempt_RT的bug和performance变得难度加大。为此在Ftrace中引入了对lock/irq/preempt/wakeup latency的动态跟踪支持机制，可以方便地分析出内核中的real-time latency 瓶颈；而lockdep机制的引入加强了对dead lock和live lock的动态探测能力；might_sleep机制加强了对atomic context下不允许sleep行为出现的动态检查能力。

通过把bug类的patches进行进一步分析和划分（如下图所示），我们发现semantic bug和concurrency bug占了大部分（Sec. 4)。对于语义bug，占了bug数量的48.3%。对于concurrency bug，占了bug数量的28.2%，语义bug和concurrency bug很难重现，需要能够对相关的上下文，比如硬件特性，时钟，irq/softirq等，有比较清楚的了解，才能修改，所以修复的难度较大。在这里面，might_sleep，atomicity violation和deadlock/livelock类占了大部分。其他类型的bug主要属于memory bugs和error_code bugs。在memory bugs中，变量未初始化，数据处理错误，资源/动态分配的内存没有释放等问题依然存在；而对于error _code bugs，编译错误和配置错误占了主要部分，这方面的修改相对比较容易一些。由于这类bug patches对内核开发者和bug 分析工具很重要，所以我们将在后面小节进行更详细的分析（Sec. 4）

![bug](chy_figs/bug-type.png)

对于performance patch，尽管在数量比较少，但能在尽量改动代码很少的情况下，兼顾non-RT下的throughput性能和和RT配置下低延迟的性能要求。特别是在Preempt_RT提供了migrate_disable/enable机制和local_lock机制后，通过对内核代码的改动来替换在各种context下的禁止调度和全局互斥的API使用，进一步提高了在UP和SMP场景下，减少preempt_disable/enable机制和全局lock机制引入了的额外开销。而对于maintenance patches，如果不考虑实际上内容重复的冗余patches，其总体数量也比较少，主要是在保证语义不变的情况下，完善和重构代码，并且添加文档。

### 3.3   Distribution and Size of Patches

Preempt_RT patches对内核的修改分布在内核的各个方面，下图显示了Preempt_RT patches对主要的内核子系统的修改程度。从中可以看到，在数量上，由于Preempt_RT patches需要支持不同类型的系统结构和硬件特征，所以对arch内核子系统和驱动子系统的修改是最多的，且主要集中在x86和arm cpu上。另外一类是kernel+init内核子系统，这主要是由于Preempt_RT patches需要对抢占（preempt）进行不同的管理与控制，所以对kernel子系统中与scheduling相关的代码进行了较多的修改，确保能够支持除了irq_disable/preempt_disable的context情况，其他情况下都允许实时的CPU抢占发生。另外，在fs/mm/net等重要的内核模块中，为了提高是实时性，也对相应的代码进行了修改，主要是放宽了对CPU抢占的约束，比如把preempt_disable函数换为migrate_disable函数等。

![patch_size](chy_figs/component_distribution.png)

Patch size是一个评价代码复杂性的一种方法。从下图中可以看出大约有50%的bug小于10行的变动，大多数的bug比较小，feature patch相对与其他patch变化比较大，对于feature patch大约有20%的补丁超过了100行，有2%-3%的patch超过了100行。但从数据上看到feature patch相对与其他patch大量存在，这里可能存在问题。feature大约等于其他补丁的总和。

![patch_size](chy_figs/patchsize.png)

## 4 Preempt_RT bugs

在本节，我们将详细研究Preempt_RT bugs，从而理解bug patterns和它的后果（consequences）。首先会对Preempt_RT bugs进行二级分类，并分析不同类型bug的数量和分布情况，并将描述bug patterns和bug consequences，然后重点对与Preempt_RT有比较直接关系的Concurrency Bug进行了详细分析。最后，我们会分析修复Concurrency Bug的方法。在分析bug前，我们需要对Linux kernel with Preempt_RT的执行上下文（execution context）进行一定的阐述。

在PREEMPT_RT kernel的执行过程中，有4种基本的执行上下文：hard interrupt context，hard interrupt thread context，soft interrupt thread context，process context。hard interrupt context是指操作系统刚接收到硬件中断后，执行屏蔽中断，处理timer等硬件相关基本中断流程，响应硬件控制器，使能中断过程的执行上下文。在此期间，操作系统使用的是中断栈，不可被抢占，可被local_irq_disable来禁止响应中断。hard interrupt thread context是指操作系统以内核线程的执行方式处理某一具体硬件中断过程的执行上下文。在此期间，此内核线程可被高优先级线程完全抢占(fully preemptible)。soft interrupt thread context是指操作系统以内核线程的执行方式处理某一具体软件中断过程的执行上下文。在此期间，此内核线程可被高优先级线程完全抢占(fully preemptible)，也可由其他线程执行local_bh_disable来禁止执行直接处理softirq相关的内核线程。process context是其他用户进程或内核进程执行过程的执行上下文。在此期间，此用户进程或内核进程可被高优先级线程完全抢占(fully preemptible)。这里完全抢占(fully preemptible)是指除了local_irq_disable, preempt_disable, raw_spin_lock外，此执行体中任意位置可以被抢占（preempt）。所以，我们把loca_irq_disable/enable，preempt_disable/enable，raw_spin_lock/unlock之间的代码执行上下文称为原子上下文atomic context，不允许出现抢占。如果在atomic context出现了会引起调度的代码，则违反代码执行的原子性，会进一步引起concurrency bug。

在SMP环境下，虽然local_irq_disable, preempt_disable可以阻止当前执行的线程/进程被本地CPU抢占以保护临界区，但无法阻止远地CPU的其他线程访问临界区的共享资源，所以需要通过migrate_disable来避免当前线程迁移到其他CPU上，避免per-cpu类型的数据访问出错。而通过rt_mutex和raw_spin_lock可以确保对全局共享资源的互斥访问，如果对这些函数使用不当，则会出现违反原子性（ atomicity-violation）相关的concurrency bug。而如何对内核中的同步函数使用不当，这会出现违反执行顺序（order-violation）相关的concurrency bug。

### 4.1 bug pattern

通过对Preempt_RT patches的分析，共有477个bugs，占整个patches的近30%。其中可进一步分类为semantics，concurrency，memory，err_code这四类，每类的描述与下表所示。semantics bugs的数量占整个bugs数量的9%，与具有的语义和执行环境相关。对于hardware/time bug，主要与具体硬件和外设相关，比如设置相关寄存器有误等，与concurrency异常/错误没有直接关系。由于time的正确处理会直接影响到kernel的正确执行，所以如果timer没有正确执行，会出现系统挂起（hang），硬件访问错误，数据访问错误等后果。对于err_access bug，由于对执行特权处理不当，导致会出现用户态程序访问内核态数据的访问错误。 由于在代码编写中，对代码所在的执行上下文考虑不够全面，导致会出现与函数语义不一致的编程逻辑有误，我们把这类错误归结为other，与concurrency异常/错误没有直接关系。

memory bugs的数量占整个bugs数量的6%，主要是资源泄漏(resource leak)，资源/变量没有初始化，变量类型错误，缓冲区溢出，数据访问权限错。相对而言，这些错误与Preempt_RT的关系不够密切，在官方Linux kernel中有同样类型的bug。

err_code bug的数量占整个bugs数量的16%，主要是kernle的编译错误和config错误。由于Linux kernel支持不同硬件和功能的多选项配置，使得kernel开发者可能只考虑了某些特定选项配置下的编译正确性，而没有足够的时间和精力去检查在其他合法选项配置下的编译正确性，导致这类相对比较简单的错误数量较高。

Table The Description of Bug Category

| Bug Category / Num | Description                              |
| :----------------: | ---------------------------------------- |
|   semantics /119   | Inconsistencies with the requirements or the programmers |
|  concurrency /254  | Mutex/Synchronization problems among the concurrent tasks |
|     memory /29     | Bugs caused by improper handling of memory objects. |
|    err_code/75     | compiling kernel error or config kernel error |

Table The Description of Semantic Bug

| Semantic Bug/ Num | Description         |
| ----------------- | ------------------- |
| hardware / 24     | 硬件初始化/工作流控制逻辑错误     |
| time / 19         | 时间处理相关的错误           |
| err_access / 3    | 引起用户态程序访问内核态数据的访问错误 |
| other / 75        | 与函数语义不一致的其他编程逻辑有误   |


concurrency bugs的数量占整个bugs数量的69%，大部分与违反原子性（ atomicity-violation）相关，还有部分与违反执行顺序（order-violation）相关。下面将进一步深入分析concurrency bugs。

### 4.2 Concurrency Bug

对于占bug数量比例最多的concurrency bug，我们进一步细分为8类bug，具体如下表所示而migration/preempt/scheduling/irq/softirq bug与concurrency异常/错误有相对比较近的关系，大部分归结为而这类bug是我们主要的分析对象。

| Concurrency Bug / Num | Description                              |
| --------------------- | ---------------------------------------- |
| migration  / 14       | 与线程/进程迁移处理中的错误                           |
| preempt  / 29         | 与线程/进程能否抢占相关的错误                          |
| scheduling /10        | 与线程/进程调度相关的错误                            |
| irq/softirq / 64      | 与设置中断/软中断相关的错误                           |
| mutex / 43            | 临界区没有保护好/过度保护共享资源的互斥(mutex)访问.           |
| order / 17            | 没有确保执行的顺序性(sync,barrier),或者barrier工作无效了。 |
| deadlock / 67         | 一个线程获取部分资源，等待另一线程拥有的资源，线程间形成了依赖环，导致死锁    |
| livelock / 10         | 一个线程由于调度/资源等因素，在不确定的长时间范围内得不到执行，导致活锁     |

#### migration相关：

migration bugs与跨CPU的per-cpu data访问和per-cpu kernel thread有直接的关系。由于应用通过系统调用可设置进程与CPU的绑定关系，且内核中也可以设置线程是否允许迁移，从而可能使得migration_disable/enable执行无效，导致出现与迁移相关的concurrency bug。这使得需要了解Kernel中与migration相关的其他控制逻辑，使得它们与Preempt_RT提供的migration_disable/enable不会出现矛盾的情况。另外，migration_disable/enable之间的代码，可以确保对per-cpu数据的访问不会由于迁移到其他cpu上，从而导致per-cpu数据访问错误，所以，需要检查代码中有关per-cpu数据访问的代码是否已经有migration_disable/enable的保护，或者是更强的preempt_disable/enable，loca_irq_disable/enable的保护，如何没有，则会出现严重的数据访问错和系统崩溃。

#### preempt/scheduling/irq/softirq相关：

preempt/irq/softirq bugs与Local CPU上的调度与抢占有直接的关系。在kernel代码中，如果有在atomic context中执行的代码会有Local CPU的抢占行为发生，这意味着在不允许调度/阻塞的地方执行了调度/阻塞的操作，会导致时长不定的长延迟或死锁等情况的发生。为此，需要在控制逻辑上把这部分代码移到其他不在atomic context的地方去执行，才能避免这个问题。或者是在允许抢占行为的函数中添加might_sleep等动态检查函数，这样在atomic context中，如果执行了might_sleep函数，则kernel或报告错误，从而帮助内核开发者定位和修复错误。

mutex相关：

mutex bug与Uniprocessor和MultiProcessor情况下的互斥资源保护有直接关系。kernel with Preempt-RT中存在两类需要互斥保护的数据：per-cpu data，只能被本地cpu访问和global data，可被所有CPU访问。为了减少互斥带来的性能开销，在kernel with Preempt-RT中存在多种类型的函数来确保在不同级别上的互斥。对于Uniprocessor，可以通过local_irq_disable/preempt_disable/local_lock等函数，并结合各种lock等函数来确保per-cpu data和global data访问的在local CPU上的互斥性。对于Multiprocessor，可以通过migration_disable/spin_lock/raw_spin_lock等机制来确保在multi cpu之间的互斥性。为编程的效率，kernel在这些底层基础函数之上进行了基于高层语义的函数封装，便于在driver/arch/memory/net上的kernel 开发。这使得与mutex相关的函数层次不一，可适合的场景多样，这进一步加大了开发者对选择合理的内核函数和函数组合来保护需要互斥访问的资源的难度，很容易产生mutex bug。

#### order/dead lock/live lock相关：

order/dead lock/live lock与并发执行情况下的执行顺序和执行的时机相关。对于order bug，由于与执行操作的先后顺序相关。一种情况是与具体硬件（比如clock）和内核子系统（比如network）某些操作序列执行完毕后才能执行接下来的操作，但由于实际代码编写中对于操作序列，并没有完整执行，导致会出现硬件错误，数据访问出错，系统挂起等问题。另外一种情况是在non-RT和RT两种配置情况下，同样函数名的函数有不同的语义，所以需要针对操作序列顺序不一致， 从A()-->B()-->C()变成了A()-->C()-->B()。这类问题是由于

对于dead lock bugs，一种情况是内核线程嵌套调用mutex lock相关操作，导致死锁。另外一种情况是在一个内核线程中的atomic context执行了抢占/阻塞操作，引发另外一个线程再次调用mutex lock相关操作，导致死锁。或者是本来应该用mutex lock相关操作形成atomic context，但实际上的相关操作并没有形成atomic context，从而导致死锁。

对于live_lock bug，大部分与抢占/同步相关的内核函数的执行时机相关。在atomic context中执行的代码，一旦离开了atomic context，就需要进行抢占检查（preemption check），从而可确保不会有live lock的情况。由于离开atomic context的代码函数多种多样，所以开发者可能会忽略对离开atomic context后的抢占检查。为此，需要分析离开atomic context的共有控制逻辑，并在每个共有控制逻辑中确保执行了抢占检查。

### 4.3 Fix Strategies 

对于不同类型的bugs，有专门正对下的修复策略，但也有一些共性的修复策略。下面的表格描述和统计了对所有bug的修复策略。对于属于编译出错和config出错的err_code bug，一般的错误原因通过编译器的编译错误输出就可以看到，错误现象比较简单和直接，且容易修改，主要的解决办法就是根据编译器的编译错误输出直接修改源文件中的语法错误和config文件的配置错误。对于memory bug，其错误后果需要在运行时才能看到，所以首先需要对运行时的kernel error/bug log信息进行分析，并采用相对应的修改策略，比如i变量类型进行修改，完善变量的初始化过程，确保数据资源的合理动态申请与释放等。相对而言，err_code bug和memory bug与Preempt_RT的关系不大，与官方kernel的patch中同类bug的修复策略基本一样。

对于semantic bug的修复策略，大部分与具体硬件控制规范或软件逻辑有关，比如对于硬件控制的处理流程有误，对错误/异常情况的处理考虑不全，某功能的实现缺失等，所以修复方法差异性较大，比较难找到共性的地方。而semantic bug与Preempt_RT有一定的直接或间接关系。特别是如果深入分析，会发现部分修改的逻辑其实与同步互斥相关，其所涉及的函数表面上看与Preempt_RT相关的底层基础同步/互斥函数无关，但通过基于call graph等静态分析，可以发现这些高层函数会直接或间接地调用与Preempt_RT相关的底层基础同步/互斥函数，从而修复了与concurrency bug一样的问题。另外还有一类修复策略与动态检查相关，通过在代码中添加runtime check，类似动态的assert功能，可有效地在运行时发现问题，并可进一步解决未来会出现的bug。

| Fix Method / Num   | Description                              |
| ------------------ | ---------------------------------------- |
| hardware /24       | 硬件相关的修复                                  |
| mutex / 58         | 互斥相关的修复                                  |
| sync\|order / 23   | 同步/执行顺序相关的修复                             |
| irq\|softirq / 66  | 中断/软中断相关的修复                              |
| preempt / 39       | 抢占相关的修复                                  |
| migration / 14     | 迁移相关的修复                                  |
| idle  / 4          | idle OR suspend/resume相关的修复              |
| sched / 10         | 调度相关的修复                                  |
| memory /18         | 针对variable的类型变化/初始化/申请与释放等修复             |
| config /13         | config相关的修复                              |
| syntax /53         | 修复编译语法错误                                 |
| runtime check / ?? | add/modify might_sleep() function/condition to do runtime check |
| semantics /156??   | 不属于上述修复手段，与具体代码逻辑有关的语义修复                 |

由于concurrency bug直接与Preempt_RT相关，且数量最多，对于concurrency bug的修复策略将详细分析。首先之前已提到concurrency bug大部分与违反原子性（ atomicity-violation）相关，还有部分与违反执行顺序（order-violation）相关。

#### Fix Strategies for  atomicity-violation bug

由于在kernel with Preempt_RT中的atomic context可细分为多个层面，具体描述如下：

Table X:  Description of different atomicity context in Linux Preempt-RT

| Basic Atomicity Context | Description                              |
| ----------------------- | ---------------------------------------- |
| spin critical section   | can mutex access global resource with spin_lock method in Multi Processors env. |
| sleep critical section  | can mutex access global resource with sleepable_lock method in Multi Processors env. |
| no_interrupt            | disable interrupt and can mutex access per-cpu resource in local CPU env. |
| no_preempt              | disable sched/preempt and can mutex access per-cpu resource in local CPU env. |
| no_migrate              | disable migrating to other CPU and can avoid access per-cpu resource of other CPU env. |
| no_softirq/bh           | disable migrating softirq thread if task.softirq_nestcnt==1 and can avoid access per-cpu resource of other CPU env. |

这里需要注意，对于如果通过local_irq_disable实现了no_interrupt atomicity level则也就意味这实现了no_softirq/bh，no_preempt和no_migrate。它们之间的atomic强度为:

```
no_interrupt>no_preempt>no_migrate>no_softirq/bh
```

这里no_softirq/bh是一种有条件的no_migrate atomicity level，它只有在current的task.softirq_nestcnt==1的情况下才处于no_migrate atomicity level。另外，spin critical section和 sleep  critical section是属于一个Basic Atomicity集合，而其他的属于另外一个Basic Atomicity集合，这两个集合中的item可组合，形成compound atomicity。但需要注意，sleep critical section不能与禁止切换的no_interrupt和no_preempt组合在一起。

正对不同类型的共享资源，需要用能够形成正确的compound atomicity context。正是由于 atomicity context和共享资源特征的多样性，使得kernel开发者容易出现错误。对于违反原子性（ atomicity-violation）的bug，通常的修复策略是针对共享资源特征用符合atomic强度的atomicity context。另外，可充分利用kernel中已有的might_sleep和添加条件判断增加发现新bug的可能性。

#### Fix Strategies for  order-violation bug




## 5  Program Rules in Preempt_RT

### 




## 6 Related work

## 7 Conclusions

## References

- [PREEMPT_RT](http://rt.wiki.kernel.org/index.php/Main_Page)

- [RTAI](https://www.rtai.org/)

- [xenomai](http://www.xenomai.org/index.php/Main_Page)

- [dual-core RTLINUX](http://www.windriver.com/products/platforms/real-time_core/)

- [xtratum](http://www.xtratum.org/)

- [A realtime preemption overview](https://old.lwn.net/Articles/146861/)

- [Different approaches to Linux realtime](http://lwn.net/Articles/143323/)

- [Per-CPU variables and the realtime tree](https://lwn.net/Articles/452884)

- [The return of simple wait queues](https://lwn.net/Articles/661424/)

- [Realtime mainlining](https://lwn.net/Articles/662833/)

- [PREEMPT_RT patchset](https://www.kernel.org/pub/linux/kernel/projects/rt/)

- [Realtime preemption and read-copy-update](https://lwn.net/Articles/129511/)

- [rationale for timer/hrtimer split](http://lwn.net/Articles/152363/)

- [deferrable timers](http://lwn.net/Articles/228143/)

- [high-resolution timer API – dated](http://lwn.net/Articles/167897/)

- [Threaded Interrupts Approaches, October 2004](http://lwn.net/Articles/106010/) 

- [Threaded Interrupts Debate, June 2005](http://lwn.net/Articles/138174/)
- [Linux 死锁检测模块 Lockdep 简介](http://blog.jobbole.com/100078/)
  ​

- [• http://en.wikipedia.org/wiki/RCU
  • http://lwn.net/Articles/128228/ (early realtime-RCU attempt)
  • http://www.rdrop.com/users/paulmck/RCU/OLSrtRCU.2006.08.11a.pdf
  (realtime-RCU OLS paper)
  • http://www.rdrop.com/users/paulmck/RCU/ (More RCU papers)
  • http://www.rdrop.com/users/paulmck/RCU/linuxusage.html (Graphs)
  • http://lwn.net/Articles/201195/ (Jon Corbet realtime-RCU writeup)
  • http://lwn.net/Articles/220677/ (RCU priority boosting)
  • http://lwn.net/Articles/220677/ (patch for higher-performance RCU)

- Threaded Interrupts softirq splitting, June 2005](http://lwn.net/Articles/139062/)




## QA

### 分析real-time的性能层次？

### 支持的cpu的情况？

### 为了支持新内核，需要增加的新patch的情况如何？这说明了upate的困难度， 是否也可看看seda的支持能力？

### concurrency bug都应该与rt-linux相关？如何统计linux kernel的concurrency bug?

### definitions/types of the bugs/faults

### What code is analyzed?  rt-patch在内核不同模块中的分布，这说明了linux对rt的支持程度，特别是在driver方面

### How many faults are there?

### Where are the faults?
