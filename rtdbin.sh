#!/bin/bash
test -z $1 && file=- || file=$1
test -z $1 && lang=txt || lang="${file#*.}"
curl -s -F file=@$file -F "lang=$lang" -w %{redirect_url}\n https://bin.readthedocs.fr/new
