import sys
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi

from qldvsx import sanxuat_w
from qldvpp import phanphoi_w
from qlsp import sanpham_w
from qlbh import banhang_w
from qlnv import nhanvien_w
from thongke import thongke_w
from login import Login_w
from main import Main


class control(QMainWindow):
    def __init__(self):
        super().__init__()

        # Đưa form (Widgets) vào biến tương ứng
        self.login_window = Login_w()
        self.main_window = Main()
        self.qldvsx_window = sanxuat_w()
        self.qldvpp_window = phanphoi_w()
        self.qlsp_window = sanpham_w()
        self.qlbh_window = banhang_w()
        self.qlnv_window = nhanvien_w()
        self.thongke_window = thongke_w()
        
        # Tạo sự kiện cho các nút trong form main
        self.login_window.login_success.connect(self.main)
        self.main_window.logout.connect(self.login)
        self.main_window.sx.connect(self.qldvsx)
        self.main_window.pp.connect(self.qldvpp)
        self.main_window.sp.connect(self.qlsp)
        self.main_window.bh.connect(self.qlbh)
        self.main_window.nv.connect(self.qlnv)
        self.main_window.thongke.connect(self.thongke)
        
        # Tạo sự kiện cho nút Thoát trong các form tương ứng
        self.qldvsx_window.sx.connect(self.back_main)
        self.qldvpp_window.pp.connect(self.back_main)
        self.qlsp_window.sp.connect(self.back_main)
        self.qlbh_window.bh.connect(self.back_main)
        self.qlnv_window.nv.connect(self.back_main)
        self.thongke_window.thongke.connect(self.back_main)
        
    def login(self):
        self.main_window.close()
        self.login_window.show() 
    
    def main(self):
        #self.login_window.close()
        self.main_window.show()

    def qldvsx(self):
        #self.main_window.close()
        self.qldvsx_window.show()
    
    def qldvpp(self):
        #self.main_window.close()
        self.qldvpp_window.show()
        
    def qlsp(self):
        #self.main_window.close()
        self.qlsp_window.show()

    def qlbh(self):
        #self.main_window.close()
        self.qlbh_window.show()
        
    def qlnv(self):
        #self.main_window.close()
        self.qlnv_window.show()
        
    def thongke(self):
        #self.main_window.close()
        self.thongke_window.show()
        
    def back_main(self):
        self.main_window.show()
        self.qldvsx_window.close()
        self.qldvpp_window.close()
        self.qlsp_window.close()
        self.qlbh_window.close()
        self.qlnv_window.close()
        self.thongke_window.close()
        self.main_window.show()
        
 
# MAIN   
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    control_window = control()
    control_window.login()
    sys.exit(app.exec())