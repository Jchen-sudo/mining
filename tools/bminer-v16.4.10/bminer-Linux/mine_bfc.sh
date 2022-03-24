#!/bin/sh

ADDRESS=bminer
USERNAME=$ADDRESS.w
POOL=ss.bfcpool.com:3333
SCHEME=bfc

./bminer -uri $SCHEME://$USERNAME@$POOL -api 127.0.0.1:1880
