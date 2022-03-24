# 混合 csv 的数据 未做随机混合
import argparse

def mix_data(args):
    with open(args.output, 'w') as fout:
        with open(args.input[0], 'r') as fin:
            fout.write(fin.readline())
        for fin in args.input:
            with open(fin, 'r') as fin:
                fout.writelines(fin.readlines()[1:])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='mix Program. 未做随机混合 注意：输入文件必须是 csv 格式，并且每个文件的第一行都是 header') 
    
    # 定义参数
    parser.add_argument('-i', '--input', type=str,nargs='+', help='input file, can be more than one, or a dictory (end with /)')
    parser.add_argument('-o', '--output', type=str, help='output file')

    # 解析参数
    args = parser.parse_args()
    if not args.input:
        print('input file is needed')
        exit()
    # 如果输入是目录
    if len(args.input) == 1 and (args.input[0][-1] == '/' or args.input[0][-1] == '\\'):
        import os
        files = os.listdir(args.input[0])
        args.input = [args.input[0] + f for f in files]
    
    print('input:', args.input)
    if not args.output:
        args.output = './mixed.csv'
    print('output:', args.output)

    mix_data(args)

    print('Done!')