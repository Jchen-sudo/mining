# coding:UTF-8
# 统计异常告警数据以供可视化

import collections
import time
from datetime import datetime

def get_most10(warning_list: list, key: str):
    '''统计最多的10个 key 的频数'''
    warn_count = collections.Counter([i[key] for i in warning_list])
    d = dict(warn_count.most_common(10))
    return [{'name': k, 'value': v} for k, v in d.items()]



def get_all(warning_list: list):
    return {'most_warn': get_most10(warning_list,'warn'),
            'most_ip_port': get_most10(warning_list,'ip_port'),
            'time_flow': get_time_flow(warning_list)}

def get_time_flow(warning_list: list):
    '''统计随时间变化的告警数量'''
    # 适应未修改的bug
    # time_stamps = [datetime.strptime(i['time'], '%Y-%m-%d %H:%M:%S') for i in warning_list]
    time_stamps = []
    for i in warning_list:
        try:
            time_stamps.append(datetime.strptime(i['time'], '%Y-%m-%d %H:%M:%S'))
        except:
            pass
    time_stamps.sort()
    # 分成10个时间段，统计每个时间段的告警数量
    start_time = time_stamps[0]
    d_time = (time_stamps[-1] - start_time)/10
    count = {}
    end_time = start_time
    for i in range(10):
        end_time += d_time
        s = 0
        while time_stamps and time_stamps[0] <= end_time:
            time_stamps.pop(0)
            s += 1
        count[str(end_time)] = s
    return [{'name': k, 'value': v} for k, v in count.items()]
    


# for test
if __name__ == '__main__':
    warning_list = [{'data': '', 'ip_port': '11', 'time': '2022-02-08 09:47:04', 'warn': 'a'},
                    {'data': '', 'ip_port': '12', 'time': '2022-02-08 09:46:04', 'warn': 'b'},
                    {'data': '', 'ip_port': '12', 'time': '2022-02-08 09:46:44', 'warn': 'b'},
                    {'data': '', 'ip_port': '12', 'time': '2022-02-08 09:46:24', 'warn': 'b'},
                    {'data': '', 'ip_port': '12', 'time': '2022-02-08 09:46:34', 'warn': 'b'},
                    {'data': '', 'ip_port': '22', 'time': '2022-02-08 09:49:04', 'warn': 'a'}]
    print(get_all(warning_list))
    # print(get_time_flow(warning_list))
