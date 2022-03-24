#!/bin/sh

# Change the following address to your address
ADDRESS=21oMAVzu7cFJriWXiUogLWDEbUYwgKhpCW4wyH56wTAuyJ256QKjnfLQL7qBVc2r39ke27RwhLvHGH4yNUtorWNwnavAdC5Aus2pSFdZzYodtDfMbXnLp7xaXDnzp4BZcoSH

USERNAME=$ADDRESS.w
POOL=sero.f2pool.com:4200
SCHEME=sero

./bminer -uri $SCHEME://$USERNAME@$POOL -api 127.0.0.1:1880