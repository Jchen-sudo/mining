import time
import os
import psutil
from functools import wraps

def count_time(func):
    @wraps(func)
    def int_time(*args, **kwargs):
        start_time = time.time()
        ans = func(*args, **kwargs)
        over_time = time.time()
        total_time = over_time - start_time
        # print("程序运行了 %.9f 秒" % total_time)
        return ans,total_time
    return int_time

def count_mem(func):
    @wraps(func)
    def float_info(*args, **kwargs):
        pid = os.getpid()
        p = psutil.Process(pid)
        info_start = p.memory_full_info().rss/1024 # Resident Set Size 实际使用物理内存（包含共享库占用的内存）
        ans = func(*args, **kwargs)
        info_end=p.memory_full_info().rss/1024
        mem = info_end-info_start
        print("程序占用了内存 %f KB" % mem)
        return ans, mem
    return float_info

def count_cpu_time(func):
    @wraps(func)
    def float_info(*args, **kwargs):
        pid = os.getpid()
        p = psutil.Process(pid)
        info_start = p.cpu_times().user + p.cpu_times().system
        ans = func(*args, **kwargs)
        info_end=p.cpu_times().user + p.cpu_times().system
        t = info_end-info_start
        t = round(t,2)
        print("程序占用了 cpu time %f s" % t)
        return ans,t
    return float_info

