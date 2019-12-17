#!/bin/bash
imagedir="/home/ubuntu/CompareTheBrewDev/static/images"
for file in $imagedir/uncompressed/*; do
        echo "$file"
	cwebp -q 80 "$file" -o "$file.webp"
	mv "$file.webp" "$imagedir/drinkimages/"
done

#rm -rf $imagedir/uncompressed/*
