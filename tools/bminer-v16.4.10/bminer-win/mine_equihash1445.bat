@echo OFF

REM Change the following address to your Equihash1445 addr.
SET ADDRESS=t1ZBtpkUy1y1deYsNJnzdW4tk7HiJEcfUzr

SET USERNAME=%ADDRESS%.w
SET POOL=btcz.2miners.com:2020
SET SCHEME=equihash1445

REM =====================================================================
REM Change pers according to the coin you want to mine. For example:
REM Coin:         Pers
REM BitcoinZ:     BitcoinZ
REM Safe Coin:    Safecoin
REM ZelCash:      ZelProof
REM SnowGem:      sngemPoW
REM Bitcoin Gold: BgoldPoW
REM You can also SET PERS=auto for certain pools, e.g. altpool, zergpool
REM =====================================================================
SET PERS=BitcoinZ

START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%@%POOL% -api 127.0.0.1:1880 -pers %PERS%
