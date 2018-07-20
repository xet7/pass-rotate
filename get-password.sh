#!/usr/bin/env bash

# ACCOUNT="foo account"

uuidList="$(op list items --vault=testpass | jq -r '.[].uuid')"

MATCH=

for uuid in ${uuidList}; do
    title="$(op get item --vault=testpass "$uuid" | jq -r '.details.title')"

    if [ "${ACCOUNT}" == "${title}" ]; then
        echo Match found 1>&2
        MATCH=$uuid
        break
    fi
done

if [ -z "${MATCH}" ]; then
    echo No match found 1>&2
    exit 1
fi

op get item --vault=testpass "$MATCH" | jq 1>&2
op get item --vault=testpass "$MATCH" | jq -r '.details.fields[] | select(.type=="P") | .value'