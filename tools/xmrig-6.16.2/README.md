##XMR挖矿程序【linux版本】

```
chmod +x xmrig 
./xmrig 
vim config.json 
```
自行更改config.json中的字段，在'pools'里更改自己的钱包地址和矿池地址【可选】，不同矿池地址的不同端口所采用的速率、是否加密等规则不同，可以收集些常见矿池贴在下面。
另附命令行参数快速启动：
```
./xmrig --url=矿池地址:端口  --user=钱包地址 -t 线程数

./xmrig --url=47.234.188.221:5555 --user=45UNGwUMKR7AKWQK8xNWMu6sjKP4AgAhAHatGY9RgDsY3D9uHAoKpamXF3zSp8pQW9jKFS27pvfQoH5xyUb8oPMq8aS4UZf

```