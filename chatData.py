import argparse
import pandas as pd
import subprocess
from tqdm import tqdm
from multiprocessing import Pool

# 解析命令行参数
parser = argparse.ArgumentParser(description='读取预处理过的Excel格式会话记录并解密会话为JSONL文件')
parser.add_argument('file_name', help='预处理过的会话记录文件，如：chat.xlsx')
args = parser.parse_args()

# 读取Excel文件
print(f"开始加载文件{args.file_name}……💕")
df = pd.read_excel(args.file_name, engine='openpyxl')

# 获取encrypt_key和encrypt_chat_msg列的数据
encrypt_key = df['encrypt_key'].tolist()
encrypt_chat_msg = df['encrypt_chat_msg'].tolist()

# 构造指令
cmd = ['./sdktools', '3']


def process_data(i):
    # 将encrypt_key和encrypt_chat_msg列中的数据依次传递给指令
    subprocess.run(cmd + [encrypt_key[i], encrypt_chat_msg[i]],
                   stdout=subprocess.PIPE)


if __name__ == '__main__':
    # 使用多进程加速数据处理过程
    print("开始解密聊天记录……💕")
    with Pool() as p:
        for _ in tqdm(p.imap_unordered(process_data, range(len(encrypt_key))),
                      total=len(encrypt_key), desc='Processing'):
            pass

    # 打印结果
    print('数据处理完成 ✔')
