import os
from split_pcap_for_ml import run_preprocess

out_dir = "./split_flow/normal"
in_dir = "./dataset/normal"

normal_filenames = next(os.walk(in_dir), (None, None, []))[2]
for filename in normal_filenames:
    run_preprocess(in_dir + "/" + filename, out_dir)

out_dir = "./split_flow/abnormal"
in_dir = "./dataset/abnormal"

abnormal_filenames = next(os.walk(in_dir), (None, None, []))[2]
for filename in abnormal_filenames:
    run_preprocess(in_dir + "/" + filename, out_dir)
