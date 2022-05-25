# mining
加密货币流量处理合作仓库，目前方向关注pacp流量包向机器学习数据集的转化，相关特征提取。仓库同步处理代码和测试数据及尝试处理结果。

【腾讯文档】pcap数据包处理&特征提取
https://docs.qq.com/doc/DT3hMSmhOZ2lkanpQ
## 目录结构：

```
│  parse_pcap.py
│  README.md
│
├─data
│  ├─csv
│  │      XMR_1.8k.csv [...]
│  │
│  └─pacp
│          XMR_1.8K.pcap [...]
│
└─tools
    └─xmrig-6.16.2 [...]
```

#### 说明：
         data部分对应文件夹存储pacp数据包和转换的csv，命名格式为：[币种]_[算力]_[序号]。

上传数据包同时有必要可以上传数据包生成代码或脚本，数据包解析转换等代码，命名方式参考同上。



## Logo

![](README/vis_all.png)