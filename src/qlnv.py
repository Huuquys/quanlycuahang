import sys
import conn
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from conn import Myconnection, CloseConnection
db = Myconnection()
cur = db.cursor()

class nhanvien_w(QMainWindow):
    nv = QtCore.pyqtSignal()
    def __init__(self):
        super(nhanvien_w, self).__init__()
        uic.loadUi('view/qlnv.ui', self)
        
        # tableWidget
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tb_qlnv")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        #gọi hàm loaddata
        self.loaddata()
        self.btn_again.clicked.connect(self.loaddata)
        
        # Kết nối tín hiệu
        self.tableWidget.itemSelectionChanged.connect(self.display_row)
        self.btn_thoat_qlnv.clicked.connect(self.Exit)
        self.btn_them_qlnv.clicked.connect(self.them)
        self.btn_sua_qlnv.clicked.connect(self.sua)
        self.btn_xoa_qlnv.clicked.connect(self.xoa)
        self.btn_timkiem_qlnv.clicked.connect(self.timkiem)
        
    # show data lên table
    def loaddata(self):
        sql = "SELECT * FROM qlnv"
        cur.execute(sql)
        results = cur.fetchall()
        
        # Xóa dữ liệu cũ trên bảng de them moi
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        
        if results:
            #self.tableWidget.setRowCount(len(results))
            for row_number, row_data in enumerate(results):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    
        else:
            print("Không tìm thấy kết quả cho câu truy vấn.")
    
    #chọn và hiển thị dòng trên table
    def display_row(self):
        current_row = self.tableWidget.currentRow()
        
        if current_row >= 0:
            # Lấy dữ liệu của dòng đang được chọn
            row_data = []
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(current_row, col)
                if item:
                    row_data.append(item.data(QtCore.Qt.ItemDataRole.DisplayRole))
                else:
                    row_data.append('')
            
            # Đưa dữ liệu lên các LineEdit
            #self.txtMaphong.setText(row_data[0])
            self.txt_qlnv_tn.setText(row_data[1])
            self.txt_qlnv_dc.setText(row_data[2])
            self.txt_qlnv_sdt.setText(row_data[3])
            self.txt_qlnv_cv.setText(row_data[4])
            self.txt_qlnv_l.setText(row_data[5])
    
    def them(self):
        ten = self.txt_qlnv_tn.text ()
        dc = self.txt_qlnv_dc.text()
        sdt = self.txt_qlnv_sdt.text()
        cv = self.txt_qlnv_cv.text()
        l = self.txt_qlnv_l.text()
        
        sql = "INSERT INTO qlnv (ten, diachi, sdt, chucvu, luong) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, (ten, dc, sdt, cv, l))
        db.commit()
        self.loaddata()    
        
    def sua(self):
        current_row = self.tableWidget.currentRow()
        if current_row >= 0:
            ten = self.txt_qlnv_tn.text ()
            dc = self.txt_qlnv_dc.text()
            sdt = self.txt_qlnv_sdt.text()
            cv = self.txt_qlnv_cv.text()
            l = self.txt_qlnv_l.text()
        
            # Lấy mã phân phối từ cột đầu tiên trong hàng hiện tại
            id = self.tableWidget.item(current_row, 0).text()
        
            sql = "UPDATE qlnv SET ten = %s, diachi = %s, sdt = %s, chucvu = %s, luong = %s WHERE id = %s"
            cur.execute(sql, (ten, dc, sdt, cv, l, id))
            db.commit()
            self.loaddata() 
    
    def xoa(self):
        current_row = self.tableWidget.currentRow()
        if current_row >= 0:
            # Lấy giá trị của cột đầu tiên (mã phân phối) trong hàng hiện tại
            id = self.tableWidget.item(current_row, 0).text()
            
            sql = "DELETE FROM qlnv WHERE id = %s"
            cur.execute(sql, (id,))
            db.commit()
            self.loaddata()
    
    def timkiem(self):
        search_criteria = self.tim_qlnv.text().split()
        sql = "SELECT * FROM qlnv WHERE 1=1"
        for criteria in search_criteria:
            sql += f" AND (id LIKE '%{criteria}%' OR ten LIKE '%{criteria}%' OR diachi LIKE '%{criteria}%' OR sdt LIKE '%{criteria}%' OR chucvu LIKE '%{criteria}%' OR luong LIKE '%{criteria}%' ) "
        cur.execute(sql)
        results = cur.fetchall()

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        if results:
            for row_number, row_data in enumerate(results):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        else:
            print("Không tìm thấy kết quả phù hợp.")
        
    def Exit(self):
        select_option = QMessageBox.warning(self, "Exit", "Bạn có muốn thoát không?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if select_option == QMessageBox.StandardButton.Yes:
            self.close()
            self.nv.emit()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qlnv_window = nhanvien_w()
    qlnv_window.show()
    sys.exit(app.exec())