from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import sqlite3
import time

import UI_Login
import UI_TB_Login
import UI_Main
import UI_SHOW_INFO
import UI_Webcam
import UI_NotificationLogout
import UI_Notification_Nodate

def time_to_string(time=time.localtime(time.time())):
    day = str(time.tm_mday)
    month = str(time.tm_mon)
    return day + "/" + month


class MAIN:

    notification_win = None
    ui_notification_login = None

    def __init__(self):
        self.login_win = QMainWindow()
        self.ui_login = UI_Login.Ui_MainWindow()
        self.ui_login.setupUi(self.login_win)
        self.login_win.show()

    #   Xử lý sự kiện clicked
        self.ui_login.btn_dangnhap.clicked.connect(self.CheckLogin)

    def CheckLogin(self):
        if self.ui_login.error_login:
            self.notification_win = QMainWindow()
            self.ui_notification_login = UI_TB_Login.Ui_MainWindow()
            self.ui_notification_login.setupUi(self.notification_win)
            self.notification_win.show()
            self.ui_notification_login.pushButton.clicked.connect(self.Hide_ui_notification)

        elif self.ui_login.error_login == False:
            self.login_win.hide()
        #   Màn hình chính
            self.main_win = QMainWindow()
            self.ui_main = UI_Main.Ui_MainWindow(self.ui_login.teacher_name, self.ui_login.id_teacher)
            self.ui_main.setupUi(self.main_win)
            self.ui_main.teacher_name = self.ui_login.teacher_name
        #   Xử lý clicked giao diện chính
            self.ui_main.btn_diemdanh.clicked.connect(self.log_data)
            self.ui_main.btn_thongtindiemdanh.clicked.connect(self.ShowInFo)
            self.ui_main.btn_logout.clicked.connect(self.LogOut)

            self.main_win.show()
    def log_data(self):
        current_index = self.ui_main.listWidget.currentRow()
        subject_id = self.ui_main.list_class[current_index]
        conn = sqlite3.connect('data.db')
        sql_check_date = "SELECT maLHP FROM Thoikhoabieu_Lophocphans WHERE " \
                         "maLHP ='"+subject_id+"' AND ngayHoc = '"+time_to_string()+"';"
        result_check_date = conn.execute(sql_check_date)
        if result_check_date.fetchone():
            self.webcam_win = QMainWindow()
            self.ui_webcam = UI_Webcam.Ui_MainWindow(subject_id)
            self.ui_webcam.setupUi(self.webcam_win)
            self.webcam_win.show()
            self.ui_webcam.gddd_thoat.clicked.connect(self.OutCam)
        else:
            self.notification_nodate_win = QMainWindow()
            self.ui_notification_nodate = UI_Notification_Nodate.Ui_MainWindow()
            self.ui_notification_nodate.setupUi(self.notification_nodate_win)
            self.notification_nodate_win.show()
            self.ui_notification_nodate.btn_ok.clicked.connect(self.notification_nodate_win.hide)
        conn.close()

        # print(self.ui_main.listWidget.item(current_index).text())

    def OutCam(self):
        self.ui_webcam.capture.release()
        self.webcam_win.hide()

    def LogOut(self):
            self.notification_logout_win = QMainWindow()
            self.ui_notification_logout = UI_NotificationLogout.Ui_MainWindow()
            self.ui_notification_logout.setupUi(self.notification_logout_win)
            self.notification_logout_win.show()

            self.ui_login.teacher_name = None
            self.ui_main.teacher_id = None

            self.ui_notification_logout.btn_no.clicked.connect(self.notification_logout_no)
            self.ui_notification_logout.btn_yes.clicked.connect(self.notification_logout_yes)

    def notification_logout_no(self):
        self.notification_logout_win.hide()
    def notification_logout_yes(self):
        # self.notification_nodate_win.hide()
        # self.info_win.hide()
        self.ui_login.teacher_name = None
        self.ui_login.id_teacher = None

        self.notification_logout_win.hide()
        self.main_win.hide()

        self.login_win.show()
        self.ui_login.input_matkhau.setText(None)
        self.ui_main.list_class_show.clear()
        self.ui_main.list_class.clear()

    def ShowInFo(self):
        currentIndex = self.ui_main.listWidget.currentRow()
        maLHP = self.ui_main.list_class[currentIndex]
        conn = sqlite3.connect("data.db")
        sql_maHp = "SELECT maHP FROM Lophocphans WHERE maLHP = '" + maLHP + "';"
        maHP = conn.execute(sql_maHp).fetchone()[0]
        sql = "SELECT tenHP FROM Hocphans WHERE Hocphans.maHP = '" + maHP + "'"
        tenHP = conn.execute(sql).fetchone()[0]

        self.info_win = QMainWindow()
        self.ui_info = UI_SHOW_INFO.Ui_MainWindow(maLHP, self.ui_login.teacher_name, tenHP)
        self.ui_info.setupUi(self.info_win)
        self.info_win.show()
        conn.close()

    def Hide_ui_notification(self):
        self.notification_win.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MAIN()
    sys.exit(app.exec_())
