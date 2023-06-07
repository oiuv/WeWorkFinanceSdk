import json
import pandas as pd


def process_chat_data(file_name, encoding='utf-8'):
    # 打开 JSONL 文件，并逐行读取数据
    print(f"开始加载文件{file_name}……💕")
    with open(file_name, 'r', encoding=encoding) as f:
        # 定义一个空列表用于存储数据
        data_list = []
        data_text = []
        data_image = []
        data_voice = []
        data_video = []
        data_file = []
        data_call = []

        for line in f:
            try:
                # 将 JSON 字符串转换为 Python 对象
                data = json.loads(line)
            except json.JSONDecodeError:
                # 如果不是有效的 JSON 数据，则跳过该行
                continue

            # 判断 action 是否为 send
            if data.get('action') == 'send':
                # 选择需要的字段
                selected_data = {
                    'msgid': data['msgid'],
                    'from': data['from'],
                    'tolist': '|'.join(data['tolist']),
                    'msgtime': data['msgtime'],
                    'msgtype': data['msgtype']
                }

                # 将选择的数据添加到列表中
                data_list.append(selected_data)

                # 处理不同类型数据
                if data.get('msgtype') == 'text':
                    selected_data = {
                        'msgid': data['msgid'],
                        'content': data['text']['content']
                    }
                    data_text.append(selected_data)
                if data.get('msgtype') == 'image':
                    selected_data = {
                        'msgid': data['msgid'],
                        'md5sum': data['image']['md5sum'],
                        'filesize': data['image']['filesize'],
                        'sdkfileid': data['image']['sdkfileid']
                    }
                    data_image.append(selected_data)
                if data.get('msgtype') == 'voice':
                    selected_data = {
                        'msgid': data['msgid'],
                        'md5sum': data['voice']['md5sum'],
                        'voice_size': data['voice']['voice_size'],
                        'play_length': data['voice']['play_length'],
                        'sdkfileid': data['voice']['sdkfileid']
                    }
                    data_voice.append(selected_data)
                if data.get('msgtype') == 'video':
                    selected_data = {
                        'msgid': data['msgid'],
                        'md5sum': data['video']['md5sum'],
                        'filesize': data['video']['filesize'],
                        'play_length': data['video']['play_length'],
                        'sdkfileid': data['video']['sdkfileid']
                    }
                    data_video.append(selected_data)
                if data.get('msgtype') == 'file':
                    selected_data = {
                        'msgid': data['msgid'],
                        'md5sum': data['file']['md5sum'],
                        'filename': data['file']['filename'],
                        'fileext': data['file']['fileext'],
                        'filesize': data['file']['filesize'],
                        'sdkfileid': data['file']['sdkfileid']
                    }
                    data_file.append(selected_data)
                if data.get('msgtype') == 'meeting_voice_call':
                    selected_data = {
                        'msgid': data['msgid'],
                        'voiceid': data['voiceid'],
                        'endtime': data['meeting_voice_call']['endtime'],
                        'sdkfileid': data['meeting_voice_call']['sdkfileid']
                    }
                    data_call.append(selected_data)

    # 创建空的 DataFrame
    df = pd.DataFrame()

    # 将列表转换为 pandas DataFrame 格式
    df = pd.DataFrame(data_list)

    # 去重
    df.drop_duplicates(inplace=True)

    # 将 DataFrame 写入 Excel 文件
    write_to_excel(df, "chat_list.xlsx", 'list')

    # 定义消息类型
    msg_types = ['text', 'image', 'voice', 'video', 'file', 'call']

    for type in msg_types:
        # 获取相应类型的数据
        data = locals()[f"data_{type}"]

        # 创建 DataFrame
        df = pd.DataFrame(data)

        # 去重
        df.drop_duplicates(inplace=True)

        # 将 DataFrame 写入 Excel 文件
        write_to_excel(df, f"chat_{type}.xlsx", type)

        # 打印结果
        print(f'chat_{type}.xlsx 已保存 ✔')


def write_to_excel(df, file_name, sheet_name):
    # 将 DataFrame 写入 Excel 文件
    with pd.ExcelWriter(file_name) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)


if __name__ == '__main__':
    process_chat_data('chatdata.jsonl')
