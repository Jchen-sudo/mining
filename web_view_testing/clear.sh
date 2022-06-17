#!/bin/bash
# 清除文件夹下的临时文件
echo "清除./database/pcaps/*.pcap..."
rm -rf ./database/pcaps/*.pcap && echo "清除完成"