#!/bin/bash

a=(2.6.22 2.6.23 2.6.24 2.6.25 2.6.26 2.6.29 3.0 3.2 3.4 3.6 3.8 3.10 3.12 3.14 3.18 4.0 4.1 4.4 4.6 4.8 4.9 4.11)
#echo $a
#num=0
for i in ${a[@]}; do
   cd $i; ls -l|wc; cd ..
done >nums.txt
vers_num=`wc nums.txt|awk '{print $1}'`
patches_num=`awk '{sum+=$1} END{print sum}' nums.txt`

echo kernel version number $vers_num, patches number $patches_num 
