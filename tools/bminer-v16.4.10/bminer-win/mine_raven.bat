@echo OFF
REM Change the following address to your address
SET ADDRESS=RBEe49BYHAhik9mRoQZcPimtb4yoPS2LB8

SET USERNAME=$ADDRESS.w
SET POOL=rvnt.minermore.com:4505
SET SCHEME=raven

SET PWD=foo

START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%:%PWD%@%POOL% -api 127.0.0.1:1880
