import socket
import rsa

# 生成一对公钥和私钥
(public_key, private_key) = rsa.newkeys(512)
# 保存为OpenSSL格式
with open('./rsa_key_client/public_key.pem', 'w') as f:
    f.write(public_key.save_pkcs1().decode())

with open('./rsa_key_client/private_key.pem', 'w') as f:
    f.write(private_key.save_pkcs1().decode())

# 创建socket对象
client_root_ca_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接根CA服务器
client_root_ca_socket.connect(('localhost', 8080))
# 关闭socket
client_root_ca_socket.close()

