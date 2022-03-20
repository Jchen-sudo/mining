#!/bin/sh

# Change the following address to your Equihash1445 addr.
ADDRESS=t1ZBtpkUy1y1deYsNJnzdW4tk7HiJEcfUzr

USERNAME=$ADDRESS.w
POOL=btcz.2miners.com:2020
SCHEME=equihash1445

# =====================================================================
# Change pers according to the coin you want to mine. For example:
# Coin:         Pers
# BitcoinZ:     BitcoinZ
# Safe Coin:    Safecoin
# ZelCash:      ZelProof
# SnowGem:      sngemPoW
# Bitcoin Gold: BgoldPoW
# You can also use PERS=auto for certain pools, e.g. altpool, zergpool
# =====================================================================
PERS=BitcoinZ

./bminer -uri $SCHEME://$USERNAME@$POOL -api 127.0.0.1:1880 -pers $PERS
