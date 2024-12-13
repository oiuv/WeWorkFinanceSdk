import pandas as pd
import subprocess
import time

import os
import shutil
import datetime

def get_file(msgtype, ext, file=0):
    try:
        # 读取Excel文件
        df = pd.read_excel(f'chat_{msgtype}.xlsx', header=0)
    except FileNotFoundError as e:
        print(f"文件 {f'chat_{msgtype}.xlsx'} 不存在。错误信息: {e}")
        return  # 直接返回，不执行后续代码

    # 遍历每一行，读取fileid和msdid字段并调用外部指令
    for index, row in df.iterrows():
        fileid = row['sdkfileid']
        # 根据msgtype设置filename  
        if msgtype == 'call':
            filename = row['voiceid']
        else:  
            filename = row['md5sum']
        if file == 1:
            ext = row['fileext']
        path = f'data/{msgtype}/{filename}.{ext}'
        # 检查文件是否已存在  
        if os.path.exists(path):  
            print(f"文件已存在: {path}")  
        else:  
            # 调用外部指令  
            subprocess.run(['./sdktools', '2', fileid, path])


# 统计代码运行时间
start_time = time.time()
# 调用函数，传入文件类型和扩展名
# 图片
get_file('image', 'jpg')
print('图片消息存档完成 🧡')
# 语音
get_file('voice', 'amr')
print('语音消息存档完成 💛')
# 视频
get_file('video', 'mp4')
print('视频消息存档完成 💚')
# 文件
get_file('file', '', file=1)
print('文件消息存档完成 💙')
# 通话
get_file('call', 'mp3')
print('通话消息存档完成 💜')
# 输出代码运行时间
end_time = time.time()
print(f"获取资源耗时 {end_time - start_time:.2f} 秒")

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
