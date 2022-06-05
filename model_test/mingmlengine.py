from nfstream import NFStreamer
import joblib
from my_model_test import *
from tqdm import tqdm
# 统计图
import matplotlib.pyplot as plt
# 画频数图
def plot_freq(dataframe):
    plt.title('running time')
    plt.hist(dataframe, bins=50)
    plt.show()


mlmodel = joblib.load('RF.joblib')
FEATURE_COLUMNS = [21, 26, 50, 16, 66, 52, 74, 42, 23, 44, 51, 33, 48, 58, 73,
                    57, 47, 65, 28, 43, 39, 18, 30, 32, 22, 9, 31, 17, 27, 36, 38, 34, 46, 60, 49]

# @count_info
# @count_time
# @count_mem
@count_time
def predict(dataframe):
    return mlmodel.predict(dataframe)

# @count_info
# @count_cpu_time
def main():
    # 离线模块要输入字段删选的featureColumns
    miningFlows = NFStreamer(source="../../sniff_test/last_100_minutes.pcap",
                             statistical_analysis=True).to_pandas()
    miningFlows = miningFlows.iloc[:, FEATURE_COLUMNS]
    print('数据包大小：')
    print(f"{len(miningFlows)}行{len(miningFlows.columns)}列")
    
    ts = []
    for i in tqdm(range(1000)):
        _, t = predict(miningFlows.values)
        ts.append(t/1222)
    print(ts)
    print('平均：',sum(ts)/len(ts))
    plot_freq(ts)
    
    

if __name__ == "__main__":
    t = []
    main()
    # for i  in range(10):
    #     t.append(main()[1])
    # print(t)
    # print(sum(t)/len(t))
    # plot_freq(t)
    