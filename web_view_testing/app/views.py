import imp
from tkinter.messagebox import NO
from app import app
from flask import jsonify, render_template, request, flash, redirect, url_for, send_from_directory
from .forms import Upload, ProtoFilter
from .utils.upload_tools import allowed_file, get_filetype, random_name
from .utils.pcap_decode import PcapDecode
from .utils.pcap_filter import get_all_pcap, proto_filter, showdata_from_id
from .utils.proto_analyzer import common_proto_statistic, pcap_len_statistic, http_statistic, dns_statistic, most_proto_statistic
from .utils.flow_analyzer import time_flow, data_flow, get_host_ip, data_in_out_ip, proto_flow, most_flow_statistic
from .utils.ipmap_tools import getmyip, get_ipmap, get_geo
from .utils.data_extract import web_data, telnet_ftp_data, mail_data, sen_data, client_info
from .utils.except_info import exception_warning
from .utils.file_extract import web_file, ftp_file, mail_file, all_files
from scapy.all import rdpcap, PacketList
import os
import hashlib

# 导入函数到模板中
app.jinja_env.globals['enumerate'] = enumerate

PD = PcapDecode()  # 解析器
filepath = './database/'
PCAP_NAME = '2K.pcap'
ONPCAPS = None
PCAPS = rdpcap(os.path.join(filepath, PCAP_NAME)) 
# ONPCAPS = rdpcap(os.path.join(filepath, ONPCAPS_NAME))

from datetime import datetime, timedelta
def pcap_cut(t: int) -> PacketList:
    dirPath = './database/pcaps/'
    p = PacketList()
    for i in range(0, t):
        lt = datetime.now() - timedelta(minutes=i)
        filePath = f'{dirPath}{lt.strftime("%Y-%m-%d %H:%M")}.pcap'
        # check if file exists
        if os.path.exists(filePath):
            p = rdpcap(filePath) + p # 保持时间顺序
    assert p.__len__() > 0
    return p


#--------------------------- 口令认证 ---------------------------------#
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from gmssl.sm3 import sm3_hash,bytes_to_list
sm3_hash_str = lambda x: sm3_hash(bytes_to_list(x.encode('utf8')))
auth = HTTPBasicAuth()
users = {
    "admin": generate_password_hash(sm3_hash_str("123456")),
    "user": generate_password_hash(sm3_hash_str("88888888"))
}
@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), sm3_hash_str(password)):
        return username
     

@app.route('/', methods=['POST', 'GET'])
@app.route('/login/', methods=['POST', 'GET'])
@auth.login_required
def login():
    return render_template('./home/login.html')

@app.route('/index/', methods=['POST', 'GET'])
def index():
    return render_template('./home/index.html')
    

@app.route('/flow/')
def flow():
    '''返回静态的实时流量分析页面'''
    global ONPCAPS
    ONPCAPS = pcap_cut(2)    #读取实时流量数据包
    time_flow_dict = time_flow(ONPCAPS)
    host_ip = get_host_ip(ONPCAPS)
    data_flow_dict = data_flow(ONPCAPS, host_ip)
    data_ip_dict = data_in_out_ip(ONPCAPS, host_ip)
    proto_flow_dict = proto_flow(ONPCAPS)
    most_flow_dict = most_flow_statistic(ONPCAPS, PD)
    most_flow_dict = sorted(most_flow_dict.items(),
                                key=lambda d: d[1], reverse=True)
    if len(most_flow_dict) > 10:
        most_flow_dict = most_flow_dict[0:10]
    most_flow_key = list()
    for key, value in most_flow_dict:
        most_flow_key.append(key)
    return render_template(
        './dataanalyzer/flowanalyzer.html', 
        time_flow_keys=list(time_flow_dict.keys()), 
        time_flow_values=list(time_flow_dict.values()), 
        data_flow=data_flow_dict, ip_flow=data_ip_dict, 
        proto_flow=list(proto_flow_dict.values()), 
        most_flow_key=most_flow_key, 
        most_flow_dict=most_flow_dict) 

@app.route('/api/flow_async/')
def api_flow_async():
    '''实时流量分析api'''
    global ONPCAPS
    ONPCAPS = pcap_cut(2)    #读取实时流量数据包
    time_flow_dict = time_flow(ONPCAPS)
    host_ip = get_host_ip(ONPCAPS)
    data_flow_dict = data_flow(ONPCAPS, host_ip)
    data_ip_dict = data_in_out_ip(ONPCAPS, host_ip)
    proto_flow_dict = proto_flow(ONPCAPS)
    most_flow_dict = most_flow_statistic(ONPCAPS, PD)
    most_flow_dict = sorted(most_flow_dict.items(),
                            key=lambda d: d[1], reverse=True)
    if len(most_flow_dict) > 10:
        most_flow_dict = most_flow_dict[0:10]
    most_flow_key = list()
    for key, value in most_flow_dict:
        most_flow_key.append(key)
    r =  {
        'time_flow_keys':list(time_flow_dict.keys()), 
        'time_flow_values':list(time_flow_dict.values()), 
        'data_flow':data_flow_dict, 
        'ip_flow':data_ip_dict, 
        'proto_flow':list(proto_flow_dict.values()), 
        'most_flow_key':most_flow_key, 
        'most_flow_dict':most_flow_dict
    }
    # 返回json数据
    return jsonify(r)

