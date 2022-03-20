@echo OFF
REM Change the following address to your BTM addr.
SET ADDRESS=bminer
SET USERNAME=%ADDRESS%.w
SET POOL=ss.bfcpool.com:3333
SET SCHEME=bfc
START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%@%POOL% -api 127.0.0.1:1880
