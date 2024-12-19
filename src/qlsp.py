import sys
import conn
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtCore import QDate
from conn import Myconnection, CloseConnection
db = Myconnection()
cur = db.cursor()

class sanpham_w(QMainWindow):
    sp = QtCore.pyqtSignal()
    def __init__(self):
        super(sanpham_w, self).__init__()
        uic.loadUi('view/qlsp.ui', self)
        
        # tableWidget
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tb_qlsp")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        #gọi hàm loaddata
        self.loaddata()
        self.btn_again.clicked.connect(self.loaddata)
        
        # Kết nối tín hiệu của table_widget
        self.tableWidget.itemSelectionChanged.connect(self.display_row)
        self.btn_thoat_qlsp.clicked.connect(self.Exit)
        self.btn_them_qlsp.clicked.connect(self.them)
        self.btn_sua_qlsp.clicked.connect(self.sua)
        self.btn_xoa_qlsp.clicked.connect(self.xoa)
        self.btn_timkiem_qlsp.clicked.connect(self.timkiem)
        
    def Exit(self):
        select_option = QMessageBox.warning(self, "Exit", "Bạn có muốn thoát không?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if select_option == QMessageBox.StandardButton.Yes:
            self.close()
            self.sp.emit()
        
    # show data lên table
    def loaddata(self):
        sql = "SELECT * FROM qlsp"
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
                    if column_number == 2: 
                        sql = "SELECT ten FROM qldvsx WHERE id = %s"
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
            self.txt_qlsp_sp.setText(row_data[1])
            self.txt_qlsp_nsx.setText(row_data[2])
            self.txt_qlsp_sl.setText(row_data[3])
            self.txt_qlsp_dg.setText(row_data[4])
            self.txt_qlsp_tong.setText(row_data[5])
            
            date_str = row_data[6]  # Giả sử row_data[5] chứa chuỗi ngày tháng
            # Chuyển đổi chuỗi ngày tháng thành đối tượng QDate
            date = QDate.fromString(date_str, "dd-MM-yyyy")
            # Đặt giá trị ngày tháng cho QDateTimeEdit
            self.time_qlsp_nn.setDate(date)    
        
    def them(self):
        sp = self.txt_qlsp_sp.text ()
        nsx = self.txt_qlsp_nsx.text()
        sl = self.txt_qlsp_sl.text()
        dg = self.txt_qlsp_dg.text()
        tong = self.txt_qlsp_tong.text()
        # Lấy giá trị ngày tháng từ QDateTimeEdit
        date = self.time_qlsp_nn.date()
        nn = date.toString("dd-MM-yyyy")
        
        # Lấy ID của phân phối dựa trên tên
        sql_npp_id = "SELECT id FROM qldvsx WHERE ten = %s"
        cur.execute(sql_npp_id, (nsx,))
        nsx_id = cur.fetchone()[0]  # Lấy ID đầu tiên từ kết quả truy vấn
        
        sql = "INSERT INTO qlsp (ten, sanxuat_d, soluong, dongia, tong, ngaynhap) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (sp, nsx_id, sl, dg, tong, nn))
        db.commit()
        self.loaddata()
        
    def sua(self):
        current_row = self.tableWidget.currentRow()
        if current_row >= 0:
            sp = self.txt_qlsp_sp.text ()
            nsx = self.txt_qlsp_nsx.text()
            sl = self.txt_qlsp_sl.text()
            dg = self.txt_qlsp_dg.text()
            tong = self.txt_qlsp_tong.text()
            date = self.time_qlsp_nn.date()
            nb = date.toString("dd-MM-yyyy")
            # Lấy mã phân phối từ cột đầu tiên trong hàng hiện tại
            id = self.tableWidget.item(current_row, 0).text()
            
            # Lấy ID của phân phối dựa trên tên
            sql_npp_id = "SELECT id FROM qldvsx WHERE ten = %s"
            cur.execute(sql_npp_id, (nsx,))
            nsx_id = cur.fetchone()[0]  # Lấy ID đầu tiên từ kết quả truy vấn
            
            sql = "UPDATE qlsp SET ten = %s, sanxuat_id = %s, soluong = %s, dongia = %s, tong = %s, ngaynhap = %s WHERE id = %s"
            cur.execute(sql, (sp, nsx_id, sl, dg,tong, nb, id))
            db.commit()
            self.loaddata() 
    
    def xoa(self):
        current_row = self.tableWidget.currentRow()
        if current_row >= 0:
            # Lấy giá trị của cột đầu tiên (mã phân phối) trong hàng hiện tại
            id = self.tableWidget.item(current_row, 0).text()
            
            sql = "DELETE FROM qlsp WHERE id = %s"
            cur.execute(sql, (id,))
            db.commit()
            self.loaddata()
    
    def timkiem(self):
        search_criteria = self.tim_qlsp.text().split()
        
        # sql = "SELECT * FROM qlsp WHERE 1=1"
        sql = "SELECT qlsp.id, qlsp.ten, qldvsx.ten, qlsp.soluong, qlsp.dongia, qlsp.tong, qlsp.ngaynhap FROM qlsp INNER JOIN qldvsx ON qlsp.sanxuat_id = qldvsx.id"
        for criteria in search_criteria:
            sql += f" AND (qlsp.id LIKE '%{criteria}%' OR qlsp.ten LIKE '%{criteria}%' OR qldvsx.ten LIKE '%{criteria}%' OR qlsp.soluong LIKE '%{criteria}%' OR qlsp.dongia LIKE '%{criteria}%' OR qlsp.tong LIKE '%{criteria}%' OR qlsp.ngaynhap LIKE '%{criteria}%' ) "
        
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
        
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qlsp_window = sanpham_w()
    qlsp_window.show()
    sys.exit(app.exec())