import socket
import rsa


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
with open('./ca_key/public_key.pem') as f:
    ca_public_key = rsa.PublicKey.load_pkcs1(f.read().encode())
with open('./certification/hash.pem','rb') as f:
    hash=f.read()
with open('./certification/signature.pem','rb') as f:
    signature=f.read()
# 使用公钥验证数字签名
if rsa.verify(hash, signature, ca_public_key):
    print('签名验证成功')
    communication()
else:
    print('签名验证失败！')









# server_ca_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_ca_socket.connect(('localhost', 8080))
# # 接收root_ca发来的hash与signature
# hash = server_ca_socket.recv(1024)
# signature = server_ca_socket.recv(1024)
#public_root_ca_key = server_ca_socket.recv(1024)

# # 使用公钥验证数字签名
# if rsa.verify(hash, signature, public_root_ca_key):
#     server_ca_socket.close()
#     print(f'签名验证成功: {signature.decode()}')
#     # 创建一个线程对象
#     thread = threading.Thread(target=communication)
#     # 启动线程
#     thread.start()
#     # 等待线程结束
#     thread.join()
#     print('Child thread finished')
#
# else:
#     print('签名验证失败！')
#     server_ca_socket.close()