@app.route('/flow_async/')
def flow_async():
    '''动态的实时流量分析展示界面'''
    return render_template('./dataanalyzer/asyncflowanalyzer.html')


#---------------------------在线分析/基本信息---------------------------------#
@app.route('/online/database/', methods=['GET', 'POST'])
def online_basedata():
    '''
    基础数据解析
    '''
    global ONPCAPS,PD
    if ONPCAPS == None:
        flash("系统初始化中，请稍后!")
        return redirect(url_for('upload'))
    else:
        # 将筛选的type和value通过表单获取
        filter_type = request.form.get('filter_type', type=str, default=None)
        value = request.form.get('value', type=str, default=None)
        # 如果有选择，通过选择来获取值
        if filter_type and value:
            pcaps = proto_filter(filter_type, value, ONPCAPS, PD)
        # 默认显示所有的协议数据
        else:
            pcaps = get_all_pcap(ONPCAPS, PD)
        return render_template('./dataanalyzer/onbasedata.html', pcaps=pcaps)

#详细数据
@app.route('/ondatashow/', methods=['POST', 'GET'])
def ondatashow():
    if ONPCAPS == None:
        flash("请先上传要分析的数据包!")
        return redirect(url_for('upload'))
    else:
        dataid = request.args.get('id')
        dataid = int(dataid) - 1
        data = showdata_from_id(ONPCAPS, dataid)
        return data

#---------------------------在线分析/协议分析---------------------------------#
@app.route('/online/protoanalyzer/', methods=['POST', 'GET'])
def online_protoanalyzer():
    global ONPCAPS,PD
    if ONPCAPS == None:
        flash("请先上传要分析的数据包!")
        return redirect(url_for('index'))
    else:
        data_dict = common_proto_statistic(ONPCAPS)
        pcap_len_dict = pcap_len_statistic(ONPCAPS)
        pcap_count_dict = most_proto_statistic(ONPCAPS, PD)
        http_dict = http_statistic(ONPCAPS)
        http_dict = sorted(http_dict.items(),
                           key=lambda d: d[1], reverse=False)
        http_key_list = list()
        http_value_list = list()
        for key, value in http_dict:
            http_key_list.append(key)
            http_value_list.append(value)
        dns_dict = dns_statistic(ONPCAPS)
        dns_dict = sorted(dns_dict.items(), key=lambda d: d[1], reverse=False)
        dns_key_list = list()
        dns_value_list = list()
        for key, value in dns_dict:
            dns_key_list.append(key.decode('utf-8'))
            dns_value_list.append(value)
        return render_template('./dataanalyzer/protoanalyzer.html', data=list(data_dict.values()), pcap_len=pcap_len_dict, pcap_keys=list(pcap_count_dict.keys()), http_key=http_key_list, http_value=http_value_list, dns_key=dns_key_list, dns_value=dns_value_list, pcap_count=pcap_count_dict)



#---------------------------离线分析/数据包上传---------------------------------#
@app.route('/offline/upload/', methods=['POST', 'GET'])
def upload():
    upload = Upload()
    if request.method == 'GET':
        return render_template('./upload/upload.html')
    elif request.method == 'POST':
        pcap = upload.pcap.data
        if upload.validate_on_submit():
            pcapname = pcap.filename
            if allowed_file(pcapname):
                name1 = random_name()
                name2 = get_filetype(pcapname)
                global PCAP_NAME, PCAPS
                PCAP_NAME = name1 + name2
                try:
                    pcap.save(os.path.join(filepath, PCAP_NAME))
                    PCAPS = rdpcap(os.path.join(filepath, PCAP_NAME))     #PCAPS为已读取的pcap文件
                    flash('恭喜你,上传成功！')
                    return render_template('./upload/upload.html')
                except Exception as e:
                    flash('上传错误,错误信息:' +str(e))
                    return render_template('./upload/upload.html')
            else:
                flash('上传失败,请上传允许的数据包格式!')
                return render_template('./upload/upload.html')
        else:
            return render_template('./upload/upload.html')

