import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMainWindow
from PyQt5.QtCore import Qt

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Danh sách điểm danh')
        self.setGeometry(100, 100, 1000, 600)

        self.col = 0
        self.row = 0

        self.maLop = "202110503190002"
        self.list_lable =['Mã sinh viên', 'Họ đệm', 'Tên']

        conn = sqlite3.connect("data_demo.db")
        sql_select_day = "SELECT ngayHoc FROM Thoikhoabieulophocphans WHERE maLop = " + str(self.maLop)
        list_day = conn.execute(sql_select_day)
        for item in list_day:
            self.list_lable.append(item[0])
        sql_thongtindiemdanh = "SELECT Sinhviens.maSV, hoDem, ten, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10 FROM Sinhviens " \
                               "INNER JOIN Lophocphans ON Sinhviens.maSV = Lophocphans.maSV WHERE Lophocphans.maLop = " + self.maLop + \
                               "  ORDER BY ten"
        self.thongtindiemdanh = conn.execute(sql_thongtindiemdanh)

        sql_count_row = "SELECT COUNT(*) FROM Lophocphans WHERE maLop = "+self.maLop

        cursor = conn.execute(sql_count_row)

        for item in cursor:
            self.row = item[0]
        self.col = len(self.list_lable)

        self.initUI()
        conn.close()
    def initUI(self):
        table_widget = QTableWidget(self.row, self.col)
        table_widget.setHorizontalHeaderLabels(self.list_lable)

        self.ShowInForm(table_widget)

        table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        vbox = QVBoxLayout()
        vbox.addWidget(table_widget)
        self.setLayout(vbox)

    def ShowInForm(self, tableWidget):
        for index_row, data_row in enumerate(self.thongtindiemdanh):
            for index_col, data_col in enumerate(data_row):
                data_col = QTableWidgetItem(data_col)
                data_col.setTextAlignment(Qt.AlignCenter)
                tableWidget.setItem(index_row, index_col, data_col)


def Thongtindiemdanh(Check = True):
    app = QApplication(sys.argv)
    table_widget = TableWidget()
    if Check:
        table_widget.show()
    else:
        table_widget.hide()
    sys.exit(app.exec_())

Thongtindiemdanh()