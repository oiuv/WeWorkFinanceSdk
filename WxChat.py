import json
import os
import subprocess
import time
import pandas as pd
from tqdm import tqdm
from decrypt import decrypt_data


class WxChat:

    def __init__(self, seq_file='seq.txt', sdktools_path='./sdktools'):
        # 从文件读取起始 seq
        try:
            with open(seq_file, 'r') as f:
                self.seq = int(f.read().strip())
        except FileNotFoundError:
            self.seq = 0

        self.limit = 1000  # 每次拉取数据的条数
        self.seq = self.seq // self.limit * self.limit
        self.sdktools_path = sdktools_path

    def get_data(self):
        # 循环拉取数据
        while True:
            # 执行拉取数据的命令
            cmd = f"{self.sdktools_path} 1 {self.seq} {self.limit}"
            os.system(cmd)

            # 读取本地文件中的数据
            with open('chat.jsonl', 'r') as f:
                lines = f.readlines()

            # 解析最后一行数据
            last_line = lines[-1].strip()  # 读取最后一行数据
            last_data = json.loads(last_line)[
                'chatdata']  # 解析最后一行数据中的 chatdata 字段

            # 如果数据为空（无权访问）
            if not last_data:
                break

            # 更新 seq 参数，准备拉取下一批数据
            self.seq = last_data[-1]['seq']  # 获取最后一条数据的 seq，作为下一次拉取数据的起始 seq

            # 输出拉取进度，显示已拉取多少 seq
            print(f"当前拉取进度：第 {self.seq} 条数据 ✔")

            # 如果拉取到的数据不足 1000 条，则退出循环
            if len(last_data) < self.limit:
                break

        # 存储最终的 seq 值到文件中
        with open('seq.txt', 'w') as f:
            f.write(str(self.seq))

    def data_to_excel(self, file_name):
        # 统计代码运行时间
        start_time = time.time()

        # 创建一个空的 DataFrame
        df = pd.DataFrame()

        # 打开 JSONL 文件，并逐行读取数据
        print(f"开始加载文件{file_name}……💕")
        with open(file_name, 'r') as f:
            for line in f:
                # 将 JSON 字符串转换为 Python 对象
                data = json.loads(line)
                # 将 chatdata 字段中的数据添加到 DataFrame 中
                df = pd.concat(
                    [df, pd.DataFrame.from_records(data['chatdata'])])

        # 输出 DataFrame
        print(df)

        # 去重
        print("开始数据去重处理……💕")
        df.drop_duplicates(subset=['seq'], inplace=True)

        # 解密随机密钥
        print("开始解密随机密钥……💕")
        tqdm.pandas(desc="Decrypting random key")
        df['decrypt_random_key'] = df['encrypt_random_key'].progress_apply(decrypt_data)

        # 将 DataFrame 写入 Excel 文件
        print("数据存档中……💕")
        file_prefix = file_name.split('.')[0]
        df.to_excel(f"{file_prefix}.xlsx", index=False)

        # 输出 DataFrame
        print(df)

        # 输出代码运行时间
        end_time = time.time()
        print(f"数据预处理耗时 {end_time - start_time:.2f} 秒")

    def chat_data(self, file_name):
        # 统计代码运行时间
        start_time = time.time()

        # 读取Excel文件
        print(f"开始加载文件{file_name}......💕")
        df = pd.read_excel(file_name, engine='openpyxl')

        # 获取decrypt_random_key和encrypt_chat_msg列的数据
        decrypt_random_key = df['decrypt_random_key'].tolist()
        encrypt_chat_msg = df['encrypt_chat_msg'].tolist()

        # 构造指令
        cmd = [self.sdktools_path, '3']

        # 解密聊天记录
        print("开始解密聊天记录......💕")
        for i in tqdm(range(len(decrypt_random_key)), desc='Processing'):
            subprocess.run(cmd + [decrypt_random_key[i], encrypt_chat_msg[i]],
                           stdout=subprocess.PIPE)

        # 打印结果
        print('数据解密完成 ✔')

        # 输出代码运行时间
        end_time = time.time()
        print(f"解密耗时 {end_time - start_time:.2f} 秒")


if __name__ == '__main__':
    wx_chat = WxChat()
    wx_chat.get_data()
    wx_chat.data_to_excel('chat.jsonl')
    wx_chat.chat_data('chat.xlsx')
