import hashlib, socket
import rsa_all as rsa
import threading


# 与服务端进行验证
def verification():
    # 处理服务端的请求
    # 创建socket对象
    root_ca_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    root_ca_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 监听端口   最多一个
    root_ca_socket.bind(('localhost', 9000))
    root_ca_socket.listen(1)
    # 等待服务端连接
    (server_socket, address) = root_ca_socket.accept()
    print("server connected...")
    # 将hash与signature发送给服务端，供其验证客户端身份
    server_socket.sendall(hash)
    server_socket.sendall(signature)
    # 发送root_ca的公钥
    server_socket.sendall(pubkey)

    # Verifying the signature using the public key
    print(rsa.verify(hash, signature, pubkey))


# socket setting
# 创建socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 监听端口
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

# 等待客户端连接
(client_socket, address) = server_socket.accept()
print("client connected...")
# Generating public and private keys
(pubkey, privkey) = rsa.newkeys(512)

#保存ca的公钥私钥
with open('ca_key/public_key.pem', 'w') as f:
    f.write(pubkey.save_pkcs1().decode())

with open('ca_key/private_key.pem', 'w') as f:
    f.write(privkey.save_pkcs1().decode())

# 读取客户端的公钥
with open('./rsa_key_client/public_key.pem', 'rb') as f:
    client_public_key = str(rsa.PublicKey.load_pkcs1(f.read()))
print(client_public_key)
# 根CA用自己的私钥对客户端公钥数字签名
# Creating a message to be signed   b代表byte    str--->bytes : str.encode()
message = client_public_key.encode()

# Hashing the message using SHA-256
hash = hashlib.sha256(message).digest()

# Signing the hash using the private key
signature = rsa.sign(hash, privkey, 'SHA-256')
with open('./certification/signature.pem', 'wb') as f:
    f.write(signature)
with open('./certification/hash.pem', 'wb') as f:
    f.write(hash)


##############################################
# # 创建一个线程对象
# thread = threading.Thread(target=verification)
# # 启动线程
# thread.start()
# # 等待线程结束
# thread.join()
# print('Child thread finished')