#---------------------------离线分析/基本信息---------------------------------#
@app.route('/database/', methods=['GET', 'POST'])
def basedata():
    '''
    基础数据解析
    '''
    global PCAPS,PD
    if PCAPS == None:
        flash("请先上传离线数据!")
        return redirect(url_for('upload'))
    else:
        # 将筛选的type和value通过表单获取
        filter_type = request.form.get('filter_type', type=str, default=None)
        value = request.form.get('value', type=str, default=None)
        # 如果有选择，通过选择来获取值
        if filter_type and value:
            pcaps = proto_filter(filter_type, value, PCAPS, PD)
        # 默认显示所有的协议数据
        else:
            pcaps = get_all_pcap(PCAPS, PD)
        return render_template('./dataanalyzer/basedata.html', pcaps=pcaps)

#详细数据
@app.route('/datashow/', methods=['POST', 'GET'])
def datashow():
    global PCAPS,PD
    if PCAPS == None:
        flash("请先上传要分析的数据包!")
        return redirect(url_for('upload'))
    else:
        dataid = request.args.get('id')
        dataid = int(dataid) - 1
        data = showdata_from_id(PCAPS, dataid)
        return data
#-------------------------------离线分析/协议分析------------------------------#
@app.route('/protoanalyzer/', methods=['POST', 'GET'])
def protoanalyzer():
    global PCAPS,PD
    if PCAPS == None:
        flash("请先上传要分析的数据包!")
        return redirect(url_for('upload'))
    else:
        data_dict = common_proto_statistic(PCAPS)
        pcap_len_dict = pcap_len_statistic(PCAPS)
        pcap_count_dict = most_proto_statistic(PCAPS, PD)
        http_dict = http_statistic(PCAPS)
        http_dict = sorted(http_dict.items(),
                           key=lambda d: d[1], reverse=False)
        http_key_list = list()
        http_value_list = list()
        for key, value in http_dict:
            http_key_list.append(key)
            http_value_list.append(value)
        dns_dict = dns_statistic(PCAPS)
        dns_dict = sorted(dns_dict.items(), key=lambda d: d[1], reverse=False)
        dns_key_list = list()
        dns_value_list = list()
        for key, value in dns_dict:
            dns_key_list.append(key.decode('utf-8'))
            dns_value_list.append(value)
        return render_template('./dataanalyzer/protoanalyzer.html', data=list(data_dict.values()), pcap_len=pcap_len_dict, pcap_keys=list(pcap_count_dict.keys()), http_key=http_key_list, http_value=http_value_list, dns_key=dns_key_list, dns_value=dns_value_list, pcap_count=pcap_count_dict)

#---------------------------------------离线/挖矿告警---------------------------------#   
@app.route('/exceptinfo/', methods=['POST', 'GET'])
def exceptinfo():
    if PCAPS == None:
        flash("请先上传要分析的数据包!")
        return redirect(url_for('upload'))
    else:
        dataid = request.args.get('id')
        host_ip = get_host_ip(PCAPS)
        warning_list = exception_warning(PCAPS, host_ip)
        if dataid:
            if warning_list[int(dataid)-1]['data']:
                return warning_list[int(dataid)-1]['data'].replace('\r\n', '<br>')
            else:
                return '<center><h3>无相关数据包详情</h3></center>'
        else:
            return render_template('./exceptions/exception.html', warning=warning_list)

@app.route('/api/exceptinfo/')
def api_exceptinfo():
    if PCAPS == None:
        return jsonify([])
    else:
        host_ip = get_host_ip(PCAPS)
        warning_list = exception_warning(PCAPS, host_ip)
        return jsonify(except_visual.get_all(warning_list))
    
@app.route('/warn_async/')
def warn_async():
    '''动态的实时流量分析展示界面'''
    return render_template('./exceptions/asyncwarn.html')


#---------------------------------------在线/挖矿告警---------------------------------#  
@app.route('/onexceptinfo/', methods=['POST', 'GET'])
def onexceptinfo():
    if ONPCAPS == None:
        flash("系统正在初始化，请稍等")
        return redirect(url_for('upload'))
    else:
        dataid = request.args.get('id')
        host_ip = get_host_ip(ONPCAPS)
        warning_list = exception_warning(ONPCAPS, host_ip)
        if dataid:
            if warning_list[int(dataid)-1]['data']:
                return warning_list[int(dataid)-1]['data'].replace('\r\n', '<br>')
            else:
                return '<center><h3>无相关数据包详情</h3></center>'
        else:
            return render_template('./exceptions/exception.html', warning=warning_list)

from .utils import except_visual
@app.route('/api/onexceptinfo/')
def api_onexceptinfo():
    if ONPCAPS == None:
        return jsonify([])
    else:
        host_ip = get_host_ip(ONPCAPS)
        warning_list = exception_warning(ONPCAPS, host_ip)
        return jsonify(except_visual.get_all(warning_list))

@app.route('/xmr/')
def xmr():

    return render_template('./evidence/xmr.html')

#---------------------------------------error 界面---------------------------------#  

@app.errorhandler(404)  
def error_date(error):  
    return render_template('./error/404.html'), 404

@app.errorhandler(500)  
def error_date(error):  
    return render_template('./error/500.html'), 500
