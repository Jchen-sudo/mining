#! /bin/bash
# 挖矿流量捕获脚本,待更新。。。。

if ! [ -x "$(command -v tcpdump)" ]; then 
    echo '未检测到tcpdump安装，正在安装。请确保root权限';
    sudo apt-get install tcpdump;
fi

if ! [-d /xmrig]; then
    pass; #建一个ftp方便在服务器部一键署;
fi

d=$(date "+%Y-%m-%d")
chmod 777 /xmrig/xmrig;

nohup ./xmrig > xmr.log 2>&1 &;

tcpdump tcp -t -s 0 -c 10 and dst port 9000 or src port 9000  -w ./$d.cap;   #抓取对应矿池端口的流量
