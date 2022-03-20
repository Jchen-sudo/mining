#!/bin/sh

# Change the following address to your ETH addr.
ADDRESS=0x6D2a79507C67A8ACBc01D16a4858469677792C39

USERNAME=$ADDRESS.w
POOL=eth-us-west1.nanopool.org:9999
# Change SCHEME according to your POOL. For example:
# ethash:     Nanopool
# ethproxy:   BTC.com, Ethermine, PandaMiner, Sparkpool
# ethstratum: Antpool.com, BTC.com, F2pool, Huobipool.com, Miningpoolhub
SCHEME=ethash

./bminer -uri $SCHEME://$USERNAME@$POOL -api 127.0.0.1:1880
