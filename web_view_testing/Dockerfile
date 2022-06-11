FROM python:3.8
WORKDIR /Project/demo
COPY requirements.txt ./
RUN apt-get update && apt-get install tcpdump -y
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN ln -s -f /usr/lib/x86_64-linux-gnu/libc.a /usr/lib/x86_64-linux-gnu/liblibc.a
COPY . .
CMD ["python", "run.py"]

# 注：
# 第6行(RUN ln ...)的问题参见：https://stackoverflow.com/questions/65410481/filenotfounderror-errno-2-no-such-file-or-directory-bliblibc-a
# 创建镜像
# sudo docker build -t 'framist/miningovern:0.0.3' . 
# 发布镜像
# sudo docker push framist/miningovern:0.0.3
# 起 docker (临时)
# sudo docker run --name miningovern -it --rm -p 8081:8081 framist/miningovern:0.0.3
