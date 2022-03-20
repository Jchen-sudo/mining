@echo OFF
SET ADDRESS=bminergrin

SET USERNAME=%ADDRESS%.w
SET POOL=cfx.f2pool.com:6800
SET SCHEME=conflux

START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%@%POOL% -api 127.0.0.1:1880
