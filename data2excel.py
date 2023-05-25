import json
import pandas as pd
import sys

# 获取命令行参数中的文件名
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    print("请指定要读取的 JSONL 文件名。")
    sys.exit()

# 创建一个空的 DataFrame
df = pd.DataFrame()

# 打开 JSONL 文件，并逐行读取数据
with open(file_name, 'r') as f:
    for line in f:
        # 将 JSON 字符串转换为 Python 对象
        data = json.loads(line)
        # 将 chatdata 字段中的数据添加到 DataFrame 中
        df = pd.concat([df, pd.DataFrame.from_records(data['chatdata'])])

# 输出 JSONL 文件中的最后一个数据
print(json.dumps(data['chatdata'][-1], indent=4))

# 去重
df.drop_duplicates(inplace=True)

# 将 DataFrame 写入 Excel 文件
file_prefix = file_name.split('.')[0]
df.to_excel(f"{file_prefix}.xlsx", index=False)

# 输出 DataFrame
print(df)