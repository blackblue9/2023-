from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QDialog
from PyQt5.QtGui import *
from sender_base_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from client_send import client_send
from client_send import verify_certification
import socket
import rsa
from cerficate_false_dialog import Ui_Dialog


class DetailUI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(DetailUI, self).__init__()
        self.cericate_dialog = None
        self.setupUi(self)
        self.setWindowTitle("Sender")
        self.client_message = ''
        self.server_message = ''
        self.textbrowser_message = ''
        self.verify_info = False
        self.client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_server_socket.connect(('localhost', 8000))
        self.public_key_data = self.client_server_socket.recv(1024)

        ###验证签名
        self.verify_message = verify_certification()
        if self.verify_message == '签名验证成功':
            self.verify_info = True
            self.cericate_dialog = childWindow()
            self.cericate_dialog.child.textBrowser.setText('签名验证成功')
            self.cericate_dialog.show()
    def client_send_message_btn(self):
        self.client_message = self.plainTextEdit.toPlainText()
        self.plainTextEdit.setPlainText('')
        # print(self.client_message)
        self.textbrowser_message += '已发送消息:' + self.client_message + '\n'
        self.textBrowser.setText(self.textbrowser_message)
        # print('client_send_message')

        message = self.client_message.encode()
        # print('message', message)

        ###如果已经验证过签名且通过验证，则直接发送，否则弹出报错窗口
        if self.verify_info:
            server_public_key = rsa.PublicKey.load_pkcs1(self.public_key_data)
            encrypted_message = rsa.encrypt(message, server_public_key)
            # 发送加密后的消息给receiver
            # print(encrypted_message)
            self.client_server_socket.sendall(encrypted_message)
        else:
            self.cericate_dialog = childWindow()
            self.cericate_dialog.show()

    def runModel(self):
        pass


###验签错误子窗口
class childWindow(Ui_Dialog, QDialog):
    def __init__(self):
        #super(Ui_Dialog, self).__init__()
        QDialog.__init__(self)
        self.child = Ui_Dialog()  # 子窗口的实例化
        self.child.setupUi(self)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ex = DetailUI()
    ex.show()
    sys.exit(app.exec_())
