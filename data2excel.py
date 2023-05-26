import argparse
import json
import pandas as pd
import time
from tqdm import tqdm
from decrypt import decrypt_data

# 解析命令行参数
parser = argparse.ArgumentParser(description='读取JSONL格式的原始会话记录并处理后转存为Excel文件')
parser.add_argument('file_name', help='JSONL格式会话记录文件，如：chat.jsonl')
args = parser.parse_args()

# 统计代码运行时间
start_time = time.time()

# 创建一个空的 DataFrame
df = pd.DataFrame()

# 打开 JSONL 文件，并逐行读取数据
print(f"开始加载文件{args.file_name}……💕")
with open(args.file_name, 'r') as f:
    for line in f:
        # 将 JSON 字符串转换为 Python 对象
        data = json.loads(line)
        # 将 chatdata 字段中的数据添加到 DataFrame 中
        df = pd.concat([df, pd.DataFrame.from_records(data['chatdata'])])

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
file_prefix = args.file_name.split('.')[0]
df.to_excel(f"{file_prefix}.xlsx", index=False)

# 输出 DataFrame
print(df)

# 输出代码运行时间
end_time = time.time()
print(f"代码运行时间为 {end_time - start_time:.2f} 秒")
