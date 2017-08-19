#!/bin/bash

#echo semantics `grep '^\*.*{C::bug::semantics' history.org|wc|awk '{print $1}'`
#echo concurrency `grep '^\*.*{C::bug::concurrency' history.org|wc|awk '{print $1}'`
#echo performance `grep '^\*.*{C::performance::' history.org|wc|awk '{print $1}'`
#echo bug `grep '^\*.*{C::bug::' history.org|wc|awk '{print $1}'`

bug_total=`grep '^\*.*{C::bug::' history.org|wc|awk '{print $1}'`
#semantics=`grep '^\*.*{C::bug::semantics' history.org|wc|awk '{print $1}'`
#concurrency=`grep '^\*.*{C::bug::concurrency' history.org|wc|awk '{print $1}'`

semantics=233
concurrency=136
echo total bugs is $bug_total
echo semantics bug $semantics :: `qalc  $semantics/$bug_total`
echo concurrency bug $concurrency :: `qalc  $concurrency/$bug_total`

