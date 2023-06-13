import pandas as pd
import subprocess


def get_file(msgtype, ext, file=0):
    # 读取Excel文件
    df = pd.read_excel(f'chat_{msgtype}.xlsx', header=0)

    # 遍历每一行，读取fileid和msdid字段并调用外部指令
    for index, row in df.iterrows():
        fileid = row['sdkfileid']
        msgid = row['msgid']
        if file == 1:
            ext = row['fileext']
        path = f'data/{msgtype}/{msgid}.{ext}'
        subprocess.run(['./sdktools', '2', fileid, path])


# 调用函数，传入文件类型和扩展名
# 图片
get_file('image', 'jpg')
# 语音
get_file('voice', 'amr')
# 视频
get_file('video', 'mp4')
# 文件
get_file('file', file=1)
# 通话
get_file('call', 'mp3')