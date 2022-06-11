# XMR 挖矿程序 - docker

xmrig 容器根据 Dockerfile 创建

先起 miningovern：

```
sudo docker run --name miningovern -it --rm -p 8081:8081 framist/miningovern:0.0.3
```

 再：

```
sudo docker run -it --rm --network container:miningovern xmrig
```



## 加密通讯

```
./xmrig
```



## 无加密通讯

```
./xmrig -o xmr.crypto-pool.fr:3333 -u 45UNGwUMKR7AKWQK8xNWMu6sjKP4AgAhAHatGY9RgDsY3D9uHAoKpamXF3zSp8pQW9jKFS27pvfQoH5xyUb8oPMq8aS4UZf
```

