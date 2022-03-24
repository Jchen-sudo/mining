#!/bin/sh

#Change the following address to your addresses
ADDRESS=0xb76d43eAaB2e905028a7f0F3aF13C7A84c477B9f
ADDRESS_2=hs1qw2a7qm69j8sj030sfqa97p5nxsqgdxv74da5z2

USERNAME=$ADDRESS.w
POOL=eth-us-west1.nanopool.org:9999
# Change SCHEME according to your POOL. For example:
# ethash:     Nanopool
# ethproxy:   Ethermine, Sparkpool
# ethstratum: F2pool, Miningpoolhub
SCHEME=ethstratum

USERNAME_2=$ADDRESS_2.w
POOL_2=hns.f2pool.com:6000
SCHEME_2=handshake

./bminer -uri $SCHEME://$USERNAME@$POOL -uri2 $SCHEME_2://$USERNAME_2@$POOL_2 -dual-intensity 1 -dual-subsolver 0 -api 127.0.0.1:1880
