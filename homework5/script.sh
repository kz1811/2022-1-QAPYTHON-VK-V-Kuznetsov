#!/bin/bash

# Общее количество запросов

echo 'Number of requests:';
echo;
cat access.log | wc -l;
echo;

# Количество запросов по типу

echo 'Number of requests by type:';
echo;
cat access.log | cut -d '"' -f2 | cut -d ' ' -f1 | sort | uniq -c | sort -n
echo;

#Топ 10 наиболее частых запросов

echo 'Top 10 often requests:';
echo;
cat access.log | cut -d '"' -f2 | sort | uniq -c | sort -r | head -10
echo;

#Топ 5 наиболее длинных запросов с кодом ответа 4ХХ

echo 'Top 5 most longest requests with response code 4XX:'
echo;
awk '($9 ~/4[0-9][0-9]/)' access.log | cut -d '"' -f2 | cut -d ' ' -f2 | awk "{print length, \$0}" | sort -n | awk "{\$1=\"\"; print substr(\$0,2,length-1)}" | tail -n5
echo;

#Топ 5 пользователей по количеству запросов, завершившихся ошибкой 5ХХ

echo '5 users with the biggest num of requests with response code 5XX:';
echo;
awk '($9 ~/5[0-9][0-9]/)' access.log | awk '{print $1}' | uniq -c | sort -r | head -5
