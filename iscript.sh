#!/bin/bash
workdir="/home/ubuntu/CompareTheBrewDev"
GREEN='\033[0;32m'
NC='\033[0m' # No Color

#time="$(date +"%Y-%m-%d")"
#echo "${GREEN}IMAGES${NC}"
#sudo python3 imagedl.py #> "$workdir/log/image-$time.log"

# convert to webp format
echo "${GREEN}PNG CONVERT${NC}"
imagedir="/home/ubuntu/CompareTheBrewDev/static/images"
cd $imagedir/uncompressed
sudo mogrify -format png *.webp
for file in $imagedir/uncompressed/*.png; do
        echo "$file"
	mv "$file" "$imagedir/drinkimages/"
done

## delete extra images that have otherwise been compressed
#rm -rf $imagedir/uncompressed/*

