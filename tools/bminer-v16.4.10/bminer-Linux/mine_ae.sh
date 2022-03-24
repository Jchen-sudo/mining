#!/bin/sh

# Change the following address to your BTM addr.
ADDRESS=ak_27we6r5KVGpErVGedqFByq2GAEYrUP39G51jnadMRrDux1YDay

USERNAME=$ADDRESS.w
POOL=ae.f2pool.com:7898
SCHEME=aeternity

./bminer -uri $SCHEME://$USERNAME@$POOL -api 127.0.0.1:1880
