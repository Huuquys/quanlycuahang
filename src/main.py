import sys
import conn

from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from conn import Myconnection, CloseConnection
from PyQt6.QtCore import QResource, QCoreApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QApplication
from qldvsx import sanxuat_w
from qldvpp import phanphoi_w
from qlsp import sanpham_w
from qlbh import banhang_w
from qlnv import nhanvien_w
from thongke import thongke_w


class Main(QMainWindow):
    sx = QtCore.pyqtSignal()
    pp = QtCore.pyqtSignal()
    sp = QtCore.pyqtSignal()
    bh = QtCore.pyqtSignal()
    nv = QtCore.pyqtSignal()
    thongke = QtCore.pyqtSignal()
    logout = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('view/trangchu.ui', self)
        
        
        # Tạo một QPixmap từ đường dẫn tương đối hoặc đường dẫn tuyệt đối của ảnh
        pixmap = QPixmap("view/nuoc-ngot-co-ga-1.jpg")  # Đường dẫn tới ảnh của bạn
        # Đặt ảnh vào QLabel
        self.label.setPixmap(pixmap)
        # Điều chỉnh kích thước ảnh để phù hợp với QLabel
        pixmap = pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        # Hiển thị QLabel
        self.label.show()

        # Tạo sự kiện cho các nút trong form
        self.btn_dx.clicked.connect(self.Exit)
        self.btn_index_qldvsx.clicked.connect(self.sanxuat_w)
        self.btn_index_qldvpp.clicked.connect(self.phanphoi_w)
        self.btn_index_qlsp.clicked.connect(self.sanpham_w)
        self.btn_index_qlbh.clicked.connect(self.banhang_w)
        self.btn_index_qlnv.clicked.connect(self.nhanvien_w)
        self.btn_index_thongke.clicked.connect(self.thongke_w)
        
        
        
        
        
        
        
        
        
        
        
    # các hàm(def) sự kiện
    def Exit(self):
        select_option = QMessageBox.warning(self, "Exit", "Bạn có muốn đăng xuất không?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if(select_option == QMessageBox.StandardButton.Yes):
            self.close()
            self.logout.emit()
           
           
    
    def sanxuat_w(self):
            self.qldvsx_window = sanxuat_w()
            self.qldvsx_window.show()
            self.sx.emit()
    def phanphoi_w(self):
            self.qldvpp_window = phanphoi_w()
            self.qldvpp_window.show()
            self.pp.emit()
    def sanpham_w(self):
            self.qlsp_window = sanpham_w()
            self.qlsp_window.show()
            self.sp.emit()
    def banhang_w(self):
            self.qlbh_window = banhang_w()
            self.qlbh_window.show()
            self.bh.emit()
    def nhanvien_w(self):
            self.qlnv_window = nhanvien_w()
            self.qlnv_window.show()
            self.nv.emit()
    def thongke_w(self):
            self.thongke_window = thongke_w()
            self.thongke_window.show()
            self.thongke.emit()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec())
    

    
        
