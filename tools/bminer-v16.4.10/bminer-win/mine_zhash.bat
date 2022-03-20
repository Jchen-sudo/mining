@echo OFF
REM Change the following address to your Zhash addr.
SET ADDRESS=GNjEhF8dfiCj9JSntTnsovb2c3z2kptfwi
SET USERNAME=%ADDRESS%.w
SET POOL=main.pool.gold:3050
SET SCHEME=zhash
START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%@%POOL% -api 127.0.0.1:1880
