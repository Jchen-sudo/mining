#coding:UTF-8

from flask import Flask

app = Flask(__name__)


app.config.from_object('config')

from app import views

# sniff 进程
from database.sniff_background import sniff_main
from multiprocessing import Process
class sniff_Process(Process): 
    def __init__(self):
        super(sniff_Process,self).__init__()

    def run(self):
        sniff_main()
        print('sniff_Process exit')

p = sniff_Process() #实例化进程对象
p.start()
