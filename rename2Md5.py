import os
import hashlib

def calculate_md5(file_path):
    """计算文件的MD5哈希值"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buffer = f.read()
        hasher.update(buffer)
    return hasher.hexdigest()

def rename_files_with_md5(directory):
    """将指定目录中的文件重命名为其MD5哈希值"""
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                # 计算文件的MD5哈希值
                md5_hash = calculate_md5(file_path)
                # 获取文件扩展名
                _, file_extension = os.path.splitext(filename)
                # 构造新文件名（MD5哈希值 + 扩展名）
                new_filename = md5_hash + file_extension
                # 新文件路径
                new_file_path = os.path.join(root, new_filename)
                # 如果新文件已存在，则删除原始文件
                if os.path.exists(new_file_path):
                    os.remove(file_path)
                    print(f"Deleted duplicate file: {file_path}")
                else:
                    # 否则，重命名文件为MD5哈希值
                    os.rename(file_path, new_file_path)
                    print(f"Renamed file: {file_path} -> {new_file_path}")

# 指定要处理的目录
directory = 'data/file'
# 调用函数来重命名文件
rename_files_with_md5(directory)
