import sys
import conn
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from conn import Myconnection, CloseConnection
from main import Main

db = Myconnection()
cur = db.cursor()

#Cửa sổ Login
class Login_w(QMainWindow):
    login_success = QtCore.pyqtSignal()
    def __init__(self):
        super(Login_w, self).__init__()
        uic.loadUi('view/logindemo.ui', self)
        
        
        self.btn_thoat_login.clicked.connect(self.Exit)
        self.btn_dn.clicked.connect(self.login)
        
        self.fix()
        
    
    # Đăng nhập        
    def login(self):
        username = self.txt_tk.text()
        password = self.txt_mk.text()
        
        cur.execute("Select * from login where taikhoan = %s AND matkhau = %s" , (username, password) )
        
        kt=cur.fetchone()
        if kt:
            #QMessageBox.information(self, "đăng nhập", "Thành công.")
            self.main_window = Main()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.information(self, "Lỗi đăng nhập", "Tài khoản hoặc mật khẩu không đúng.")
        
    # các hàm(def) sự kiện
    def Exit(self):
        select_option = QMessageBox.warning(self, "Exit", "Bạn có muốn thoát không?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if(select_option == QMessageBox.StandardButton.Yes):
            self.close()
            self.logout.emit()
        
    def fix(self):
        #fix ưindow
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
#xử lý
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    login_window = Login_w()
    login_window.show()
    sys.exit(app.exec())
    
    

    
