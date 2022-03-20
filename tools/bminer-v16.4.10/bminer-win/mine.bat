@echo OFF
REM Change the following address to your ETH addr.
SET ADDRESS=0x6D2a79507C67A8ACBc01D16a4858469677792C39

SET USERNAME=%ADDRESS%.w
REM Change SCHEME according to your POOL. For example:
REM ethash:     Nanopool
REM ethproxy:   BTC.com, Ethermine, PandaMiner, Sparkpool
REM ethstratum: Antpool.com, BTC.com, F2pool, Huobipool.com, Miningpoolhub
SET POOL=eth-us-west1.nanopool.org:9999
SET SCHEME=ethash

START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%@%POOL% -api 127.0.0.1:1880
