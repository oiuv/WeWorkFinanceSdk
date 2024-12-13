import os
import shutil
import datetime

# 获取今天的日期，格式为YYYYMMDD
today = datetime.datetime.today().strftime('%Y%m%d')

# 在data目录下新建以今天日期为名称的目录
dir_path = os.path.join('data', today)
os.makedirs(dir_path, exist_ok=True)

# 获取当前目录下所有扩展名为.xlsx和.jsonl的文件路径
files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.jsonl'))]

# 将这些文件移动到新建的目录中
for file in files:
    shutil.move(file, os.path.join(dir_path, file))
