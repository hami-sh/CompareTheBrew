#!/bin/bash
workdir="/home/ubuntu/CompareTheBrewDev"

# begin - scrape bws website
## beer
n=0
until [ $n -ge 5 ]
do 
   #echo "$(date +"%Y-%m-%d %T")"
   #python3 ./scrape.py bws beer 0 > "$(date +"%Y-%m-%d %T")".log 2> "$(date +"%Y-%m-%d %T")".err && break
   time="$(date +"%Y-%m-%d")"
   log="$workdir/log/beer-$time.log"
   err="$workdir/log/beer-$time.err"
   cmd="python3 ./scrape.py bws beer 0"
   echo "$(cmd)" > "$log" 2> "$err" && break
   n=$[$n+1]
   sleep 5
done

## wine
n=0
until [ $n -ge 5 ]
do
   #echo "$(date +"%Y-%m-%d %T")"
   #python3 ./scrape.py bws beer 0 > "$(date +"%Y-%m-%d %T")".log 2> "$(date +"%Y-%m-%d %T")".err && break
   time="$(date +"%Y-%m-%d")"
   log="$workdir/log/wine-$time.log"
   err="$workdir/log/wine-$time.err"
   cmd="python3 ./scrape.py bws wine 0"
   echo "$(cmd)" > "$log" 2> "$err" && break
   n=$[$n+1]
   sleep 5
done

## spirits
n=0
until [ $n -ge 5 ]
do
   #echo "$(date +"%Y-%m-%d %T")"
   #python3 ./scrape.py bws beer 0 > "$(date +"%Y-%m-%d %T")".log 2> "$(date +"%Y-%m-%d %T")".err && break
   time="$(date +"%Y-%m-%d")"
   log="$workdir/log/spirits-$time.log"
   err="$workdir/log/spirits-$time.err"
   cmd="python3 ./scrape.py bws spirits 0"
   echo "$(cmd)" > "$log" 2> "$err" && break
   n=$[$n+1]
   sleep 5
done

# scrape other websites

# ...
# ...
# ...

# download images
time="$(date +"%Y-%m-%d")"
python3 imagedl.py > "$workdir/log/image-$time.log"

# convert to webp format
imagedir="/home/ubuntu/CompareTheBrewDev/static/images"
for file in $imagedir/uncompressed/*; do
        echo "$file"
        cwebp -q 80 "$file" -o "$file.webp"
        mv "$file.webp" "$imagedir/drinkimages/"
done

## delete extra images that have otherwise been compressed
rm -rf $imagedir/uncompressed/*

