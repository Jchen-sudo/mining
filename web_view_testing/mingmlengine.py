from nfstream import NFStreamer
import joblib

mlmodel = joblib.load('RF.joblib')

def predict(dataframe):
    if mlmodel.predict(dataframe)[0] == 1:
            return 'Anomaly'
    else:
            return 'Normal'


if __name__ == "__main__":
    miningFlows = NFStreamer(source="./mergedMining.pcap", statistical_analysis=True).to_pandas()  #离线模块要输入字段删选的featureColumns
    featureColumns=[21, 26, 50, 16, 66, 52, 74, 42, 23, 44, 51, 33, 48, 58, 73, 57, 47, 65, 28, 43, 39, 18, 30, 32, 22, 9, 31, 17, 27, 36, 38, 34, 46, 60, 49]
    miningFlows =  miningFlows.iloc[:, featureColumns]
    print(predict(miningFlows.values))