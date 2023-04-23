import os
from PyQt5.QtCore import QDir, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QDialog
from PyQt5.QtGui import *
from receiver import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import socket
import rsa
import threading


class DetailUI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(DetailUI, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Receiver")
        self.client_message = ''
        self.server_message = ''
        self.textbrowser_message = ''

        ##这块是尝试用普通子线程，后续有问题，故下文采用qthread子线程才能在子线程更新ui
        # self.client_th = threading.Thread(target=self.tcp_client_concurrency)
        # self.client_th.setDaemon(True)
        # self.client_th.start()
        # self.textBrowser.setText(self.textbrowser_message)

        ###开启子线程循环接收sender消息
        self.client_th = Mythread()
        self.client_th.breakSignal.connect(self.update_browser)
        self.client_th.start()

    # 用来更新主界面UI的函数，与子线程绑定
    def update_browser(self, str):
        self.textBrowser.setText(str)

    # 暂时没用
    def tcp_client_concurrency(self):
        # 如果签名认证成功进行接下来的操作
        # 创建socket对象
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 监听端口
        server_socket.bind(('localhost', 8000))
        server_socket.listen(1)
        # 等待sender连接
        (client_socket, address) = server_socket.accept()
        print("sender connected...")
        # 发送公钥给客户端
        client_socket.sendall(self.public_key.save_pkcs1())
        client_socket.sendall(self.private_key.save_pkcs1())

        while 1:
            # 接收客户端发送的加密后的消息
            encrypted_message = client_socket.recv(1024)
            # 使用私钥解密消息
            decrypted_message = rsa.decrypt(encrypted_message, self.private_key).decode()
            print('解密Sender发送的消息为：' + decrypted_message)
            self.textbrowser_message += '来自Sender的消息:' + decrypted_message + '\n'

    def runModel(self):
        pass


###更新主界面text browser的线程类
class Mythread(QThread):
    # 定义信号,定义参数为str类型
    breakSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # 下面的初始化方法都可以，有的python版本不支持
        #  super(Mythread, self).__init__()

    def run(self):
        # sender已经发送的消息列表
        textbrowser_message = ''

        # 生成一对公钥和私钥
        (self.public_key, self.private_key) = rsa.newkeys(512)
        # 保存为OpenSSL格式
        with open('./rsa_key_server/public_key.pem', 'w') as f:
            f.write(self.public_key.save_pkcs1().decode())

        with open('./rsa_key_server/private_key.pem', 'w') as f:
            f.write(self.private_key.save_pkcs1().decode())
        # 显示公钥和私钥
        print(f'Server public key: {self.public_key}')
        print(f'Server private key: {self.private_key}')

        # 创建socket对象，等待sender连接8000端口进行通信
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 监听8000端口
        server_socket.bind(('localhost', 8000))
        server_socket.listen(1)
        # 等待sender连接
        (client_socket, address) = server_socket.accept()
        print("sender connected...")
        # 发送公钥给sender
        client_socket.sendall(self.public_key.save_pkcs1())
        client_socket.sendall(self.private_key.save_pkcs1())

        # 死循环，不断接收sender方发送的消息，并且用自己的私钥解密，然后利用槽变量把消息列表发送给主线程，在主线程中更新UI界面
        while 1:
            # 接收sender发送的加密后的消息
            encrypted_message = client_socket.recv(1024)
            # 使用私钥解密消息
            decrypted_message = rsa.decrypt(encrypted_message, self.private_key).decode()
            print('解密Sender发送的消息为：' + decrypted_message)
            textbrowser_message += '来自Sender的消息:' + decrypted_message + '\n'

            # 发送消息至主线程
            self.breakSignal.emit(textbrowser_message)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ex = DetailUI()
    ex.show()
    sys.exit(app.exec_())
