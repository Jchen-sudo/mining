from regexmaker.trieTree import trieTree, treeNode, example_cut_condition_func, example_upgrade_func
import re
import logging
from typing import List, Tuple, Callable, Dict
from colorize import *

def make_regex(dataset: List[List[str]], delimiter: List[str], cut_thres: float, 
                repeat_thres: int, repeat_cnt_thres: int, upgrade_thres: int, iters: int,
                 cut_func: Callable[[List[treeNode]], Dict[treeNode, float]] = example_cut_condition_func,
                 upgrade_func: Callable[[str], str] = example_upgrade_func) -> str:
    tree = trieTree(dataset, delimiter, cut_func, cut_thres, repeat_thres, repeat_cnt_thres, upgrade_thres, upgrade_func)
    notice("Creating regex with TrieTree...")
    tree.iter(iters)
    notice("Iteration finished, creating regex...")
    return tree.create_regex()


def check_regex(dataset: List[List[str]], regex: str) -> float:
    correct_cnt = 0
    for data in dataset:
        data_string = "".join(i for i in data)
        try:
            if re.match(regex, data_string) != None:
                correct_cnt += 1
        except:
            pass
    return correct_cnt / len(dataset)


def make_dataset(input_dataset: List[bytes], delimiter: List[str]) -> List[List[str]]:
    raw_dataset = []
    for data in input_dataset:
        try:
            raw_dataset.append(data.decode())
        except UnicodeDecodeError:
            pass
    dataset = []
    for line in raw_dataset:
        st = []
        i = 0
        while i < len(line):
            for gram in delimiter:
                if line[i:].startswith(gram):
                    st.append(gram)
                    i += len(gram)
                    break
            else:
                st.append(line[i])
                i += 1
        dataset.append(st)
    return dataset