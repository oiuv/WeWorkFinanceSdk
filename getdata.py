import os
import json

# 从文件读取起始 seq
try:
    with open('seq.txt', 'r') as f:
        seq = int(f.read().strip())
except FileNotFoundError:
    seq = 0

# 定义拉取数据的参数
limit = 1000  # 每次拉取数据的条数
seq = seq // limit * limit

# 循环拉取数据
while True:
    # 执行拉取数据的命令
    cmd = f"./sdktools 1 {seq} {limit}"
    os.system(cmd)

    # 读取本地文件中的数据
    with open('chat.jsonl', 'r') as f:
        lines = f.readlines()

    # 解析最后一行数据
    last_line = lines[-1].strip()  # 读取最后一行数据
    last_data = json.loads(last_line)['chatdata']  # 解析最后一行数据中的 chatdata 字段

    # 更新 seq 参数，准备拉取下一批数据
    seq = last_data[-1]['seq']  # 获取最后一条数据的 seq，作为下一次拉取数据的起始 seq

    # 输出拉取进度，显示已拉取多少 seq
    print(f"当前拉取进度：第 {seq} 条数据 ✔")

    # 如果拉取到的数据不足 1000 条，则退出循环
    if len(last_data) < limit:
        break

# 存储最终的 seq 值到文件中
with open('seq.txt', 'w') as f:
    f.write(str(seq))
