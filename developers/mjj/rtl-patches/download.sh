#!/bin/bash

cat list.txt | while read f; do
    fn=`basename $f`
    ver=`echo $fn | sed "s/patch[^-]*-//g" | sed "s/-broken-out//g" | sed "s/\.tar.*//g"`
    if [[ $ver =~ ^2.* ]]; then
	ver=`echo $ver | grep -o "^2\.6\.[0-9]*"`
    else
	ver=`echo $ver | grep -o "^[34]\.[0-9]*"`
    fi
    wget -nc $f && tar xf $fn && mv patches $ver
done
