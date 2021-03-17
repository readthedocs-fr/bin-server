#!/bin/bash
test -z $1 && file=- || file=$1
test -z $1 && lang=txt || lang="${file#*.}"
url=$(curl -s -F file=@$file -F "lang=$lang" -w %{redirect_url} https://bin.readthedocs.fr/new)
