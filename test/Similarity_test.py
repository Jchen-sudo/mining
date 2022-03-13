import csv

with open(r'./data/csv/XMR_1.8K.pcap_Flow_CIC.csv', 'r') as f:
    reader = csv.reader(f)

    headers = next(reader)
    # print(headers)
    rows1 = [row[7:83] for row in reader] # 取8~83列


with open(r'./data/csv/WhiteStream/Steam.exe_21688.pcap_Flow.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    rows2 = [row[7:83] for row in reader] # 取8~83列


rows = rows1 + rows2
# rows.append(rows2)

# 标准化
from sklearn.preprocessing import StandardScaler, MinMaxScaler
rows_standscaler = StandardScaler().fit_transform(rows)
rows_minmaxscaler = MinMaxScaler().fit_transform(rows)
print(rows_standscaler)
print(rows_minmaxscaler)



# 可以PCA降维后再计算相似度，这先空着

# 相似度计算
# 因为可能有潜在的正比关系，所以可以用余弦相似度试试
from sklearn.metrics.pairwise import cosine_similarity
result=cosine_similarity(rows_standscaler[0].reshape(1,-1), rows_standscaler[-1].reshape(1,-1))
print('相似度：', result)

# 测试发现，同类的相似度比较高，异类的相似度比较低
# 实验性的测试，需要通过理论进一步的优化
