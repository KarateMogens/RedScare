#!/bin/bash

cwd=$(pwd)
output="$cwd/results.txt"
threshold=0 # Set lower bound; graphs with fewer vertices will be ignored.
cd ./data
> $output
for f in *.txt; do
  read -r -a firstline < "$f"
  if [ "${firstline[0]}" -ge "$threshold" ]; then
    echo "Working on $f...";
    printf "${f%.*}\t" >> $output;
    cat "$f" | python3 "../redscare.py" >> $output;
  fi
done
