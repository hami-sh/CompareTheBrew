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
   cmd="python3 ./scrape.py bws beer 0"
   echo "$cmd" > "$log" 2> "$err" && break
   n=$[$n+1]
   sleep 1
done

## wine
n=0
until [ $n -ge 5 ]
do
   #echo "$(date +"%Y-%m-%d %T")"
   #python3 ./scrape.py bws beer 0 > "$(date +"%Y-%m-%d %T")".log 2> "$(date +"%Y-%m-%d %T")".err && break
   time="$(date +"%Y-%m-%d %T")"
   log="$workdir/log/wine-$time.log"
   err="$workdir/log/wine-$time.err"
   cmd="python3 ./scrape.py bws wine 0"
   echo "$cmd" > "$log" 2> "$err" && break
   n=$[$n+1]
   sleep 1
done

## spirits
n=0
until [ $n -ge 5 ]
do
   #echo "$(date +"%Y-%m-%d %T")"
   #python3 ./scrape.py bws beer 0 > "$(date +"%Y-%m-%d %T")".log 2> "$(date +"%Y-%m-%d %T")".err && break
   time="$(date +"%Y-%m-%d %T")"
   log="$workdir/log/spirits-$time.log"
   err="$workdir/log/spirits-$time.err"
   cmd="python3 ./scrape.py bws spirits 0"
   echo "$cmd" > "$log" 2> "$err" && break
   n=$[$n+1]
   sleep 1
done

# scrape other websites

# ...
# ...
# ...

# download images
time="$(date +"%Y-%m-%d %T")"
python3 imagedl.py > "$workdir/log/image-$time.log"
