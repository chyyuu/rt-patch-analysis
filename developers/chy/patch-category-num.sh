#!/bin/bash
total=`grep '^\*.*{C::' history.org|wc|awk '{print $1}'`
maintain=`grep '^\*.*{C::maintain::' history.org|wc|awk '{print $1}'`
feature=`grep '^\*.*{C::feature::' history.org|wc|awk '{print $1}'`
performance=`grep '^\*.*{C::performance::' history.org|wc|awk '{print $1}'`
bug=`grep '^\*.*{C::bug::' history.org|wc|awk '{print $1}'`
echo total patches is $total
echo maintain $maintain :: `qalc  $maintain/$total`
echo feature $feature :: `qalc  $feature/$total`
echo performance $performance :: `qalc  $performance/$total`
echo bug  $bug :: `qalc  $bug/$total`
