# label数据，存放在 labeled_data 里 
# 白流量是1，黑为0
# 发现只要替换`NeedManualLabel`值就可以了
import argparse

def label(args):
    with open(args.input, 'r') as fin:
        with open(args.output, 'w') as fout:
            while True:
                l = fin.readline()
                if not l:
                    break
                fout.write(l.replace('NeedManualLabel', args.label))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='label Program.') 
    
    # 定义参数
    parser.add_argument('-i', '--input', type=str, help='input file')
    parser.add_argument('-o', '--output', type=str, help='output file')
    parser.add_argument('-l', '--label', type=str, help='label')

    # 解析参数
    args = parser.parse_args()
    print('input:', args.input)
    if not args.output:
        args.output = args.input[:-4] + '_labeled.csv'
    print('output:', args.output)
    print('label:', args.label)

    label(args)

    print('Done!')
    
    
