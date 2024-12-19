import sys
import conn
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtCore import QDate
from PyQt6.QtCore import pyqtSlot
from conn import Myconnection, CloseConnection
db = Myconnection()
cur = db.cursor()

class banhang_w(QMainWindow):
    bh = QtCore.pyqtSignal()
    def __init__(self):
        super(banhang_w, self).__init__()
        uic.loadUi('view/qlbh.ui', self)
    
        # tableWidget
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tb_qlbh")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        #gọi hàm loaddata
        self.loaddata()
        self.btn_again.clicked.connect(self.loaddata)
        
        # Kết nối tín hiệu của table_widget
        self.tableWidget.itemSelectionChanged.connect(self.display_row)
        self.btn_thoat_qlbh.clicked.connect(self.Exit)
        self.btn_them_qlbh.clicked.connect(self.them)
        self.btn_sua_qlbh.clicked.connect(self.sua)
        # self.btn_sua_qlbh.clicked.connect(self.thanhtien)
        self.btn_xoa_qlbh.clicked.connect(self.xoa)
        self.btn_timkiem_qlbh.clicked.connect(self.timkiem)
        
        
        self.txt_qlbh_tong.textChanged.connect(self.thanhtien)
        
        # #set độ dài cho cột
        # self.tableWidget.setColumnWidth(0, 50)
        # self.tableWidget.setColumnWidth(1, 100)
        
    # show data lên table
    def loaddata(self):
        sql = "SELECT * FROM qlbh"
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
                    item = QTableWidgetItem()
                    if column_number == 1:  # Nếu là cột chứa id sản phẩm
                        # Lấy tên sản phẩm dựa trên id
                        sql = "SELECT ten FROM qlsp WHERE id = %s"  # Thay 'products' bằng tên bảng sản phẩm của bạn
                        cur.execute(sql, (data,))
                        spid = cur.fetchone()[0]
                        item.setData(QtCore.Qt.ItemDataRole.DisplayRole, spid)
                    elif column_number == 2: 
                        sql = "SELECT ten FROM qldvpp WHERE id = %s"
                        cur.execute(sql, (data,))
                        ppid = cur.fetchone()[0]
                        item.setData(QtCore.Qt.ItemDataRole.DisplayRole, ppid)
                    else:
                        item.setData(QtCore.Qt.ItemDataRole.DisplayRole, str(data))
                    self.tableWidget.setItem(row_number, column_number, item)
        else:
            print("Không tìm thấy kết quả cho câu truy vấn.")
            
    #chọn và hiển thị dòng của table
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
            self.txt_qlbh_sp.setText(row_data[1])
            self.txt_qlbh_npp.setText(row_data[2])
            self.txt_qlbh_sl.setText(row_data[3])
            self.txt_qlbh_dg.setText(row_data[4])
            self.txt_qlbh_tong.setText(row_data[5])
            date_str = row_data[6]  # Giả sử row_data[5] chứa chuỗi ngày tháng
            # Chuyển đổi chuỗi ngày tháng thành đối tượng QDate
            date = QDate.fromString(date_str, "dd-MM-yyyy")
            # Đặt giá trị ngày tháng cho QDateTimeEdit
            self.time_qlbh_nb.setDate(date)
            
    #@pyqtSlot(str)  # Đánh dấu phương thức 'thanhtien' là một khe cắm (slot) với đối số là một chuỗi (str)       
    def thanhtien(self, t):
        dg = int(self.txt_qlbh_dg.text())
        sl = int(self.txt_qlbh_sl.text())
        tien = dg * sl
        self.txt_qlbh_tong.setText(str(tien))

            
    def them(self):
        sp = self.txt_qlbh_sp.text ()
        npp = self.txt_qlbh_npp.text()
        sl = self.txt_qlbh_sl.text()
        dg = self.txt_qlbh_dg.text()
        tong = self.txt_qlbh_tong.text()
        # Lấy giá trị ngày tháng từ QDateTimeEdit
        date = self.time_qlbh_nb.date()
        nb = date.toString("dd-MM-yyyy")
        
        # Lấy ID của sản phẩm dựa trên tên
        sql_sp_id = "SELECT id FROM qlsp WHERE ten = %s"
        cur.execute(sql_sp_id, (sp,))
        sp_id = cur.fetchone()[0]  # Lấy ID đầu tiên từ kết quả truy vấn
        
        # Lấy ID của phân phối dựa trên tên
        sql_npp_id = "SELECT id FROM qldvpp WHERE ten = %s"
        cur.execute(sql_npp_id, (npp,))
        npp_id = cur.fetchone()[0]  # Lấy ID đầu tiên từ kết quả truy vấn
        
        sql = "INSERT INTO qlbh (sanpham_id, phanphoi_id, soluong, dongia, tong, ngayban) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (sp_id, npp_id, sl, dg, tong, nb))
        db.commit()
        self.loaddata()
        
    def sua(self):
        current_row = self.tableWidget.currentRow()
        if current_row >= 0:
            sp = self.txt_qlbh_sp.text ()
            npp = self.txt_qlbh_npp.text()
            sl = self.txt_qlbh_sl.text()
            dg = self.txt_qlbh_dg.text()
            tong = self.txt_qlbh_tong.text()
            date = self.time_qlbh_nb.date()
            nb = date.toString("dd-MM-yyyy")
            
            # Lấy ID của sản phẩm dựa trên tên
            sql_sp_id = "SELECT id FROM qlsp WHERE ten = %s"
            cur.execute(sql_sp_id, (sp,))
            sp_id = cur.fetchone()[0]  # Lấy ID đầu tiên từ kết quả truy vấn
            
            # Lấy ID của phân phối dựa trên tên
            sql_npp_id = "SELECT id FROM qldvpp WHERE ten = %s"
            cur.execute(sql_npp_id, (npp,))
            npp_id = cur.fetchone()[0]  # Lấy ID đầu tiên từ kết quả truy vấn
            
            # Lấy mã phân phối từ cột đầu tiên trong hàng hiện tại
            id = self.tableWidget.item(current_row, 0).text()
            
            sql = "UPDATE qlbh SET sanpham_id = %s, phanphoi_id = %s, soluong = %s, dongia = %s, tong = %s, ngayban = %s WHERE id = %s"
            cur.execute(sql, (sp_id, npp_id, sl, dg,tong, nb, id))
            db.commit()
            self.loaddata() 
    
    def xoa(self):
        current_row = self.tableWidget.currentRow()
        if current_row >= 0:
            # Lấy giá trị của cột đầu tiên (mã phân phối) trong hàng hiện tại
            id = self.tableWidget.item(current_row, 0).text()
            
            sql = "DELETE FROM qlbh WHERE id = %s"
            cur.execute(sql, (id,))
            db.commit()
            self.loaddata()
    
    def timkiem(self):
        search_criteria = self.tim_qlbh.text().split()
        
        # sql = "SELECT * FROM qlbh WHERE 1=1"
        sql = "SELECT qlbh.id, qlsp.ten, qldvpp.ten, qlbh.soluong, qlbh.dongia, qlbh.tong, qlbh.ngayban FROM qlbh INNER JOIN qlsp ON qlbh.sanpham_id = qlsp.id INNER JOIN qldvpp ON qlbh.phanphoi_id = qldvpp.id "
        for criteria in search_criteria:
            sql += f" AND (qlbh.id LIKE '%{criteria}%' OR qlsp.ten LIKE '%{criteria}%' OR qldvpp.ten LIKE '%{criteria}%' OR qlbh.soluong LIKE '%{criteria}%' OR qlbh.dongia LIKE '%{criteria}%' OR qlbh.tong LIKE '%{criteria}%' OR qlbh.ngayban LIKE '%{criteria}%' ) "
        # sql = "SELECT qlbh.id, qlbh.ngayban, qlsp.ten, qlbh.tong FROM qlbh LEFT JOIN qlsp ON qlbh.sanpham_id = qlsp.id"
        
        cur.fetchall()
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
            self.bh.emit()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qlbh_window = banhang_w()
    qlbh_window.show()
    sys.exit(app.exec())