#!/bin/sh
count=0
while [ $count -lt 12 ]; do
        count=$(($count+1))
        rm -r "Output 0$count"
done
exit 0
