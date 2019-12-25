#!/bin/bash
time="$(date +"%d-%m-%Y")"
sudo /home/ubuntu/CompareTheBrewDev/pipeline.sh 2>&1 | tee /home/ubuntu/CompareTheBrewDev/log/$time.log
