"""
这个程序的思路在于对数据集中的数据产生一个扰动。
"""

import random
import string
from typing import List

def example_data_mutation_func1(dataset: List[List[str]], delimiter: List[str], mutated_rate: float = 0.3) -> List[List[str]]:
    """
    构造单点的改变
    """
    mutated_dataset = []
    for data in dataset:
        mutated_dataset.append(data)
        for i in range(len(data)):
            if random.random() < mutated_rate:
                if data[i] in string.ascii_lowercase:
                    data_copy = data.copy()
                    data_copy[i] = random.choice(string.ascii_lowercase)
                    mutated_dataset.append(data_copy)
                elif data[i] in string.digits:
                    data_copy = data.copy()
                    data_copy[i] = random.choice(string.digits)
                    mutated_dataset.append(data_copy)
                elif data[i] in string.ascii_uppercase:
                    data_copy = data.copy()
                    data_copy[i] = random.choice(string.ascii_uppercase)
                    mutated_dataset.append(data_copy)
    return mutated_dataset

def example_data_mutation_func2(dataset: List[List[str]], delimiter: List[str], expand_rate: float = 10) -> List[List[str]]:
    """
    在数据载荷部分构造连续的扰动
    """
    assert expand_rate > 1
    expand_size = int(len(dataset) * expand_rate)
    mutated_dataset = dataset.copy()
    for _ in range(expand_size - len(dataset)):
        data = random.choice(dataset).copy()
        for j in range(len(data)):
            if j in delimiter:
                continue
            if data[j] in string.ascii_lowercase:
                data[j] = random.choice(string.ascii_lowercase)
            elif data[j] in string.digits:
                data[j] = random.choice(string.digits)
            elif data[j] in string.ascii_uppercase:
                data[j] = random.choice(string.ascii_uppercase)
        mutated_dataset.append(data)
    return mutated_dataset
