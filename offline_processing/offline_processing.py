from parsepcap import read_payload
from feature_screen import delimiter_cut, screen_gram_by_freq
from regexmaker.regexMaker import make_regex, check_regex, make_dataset
from colorize import *
import argparse

desc = """
Preprocessing private protocol pcap file for regex signalture extracting.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-i", "--input", type=str, help="input file")
    parser.add_argument("-o", "--output", type=str, help="output file directory")
    arg = parser.parse_args()
    if not arg.input or not arg.output:
        error("You should specify the input and output argument!")
        exit(0)
    try:
        dataset = read_payload(arg.input)
    except FileNotFoundError:
        error("File not found!")
        exit(0)
    # 先用delimiter cut的方法，N-gram不靠谱
    notice("Using delimiter cut to get grams...")
    delimiter = r"[\"',. \n{}\[\]:]"
    notice("Delimiter: " + delimiter)
    notice("Cutting...")
    grams = delimiter_cut(dataset, delimiter)
    valid_grams = screen_gram_by_freq(grams)
    notice("Cutting finished!")
    notice("Preprocessing dataset for regex extracting...")
    dataset = make_dataset(dataset, valid_grams)
    regex = make_regex(dataset, grams, 0, 2, 2, 2, 10)
    notice("Regex: ")
    print(regex)
    notice("Checking regex...Accuracy: ")
    print(check_regex(dataset, regex))