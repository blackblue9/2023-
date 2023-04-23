import os
import socket
import rsa

# # 创建socket对象
# client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_server_socket.connect(('localhost', 8000))
# # 接收服务端发送的公钥
# public_key_data = client_server_socket.recv(1024)
# # 如果服务端验证成功
# # 加载服务端公钥
# server_public_key = rsa.PublicKey.load_pkcs1(public_key_data)
# # 加密消息并生成数字签名
# message = b'Hello, server!'
# encrypted_message = rsa.encrypt(message, server_public_key)
# # 发送加密后的消息给服务端
# client_server_socket.sendall(encrypted_message)

def client_send(client_server_socket, msg, server_public_key):
    # if not TelnetPort('localhost', 8000):
    #     # 创建socket对象
    #     client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     client_server_socket.connect(('localhost', 8000))

    # client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_server_socket.connect(('localhost', 8000))
    # 接收服务端发送的公钥
    # public_key_data = client_server_socket.recv(1024)
    # 如果服务端验证成功
    # 加载服务端公钥
    # server_public_key = rsa.PublicKey.load_pkcs1(public_key_data)
    # 加密消息并生成数字签名
    # message = b'Hello, server222!'
    message = msg.encode()
    print('message', message)
    encrypted_message = rsa.encrypt(message, server_public_key)
    # 发送加密后的消息给服务端
    print(encrypted_message)
    client_server_socket.sendall(encrypted_message)

def verify_certification():
    ##################################################################
    # 处理根CA的事务
    if os.path.isfile('./ca_key/public_key.pem'):
        with open('./ca_key/public_key.pem') as f:
            ca_public_key = rsa.PublicKey.load_pkcs1(f.read().encode())
    if os.path.isfile('./certification/hash.pem'):
        with open('./certification/hash.pem', 'rb') as f:
            hash = f.read()
    else:
        print('此用户没有数字签名,不可进行通信')
        return '此用户没有数字签名,不可进行通信'
        #exit()
    if os.path.isfile('./certification/signature.pem'):
        with open('./certification/signature.pem', 'rb') as f:
            signature = f.read()
    else:
        print('此用户没有数字签名,不可进行通信')
        return '此用户没有数字签名,不可进行通信'
        #exit()
    # 使用公钥验证数字签名
    if rsa.verify(hash, signature, ca_public_key):
        print('签名验证成功')
        filename_hash = './certification/hash.pem'  # 文件名及路径
        filename_sig = './certification/signature.pem'
        try:
            os.remove(filename_hash)
            os.remove(filename_sig)
            print(f'{filename_hash, filename_sig}已经被成功删除')
        except OSError as e:
            print(f'删除失败：{e}')
        return '签名验证成功'
    else:
        print('签名验证失败！请在根CA注册公钥证书')
        return '签名验证失败！请在根CA注册公钥证书'