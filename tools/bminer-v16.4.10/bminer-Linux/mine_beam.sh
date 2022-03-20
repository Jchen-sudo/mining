#!/bin/sh

# Change the following address to your BEAMaddr.
ADDRESS=3a13205ec464807c9400f0fde8d56ac49da03bb3812055f08844fe2eaf0b9166

USERNAME=$ADDRESS.w
POOL=beam.sparkpool.com:2222
SCHEME=beamhash3+ssl

./bminer -uri $SCHEME://$USERNAME@$POOL -api 127.0.0.1:1880
