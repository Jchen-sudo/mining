from pickle import TRUE
from scapy.all import rdpcap
import os
from collections import OrderedDict

#coding:UTF-8


from scapy.all import *
import time

#Web连接数据HTTP 80,8080
def get_host_ip(PCAPS):
    ip_list = list()
    for pcap in PCAPS:
        if pcap.haslayer(IP):
            ip_list.append(pcap.getlayer(IP).src)
            ip_list.append(pcap.getlayer(IP).dst)
    host_ip = collections.Counter(ip_list).most_common(1)[0][0]
    return host_ip

def web_data(PCAPS, host_ip):
    ip_port_id_list = list()
    id = 0
    for pcap in PCAPS:
        if pcap.haslayer(TCP) and pcap.haslayer(Raw):
            src = pcap.getlayer(IP).src
            dst = pcap.getlayer(IP).dst
            sport = pcap.sport
            dport = pcap.dport
            if TRUE:
                port = dport
                if src == host_ip:
                    ip = dst
                    ip_port_id_list.append({'ip_port':ip+ ':' + str(port) + ':' + 'HTTP', 'id':id})
                elif dst == host_ip:
                    ip = src
                    ip_port_id_list.append({'ip_port':ip+ ':' + str(port) + ':' + 'HTTP', 'id':id})
                else:
                    pass
            elif TRUE:
                port = sport
                if src == host_ip:
                    ip = dst
                    ip_port_id_list.append({'ip_port':ip+ ':' + str(port) + ':' + 'HTTP', 'id':id})
                elif dst == host_ip:
                    ip = src
                    ip_port_id_list.append({'ip_port':ip+ ':' + str(port) + ':' + 'HTTP', 'id':id})
                else:
                    pass
            else:
                pass
        id += 1
    ip_port_ids_dict = OrderedDict()    #{'192.134.13.234:232':[2,3,4,5],'192.134.13.234:236':[4,3,2,4,3]}
    for ip_port_id in ip_port_id_list:
        if ip_port_id['ip_port'] in ip_port_ids_dict:
            ip_port_ids_dict[ip_port_id['ip_port']].append(ip_port_id['id'])#PCAPS[ip_port_id['id']].load)
        else:
            ip_port_ids_dict[ip_port_id['ip_port']] = [ip_port_id['id']] #[PCAPS[ip_port_id['id']].load]
    ip_port_data_list = list()
    data_id = 0
    for ip_port, load_list in ip_port_ids_dict.items():
        data_id += 1
        raw_data = b''.join([PCAPS[i].load for i in load_list])
        #解决编码问题
        tmp_data = raw_data.decode('UTF-8', 'ignore')
        if ('gbk' in tmp_data) or ('GBK' in tmp_data):
            data = raw_data.decode('GBK', 'ignore')
        else:
            data = tmp_data
        ip_port_data_list.append({'data_id':data_id,'ip_port':ip_port, 'data':data, 'raw_data':raw_data, 'lens':'%.3f'%(sum([len(corrupt_bytes(PCAPS[i])) for i in load_list])/1024.0)})
    return ip_port_data_list

