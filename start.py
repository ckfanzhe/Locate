# Qt5窗口界面
# author:fanzhe date:8.22

import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from windows import Ui_Form
from Local_tools import get_link
from Locate import get_locate

class main_windows(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(main_windows, self).__init__()
        self.setFixedSize(439, 565)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_url)
        self.pushButton_2.clicked.connect(self.get_local)

    def get_url(self):
        key = self.check(0)
        if len(key)!=0:
            self.pushButton.setDisabled(True)
            self.logs = Get_url(key[0])
            self.logs.get_info.connect(self.handle)
            self.logs.start()

    def get_local(self):
        key = self.check(1)
        if len(key) != 0:
            # self.pushButton.setDisabled(True)
            self.logs = Get_local(key[0])
            self.logs.get_locals.connect(self.handle_1)
            self.logs.start()

    def handle(self,to_show):
        if to_show!='error':
            self.textEdit.setText(str(to_show[0]))
        else:
            self.textEdit.setText('秘钥错误或者已存在！')
            self.pushButton.setDisabled(False)

    def handle_1(self,show_local):
        if show_local!='error':
            self.textEdit_2.setText(str(show_local[0]))
        else:
            self.textEdit.setText('没有信息！')
            self.pushButton_2.setDisabled(False)

    def check(self, obj):
        if obj==0:
            key = self.lineEdit.text()  # 获取第一个文本框中的内容存入key
            if not len(str(key)):
                self.textEdit.setText('秘钥不能为空！')
                return []
            else:
                self.textEdit.setText('')
                return [key]
        elif obj==1:
            key = self.lineEdit_2.text()  # 获取第二个文本框中的内容存入key
            if not len(str(key)):
                self.textEdit_2.setText('秘钥不能为空！')
                return []
            else:
                self.textEdit_2.setText('')
                return [key]

class Get_url(QThread):
    # qt多线程,用于同一窗口执行其他高延迟的行为
    get_info = pyqtSignal(list)
    def __init__(self, key, parent=None):
        super(Get_url, self).__init__(parent)
        self.key = key

    # def __del__(self):  # 析构函数
    #     self.wait()

    def run(self):
        result = get_link(self.key, 1)
        self.get_info.emit(result)  # 传送结果

class Get_local(QThread):
    # qt多线程,用于同一窗口执行其他高延迟的行为
    get_locals = pyqtSignal(list)
    def __init__(self, key, parent=None):
        super(Get_local, self).__init__(parent)
        self.key = key

    # def __del__(self):  # 析构函数
    #     self.wait()
    def run(self):
        result = get_locate(self.key, 1)
        self.get_locals.emit(result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = main_windows()
    window.show()
    sys.exit(app.exec_())