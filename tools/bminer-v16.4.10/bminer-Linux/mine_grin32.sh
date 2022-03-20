#!/bin/sh

# Change the following address to your GRIN addr.
ADDRESS=bminergrin
USERNAME=$ADDRESS.worker
POOL=grin29.f2pool.com:13654
SCHEME=cuckatoo32
PWD=foo

./bminer -uri $SCHEME://$USERNAME:$PWD@$POOL -api 127.0.0.1:1880
