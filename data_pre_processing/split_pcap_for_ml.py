import dpkt
import argparse

def get_ip_from_bytes(ip_bytes):
    return '.'.join([str(int.from_bytes(ip_bytes[i:i+1], byteorder='big')) for i in range(0, len(ip_bytes), 1)])

def get_pkt_tuple(pkt):
    src_ip = pkt.data.src
    dst_ip = pkt.data.dst
    src_port = pkt.data.data.sport
    dst_port = pkt.data.data.dport
    proto = pkt.data.p
    if int.from_bytes(src_ip, byteorder='big') < int.from_bytes(dst_ip, byteorder='big'):
        return "{}-{}-{}-{}-{}".format(get_ip_from_bytes(src_ip), get_ip_from_bytes(dst_ip), src_port, dst_port, proto)
    else:
        return "{}-{}-{}-{}-{}".format(get_ip_from_bytes(dst_ip), get_ip_from_bytes(src_ip), dst_port, src_port, proto)

def run_preprocess(input_file, out_dir):
    pcap_file = open(input_file, "rb")
    pcap = dpkt.pcap.Reader(pcap_file)
    pkt_list = []
    for _, buffer in pcap:
        pkt_list.append(dpkt.ethernet.Ethernet(buffer))
    tuple_dict = {}
    for pkt in pkt_list:
        try:
            pkt_tuple = get_pkt_tuple(pkt)
        except:
            continue
        if pkt_tuple not in tuple_dict:
            tuple_dict[pkt_tuple] = [pkt]
        else:
            tuple_dict[pkt_tuple].append(pkt)
            
    for pkt_tuple in list(tuple_dict):
        if tuple_dict[pkt_tuple][0].data.p != 6:
            del tuple_dict[pkt_tuple]

    for pkt_tuple in tuple_dict:
        try:
            flow_data = b""
            flow_id = 0
            flow_est = True
            for pkt in tuple_dict[pkt_tuple]:
                if not flow_est:
                    if pkt.data.data.flags != 0x18:
                        continue
                    else:
                        flow_est = True
                if pkt.data.data.flags==0x18: # TCP PSH,ACK
                    temp_pkt = pkt.data
                    temp_pkt.src = b"\x00" * 4
                    temp_pkt.dst = b"\x00" * 4
                    temp_pkt.data.sport = 0
                    temp_pkt.data.dport = 0
                    flow_data += bytes(temp_pkt)
                else:
                    if pkt.data.data.flags & 0x1 == 1: # TCP FIN
                        if len(flow_data) > 1024:
                            with open("./{}/{}--{}.txt".format(out_dir, pkt_tuple, flow_id), "wb") as f:
                                f.write(flow_data)
                            flow_id += 1
                            flow_data = b""
                            flow_est = False
            if len(flow_data) > 1024:
                    with open("./{}/{}--{}.txt".format(out_dir, pkt_tuple, flow_id), "wb") as f:
                        f.write(flow_data)
        except:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='preprocessing the flow data')
    parser.add_argument('-i', '--input', type=str, help='input file')
    parser.add_argument('-d', '--directory', type=str, help='output dir')
    args = parser.parse_args()
    input_file = args.input
    out_dir = args.directory
    run_preprocess(input_file, out_dir)
