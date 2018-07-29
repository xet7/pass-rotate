#!/usr/bin/env bash

# Find previous account password

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

# ACCOUNT="foo account"
# Generate password

PASSWORD="$(openssl rand 30 -base64)"

# PASSWORD ="Password with a space"

# Build the object

#USERNAME_OBJECT=$(jo value=$ACCOUNT type=T name=username designation=username)
#PASSWORD_OBJECT=$(jo value=$PASSWORD type=P name=password designation=password)

# OBJECT=$(jo -p -- -s notesPlain="${ACCOUNT}" sections=[] fields=$(jo -a ${USERNAME_OBJECT} ${PASSWORD_OBJECT}))

ENCODED=$(cat <<EOF | op encode
{
    "notesPlain": "${ACCOUNT}",
    "sections": [],
    "title": "${ACCOUNT}",
    "overview": {
        "title": "${ACCOUNT}"
    },
    "fields": [
        {
            "value": "${ACCOUNT}",
            "type": "T",
            "name": "username",
            "designation": "username"
        },
        {
            "value": "${PASSWORD}",
            "type": "P",
            "name": "password",
            "designation": "password"
        }
    ]
}
EOF
)

#
#
## Create item in OP
#
op create item Login "$ENCODED" --title "${ACCOUNT}" --vault=testpass 1>&2

# Delete previous entry

if [ ! -z "${MATCH}" ]; then
    op delete item --vault=testpass "$MATCH" | jq 1>&2
fi

echo -ne "$PASSWORD"
exit 0