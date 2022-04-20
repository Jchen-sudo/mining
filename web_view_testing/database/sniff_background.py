from datetime import datetime
from scapy.all import sniff, wrpcap
import os
# https://www.osgeo.cn/scapy/api/scapy.sendrecv.html?highlight=sniff#scapy.sendrecv.sniff

_TIME_TEMPLATE = "%Y-%m-%d %H:%M"



def sniff_callback(packet):
    # print(packet.summary())
    # 储存为pacp文件
    wrpcap(f'./database/pcaps/{datetime.now().strftime(_TIME_TEMPLATE)}.pcap',packet, append=True)

def sniff_main():
    # 判断是否存在pcaps文件夹
    if not os.path.exists('./database/pcaps/'):
        os.mkdir('./database/pcaps/')
    filter = ""
    sniff(filter=filter, prn=sniff_callback,  count=0)


def main():
    sniff_main()

if __name__ == '__main__':
    main()


'''
sniff:
count -- 要捕获的数据包数。0表示无穷大。
store -- 是存储嗅探包还是丢弃它们
prn -- 应用于每个数据包的函数。如果返回某个内容，则显示该内容。--例如：prn=lambda x:x.summary（）
session -- 会话=用于处理数据包流的流解码器。--例如：session=TCPSession请参阅下面的详细信息。
filter -- 要应用的BPF筛选器。
lfilter -- 应用于每个包的Python函数，以确定是否可以执行进一步的操作。--例如：lfilter=lambda x:x.haslayer（填充）
offline -- PCAP文件（或PCAP文件列表）从中读取数据包，而不是嗅探它们
quiet -- 当设置为True时，将丢弃进程stderr（默认值：False）。
timeout -- 在给定时间后停止嗅探（默认值：无）。
L2socket -- 使用提供的L2socket（默认值：use conf.L2listen）。
opened_socket -- 提供一个对象（或一个对象列表），以便在上使用.recv（）。
stop_filter -- Python函数应用于每个包，以确定是否必须在此包之后停止捕获。--例如：stop_filter=lambda x:x.haslayer（TCP）
iface -- 接口或接口列表（默认值：无用于在所有接口上探查）。
monitor -- 使用监视器模式。可能并非所有操作系统都可用
started_callback -- 在嗅探器开始嗅探时立即调用（默认值：None）。
'''
