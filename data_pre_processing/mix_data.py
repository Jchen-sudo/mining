# 混合 csv 的数据
import argparse

def mix_data(args):
    with open(args.output, 'w') as fout:
        with open(args.input[0], 'r') as fin:
            fout.write(fin.readline())
        for fin in args.input:
            with open(fin, 'r') as fin:
                fout.writelines(fin.readlines()[1:])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='mix Program.\n未做随机混合 \n注意：输入文件必须是 csv 格式，并且每个文件的第一行都是 header') 
    
    # 定义参数
    parser.add_argument('-i', '--input', type=str,nargs='+', help='input file, can be more than one')
    parser.add_argument('-o', '--output', type=str, help='output file')

    # 解析参数
    args = parser.parse_args()
    if not args.input:
        print('input file is needed')
        exit()
    print('input:', args.input)
    if not args.output:
        args.output = './mixed.csv'
    print('output:', args.output)

    mix_data(args)

    print('Done!')