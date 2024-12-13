import os
import pandas as pd


def merge_excel_files():
    # 获取当前目录下所有以merge开头的xlsx文件
    file_list = [
        f for f in os.listdir()
        if f.startswith('merge') and f.endswith('.xlsx')
    ]
    if not file_list:
        print('No files to merge.')
        return

    # 创建一个空的DataFrame
    df = pd.DataFrame()

    # 循环读取每个Excel文件并合并到df中
    for file in file_list:
        # 读取Excel文件
        temp_df = pd.read_excel(file, engine='openpyxl')
        # 合并到df中
        df = pd.concat([df, temp_df])

    # 去重
    df.drop_duplicates(inplace=True)

    # 保存到新的Excel文件中
    df.to_excel('Merged.xlsx', index=False)
    print('Files merged successfully.')


if __name__ == '__main__':
    merge_excel_files()
