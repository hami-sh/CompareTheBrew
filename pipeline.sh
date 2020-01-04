#!/bin/bash
workdir="/home/ubuntu/CompareTheBrewDev"
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# begin - scrape bws website
## beer
n=0
until [ $n -ge 5 ]
do 
   echo "${GREEN}BEER <$(date +"%T")>${NC}"
   #python3 ./scrape.py bws beer 0 > "$(date +"%Y-%m-%d %T")".log 2> "$(date +"%Y-%m-%d %T")".err && break
   time="$(date +"%d-%m-%Y")"
   echo "start"
   log="$workdir/log/beer-$time.log"
   err="$workdir/log/beer-$time.err"
   sudo python3 $workdir/scrape.py bws beer 0 && break
   n=$[$n+1]
   sleep 5
done

## wine
n=0
until [ $n -ge 5 ]
do  
   echo "${GREEN}WINE <$(date +"%T")>${NC}"
   #python3 ./scrape.py bws beer 0 > "$(date +"%Y-%m-%d %T")".log 2> "$(date +"%Y-%m-%d %T")".err && break   
   time="$(date +"%d-%m-%Y")"
   log="$workdir/log/wine-$time.log"
   err="$workdir/log/wine-$time.err"
   sudo python3 $workdir/scrape.py bws wine 0 && break
   n=$[$n+1]
   sleep 5
done

## spirits
n=0
until [ $n -ge 5 ]
do  
   echo "${GREEN}SPIRITS <$(date +"%T")>${NC}"
   #echo "$(date +"%Y-%m-%d %T")"
   #python3 ./scrape.py bws beer 0 > "$(date +"%Y-%m-%d %T")".log 2> "$(date +"%Y-%m-%d %T")".err && break
   time="$(date +"%Y-%m-%d")"
   log="$workdir/log/spirits-$time.log"
   err="$workdir/log/spirits-$time.err" 
   sudo python3 $workdir/scrape.py bws spirits 0 && break
   n=$[$n+1]
   sleep 5
done

# scrape other websites

# ...
# ...
# ...

# download images
time="$(date +"%Y-%m-%d")"
echo "${GREEN}IMAGES${NC}"
sudo python3 imagedl.py #> "$workdir/log/image-$time.log"

# convert to webp format
echo "${GREEN}PNG CONVERT${NC}"
imagedir="/home/ubuntu/CompareTheBrewDev/static/images"
cd $imagedir/uncompressed
sudo mogrify -format png *.webp
for file in $imagedir/uncompressed/*; do
        echo "$file"
	mv "$file.png" "$imagedir/drinkimages/"
done

## delete extra images that have otherwise been compressed
#rm -rf $imagedir/uncompressed/*

