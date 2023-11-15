#!/bin/bash

nginx_log="/var/log/nginx/access.log"
file_log="/var/www/html/logs/osnovnoi.log"
log_clear="/var/www/html/logs/clear.log"
err5xx="/var/www/html/logs/err500.log"
err4xx="/var/www/html/logs/err400.log"


while true; do
    dif=$(diff "$nginx_log" "$file_log")

    if [ -n "$dif" ]; then
        while read line; do
        errcode=$(echo "$line" | awk '{print $7}')
        echo "$line" >> "$file_log"
        if [[ "$errcode" == 4* ]]; then
            echo "$line" >> "$err4xx"
        elif [[ "$errcode" == 5* ]]; then
            echo "$line" >> "$err5xx"
        fi
    done < <(tail -n +"$(($(wc -l < /var/www/html/logs/osnovnoi.log) + 1))" "$nginx_log")

    fi

    if [ $(stat -c %s "$file_log") -gt 100000 ]; then
        echo "$(date): Cleared logs. Cleared $(wc -l < /var/www/html/logs/osnovnoi.log) strings." >> "$log_clear"
        > "$file_log"

    fi

    sleep 5
done
