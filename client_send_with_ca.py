import socket
import rsa


# 与服务端进行通信
def communication(socket):
    socket.connect(('localhost', 8000))
    # 接收服务端发送的公钥
    public_key_data = socket.recv(1024)
    # 如果服务端验证成功
    # 加载服务端公钥
    server_public_key = rsa.PublicKey.load_pkcs1(public_key_data)
    # 加密消息并生成数字签名
    message = b'Hello, server!'
    encrypted_message = rsa.encrypt(message, server_public_key)
    # 发送加密后的消息给服务端
    socket.sendall(encrypted_message)


# 创建socket对象
client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 如果签名认证成功进行接下来的操作
communication(client_server_socket)
# 关闭socket
client_server_socket.close()
