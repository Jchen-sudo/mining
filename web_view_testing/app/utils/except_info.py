#coding:UTF-8


from scapy.all import *
import time
from .data_extract import web_data
from ..utils.proto_analyzer import dns_statistic


#ioc匹配ip地址
def ip_warning(PCAPS):
    with open('./app/utils/warning/ip.json', 'r', encoding='UTF-8') as f:
        warns = f.readlines()
    warn_list = list()
    for warn in warns:
        warn_list.append(warn.rstrip('\n').rstrip(' '))
    ip_warning  = list()
    srcs = list()
    dsts = list()
    for pcap in PCAPS:
        if pcap.haslayer(TCP):
            tcp = pcap.getlayer(TCP)
            src = pcap.getlayer(IP).src
            dst = pcap.getlayer(IP).dst
            sport = tcp.sport
            dport = tcp.dport
            if src not in srcs:
                if src in warn_list:
                    ip_warning.append({'ip_port': dst+':'+str(dport), 'warn': u'源ip捕获:'+src, 'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pcap.time)),'data':pcap.summary()})
                    srcs.append(src)
            if dst not in dsts:
                if dst in warn_list:
                    ip_warning.append({'ip_port': src+':'+str(sport), 'warn': u'目的ip捕获:'+dst, 'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pcap.time)),'data':pcap.summary()})
                    dsts.append(dst)
 
    return ip_warning

#dns查询匹配
def dns_warning(PCAPS): 
    with open('./app/utils/warning/domain.json', 'r', encoding='UTF-8') as f:
        warns = f.readlines()
    warn_list = list()
    for warn in warns:
        warn_list.append(warn)
    dns_warning = list()
    dns_dict = dns_statistic(PCAPS)
    for key,value in dns_dict.items():
        if value in warn_list:
            dns_warning.append({'ip_port':key.decode('utf-8'),'warn':'DNS匹配域名'+value,'time':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time)),'data':value})
    return dns_warning
        
            


#特殊字段匹配
def stratum_warning(PCAPS, host_ip):
    with open('./app/utils/warning/HTTP_ATTACK', 'r', encoding='UTF-8') as f:
        attacks = f.readlines()
    ATTACK_DICT = dict()
    for attack in attacks:
        attack = attack.strip()
        ATTACK_DICT[attack.split(' : ')[0]] = attack.split(' : ')[1]
    webdata = web_data(PCAPS, host_ip)
    webwarn_list = list()

    for web in webdata:
        data = web['data']
        for pattn, attk in ATTACK_DICT.items(): #特征码和攻击名称
            if pattn.upper() in data.upper():
                webwarn_list.append({'ip_port': web['ip_port'].split(':')[0]+':'+web['ip_port'].split(':')[1], 'warn':attk, 'time':pattn, 'data':data})
   
    return webwarn_list



def exception_warning(PCAPS, host_ip):
    warn_list = list()
    ip_list = ip_warning(PCAPS)
    stratum_list = stratum_warning(PCAPS, host_ip)
    dns_list = dns_warning(PCAPS)
    if ip_list:
        warn_list.extend(ip_list)
    if stratum_list:
        warn_list.extend(stratum_list)
    if dns_list:
        warn_list.append(dns_list)
    return warn_list