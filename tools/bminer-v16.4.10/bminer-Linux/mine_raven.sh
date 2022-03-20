#!/bin/sh

# Change the following address to your address
ADDRESS=RBEe49BYHAhik9mRoQZcPimtb4yoPS2LB8

USERNAME=$ADDRESS.w
POOL=rvnt.minermore.com:4505
SCHEME=raven

./bminer -uri $SCHEME://$USERNAME@$POOL -api 127.0.0.1:1880
