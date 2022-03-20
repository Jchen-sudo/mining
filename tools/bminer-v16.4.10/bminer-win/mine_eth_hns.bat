@echo OFF
REM Change the following address to your addresses
SET ADDRESS=0xb76d43eAaB2e905028a7f0F3aF13C7A84c477B9f
SET ADDRESS_2=hs1qw2a7qm69j8sj030sfqa97p5nxsqgdxv74da5z2

SET USERNAME=%ADDRESS%.w
REM Change SCHEME according to your POOL. For example:
REM ethash:     Nanopool
REM ethproxy:   Ethermine, Sparkpool
REM ethstratum: F2pool, Miningpoolhub
SET POOL=eth-us-west1.nanopool.org:9999
SET SCHEME=ethstratum

SET USERNAME_2=%ADDRESS_2%.w
SET POOL_2=hns.f2pool.com:6000
SET SCHEME_2=handshake

START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%@%POOL% -uri2 %SCHEME_2%://%USERNAME_2%@%POOL_2% -dual-intensity 1 -dual-subsolver 0 -api 127.0.0.1:1880
