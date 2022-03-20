@echo OFF
REM Change the following address to your GRIN addr.
SET ADDRESS=bminergrin
SET USERNAME=%ADDRESS%.worker
SET POOL=grin31.f2pool.com:13654
SET SCHEME=cuckatoo31
SET PWD=foo

REM If you're passing in emails, the '@' characters need to be escaped (%%40)
REM If the pool use / to annoate rigs, the '/' charaactrs need to be escape (%%2F)
SET EMAIL=mine%%40bminer.me
START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%:%PWD%@%POOL% -api 127.0.0.1:1880
