import socket
import rsa
import threading


# 与服务端进行通信
def communication():
    client_server_socket.connect(('localhost', 8000))
    # 接收服务端发送的公钥
    public_key_data = client_server_socket.recv(1024)
    # 如果服务端验证成功
    # 加载服务端公钥
    server_public_key = rsa.PublicKey.load_pkcs1(public_key_data)
    # 加密消息并生成数字签名
    message = b'Hello, server!'
    encrypted_message = rsa.encrypt(message, server_public_key)
    # 发送加密后的消息给服务端
    client_server_socket.sendall(encrypted_message)


# 生成一对公钥和私钥
(public_key, private_key) = rsa.newkeys(512)
# 保存为OpenSSL格式
with open('./rsa_key_client/public_key.pem', 'w') as f:
    f.write(public_key.save_pkcs1().decode())

with open('./rsa_key_client/private_key.pem', 'w') as f:
    f.write(private_key.save_pkcs1().decode())

# 创建socket对象（2个）
client_root_ca_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接服务器
client_root_ca_socket.connect(('localhost', 8080))
# 如果签名认证成功进行接下来的操作


# 关闭socket
client_root_ca_socket.close()
client_server_socket.close()
