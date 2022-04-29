import os
import re

from sqlalchemy import false
numi = 0
numd =0
def fun(ip):
    try:
        ip = str(ip).split(".")
        if len(ip) != 4:
            return False
        a,b,c,d = ip
        a,b,c,d = int(a),int(b),int(c),int(d)
        if 255 >= max(a, b, c, d) and 0 <= min(a, b, c, d):
            return True
    except:
        return False
with open(os.path.expanduser('./ioc.json'), 'r') as f:
    for i in f.readlines():
        if (fun(i)):
            numi += 1
            with open (os.path.expanduser('./ip.json'), 'a') as f:
                f.write(i)
        else:
            with open (os.path.expanduser('./domain.json'), 'a') as f:
                f.write(i)
            numd += 1
print('Number of IPs: ', numi)
print('Number of Domains: ', numd)
