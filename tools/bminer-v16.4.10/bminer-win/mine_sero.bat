@echo OFF
REM Change the following address to your address

SET ADDRESS=21oMAVzu7cFJriWXiUogLWDEbUYwgKhpCW4wyH56wTAuyJ256QKjnfLQL7qBVc2r39ke27RwhLvHGH4yNUtorWNwnavAdC5Aus2pSFdZzYodtDfMbXnLp7xaXDnzp4BZcoSH
SET USERNAME=%ADDRESS%.worker
SET POOL=sero.f2pool.com:4200
SET SCHEME=sero
SET PWD=foo

START "Bminer: When Crypto-mining Made Fast" bminer.exe -uri %SCHEME%://%USERNAME%:%PWD%@%POOL% -api 127.0.0.1:1880
