#!/bin/bash
test -z $1 && file=- || file=$1
test -z $1 && lang=txt || lang="${file#*.}"
url=$(curl -s -F file=@$file -F "lang=$lang" -w %{redirect_url} https://bin.readthedocs.fr/new)
echo -n $url | xsel -p
curl -s $(echo $url | sed -E 's/^(.*)\/([a-z\.]*)$/\1\/raw\/\2/') | batcat -n -l $lang
