#!/bin/bash

# 如果没有输入参数，则提示输入参数
if [ $# -eq 0 ]; then
    echo "请输入参数："
    echo "版本号x: 0.0.x"
    exit 1
fi

# 创建镜像
./clear.sh  || { echo "command failed"; exit 1; }
echo "创建镜像...版本：0.0.$1"
sudo docker build -t "framist/miningovern:0.0.$1" . ;  || { echo "command failed"; exit 1; }
sudo docker tag framist/miningovern:0.0.$1 framist/miningovern;  || { echo "command failed"; exit 1; }
# 发布镜像
sudo docker push framist/miningovern:0.0.$1;  || { echo "command failed"; exit 1; }
# 起 docker (临时)
# sudo docker run --name miningovern -it --rm -p 8081:8081 framist/miningovern:latest