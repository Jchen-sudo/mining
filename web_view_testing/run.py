#coding:UTF-8

from app import app
# sniff 进程
from database.sniff_background import sniff_main
from multiprocessing import Process
class sniff_Process(Process): 
    def __init__(self):
        super(sniff_Process,self).__init__()

    def run(self):
        sniff_main()
        print('sniff_Process exit')

if __name__ == '__main__':
    p = sniff_Process() #实例化进程对象
    p.start()
    app.run(host='0.0.0.0', port=8081)
