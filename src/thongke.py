import sys
import conn
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from conn import Myconnection, CloseConnection
import xlsxwriter
db = Myconnection()
cur = db.cursor()

class thongke_w(QMainWindow):
    thongke = QtCore.pyqtSignal()
    def __init__(self):
        super(thongke_w, self).__init__()
        uic.loadUi('view/thongke.ui', self)
        
        self.tb_thongke.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.btnTkdt.clicked.connect(self.Tongtien)
        self.btn_xuat_thongke.clicked.connect(self.XuatExcel)
        self.btn_thoat_thongke.clicked.connect(self.Exit)
        self.btn_again.clicked.connect(self.loaddata)
        
        # tableWidget
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tb_thongke")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        self.loaddata()
        self.btn_again.clicked.connect(self.loaddata)
        
    def loaddata(self):
        
        #sql = ("Select id,ngayban, sanpham_id , tong from qlbh") 
        
        sql = "SELECT qlbh.id, qlbh.ngayban, qlsp.ten, qlbh.tong FROM qlbh LEFT JOIN qlsp ON qlbh.sanpham_id = qlsp.id"
        
        cur.execute(sql)
        results = cur.fetchall()
        self.tb_thongke.setRowCount(len(results))  
        tableRow = 0
        for row in results:
            self.tb_thongke.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tb_thongke.setItem(tableRow, 1 , QtWidgets.QTableWidgetItem(str(row[1])))
            self.tb_thongke.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tb_thongke.setItem(tableRow, 3 , QtWidgets.QTableWidgetItem(str(row[3])))
            tableRow+=1
    
        
    def Tongtien(self):
        tu = self.time_start.date().toString("dd-MM-yyyy")
        ngay = self.time_end.date().toString("dd-MM-yyyy")

        #sql = f"SELECT id, ngayban, sanpham_id, tong FROM qlbh WHERE ngayban >= '{tu}' AND ngayban <= '{ngay}'"
        
        sql = "SELECT qlbh.id, qlbh.ngayban, qlsp.ten, qlbh.tong FROM qlbh LEFT JOIN qlsp ON qlbh.sanpham_id = qlsp.id WHERE ngayban >= %s AND ngayban <= %s "
        
        cur.execute(sql, (tu, ngay))
        result = cur.fetchall()
        
        self.tb_thongke.clearContents()
        self.tb_thongke.setRowCount(len(result))
        tableRow = 0
        tongtien = 0
        for row in result:
            for col in range(len(row)):
                self.tb_thongke.setItem(tableRow, col, QtWidgets.QTableWidgetItem(str(row[col])))
                if col == 3:
                    tongtien += row[col]        
            tableRow += 1
        tongtien = format(tongtien, ',')
        tongtien += " vnđ"
        self.txtTongtien.setText(str(tongtien))
    
        
    def Exit(self):
        select_option = QMessageBox.warning(self, "Exit", "Bạn có muốn thoát không?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if select_option == QMessageBox.StandardButton.Yes:
            self.close()
            self.thongke.emit()
    
    def XuatExcel(self):
        # Tạo một workbook mới
        workbook = xlsxwriter.Workbook('view/Doanhthutheosanpham.xlsx')
        self.worksheet = workbook.add_worksheet()  # Initialize the worksheet
        # Ghi tiêu đề cột
        col_headers = ['ID', 'Thoi Gian', 'San Pham', 'Doanh Thu']
        for col, header in enumerate(col_headers):
            self.worksheet.write(0, col, header)
        # Lấy dữ liệu từ tableWidget và ghi vào file Excel
        for row in range(self.tb_thongke.rowCount()):
            for col in range(self.tb_thongke.columnCount()):
                item = self.tb_thongke.item(row, col)
                if item is not None:
                    self.worksheet.write(row + 1, col, item.text())
        # Đóng workbook
        workbook.close()
        QMessageBox.information(self, "Xuất Excel", "Đã xuất file Excel thành công!")
    def save_data(self):
        self.XuatExcel()

       
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    thongke_window = thongke_w()
    thongke_window.show()
    sys.exit(app.exec())