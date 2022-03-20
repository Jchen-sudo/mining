#!/bin/sh

# Change the following address to your Zhash addr.
ADDRESS=GNjEhF8dfiCj9JSntTnsovb2c3z2kptfwi

USERNAME=$ADDRESS.w
POOL=main.pool.gold:3050
SCHEME=zhash

./bminer -uri $SCHEME://$USERNAME@$POOL -api 127.0.0.1:1880
