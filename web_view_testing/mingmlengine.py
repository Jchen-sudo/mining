from nfstream import NFStreamer
import joblib
import time
import numpy as np
mlmodel = joblib.load('RF.joblib')

def predict(dataframe):
    if mlmodel.predict(dataframe)[0] == 1:
            return mlmodel.predict(dataframe)
    else:
            return 'Normal'


if __name__ == "__main__":
    miningFlows = NFStreamer(source="./2K.pcap", statistical_analysis=True).to_pandas()  #离线模块要输入字段删选的featureColumns
    featureColumns=[21, 26, 50, 16, 66, 52, 74, 42, 23, 44, 51, 33, 48, 58, 73, 57, 47, 65, 28, 43, 39, 18, 30, 32, 22, 9, 31, 17, 27, 36, 38, 34, 46, 60, 49]
    info=0
    infoColumns = [2,5,6,14]
    infoFlows =  miningFlows.iloc[:, infoColumns]
    #print(infoFlows.bidirectional_first_seen_ms.astype(np.float32))
    miningFlows =  miningFlows.iloc[:, featureColumns]
    ml_warnlist=list()
    for num in  mlmodel.predict(miningFlows.values):
        if num == 1:
            ml_warnlist.append ({'ip_port':infoFlows.src_ip[info]+':'+str(infoFlows.src_port[info]), 'warn': 'RF模型匹配', 'time':time.strftime('%Y-%m-%d %H:%M:%S',infoFlows.bidirectional_first_seen_ms[info]), 'data':'加密挖矿流量'})
        info+=1
    print(ml_warnlist)