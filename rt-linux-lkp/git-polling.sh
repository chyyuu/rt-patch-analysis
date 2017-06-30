#!/bin/bash

url="https://github.com/chyyuu/linux-rt-devel.git"
script="./rt-linux-lkp.sh"

ret="$(git ls-remote -q -h "$url")"

declare -A branch

prefix="refs/heads/"

while read -r line; do
	sha="$(echo "$line" | cut -f1)"
	key="$(echo "$line" | cut -f2)"
	key=${key#$prefix}
	branch[$key]=$sha
done <<< "$ret"

for key in "${!branch[@]}"; do
	echo ""$key": "${branch["$key"]}""
done

while true; do
	ret="$(git ls-remote -q -h "$url")"
	while read -r line; do
		sha="$(echo "$line" | cut -f1)"
		key="$(echo "$line" | cut -f2)"
		key=${key#$prefix}
		if [[ "${branch["$key"]}" != "$sha" ]]; then
			branch[$key]=$sha
			echo  ${script}" "${url}" "${sha}
                        #bash "$script" "$url" "$sha"
			$script "$url" "$sha"
		fi
	done <<< "$ret"
	sleep 3
done
