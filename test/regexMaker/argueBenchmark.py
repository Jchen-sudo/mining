from trieTree import trieTree, example_cut_condition_func, example_upgrade_func
import logging
import re
import matplotlib.pyplot as plt
import numpy as np

def test_correct_rate(dataset, regex):
    correct_cnt = 0
    for data in dataset:
        if re.match(regex, data):
            correct_cnt += 1
    print("Correct rate:", correct_cnt / len(dataset))
    return correct_cnt / len(dataset)


logging.basicConfig(level=logging.INFO)

with open("valid_gram.txt", "r") as f:
    raw_valid_gram = f.read()
delimiter = raw_valid_gram.split("\n")
delimiter.remove("")

with open("clean-dataset.txt", "r") as f:
    raw_data = f.read()
raw_dataset = raw_data.split("\n")
while "" in raw_dataset:
    raw_dataset.remove("")

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

correct_rate_list = []
regex_length_list = []
cut_thres_list = np.arange(0, 0.5, 0.01)

for cut_thres in cut_thres_list:
    tree = trieTree(dataset, delimiter, example_cut_condition_func, cut_thres, 2, 2, 2, example_upgrade_func)
    tree.iter(10)
    correct_rate_list.append(test_correct_rate(raw_dataset, tree.create_regex()))
    regex_length_list.append(len(tree.create_regex()))

fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)
l1 = ax.plot(cut_thres_list, correct_rate_list, label="Correct Rate")
ax2 = ax.twinx()
l2 = ax2.plot(cut_thres_list, regex_length_list, "-r", label="Regex Length")
lns = l1 + l2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)
ax.set_xlabel("Cut Threshold")
ax.set_ylabel("Correct Rate")
ax.set_ylim(0, 1.1)
ax2.set_ylabel("Regex Length")
fig.savefig("correct_rate_and_regex_length_vs_cut_thres.svg")

regex_length_list = []
upgrade_thres = np.arange(2, 5, 1)
for upgrade in upgrade_thres:
    tree = trieTree(dataset, delimiter, example_cut_condition_func, 0.2, 2, 2, upgrade, example_upgrade_func)
    tree.iter(10)
    regex_length_list.append(len(tree.create_regex()))
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)
ax.plot(upgrade_thres, regex_length_list, label="Regex Length")
ax.set_xlabel("Upgrade Threshold")
ax.set_ylabel("Regex Length")
ax.legend()
fig.savefig("regex_length_vs_upgrade_thres.svg")
