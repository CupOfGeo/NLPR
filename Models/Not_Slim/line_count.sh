#!/bin/bash
count=$(0)
for i in $(ls lyrics/)
do
NUMLINES=$(cat lyrics/$i | wc -l)
	if [ $NUMLINES -lt 40 ]
	then
	count=$[count+1]
	echo $i
	fi
done 
echo $count
