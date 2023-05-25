import pandas as pd
import subprocess

# 读取Excel文件
df = pd.read_excel('chatdata.xlsx', engine='openpyxl')

# 获取decrypt_random_key和encrypt_chat_msg列的数据
decrypt_random_key = df['decrypt_random_key'].tolist()
encrypt_chat_msg = df['encrypt_chat_msg'].tolist()

# 构造指令
cmd = ['./sdktools', '3']

for i in range(len(decrypt_random_key)):
    # 将decrypt_random_key和encrypt_chat_msg列中的数据依次传递给指令
    subprocess.run(cmd + [decrypt_random_key[i], encrypt_chat_msg[i]], stdout=subprocess.PIPE)

# 打印输出结果
print('数据处理完成 ✔')