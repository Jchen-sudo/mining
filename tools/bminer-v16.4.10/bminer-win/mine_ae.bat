@echo OFF
REM Change the following address to your BTM addr.
SET ADDRESS=ak_27we6r5KVGpErVGedqFByq2GAEYrUP39G51jnadMRrDux1YDay
SET USERNAME=%ADDRESS%.w
SET POOL=ae.f2pool.com:7898
SET SCHEME=aeternity
START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%@%POOL% -api 127.0.0.1:1880
