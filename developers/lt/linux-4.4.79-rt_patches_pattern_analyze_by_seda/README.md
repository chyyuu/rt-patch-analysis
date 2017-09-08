# README

### 项目说明

​	基于linux-4.4.79的kernel，与linux-4.4.79-rt92的patches，用seda对patches中的每个commit进行分析，抽取出pattern，最后希望能整理出一些规律。

### 项目进度

​	[*] 针对某一个commit分析pattern

​	[ ] 编写脚本，对所有commit批量分析pattern

​	[ ] 整理pattern的规律

### 文件说明

​	patterns文件夹：

​		该文件夹下每个子文件夹表示一个commit的patch，里面放了用seda分析的过程和结果文件，以及原本的patch文件，build_log	和prepare_log是过程log，coccigen_result是从patch中抽取出的pattern。

### 

​	