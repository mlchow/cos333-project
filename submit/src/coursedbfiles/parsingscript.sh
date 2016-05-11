#!/usr/bin/env bash

template=',c,TES,breadth'
while read line
do
	IFS='–' read -ra CLASS <<< "$line"
	if [[ "$CLASS" =~ .*/.* ]]; then 
		IFS='/' read -ra CROSS <<< "$CLASS"
		for i in "${CROSS[@]}"; do
			data=$i$template
			echo "$data"
		done
	else
		data=$CLASS$template
		echo "$data"
	fi
done < "file.txt" > "temp.txt"

cat temp.txt | sed 's/ //g' > temp2.txt

rm temp.txt