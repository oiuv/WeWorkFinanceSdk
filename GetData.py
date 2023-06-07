import os
import json


class GetData:

    def __init__(self, seq_file='seq.txt', data_file='chat.jsonl', limit=1000):
        self.seq_file = seq_file
        self.data_file = data_file
        self.limit = limit

    def get_seq(self):
        try:
            with open(self.seq_file, 'r') as f:
                seq = int(f.read().strip())
        except FileNotFoundError:
            seq = 0
        return seq

    def update_seq(self, seq):
        with open(self.seq_file, 'w') as f:
            f.write(str(seq))

    def get_last_data(self):
        with open(self.data_file, 'r') as f:
            lines = f.readlines()
        last_line = lines[-1].strip()
        last_data = json.loads(last_line)['chatdata']
        return last_data

    def run(self):
        seq = self.get_seq() // self.limit * self.limit
        while True:
            cmd = f"./sdktools 1 {seq} {self.limit}"
            os.system(cmd)
            last_data = self.get_last_data()
            # 如果数据为空（无权访问）
            if not last_data:
                print("Get chatdata whiteip not match ❌")
                break
            seq = last_data[-1]['seq']
            print(f"当前拉取进度：第 {seq} 条数据 ✔")
            if len(last_data) < self.limit:
                break
        self.update_seq(seq)


# 使用示例
if __name__ == '__main__':
    get_data = GetData()
    get_data.run()
