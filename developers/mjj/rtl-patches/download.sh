#!/bin/bash

truncate -s 0 vers.txt
cat list.txt | while read f; do
    fn=`basename $f`
    ver=`echo $fn | sed "s/patch[^-]*-//g" | sed "s/-broken-out//g" | sed "s/\.tar.*//g"`
    if [[ $ver =~ ^2.* ]]; then
	ver=`echo $ver | grep -o "^2\.6\.[0-9]*"`
    else
	ver=`echo $ver | grep -o "^[34]\.[0-9]*"`
    fi
    if [[ ! -d $ver ]]; then
	wget -nc $f && tar xf $fn && mv patches $ver
    fi
    echo -n "$ver " >> vers.txt
done

bash ./fix-subjects.sh
