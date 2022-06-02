import re
import random
from typing import List, Dict
import numpy as np
from colorize import *


def n_gram_algo(N: int, dataset: List[bytes]) -> Dict[bytes, List[int]]:
    gram_dic = {}
    for I in dataset:
        for i in range(len(I) - N + 1):
            gram = I[i:i+N]  # slide window to shared data frames
            gLen = 1
            while gLen < N:  # 原论文里这里是`len < N`，打错了吧
                for j in range(len(gram) - gLen + 1):
                    gram_i = gram[j:j + gLen]
                    # 原论文 if gram in dic:
                    if gram_i in gram_dic:
                        gram_dic[gram_i].append(i)
                        # if i + j not in gram_dic[gram_i]:
                        #     gram_dic[gram_i].append(i + j)
                    else:
                        gram_dic[gram_i] = [i]  # gram_dic[gram] = [i]
                    gLen += 1
            if gram in gram_dic:
                gram_dic[gram].append(i)
            else:
                gram_dic[gram] = [i]
    return gram_dic


def bytes_to_str_map(data: bytes) -> str:
    # 应当有一个bytes -> str的映射
    return data.decode("cp437")


def delimiter_cut(dataset: List[bytes], delimiter_regex: str) -> List[str]:
    dataset_str = []
    for data in dataset:
        try:
            dataset_str.append(data.decode())
        except Exception as e:
            # 不知道是混进去了啥东西
            warning("Encounting undecodable data, skipping...")
    dataset_str_split = []
    for data in dataset_str:
        data_split = re.split(delimiter_regex, data)
        while "" in data_split:
            data_split.remove("")
        dataset_str_split.append(data_split)
    return dataset_str_split


def proto_jaccard(l1: List[int], l2: List[int]) -> float:
    if len(l1) > len(l2):
        l2 += [0 for i in range(len(l1) - len(l2))]
    elif len(l1) < len(l2):
        l1 += [0 for i in range(len(l2) - len(l1))]
    inner_prod = 0
    for i in range(len(l1)):
        inner_prod += l1[i] * l2[i]
    self_inner_prod_1 = 0
    self_inner_prod_2 = 0
    for i in range(len(l1)):
        self_inner_prod_1 += l1[i] ** 2
        self_inner_prod_2 += l2[i] ** 2
    try:
        return inner_prod / (self_inner_prod_1 + self_inner_prod_2 - inner_prod)
    except:
        return 0


def test_for_calc_thres(dataset, epoches):
    score = [0 for i in range(2000)]
    for _ in range(epoches):
        shuff_dataset = dataset.copy()
        random.shuffle(shuff_dataset)
        data_len = len(dataset)
        dataset1 = shuff_dataset[0 : data_len // 2]
        dataset2 = shuff_dataset[data_len // 2:]
        if len(dataset2) != len(dataset1):
            dataset2.pop()
        dataset1_gram = n_gram_algo(10, dataset1)
        dataset2_gram = n_gram_algo(10, dataset2)
        dataset1_cnt = []
        dataset2_cnt = []
        for key in dataset1_gram: 
            dataset1_cnt.append(len(dataset1_gram[key]))
        for key in dataset2_gram:
            dataset2_cnt.append(len(dataset2_gram[key]))
        dataset1_cnt.sort(reverse=True)
        dataset2_cnt.sort(reverse=True)
        for thres in range(500):
            dataset1_cnt_cut = dataset1_cnt
            for i in range(len(dataset1_cnt)):
                if dataset1_cnt[i] < thres:
                    dataset1_cnt_cut = dataset1_cnt[0:i]
                    break
            
            dataset2_cnt_cut = dataset2_cnt
            for i in range(len(dataset2_cnt)):
                if dataset2_cnt[i] < thres:
                    dataset2_cnt_cut = dataset2_cnt[0:i]
                    break
            score[thres] += proto_jaccard(dataset1_cnt_cut, dataset2_cnt_cut)
    for i in score:
        i /= epoches
    return score


def screen_gram_by_freq(dataset_str_split: List[str]) -> List[str]:
    notice("Screening data by frequency...")
    substr_cnt = {}
    for data in dataset_str_split:
        for substr in data:
            if substr not in substr_cnt:
                substr_cnt[substr] = 0
            else:
                continue
            for data_2 in dataset_str_split:
                if substr in data_2:
                    substr_cnt[substr] += 1
    strcnt = []
    for key in substr_cnt:
        strcnt.append(substr_cnt[key])
    strcnt.sort(reverse=True)
    # 需要去手动确定一个阈值
    # 得自动化
    thres = np.log10(strcnt)
    notice("Threshold is: ".format(thres))
    valid_gram_set = []
    for key in substr_cnt:
        if substr_cnt[key] > 10:
            valid_gram_set.append(key)
    return valid_gram_set