import pandas as pd
from decrypt import decrypt_data


def merge_excel_files(excel_files):
    # 创建一个空的DataFrame
    df = pd.DataFrame()

    # 循环读取每个Excel文件并合并到df中
    for file in excel_files:
        # 读取Excel文件
        temp_df = pd.read_excel(file, engine='openpyxl')
        # 合并到df中
        df = pd.concat([df, temp_df])

    # 去重
    df.drop_duplicates(inplace=True)

    # 解密随机密钥
    df['decrypt_random_key'] = df['encrypt_random_key'].apply(decrypt_data)

    # 保存到新的Excel文件中
    df.to_excel('chatdata.xlsx', index=False)


if __name__ == '__main__':
    # 定义要合并的Excel文件名列表
    merge_excel_files(['chat.xlsx'])
