import socket
import rsa
import os


# 与客户端进行通信
def communication():
    # 创建socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 监听端口
    server_socket.bind(('localhost', 8000))
    server_socket.listen(1)
    # 等待客户端连接
    (client_socket, address) = server_socket.accept()
    print("client connected...")
    # 发送公钥给客户端
    client_socket.sendall(public_key.save_pkcs1())
    client_socket.sendall(private_key.save_pkcs1())
    # 接收客户端发送的加密后的消息
    encrypted_message = client_socket.recv(1024)
    # 使用私钥解密消息
    decrypted_message = rsa.decrypt(encrypted_message, private_key).decode()
    print('解密客户端发送的消息为：' + decrypted_message)
    # 关闭socket
    client_socket.close()
    server_socket.close()


# 生成一对公钥和私钥
(public_key, private_key) = rsa.newkeys(512)
# 保存为OpenSSL格式
with open('./rsa_key_server/public_key.pem', 'w') as f:
    f.write(public_key.save_pkcs1().decode())

with open('./rsa_key_server/private_key.pem', 'w') as f:
    f.write(private_key.save_pkcs1().decode())
# 显示公钥和私钥
print(f'Server public key: {public_key}')
print(f'Server private key: {private_key}')

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
    exit()
if os.path.isfile('./certification/signature.pem'):
    with open('./certification/signature.pem', 'rb') as f:
        signature = f.read()
else:
    print('此用户没有数字签名,不可进行通信')
    exit()
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
    communication()
else:
    print('签名验证失败！请在根CA注册公钥证书')

