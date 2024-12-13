import argparse
import json
import pandas as pd
import time
from tqdm import tqdm
from decrypt import decrypt_data


class Data2Excel:

    def __init__(self, file_name):
        self.file_name = file_name

    def load_data(self):
        df = pd.DataFrame()
        with open(self.file_name, 'r') as f:
            for line in f:
                data = json.loads(line)
                df = pd.concat([df, pd.DataFrame.from_records(data['chatdata'])])
        return df

    def drop_duplicates(self, df):
        df.drop_duplicates(subset=['seq'], inplace=True)
        return df

    def decrypt_random_key(self, df):
        tqdm.pandas(desc="Decrypting random key")
        df['encrypt_key'] = df['encrypt_random_key'].progress_apply(decrypt_data)
        return df

    def save_to_excel(self, df):
        file_prefix = self.file_name.split('.')[0]
        df.to_excel(f"{file_prefix}.xlsx", index=False)

    def run(self):
        start_time = time.time()
        print(f"开始加载文件{self.file_name}……💕")
        df = self.load_data()
        print(df)
        print("开始数据去重处理……💕")
        df = self.drop_duplicates(df)
        print("开始解密随机密钥……💕")
        df = self.decrypt_random_key(df)
        print("数据存档中……💕")
        self.save_to_excel(df)
        print(df)
        end_time = time.time()
        print(f"数据预处理耗时 {end_time - start_time:.2f} 秒")


# 使用示例
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='读取JSONL格式的原始会话记录并处理后转存为Excel文件')
    parser.add_argument('file_name', nargs='?', default='chat.jsonl', help='JSONL格式会话记录文件，如：chat.jsonl')
    args = parser.parse_args()
    data2excel = Data2Excel(args.file_name)
    data2excel.run()
