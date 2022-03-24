@echo OFF
REM Change the following address to your BEAM addr.
SET ADDRESS=3a13205ec464807c9400f0fde8d56ac49da03bb3812055f08844fe2eaf0b9166
SET USERNAME=%ADDRESS%.w
SET POOL=beam.sparkpool.com:2222
SET SCHEME=beamhash3+ssl
START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%@%POOL% -api 127.0.0.1:1880
