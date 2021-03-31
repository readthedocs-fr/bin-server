#!/bin/bash
test -z $1 && file=- || file=$1
test -z $1 && lang=txt || lang="${file#*.}"
curl_version=$(curl -V | head -n1 | cut -d ' ' -f2)
curl -s -F file=@$file -F "lang=$lang" -w "%{redirect_url}\n" -A "curl/$curl_version (+https://github.com/readthedocs-fr/bin-server)" https://bin.readthedocs.fr/new
