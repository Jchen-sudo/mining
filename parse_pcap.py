#!/usr/bin/env python
# encoding: utf-8

import sys
import socket
import dpkt

filename = "./mining.pcap"

server_ip = socket.inet_aton("10.78.128.14")
client_ip = socket.inet_aton("10.79.29.69")
serv_port = 3000

class reqData:
  def __init__(self):
    self.hincrby = 0
    self.expire = 0
    self.hgetall = 0
    self.reply = 0

class ProcRet:
  def __init__(self):
    self.port = 0
    self.pkt = {'ack':0,'syn':0,'psh':0,'fin':0,'rst':0,'urg':0}
    self.req = 0;
    self.rep = 0;
    self.ret = reqData()

def search(conn, port):
  for i in conn:
    if i.port == port:
      return i
  return None

def procRep(payload):
  string = payload.decode('utf-8','ignore')
  return string.count(':')

def procHin(payload):
  string = payload.decode('utf-8','ignore')
  return string.count('HINCRBY')

def procExp(payload):
  string = payload.decode('utf-8','ignore')
  return string.count('EXPIRE')

def procHget(payload):
  string = payload.decode('utf-8','ignore')
  return string.count('HGETALL')

def printReqData(req):
  print("HINCRBY:%d"%(req.hincrby))
  print("EXPIRE:%d"%(req.expire))
  print("REPLY:%d"%(req.reply))
  print("HGETALL:%d"%(req.hgetall))

def printProcRet(pret):
  print("Port:%d"%(pret.port))
  print(pret.pkt)
  print("Request:%d"%(pret.req))
  print("Reply:%d"%(pret.rep))
  printReqData(pret.ret)

def printAll(conn):
  for i in conn:
    printProcRet(i)


def procTcp(tcp, pret=None):
  if(None == pret):
    pret = ProcRet()
  if tcp.flags & 0x10 != 0:
    pret.pkt['ack'] += 1
  if tcp.flags & 0x02 != 0:
    pret.pkt['syn'] += 1
  if tcp.flags & 0x08 != 0:
    pret.pkt['psh'] += 1
    if tcp.sport == serv_port:
      pret.rep += 1
      pret.ret.reply += procRep(tcp.data)
    else:
      pret.req += 1
      pret.ret.hincrby += procHin(tcp.data)
      pret.ret.expire += procExp(tcp.data)
      pret.ret.hgetall += procHget(tcp.data)
  if tcp.flags & 0x01 != 0:
    pret.pkt['fin'] += 1
  if tcp.flags & 0x04 != 0:
    pret.pkt['rst'] += 1
  if tcp.flags & 0x20 != 0:
    pret.pkt['urg'] += 1
  return pret


def procPcap(pcap, conn):
  for (ts, buf) in pcap:
    eth = dpkt.ethernet.Ethernet(buf)
    ip = eth.data
    tcp = ip.data
    if serv_port == tcp.sport:
      client_port = tcp.dport
    else:
      client_port = tcp.sport
    pret = search(conn, client_port)
    if None == pret:
      pret = procTcp(tcp)
      pret.port = client_port
      conn.append(pret)
    else:
      pret = procTcp(tcp,pret)

def analyRet(conn):
  for i in conn:
    if i.ret.hgetall > 0:
      continue
    else:
      req = i.ret.hincrby + i.ret.expire
      rep = i.ret.reply
      if rep < req:
        print("Port-%d get %d reply in %d request"%(i.port,rep,req))
      else:
        print("Port-%d handle correctly reply:%d request:%d"%(i.port,rep,req))


if __name__=="__main__":
  print("begin test")
  f = open(filename,'rb')
  pcap = dpkt.pcap.Reader(f)
  conn = []
  procPcap(pcap,conn)
  analyRet(conn)
  #printAll(conn)