#!/bin/bash

while true; do
cpu_usage=$(top -bn1 | awk '/%Cpu/ {print "Usage: "$2"%, System: "$4"%, Idle: "$8}')
echo "<p> CPU usage: $cpu_usage </p>" > /var/www/html/cpu/cpu.html
sleep 1
done