class PcapDecode:
    def __init__(self):
        #ETHER:读取以太网层协议配置文件
        with open('./app/utils/protocol/ETHER', 'r', encoding='UTF-8') as f:
            ethers = f.readlines()
        self.ETHER_DICT = dict()
        for ether in ethers:
            ether = ether.strip().strip('\n').strip('\r').strip('\r\n')
            self.ETHER_DICT[int(ether.split(':')[0])] = ether.split(':')[1]

        #IP:读取IP层协议配置文件
        with open('./app/utils/protocol/IP', 'r', encoding='UTF-8') as f:
            ips = f.readlines()
        self.IP_DICT = dict()
        for ip in ips:
            ip = ip.strip().strip('\n').strip('\r').strip('\r\n')
            self.IP_DICT[int(ip.split(':')[0])] = ip.split(':')[1]

        #PORT:读取应用层协议端口配置文件
        with open('./app/utils/protocol/PORT', 'r', encoding='UTF-8') as f:
            ports = f.readlines()
        self.PORT_DICT = dict()
        for port in ports:
            port = port.strip().strip('\n').strip('\r').strip('\r\n')
            self.PORT_DICT[int(port.split(':')[0])] = port.split(':')[1]

        #TCP:读取TCP层协议配置文件
        with open('./app/utils/protocol/TCP', 'r', encoding='UTF-8') as f:
            tcps = f.readlines()
        self.TCP_DICT = dict()
        for tcp in tcps:
            tcp = tcp.strip().strip('\n').strip('\r').strip('\r\n')
            self.TCP_DICT[int(tcp.split(':')[0])] = tcp.split(':')[1]

        #UDP:读取UDP层协议配置文件
        with open('./app/utils/protocol/UDP', 'r', encoding='UTF-8') as f:
            udps = f.readlines()
        self.UDP_DICT = dict()
        for udp in udps:
            udp = udp.strip().strip('\n').strip('\r').strip('\r\n')
            self.UDP_DICT[int(udp.split(':')[0])] = udp.split(':')[1]

    #解析以太网层协议
    def ether_decode(self, p):
        data = dict()
        if p.haslayer(Ether):
            data = self.ip_decode(p)
            return data
        else:
            data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
            data['Source'] = 'Unknow'
            data['Destination'] = 'Unknow'
            data['Procotol'] = 'Unknow'
            data['len'] = len(corrupt_bytes(p))
            data['info'] = p.summary()
            return data

    #解析IP层协议
    def ip_decode(self, p):
        data = dict()
        if p.haslayer(IP):  #2048:Internet IP (IPv4)
            ip = p.getlayer(IP)
            if p.haslayer(TCP):  #6:TCP
                data = self.tcp_decode(p, ip)
                return data
            elif p.haslayer(UDP): #17:UDP
                data = self.udp_decode(p, ip)
                return data
            else:
                if ip.proto in self.IP_DICT:
                    data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                    data['Source'] = ip.src
                    data['Destination'] = ip.dst
                    data['Procotol'] = self.IP_DICT[ip.proto]
                    data['len'] = len(corrupt_bytes(p))
                    data['info'] = p.summary()
                    return data
                else:
                    data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                    data['Source'] = ip.src
                    data['Destination'] = ip.dst
                    data['Procotol'] = 'IPv4'
                    data['len'] = len(corrupt_bytes(p))
                    data['info'] = p.summary()
                    return data
        elif p.haslayer(IPv6):  #34525:IPv6
            ipv6 = p.getlayer(IPv6)
            if p.haslayer(TCP):  #6:TCP
                data = self.tcp_decode(p, ipv6)
                return data
            elif p.haslayer(UDP): #17:UDP
                data = self.udp_decode(p, ipv6)
                return data
            else:
                if ipv6.nh in self.IP_DICT:
                    data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                    data['Source'] = ipv6.src
                    data['Destination'] = ipv6.dst
                    data['Procotol'] = self.IP_DICT[ipv6.nh]
                    data['len'] = len(corrupt_bytes(p))
                    data['info'] = p.summary()
                    return data
                else:
                    data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                    data['Source'] = ipv6.src
                    data['Destination'] = ipv6.dst
                    data['Procotol'] = 'IPv6'
                    data['len'] = len(corrupt_bytes(p))
                    data['info'] = p.summary()
                    return data
        else:
            if p.type in self.ETHER_DICT:
                data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                data['Source'] = p.src
                data['Destination'] = p.dst
                data['Procotol'] = self.ETHER_DICT[p.type]
                data['len'] = len(corrupt_bytes(p))
                data['info'] = p.summary()
                return data
            else:
                data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
                data['Source'] = p.src
                data['Destination'] = p.dst
                data['Procotol'] = hex(p.type)
                data['len'] = len(corrupt_bytes(p))
                data['info'] = p.summary()
                return data

    #解析TCP层协议
    def tcp_decode(self, p, ip):
        data = dict()
        tcp = p.getlayer(TCP)
        data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
        data['Source'] = ip.src + ":" + str(ip.sport)
        data['Destination'] = ip.dst + ":" + str(ip.dport)
        data['len'] = len(corrupt_bytes(p))
        data['info'] = p.summary()
        if tcp.dport in self.PORT_DICT:
            data['Procotol'] = self.PORT_DICT[tcp.dport]
        elif tcp.sport in self.PORT_DICT:
            data['Procotol'] = self.PORT_DICT[tcp.sport]
        elif tcp.dport in self.TCP_DICT:
            data['Procotol'] = self.TCP_DICT[tcp.dport]
        elif tcp.sport in self.TCP_DICT:
            data['Procotol'] = self.TCP_DICT[tcp.sport]
        else:
            data['Procotol'] = "TCP"
        return data

    #解析UDP层协议
    def udp_decode(self, p, ip):
        data = dict()
        udp = p.getlayer(UDP)
        data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.time))
        data['Source'] = ip.src + ":" + str(ip.sport)
        data['Destination'] = ip.dst + ":" + str(ip.dport)
        data['len'] = len(corrupt_bytes(p))
        data['info'] = p.summary()
        if udp.dport in self.PORT_DICT:
            data['Procotol'] = self.PORT_DICT[udp.dport]
        elif udp.sport in self.PORT_DICT:
            data['Procotol'] = self.PORT_DICT[udp.sport]
        elif udp.dport in self.UDP_DICT:
            data['Procotol'] = self.UDP_DICT[udp.dport]
        elif udp.sport in self.UDP_DICT:
            data['Procotol'] = self.UDP_DICT[udp.sport]
        else:
            data['Procotol'] = "UDP"
        return data

PD = PcapDecode()  # 解析器
filepath = './database'
ONPCAPS_NAME = '2K.pcap'
ONPCAPS = None
PCAPS = None
PCAPS = rdpcap(os.path.join(filepath, ONPCAPS_NAME))
host_ip = get_host_ip(PCAPS)
with open('./app/utils/warning/HTTP_ATTACK', 'r', encoding='UTF-8') as f:
    attacks = f.readlines()
ATTACK_DICT = dict()
for attack in attacks:
    attack = attack.strip()
    ATTACK_DICT[attack.split(' : ')[0]] = attack.split(' : ')[1]

webdata = web_data(PCAPS, host_ip)
print(webdata)
webwarn_list = list()
for web in webdata:
    data = web['data']
    for pattn, attk in ATTACK_DICT.items(): #特征码和攻击名称
            if pattn.upper() in data.upper():
                webwarn_list.append({'ip_port': web['ip_port'].split(':')[0]+':'+web['ip_port'].split(':')[1], 'warn':attk, 'time':pattn, 'data':data})
print(webwarn_list)