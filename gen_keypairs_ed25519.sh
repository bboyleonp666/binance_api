#!/usr/bin/env bash
KEYNAME=ed25519_key

openssl genpkey -algorithm ed25519 -out $KEYNAME
openssl pkey -in ed25519_key -pubout -out $KEYNAME.pub