from distutils.log import info
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
import time
from .data_extract import web_data
from ..utils.proto_analyzer import dns_statistic
from nfstream import NFStreamer
import joblib
import re

Wallet_Addr_List = [] # 存放钱包地址的全局变量
IP_Set = set() # 存放异常IP的全局变量

# ioc匹配ip地址
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
                    IP_Set.add(dst)
                    IP_Set.add(src)
            if dst not in dsts:
                if dst in warn_list:
                    ip_warning.append({'ip_port': src+':'+str(sport), 'warn': u'目的ip捕获:'+dst, 'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pcap.time)),'data':pcap.summary()})
                    dsts.append(dst)
                    IP_Set.add(dst)
                    IP_Set.add(src)
 
    return ip_warning

# dns查询匹配
def dns_warning(PCAPS:PacketList): 
    with open('./app/utils/warning/domain.json', 'r', encoding='UTF-8') as f:
        warns = f.readlines()
    warn_list = list()
    for warn in warns:
        warn_list.append(warn)
    dns_warning = list()
    dns_dict = dns_statistic(PCAPS)
    for key,value in dns_dict.items():
        if value in warn_list:
            dns_warning.append({'ip_port':key.decode('utf-8'),
                                'warn':'DNS匹配域名'+value,
                                'time':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time)), # bug un fix!
                                'data':value})
    return dns_warning
        
            


# 报文字段匹配
def stratum_warning(PCAPS:PacketList, host_ip):
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
        for pattn, attk in ATTACK_DICT.items(): 
            if pattn.upper() in data.upper():
                webwarn_list.append({'ip_port': web['ip_port'].split(':')[0]+':'+web['ip_port'].split(':')[1], 
                                     'warn':attk, 
                                     'time':pattn, 
                                     'data':data})
                IP_Set.add(web['ip_port'].split(':')[0])
    return webwarn_list

# 匹配 login 时的 钱包地址
def login_addr_warning(PCAPS:PacketList, host_ip):
    webdata = web_data(PCAPS, host_ip)
    webwarn_list = list()
    global Wallet_Addr_List
    for web in webdata:
        data : str = web['data'] 
        m = re.search('(?<="login":")([A-z0-9]+?)(?=")',data)
        if m:
            webwarn_list.append({'ip_port': web['ip_port'].split(':')[0]+':'+web['ip_port'].split(':')[1], 
                                    'warn':'挖矿地址探查', 
                                    'time': m.group(),
                                    'data': data
                                })
            Wallet_Addr_List.append({'data_IP': web['ip_port'].split(':')[0]+':'+web['ip_port'].split(':')[1], 
                                    'data_wallet': m.group()
                                })
            IP_Set.add(web['ip_port'].split(':')[0])
    return webwarn_list    

def exception_warning(PCAPS:PacketList, host_ip):
    warn_list = list()
    ip_list = ip_warning(PCAPS)
    stratum_list = stratum_warning(PCAPS, host_ip)
    dns_list = dns_warning(PCAPS)
    login_addr_list = login_addr_warning(PCAPS, host_ip)
    if ip_list:
        warn_list.extend(ip_list)
    if stratum_list:
        warn_list.extend(stratum_list)
    if dns_list:
        warn_list.append(dns_list)
    if login_addr_list:
        warn_list.extend(login_addr_list)
    return warn_list

# 机器学习模型匹配
MLMODEL_RL = joblib.load('RF.joblib')
FEATURE_COLUMNS_RL=[21, 26, 50, 16, 66, 52, 74, 42, 23, 44, 51, 33, 48, 58, 73, 57, 47, 65, 28, 43, 39, 18, 30, 32, 22, 9, 31, 17, 27, 36, 38, 34, 46, 60, 49]
def machine_learning_warning(PCAP_NAME):
    info = 0
    miningFlows = NFStreamer(
        source=PCAP_NAME, statistical_analysis=True).to_pandas()
    infoColumns = [2, 5, 6, 14]
    infoFlows = miningFlows.iloc[:, infoColumns]
    miningFlows = miningFlows.iloc[:, FEATURE_COLUMNS_RL]
    ml_warnlist = list()
    for num in MLMODEL_RL.predict(miningFlows.values):
        if num == 1:
            ml_warnlist.append({'ip_port': infoFlows.src_ip[info]+':'+str(infoFlows.src_port[info]),
                               'warn': 'RF模型匹配', 'time': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(infoFlows.bidirectional_first_seen_ms[info])/1000)), 
                               'data': '加密挖矿流量'})
            info += 1
            IP_Set.add(infoFlows.src_ip[info])
    return ml_warnlist


