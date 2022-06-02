import dpkt
from typing import List
from colorize import *
import os

def read_payload(filename: str, including_ip_layer: bool = False) -> List[bytes]:
    notice("Opening pcap file {}".format(filename))
    pcap_file = open(filename, "rb")
    pcap = dpkt.pcap.Reader(pcap_file)
    # assuming that the payload to analyse is on 4th layer
    # otherwise we can just modify this code
    pkt_list = []
    for timestamp, buffer in pcap:
        pkt_list.append(dpkt.ethernet.Ethernet(buffer))
    dataset = []
    if not including_ip_layer:
        notice("Excluding IP layer...")
        # not include IP layer
        for pkt in pkt_list:
            try:
                if pkt.data.data.data:
                    dataset.append(pkt.data.data.data) # Ethernet/IP/TCP
            except:
                continue
    else:
        notice("Including IP layer...")
        for pkt in pkt_list:
            try:
                # cover the ip address with random padding
                pkt_data = pkt.data
                pkt_data.src = os.urandom(4)
                pkt_data.dst = os.urandom(4)
                dataset.append(bytes(pkt_data))
            except:
                continue
    notice("Finishing loading dataset.")
    return dataset
