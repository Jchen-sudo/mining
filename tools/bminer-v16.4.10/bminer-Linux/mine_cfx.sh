#!/bin/sh

ADDRESS=bminergrin
USERNAME=$ADDRESS.w
POOL=cfx.f2pool.com:6800
SCHEME=conflux

./bminer -uri $SCHEME://$USERNAME@$POOL -api 127.0.0.1:1880
