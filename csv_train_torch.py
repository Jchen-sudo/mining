import nntplib
from threading import local
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from torchvision import transforms
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, silhouette_score
import pandas as pd
import numpy as np


local_dir = "./"
iscv_filename = "test.csv"
data_columns = ['Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Total Length of Bwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length',
                'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets', 'Subflow Bwd Bytes', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min']
label_columns = ['Label']
strip_columns = ['Flow ID', 'Src IP', 'Src Port',
                 'Dst IP', 'Protocol', 'Timestamp', 'Label']


class CSVDataset(Dataset):
    def __init__(self, csv_file, preprocesser=None, transform=None):
        self.df = pd.read_csv(csv_file)
        if preprocesser:
            self.df = preprocesser(self.df)
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        target = self.df.iloc[index][:-1].to_numpy(dtype=np.float32)
        label = self.df.iloc[index][-1]
        if self.transform:
            target = self.transform(target)
        #print(len(target))
        return target, label


class CSVDataPreprocesser(object):
    def __init__(self, strip_columns=strip_columns):
        self.strip_columns = strip_columns

    def _removeAttributes(self, target):
        return target.drop(self.strip_columns, axis=1, inplace=False)

    def _cleanCustomData(self, target):
        target = target.astype(
            {'Flow Packets/s': np.float64, 'Flow Bytes/s': np.float64})
        return target[~target.isin([np.nan, np.inf, -np.inf]).any(1)]

    def _labelEncode(self, target):
        for columns in target.columns:
            if columns in label_columns:
                target[columns] = LabelEncoder().fit_transform(
                    target[columns])
        return target
        #encoder = LabelEncoder()
        #encoder.fit(target)
        #return encoder.transform(target)

    def __call__(self, target):
        target = self._cleanCustomData(target)
        target = self._removeAttributes(target)
        target = self._labelEncode(target)
        return target


if __name__ == "__main__":
    data_dir = local_dir
    csv_file = data_dir + iscv_filename
    preprocesser = CSVDataPreprocesser()
    dataset = CSVDataset(csv_file, preprocesser)
    dataloader = DataLoader(dataset, batch_size=32)

    # # Linear SVM 
    # # nnd, 麻烦死了, 不如用sklearn
    # device = torch.device("cpu")

    # model = nn.Linear(len(data_columns), 1)
    # model.to(device)
    # optim = optim.SGD(model.parameters(), lr=0.01)

    # model.train()

    # for epoch in range(10):
    #     perm = torch.randperm(len(dataset))
    #     sum_loss = 0
    #     for i, (data, label) in enumerate(dataloader):
    #         data.to(device)
    #         label.to(device)
    #         optim.zero_grad()
    #         output = model(data).squeeze()
    #         weight = model.weight.squeeze()
    #         loss = torch.mean(torch.clamp(1 - label * output, min=0))
    #         loss += 0.01 * (weight.t() @ weight) / 2.0
    #         loss.backward()
    #         optim.step()
    #         sum_loss += loss.item()
    #     print("Epoch: {:4d}\tloss: {}".format(epoch, sum_loss / len(dataset)))

    kmeans = KMeans(n_clusters=2)
    for _, (data, label) in enumerate(dataloader):
        kmeans.fit(data.numpy())
    print(kmeans.cluster_centers_)

    gnb = GaussianNB()
    for _, (data, label) in enumerate(dataloader):
        gnb.fit(data.numpy(), label.numpy())
    print(gnb.theta_)

    dt = DecisionTreeClassifier()
    for _, (data, label) in enumerate(dataloader):
        dt.fit(data.numpy(), label.numpy())
    print(dt.tree_.feature)

    rfc = RandomForestClassifier()
    for _, (data, label) in enumerate(dataloader):
        rfc.fit(data.numpy(), label.numpy())
    print(rfc.feature_importances_)