#!/bin/bash
imagedir="/home/ubuntu/CompareTheBrewDev/static/images"
cd $imagedir/uncompressed
mogrify -format png *.webp
#rm -rf $imagedir/uncompressed/*
