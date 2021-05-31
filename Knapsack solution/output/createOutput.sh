#!/bin/sh
count=0
while [ $count -lt 12  ]; do
      count=$(($count+1))
      mkdir "Output 0$count"
done
counter=0
cntfolder=1
for file in $1/*; do
        if [ $counter -eq 8  ]; then 
                counter=1
                cntfolder=$(($cntfolder+1))
        else
                counter=$(($counter+1))
        fi
        mv $file "~/home/ngctnnnn/Documents/Knapsack-solution/output/Output $cntfolder/test $counter.txt"
done
exit 0

