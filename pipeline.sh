#!/bin/bash
workdir="/home/ubuntu/CompareTheBrewDev"
# begin - scrape bws website

## beer
n=0
until [ $n -ge 5 ]
do 
   #echo "$(date +"%Y-%m-%d %T")"
   #python3 ./scrape.py bws beer 0 > "$(date +"%Y-%m-%d %T")".log 2> "$(date +"%Y-%m-%d %T")".err && break
   time="$(date +"%Y-%m-%d %T")"
   log="$workdir/log/beer-$time.log"
   err="$workdir/log/beer-$time.err"
   echo "$PATH" > "$log" 2> "$err" && break
   n=$[$n+1]
   sleep 1
done
