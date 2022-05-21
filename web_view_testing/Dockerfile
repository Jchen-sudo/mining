FROM python:3.8
WORKDIR /Project/demo

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# https://stackoverflow.com/questions/65410481/filenotfounderror-errno-2-no-such-file-or-directory-bliblibc-a
RUN ln -s -f /usr/lib/x86_64-linux-gnu/libc.a /usr/lib/x86_64-linux-gnu/liblibc.a
COPY . .

CMD ["python", "run.py"]
# for build image
# sudo docker build -t 'testflask' . 
# for 测试
# sudo docker run -it --rm -p 8081:8081 testflask
# sudo docker tag testflask framist/miningovern:0.0.1 
# sudo docker push framist/miningovern:0.0.1