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

rt-linux evolve through patches. A large number of patches are discussed and submitted to mailing lists, bug report websites, and other forums. Some are used to implement new features, while others fix existing bugs. In this section, we investigate three general questions regarding rt-linux patches. First, what are rt-linux patch types? Second, how do patches change over time? Lastly, what is the distribution of patch sizes?

In the PREEMPT_RT kernel there are 4 essential types of contexts: "hard interrupt context", "interrupt context", "soft interrupt context" and "process context". The hard interrupt context is an extremely small shim in essence - a few tens of lines total, per arch - it just deals with the interrupt controller, masks the IRQ line, acks the controller and returns. The "interrupt context" is a separate per-IRQ interrupt thread, which behaves like a process and is fully preemptible. "Soft interrupt context" is a separate per-softirq system-thread too, fully preemptible. "Process context" is what it used to be, and fully preemptible too. ['fully preemptible' means it's preemptible for in essence everything but the scheduler code and the basic RT-mutex/PI code]

## 

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

数据需要更新？？？

![patch_size](chy_figs/patchsize.png)





## 4 Preempt_RT bugs

In this section, we study rt-linux bugs in detail to understand their patterns and consequences comprehensively. First, we show the distribution of bugs in rt-linux logical components. Second, we describe our bug pattern classification, bug trends, and bug consequences.  Finally, we analyze each type of bug with a more detailed classification and a number of real examples.


> [Mao] Which bugs are going to be studied? If we only consider those explicitly
> fixed in the patchset, I doubt if we have an adequate amount of bugs to
> support our claim (25 patches w/ Call Trace in 4.9-rt1, mostly fixing
> preemptible spin locks in preempt_disabled sections).

### 4.0 some rules on RT-patch

an overview of the features/rules that the PREEMPT_RT patch provides.

1. Preemptible critical sections
2. Preemptible interrupt handlers
3. Preemptible "interrupt disable" code sequences
4. Priority inheritance for in-kernel spinlocks and semaphores
5. Deferred operations
6. Latency-reduction measures

#### Preemptible critical sections

- In PREEMPT_RT, normal spinlocks (spinlock_t and rwlock_t) are preemptible, as are RCU read-side critical sections (rcu_read_lock() and rcu_read_unlock()). 
- This preemptibility means that you can block while acquiring a spinlock, which in turn means that it is illegal to acquire a spinlock with either preemption or interrupts disabled (the one exception to this rule being the _trylock variants, at least as long as you don't repeatedly invoke them in a tight loop).
- This preemptibility also means that spin_lock_irqsave() does -not- disable hardware interrupts when used on a spinlock_t.
- what to do if you need to acquire a lock when either interrupts or preemption are disabled? You use a raw_spinlock_t instead of a spinlock_t, but continue invoking spin_lock() and friends on the raw_spinlock_t. 
- These raw locks(raw_spinlock_t,raw_rwlock_t)) should not be needed outside of a few low-level areas, such as the scheduler, architecture-specific code, and RCU.
- Since critical sections can now be preempted, you cannot rely on a given critical section executing on a single CPU -- it might move to a different CPU due to being preempted. 
- when you are using per-CPU variables in a critical section, you must separately handle the possibility of preemption: (1) Explicitly disable preemption, either through use of get_cpu_var(), preempt_disable(), or disabling hardware interrupts. (2) Use a per-CPU lock to guard the per-CPU variables. One way to do this is by using the new DEFINE_PER_CPU_LOCKED() primitive

#### Preemptible "interrupt disable" code sequences

- Code that must interact with SA_NODELAY interrupts cannot use local_irq_save(), since this does not disable hardware interrupts. Instead, raw_local_irq_save() should be used.
- Similarly, raw spinlocks (raw_spinlock_t, raw_rwlock_t, and raw_seqlock_t) need to be used when interacting with SA_NODELAY interrupt handlers.
- However, raw spinlocks and raw interrupt disabling should -not- be used outside of a few low-level areas, such as the scheduler, architecture-dependent code, and RCU.

#### Preemptible "interrupt disable" code sequences

The concept of preemptible interrupt-disable code sequences may seem to be a contradiction in terms, but it is important to keep in mind the PREEMPT_RT philosophy. This philosophy relies on the SMP capabilities of the Linux kernel to handle races with interrupt handlers, keeping in mind that most interrupt handlers run in process context. Any code that interacts with an interrupt handler must be prepared to deal with that interrupt handler running concurrently on some other CPU.

- spin_lock_irqsave() and related primitives need not disable preemption.  The reason this is safe is that if the interrupt handler runs, even if it preempts the code holding the spinlock_t, it will block as soon as it attempts to acquire that spinlock_t. The critical section will therefore still be preserved.
- local_irq_save() still disables preemption, since there is no corresponding lock to rely on.
- Using locks instead of local_irq_save() therefore can help reduce scheduling latency, but substituting locks in this manner can reduce SMP performance, so be careful.
- Code that must interact with SA_NODELAY interrupts cannot use local_irq_save(), since this does not disable hardware interrupts. Instead, raw_local_irq_save() should be used. 
- Note that SA_NODELAY should -not- be used for normal device interrupts: (1) this will degrade both interrupt and scheduling latency and (2) SA_NODELAY interrupt handlers are much more difficult to code and maintain than are normal interrupt handlers.

#### Deferred operations

- Since spin_lock() can now sleep, it is no longer legal to invoke it while preemption (or interrupts) are disabled.  In some cases, this has been solved by deferring the operation requiring the spin_lock() until preemption has been re-enabled: put_task_struct_delayed() queues up a put_task_struct() to be executed at a later time when it is legal to acquire (for example) the spinlock_t alloc_lock in task_struct. mmdrop_delayed() queues up an mmdrop() to be executed at a later time, similar to put_task_struct_delayed() above. In all of these situations, the solution is to defer an action until that action may be more safely or conveniently performed.

### 4.1 correlation between using modules and bug

内核那部分使用 rt feature容易出现bug



### 4.2 Bug Patterns

To build a more reliable rt-linux, it is important to  understand the type of bugs that are most prevalent and the typical patterns across rt-linux. Since different  types of bugs require different approaches to detect and fix, these fine-grained bug patterns provide useful information to developers and tool builders alike.

We partition rt-linux bugs into X categories based on their root causes as shown in Table X.

Figure 2(b) (page 4) shows the total number and per-centage of each type of bug across rt-linux. There are about 1800 total bugs, providing a great opportunity to explore bug patterns at scale. Semantic bugs dominate other  types . Most semantic bugs require rt-linux domain knowledge to understand, detect, and fix; generic bug-finding tools (e.g., Coverity [9]) may have a hard time finding these bugs.

in Linux 2.6.33, away from the Big Kernel Lock (BKL), which introduced a large number of concurrency bugs.



### 4.3 Bug Trends

rt-linux mature from the initial development stage to the stable stage over time, by applying bug-fixing, performance and reliability patches. Various bug detection and testing tools are also proposed to improve rt-linux stability. A natural question arises: do rt-linux bug patterns change over time, and in what way?

趋势与版本相关，需要分析各个版本之间的bug pattern的问题。

### 4.4  Bug Consequences

data corruption, system crashes, unexpected errors, deadlocks,system hangs and resource leaks

rt-linux bugs cause severe consequences; corruptions and crashes are most common; wrong behavior is uncommon; semantic bugs can lead to significant amounts of corruptions, crashes, errors, and hangs; all bug types have severe consequences.

### 4.5  Bug Pattern Examples and Analysis



## 5  determinism of Real-Time Performance

A small but important set of patches improve performance and reliability, which are quantitatively different than bug
patches (Figure X). Performance and reliability patches account for X% and X% of patches respectively.


> [Mao] If we want to collect RT performance metrics, we have to test the kernel
> on bare metal (not in VMs) to remove the interference of the VMM. We need to
> start this early next week so that the lkp-related stuff can be finished as
> planned.

###  5.1  determinism related Performance Patches

 There are a few changes in PREEMPT_RT whose primary purpose is to reduce scheduling or interrupt latency.

The first such change involves the x86 MMX/SSE hardware. This hardware is handled in the kernel with preemption disabled, and this sometimes means waiting until preceding MMX/SSE instructions complete. Some MMX/SSE instructions are no problem, but others take overly long amounts of time, so PREEMPT_RT refuses to use the slow ones.

The second change applies per-CPU variables to the slab allocator, as an alternative to the previous wanton disabling of interrupts.

### 5.2  determinism  & throughput experiments




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
