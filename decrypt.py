import sys
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher


# 从文件中读取密钥
def get_key(key_file):
    with open(key_file) as f:
        data = f.read()
        key = RSA.import_key(data)
    return key


# 使用公钥加密消息
def encrypt_data(msg):
    public_key = get_key('public.pem')
    # 使用 PKCS#1 v1.5 方式进行加密
    cipher = PKCS1_cipher.new(public_key)
    # 将消息进行 UTF-8 编码并加密
    encrypted_msg = cipher.encrypt(msg.encode("utf-8"))
    # 对加密后的消息进行 Base64 编码
    encrypted_text = base64.b64encode(encrypted_msg).decode('utf-8')
    return encrypted_text


# 使用私钥解密消息
def decrypt_data(encrypt_msg):
    private_key = get_key('private.pem')
    # 使用 PKCS#1 v1.5 方式进行解密
    cipher = PKCS1_cipher.new(private_key)
    # 对加密的消息进行 Base64 解码并解密
    decrypted_msg = cipher.decrypt(base64.b64decode(encrypt_msg),
                                   None).decode('utf-8')
    return decrypted_msg


if __name__ == '__main__':
    # 检查命令行参数
    if len(sys.argv) < 3:
        print("Usage: python decrypt.py [command] [message]")
        print("Available commands: enc, dec")
        sys.exit(1)

    # 获取命令行参数
    command = sys.argv[1]
    message = sys.argv[2]

    # 根据命令行参数选择加密或解密
    if command == "enc":
        encrypted_text = encrypt_data(message)
        print("Encrypted Message:", encrypted_text)

    elif command == "dec":
        decrypted_text = decrypt_data(message)
        print("Decrypted Message:", decrypted_text)

    else:
        print("Invalid command")
        sys.exit(1)
