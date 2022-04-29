# coding:UTF-8
# 统计异常告警数据以供可视化

from scapy.all import rdpcap, PacketList, corrupt_bytes
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.inet6 import IPv6, ICMPv6ND_NS
from scapy.layers.l2 import ARP
from scapy.layers.dns import DNS
import collections
import time

# TODO sort
def get_most10(warning_list: list, key: str):
    '''统计最多的10个 key 的频数'''
    warn_count = collections.Counter([i[key] for i in warning_list])
    d = dict(warn_count.most_common(10))
    return [{'name': k, 'value': v} for k, v in d.items()]



def get_all(warning_list: list):
    return {'most_warn': get_most10(warning_list,'warn'),
            'most_ip_port': get_most10(warning_list,'ip_port')}


# for test
if __name__ == '__main__':
    warning_list = [{'data': '', 'ip_port': '11', 'time': '', 'warn': 'a'},
                    {'data': '', 'ip_port': '12', 'time': '', 'warn': 'b'},
                    {'data': '', 'ip_port': '22', 'time': '', 'warn': 'a'}]
    print(get_all(warning_list))
