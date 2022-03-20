#!/bin/sh

ADDRESS=TmiHm6cT8sETMMRQdwzotQMYg7xTJZXHz9s
USERNAME=$ADDRESS.w
POOL=pmeer.666pool.cn:9866
SCHEME=qitmeer

./bminer -uri $SCHEME://$USERNAME@$POOL -api 127.0.0.1:1880
