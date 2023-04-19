import rsa

# 从文件中加载公钥和私钥
with open('./rsa_key_server/public_key.pem', 'rb') as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

with open('./rsa_key_server/private_key.pem', 'rb') as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

print(f'Server public key: {public_key}')
print(f'Server private key: {private_key}')