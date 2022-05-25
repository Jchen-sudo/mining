from trieTree import trieTree, example_cut_condition_func, example_upgrade_func
import logging
import time
import re
from makeMutation import example_data_mutation_func1 as create_mutation

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

print(len(dataset))
dataset_mutation = create_mutation(dataset, delimiter)
print(len(dataset_mutation))

start_time = time.time()
tree = trieTree(dataset, delimiter, example_cut_condition_func, 0.2, 2, 2, 2, example_upgrade_func)
tree.iter(10)
answer = tree.create_regex()
tot_time = time.time() - start_time
print("Generate Regex:\n" + answer)
correct_cnt = 0
for data in raw_dataset:
    if re.match(answer, data):
        correct_cnt += 1
print("Correct rate:", correct_cnt / len(raw_dataset))
with open("regex.txt", "a+") as f:
    f.write("\n============================")
    f.write("\nGenerate Regex on dataset")
    f.write("\ndataset size: " + str(len(dataset)))
    f.write("\nIteration: " + str(10))
    f.write("\nCost time: " + str(tot_time))
    f.write("\nRegex length: " + str(len(answer)))
    f.write("\nCorrect rate: {:.3f}".format(correct_cnt / len(raw_dataset)))
    f.write("\n")
    f.write(answer)
    f.write("\n============================\n")

# 
# start_time = time.time()
# tree = trieTree(dataset_mutation, delimiter, example_cut_condition_func, 0.2, 2, 2, 2, example_upgrade_func)
# tree.iter(10)
# answer = tree.create_regex()
# tot_time = time.time() - start_time
# print("Generate Regex:\n" + answer)
# correct_cnt = 0
# for data in raw_dataset:
#     if re.match(answer, data):
#         correct_cnt += 1
# print("Correct rate:", correct_cnt / len(raw_dataset))
# with open("regex.txt", "a+") as f:
#     f.write("\n============================")
#     f.write("\nGenerate Regex on mutated dataset")
#     f.write("\ndataset size: " + str(len(dataset)))
#     f.write("\nIteration: " + str(10))
#     f.write("\nCost time: " + str(tot_time))
#     f.write("\nRegex length: " + str(len(answer)))
#     f.write("\nCorrect rate: {:.3f}".format(correct_cnt / len(raw_dataset)))
#     f.write("\n")
#     f.write(answer)
#     f.write("\n============================\n")
