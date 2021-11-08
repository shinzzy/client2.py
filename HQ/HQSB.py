#%config InlineBackend.figure_format = 'retina'
import sys, re, pymysql, pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from datetime import *
from random import *

UI = '../_qt_ui/HQ.ui'

class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, QStyleOptionViewItem, QModelIndex):
        QStyledItemDelegate.initStyleOption(self, QStyleOptionViewItem, QModelIndex)
        QStyleOptionViewItem.displayAlignment = Qt.AlignCenter

class greater:
    list_bsname = []
    list_country = []
    list_city = []

class window(QDialog):
    def __init__(self):
        QDialog.__init__(self, None, Qt.WindowStaysOnTopHint)
        uic.loadUi(UI, self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.offset = None
        # 시트
        self.stylePopupOk = ("""
                QLineEdit{font: 75 12pt "맑은 고딕"; border-radius: 7px; border:4px solid rgb(30, 107, 255); padding-left: 20px; padding-right: 20px;}
                QLineEdit:focus{border: 4px solid rgb(113, 198, 255);}
                """)
        self.stylePopupError = ("""
                QLineEdit{font: 75 12pt "맑은 고딕"; border-radius: 7px; border:4px solid rgb(198, 35, 255); padding-left: 20px; padding-right: 20px;}
                """)
        comboLine = "QLineEdit{border-radius: 7px; background-color: rgb(255, 255, 255);}"


        # 이미지
        self.label.setStyleSheet('image:url(../_qt_ui/icon/icon_sb2048.png);')
        self.pushButton_graph1.setStyleSheet('image:url(../_qt_ui/icon/icon_line.png);')
        self.pushButton_graph2.setStyleSheet('image:url(../_qt_ui/icon/icon_bar.png);')

        # 콤보박스 정렬
        self.comboBox_country.setEditable(True)
        self.comboBox_country.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_country.lineEdit().setReadOnly(True)
        self.comboBox_country.lineEdit().setStyleSheet(comboLine)

        self.comboBox_city.setEditable(True)
        self.comboBox_city.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_city.lineEdit().setReadOnly(True)
        self.comboBox_city.lineEdit().setStyleSheet(comboLine)

        self.comboBox_tool1_country.setEditable(True)
        self.comboBox_tool1_country.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_tool1_country.lineEdit().setReadOnly(True)
        self.comboBox_tool1_country.lineEdit().setStyleSheet(comboLine)

        self.comboBox_tool1_h1.setEditable(True)
        self.comboBox_tool1_h1.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_tool1_h1.lineEdit().setReadOnly(True)
        self.comboBox_tool1_h1.lineEdit().setStyleSheet(comboLine)

        self.comboBox_tool1_h2.setEditable(True)
        self.comboBox_tool1_h2.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_tool1_h2.lineEdit().setReadOnly(True)
        self.comboBox_tool1_h2.lineEdit().setStyleSheet(comboLine)

        self.comboBox_tool1_m1.setEditable(True)
        self.comboBox_tool1_m1.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_tool1_m1.lineEdit().setReadOnly(True)
        self.comboBox_tool1_m1.lineEdit().setStyleSheet(comboLine)

        self.comboBox_tool1_m2.setEditable(True)
        self.comboBox_tool1_m2.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_tool1_m2.lineEdit().setReadOnly(True)
        self.comboBox_tool1_m2.lineEdit().setStyleSheet(comboLine)

        self.comboBox_tool2_country.setEditable(True)
        self.comboBox_tool2_country.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_tool2_country.lineEdit().setReadOnly(True)
        self.comboBox_tool2_country.lineEdit().setStyleSheet(comboLine)

        self.comboBox_tool2_h1.setEditable(True)
        self.comboBox_tool2_h1.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_tool2_h1.lineEdit().setReadOnly(True)
        self.comboBox_tool2_h1.lineEdit().setStyleSheet(comboLine)

        self.comboBox_tool2_h2.setEditable(True)
        self.comboBox_tool2_h2.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_tool2_h2.lineEdit().setReadOnly(True)
        self.comboBox_tool2_h2.lineEdit().setStyleSheet(comboLine)

        self.comboBox_tool2_m1.setEditable(True)
        self.comboBox_tool2_m1.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_tool2_m1.lineEdit().setReadOnly(True)
        self.comboBox_tool2_m1.lineEdit().setStyleSheet(comboLine)

        self.comboBox_tool2_m2.setEditable(True)
        self.comboBox_tool2_m2.lineEdit().setAlignment(Qt.AlignCenter)
        self.comboBox_tool2_m2.lineEdit().setReadOnly(True)
        self.comboBox_tool2_m2.lineEdit().setStyleSheet(comboLine)

        # 콤보박스 셋팅
        self.comboBox_country.addItem("")
        self.comboBox_city.addItem("")

        # 테이블 정렬
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        # self.tableWidget.setColumnWidth(1, 120)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 80)
        for i in range(8):
            # self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            self.tableWidget.setItemDelegateForColumn(i, AlignDelegate(self.tableWidget))
        # self.tableWidget.setSortingEnabled(True)

        self.tableWidget.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        # 테이블 정렬 2
        self.tableWidget2.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # self.tableWidget2.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        # self.tableWidget2.setColumnWidth(0, 40)
        for i in range(7):
            self.tableWidget2.setItemDelegateForColumn(i, AlignDelegate(self.tableWidget2))
        self.tableWidget2.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tableWidget2.setColumnWidth(0, 40)
        self.tableWidget2.setColumnWidth(1, 120)
        self.tableWidget2.setColumnWidth(2, 120)
        self.tableWidget2.setColumnWidth(3, 390)
        self.tableWidget2.setColumnWidth(4, 120)
        self.tableWidget2.setColumnWidth(5, 150)
        self.tableWidget2.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)

        # 초기창 설정 & 텍스트 리셋
        self.stackedWidget.setCurrentWidget(self.page_login)
        self.stackedWidget_in_visualize.setCurrentWidget(self.page_table)
        self.pushButton_1.clicked.connect(lambda state, clicked = self.pushButton_1 : self.textreset(state, clicked))
        self.pushButton_2.clicked.connect(lambda state, clicked = self.pushButton_2 : self.textreset(state, clicked))
        self.toolBox.currentChanged.connect(lambda state, clicked = self.toolBox : self.textreset(state, clicked))
        self.comboBox_country.currentIndexChanged.connect(lambda state, clicked = self.comboBox_country : self.textreset(state, clicked))

        # 버튼 시그널
        self.pushButton_login.clicked.connect(self.next)
        self.pushButton_quit1.clicked.connect(self.quit)
        self.pushButton_quit2.clicked.connect(self.quit)
        self.pushButton_inquiry.clicked.connect(self.inquiry)
        self.pushButton_graph1.clicked.connect(lambda state, button = self.pushButton_graph1 : self.graph(state, button))
        self.pushButton_graph2.clicked.connect(lambda state, button = self.pushButton_graph2 : self.graph(state, button))

        # indicator
        self.lineEdit_id.textEdited.connect(lambda state, select = self.lineEdit_id : self.indicator(state, select))
        self.lineEdit_bsname.textEdited.connect(lambda state, select = self.lineEdit_bsname : self.indicator(state, select))
        self.lineEdit_address.textEdited.connect(lambda state, select = self.lineEdit_address : self.indicator(state, select))
        self.lineEdit_bsname2.textEdited.connect(lambda state, select = self.lineEdit_bsname2 : self.indicator(state, select))
        self.lineEdit_address2.textEdited.connect(lambda state, select = self.lineEdit_address2 : self.indicator(state, select))
        # part of SQL
        self.pushButton_register.clicked.connect(self.register)
        self.pushButton_tool_inquiry.clicked.connect(self.tool_inquiry)
        self.pushButton_update.clicked.connect(self.update)
        self.pushButton_delete.clicked.connect(self.delete)
########################################################################################################################
    # 슬롯
########################################################################################################################
    def next(self):
        try:
            if self.lineEdit_id.text() == '123456789':
                connection = pymysql.connect \
                    (host='localhost', port=3306, user='root', password='0000', db='headquarter', charset='utf8')
                cursor = connection.cursor()
                qy = "select country, bsname from bsinfo"
                cursor.execute(qy)
                iy = cursor.fetchall()
                connection.commit()
                connection.close()
                if iy == ():
                    pass
                else:
                    country, city = zip(*iy)
                    country = list(dict.fromkeys(country))
                    city = list(dict.fromkeys(city))
                    for i in range(len(country)):
                        greater.list_country.append(country[i])
                    for j in range(len(city)):
                        greater.list_city.append(city[j])
                    for k in range(len(greater.list_country)):
                        self.comboBox_country.addItem(greater.list_country[k])
                    for h in range(len(greater.list_city)):
                        self.comboBox_city.addItem(greater.list_city[h])
                greater.list_country.clear()
                greater.list_city.clear()
                self.stackedWidget.setCurrentWidget(self.page_main)
                self.stackedWidget_in.setCurrentWidget(self.page_1)
            else:
                self.lineEdit_id.setStyleSheet(self.stylePopupError)
                self.label_login_noti.setText("암호가 일치하지 않습니다.")
        except Exception as e:
            print(e)
            pass

    def textreset(self, state, clicked):
        if clicked == self.pushButton_1:
            row_count = self.tableWidget.rowCount()
            for i in range(row_count):
                self.tableWidget.removeRow(0)
            self.stackedWidget_in.setCurrentWidget(self.page_1)
            self.stackedWidget_in_visualize.setCurrentWidget(self.page_table)
            self.label_main_noti.clear()
        elif clicked == self.pushButton_2:
            self.stackedWidget_in.setCurrentWidget(self.page_2)
            self.toolBox.setCurrentWidget(self.page_tool1)
            self.lineEdit_bsname.clear()
            self.lineEdit_address.clear()
            self.label_tool_noti.clear()
            row_count = self.tableWidget2.rowCount()
            for i in range(row_count):
                self.tableWidget2.removeRow(0)
            self.comboBox_tool1_country.setCurrentIndex(0)
            self.comboBox_tool1_h1.setCurrentIndex(0)
            self.comboBox_tool1_m1.setCurrentIndex(0)
            self.comboBox_tool1_h2.setCurrentIndex(0)
            self.comboBox_tool1_m2.setCurrentIndex(0)
        elif clicked == self.toolBox:
            self.lineEdit_bsname.clear()
            self.lineEdit_address.clear()
            self.label_tool_noti.clear()
            self.lineEdit_bsname2.clear()
            self.lineEdit_address2.clear()
            self.label_tool2_noti.clear()
            row_count = self.tableWidget2.rowCount()
            for i in range(row_count):
                self.tableWidget2.removeRow(0)
            self.comboBox_tool1_country.setCurrentIndex(0)
            self.comboBox_tool1_h1.setCurrentIndex(0)
            self.comboBox_tool1_m1.setCurrentIndex(0)
            self.comboBox_tool1_h2.setCurrentIndex(0)
            self.comboBox_tool1_m2.setCurrentIndex(0)
            self.comboBox_tool2_country.setCurrentIndex(0)
            self.comboBox_tool2_h1.setCurrentIndex(0)
            self.comboBox_tool2_m1.setCurrentIndex(0)
            self.comboBox_tool2_h2.setCurrentIndex(0)
            self.comboBox_tool2_m2.setCurrentIndex(0)
        else:
            self.label_main_noti.clear()

    def indicator(self, state, select):
        try:
            if select == self.lineEdit_id:
                self.lineEdit_id.setStyleSheet(self.stylePopupOk)
                self.label_login_noti.clear()
            elif select == self.lineEdit_bsname:
                connection = pymysql.connect \
                    (host='localhost', port=3306, user='root', password='0000', db='headquarter', charset='utf8')
                cursor = connection.cursor()
                qy = "select bsname from bsinfo"
                cursor.execute(qy)
                iy = cursor.fetchall()
                connection.commit()
                connection.close()
                greater.list_bsname = list(map(lambda x: x[0], iy))
                print(greater.list_bsname)
                if self.lineEdit_bsname.text() in greater.list_bsname:
                    self.label_tool_noti.setText("해당 지역에 등록된 지점명 입니다.")
                else:
                    self.label_tool_noti.clear()
            elif select == self.lineEdit_address:
                self.label_tool_noti.clear()
            elif select == self.lineEdit_bsname2 or select == self.lineEdit_address2:
                self.label_tool2_noti.clear()
            else:
                pass
        except Exception as e:
            print(e)
            pass

    # part of SQL
    def inquiry(self):
        self.label_main_noti.clear()
        self.tableWidget.verticalScrollBar().setValue(0)
        self.stackedWidget_in_visualize.setCurrentWidget(self.page_table)
        print("inquiry")
        row_count = self.tableWidget.rowCount()
        self.tableWidget.setSortingEnabled(False)
        for i in range(row_count):
            self.tableWidget.removeRow(0)
        try:
            country = self.comboBox_country.currentText()
            bsname = self.comboBox_city.currentText()
            ddate = self.dateEdit.text()
            print(country)
            connection = pymysql.connect \
                (host='localhost', port=3306, user='root', password='0000', db='headquarter', charset='utf8')
            cursor = connection.cursor()
            if country == "" and bsname == "":
                qy = "select * from dsinfo where ddate = '{}'"
                cursor.execute(qy.format(ddate))
            elif country != "" and bsname == "":
                qy = "select * from dsinfo where country = '{}' and ddate = '{}'"
                cursor.execute(qy.format(country, ddate))
            elif country == "" and bsname != "":
                self.label_main_noti.setText("국가를 선택해 주세요.")
            else:
                qy = "select * from dsinfo where country = '{}' and bsname = '{}' and ddate = '{}'"
                cursor.execute(qy.format(country, bsname, ddate))
            iy = cursor.fetchall()
            connection.commit()
            connection.close()
            print(iy)
            if iy == ():
                self.label_main_noti.setText("해당 국가나 지점, 날짜에 데이터가 존재하지 않습니다.")
            else:
                for i, v in enumerate(iy):
                    # print(i)
                    row_count = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_count)
                    for j in range(len(v)):
                        # v[j] = "{0:+}".format(v[j])
                        item = QTableWidgetItem(v[j])
                        item.setData(Qt.DisplayRole, v[j])
                        self.tableWidget.setItem(row_count, j, item)
                self.comboBox_country.setCurrentIndex(0)
                self.comboBox_city.setCurrentIndex(0)
                self.tableWidget.setSortingEnabled(True)
        except Exception as e:
            print(e)
            pass

    def register(self):
        self.label_tool_noti.setStyleSheet("""
        QLabel{color: rgb(255, 0, 0); font: 75 12pt "맑은 고딕";}""")
        try:
            if self.lineEdit_bsname.text() == "" or self.lineEdit_address.text() == "":
                self.label_tool_noti.setText('정보를 입력해 주세요.')
            else:
                if self.lineEdit_bsname.text() not in greater.list_bsname:
                    time = datetime.now()
                    now = time.strftime('%Y-%m-%d/%H:%M:%S')
                    connection = pymysql.connect \
                        (host='localhost', port=3306, user='root', password='0000', db='headquarter', charset='utf8')
                    cursor = connection.cursor()
                    qy1 = "SELECT MAX(BSNO) FROM BSINFO"
                    cursor.execute(qy1)
                    iy = cursor.fetchone()

                    max_count = iy[0]
                    # print(max_count)
                    if max_count == 0:
                        max_count = 1
                    else:
                        max_count = int(max_count) + 1
                    # print(max_count)
                    country = self.comboBox_tool1_country.currentText()
                    bsname = self.lineEdit_bsname.text()
                    address = self.lineEdit_address.text()
                    bhours = "{}:{} ~ {}:{}".format(self.comboBox_tool1_h1.currentText(), \
                                                    self.comboBox_tool1_m1.currentText(), \
                                                    self.comboBox_tool1_h2.currentText(), \
                                                    self.comboBox_tool1_m2.currentText())
                    approve = "0"
                    # print(bhours)
                    qy2 = "INSERT INTO BSINFO VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(qy2, (max_count, country, bsname, address, bhours, now, approve))

                    index1 = self.comboBox_country.count()
                    for j in range(index1):
                        self.comboBox_country.removeItem(1)
                    index2 = self.comboBox_city.count()
                    for j in range(index2):
                        self.comboBox_city.removeItem(1)
                    qy3 = "select country, bsname from bsinfo"
                    cursor.execute(qy3)
                    iy = cursor.fetchall()
                    connection.commit()
                    connection.close()

                    self.comboBox_tool1_country.setCurrentIndex(0)
                    self.comboBox_tool1_h1.setCurrentIndex(0)
                    self.comboBox_tool1_m1.setCurrentIndex(0)
                    self.comboBox_tool1_h2.setCurrentIndex(0)
                    self.comboBox_tool1_m2.setCurrentIndex(0)
                    country, city = zip(*iy)
                    country = list(dict.fromkeys(country))
                    city = list(dict.fromkeys(city))
                    for i in range(len(country)):
                        greater.list_country.append(country[i])
                    for j in range(len(city)):
                        greater.list_city.append(city[j])
                    for k in range(len(greater.list_country)):
                        self.comboBox_country.addItem(greater.list_country[k])
                    for h in range(len(greater.list_city)):
                        self.comboBox_city.addItem(greater.list_city[h])
                    greater.list_country.clear()
                    greater.list_city.clear()
                    self.lineEdit_bsname.clear()
                    self.lineEdit_address.clear()
                    greater.list_bsname.clear()
                    self.label_tool_noti.setStyleSheet("""
                    QLabel{color: rgb(30, 107, 255); font: 75 12pt "맑은 고딕";}""")
                    self.label_tool_noti.setText("등록이 완료 되었습니다.")
                else:
                    self.label_tool_noti.setText("해당 지역에 등록된 지점명 입니다.")
        except Exception as e:
            print(e)
            pass

    def tool_inquiry(self):
        try:
            if self.lineEdit_bsname2.text() == "":
                self.label_tool2_noti.setText("지점명을 입력해 주세요.")
            else:
                row_count = self.tableWidget2.rowCount()
                for i in range(row_count):
                    self.tableWidget2.removeRow(0)
                country = self.comboBox_tool2_country.currentText()
                bsname = self.lineEdit_bsname2.text()
                connection = pymysql.connect \
                    (host='localhost', port=3306, user='root', password='0000', db='headquarter', charset='utf8')
                cursor = connection.cursor()
                qy = "SELECT * FROM BSINFO WHERE COUNTRY = '{}' AND BSNAME = '{}'"
                cursor.execute(qy.format(country, bsname))
                iy = cursor.fetchall()
                connection.commit()
                connection.close()
                print(iy)
                if iy == ():
                    self.label_tool2_noti.setText("등록되지 않은 지점명입니다.")
                    self.lineEdit_bsname2.clear()
                else:
                    for i, v in enumerate(iy):
                        # print(i)
                        row_count = self.tableWidget2.rowCount()
                        self.tableWidget2.insertRow(row_count)
                        for j in range(len(v)):
                            item = QTableWidgetItem(v[j])
                            item.setData(Qt.DisplayRole, v[j])
                            self.tableWidget2.setItem(row_count, j, item)
                    self.comboBox_tool2_country.setCurrentIndex(0)
                    self.comboBox_tool2_h1.setCurrentIndex(0)
                    self.comboBox_tool2_m1.setCurrentIndex(0)
                    self.comboBox_tool2_h2.setCurrentIndex(0)
                    self.comboBox_tool2_m2.setCurrentIndex(0)
        except Exception as e:
            print(e)
            pass

    def update(self):
        self.label_tool2_noti.setStyleSheet("""
        QLabel{color: rgb(255, 0, 0); font: 75 12pt "맑은 고딕";}""")
        try:
            if self.tableWidget2.rowCount() != 1:
                self.label_tool2_noti.setText("수정할 지점을 먼저 조회해 주세요.")
            elif self.lineEdit_address2.text() == "":
                self.label_tool2_noti.setText("수정할 정보를 입력해 주세요.")
            else:
                connection = pymysql.connect \
                    (host='localhost', port=3306, user='root', password='0000', db='headquarter', charset='utf8')
                cursor = connection.cursor()
                address = self.lineEdit_address2.text()
                bhours = "{}:{} ~ {}:{}".format(self.comboBox_tool2_h1.currentText(), self.comboBox_tool2_m1.currentText(),
                                                self.comboBox_tool2_h2.currentText(), self.comboBox_tool2_m2.currentText())
                returned = self.tableWidget2.item(0, 2)
                # print(returned)
                bsname = QTableWidgetItem(returned).text()
                # print(bsname)
                qy = "UPDATE BSINFO SET ADDRESS = %s, BHOURS = %s WHERE BSNAME = %s"
                cursor.execute(qy, (address, bhours, bsname))
                connection.commit()
                connection.close()
                self.lineEdit_bsname2.clear()
                self.lineEdit_address2.clear()
                row_count = self.tableWidget2.rowCount()
                for i in range(row_count):
                    self.tableWidget2.removeRow(0)
                self.label_tool2_noti.setStyleSheet("""
                QLabel{color: rgb(30, 107, 255); font: 75 12pt "맑은 고딕";}""")
                self.label_tool2_noti.setText("수정이 완료 되었습니다.")
        except Exception as e:
            print(e)
            pass

    def delete(self):
        self.label_tool2_noti.setStyleSheet("""
        QLabel{color: rgb(255, 0, 0); font: 75 12pt "맑은 고딕";}""")
        try:
            if self.tableWidget2.rowCount() != 1:
                self.label_tool2_noti.setText("수정할 지점을 먼저 조회해 주세요.")
            else:
                connection = pymysql.connect \
                    (host='localhost', port=3306, user='root', password='0000', db='headquarter', charset='utf8')
                cursor = connection.cursor()
                returned = self.tableWidget2.item(0, 2)
                print(returned)
                bsname = QTableWidgetItem(returned).text()
                print(bsname)
                qy1 = """
                delete bsinfo, dsinfo
                from bsinfo join dsinfo
                on bsinfo.country = dsinfo.country and bsinfo.bsname = dsinfo.bsname
                where bsinfo.bsname = '{}'
                """
                cursor.execute(qy1.format(bsname))

                index1 = self.comboBox_country.count()
                for j in range(index1):
                    self.comboBox_country.removeItem(1)
                index2 = self.comboBox_city.count()
                for j in range(index2):
                    self.comboBox_city.removeItem(1)
                qy2 = "select country, bsname from bsinfo"
                cursor.execute(qy2)
                iy = cursor.fetchall()
                connection.commit()
                connection.close()

                country, city = zip(*iy)
                country = list(dict.fromkeys(country))
                city = list(dict.fromkeys(city))
                for i in range(len(country)):
                    greater.list_country.append(country[i])
                for j in range(len(city)):
                    greater.list_city.append(city[j])
                for k in range(len(greater.list_country)):
                    self.comboBox_country.addItem(greater.list_country[k])
                for h in range(len(greater.list_city)):
                    self.comboBox_city.addItem(greater.list_city[h])
                greater.list_country.clear()
                greater.list_city.clear()
                self.lineEdit_bsname2.clear()
                self.lineEdit_address2.clear()
                row_count = self.tableWidget2.rowCount()
                for i in range(row_count):
                    self.tableWidget2.removeRow(0)
                self.label_tool2_noti.setStyleSheet("""
                QLabel{color: rgb(30, 107, 255); font: 75 12pt "맑은 고딕";}""")
                self.label_tool2_noti.setText("철회가 완료 되었습니다.")
        except Exception as e:
            print(e)
            pass

    # data visualization
    def graph(self, state, button):
        self.label_main_noti.clear()
        self.hLayout1.takeAt(0)
        self.hLayout2.takeAt(0)
        self.label_main_noti.clear()
        self.comboBox_country.setCurrentIndex(0)
        self.comboBox_city.setCurrentIndex(0)
        try:
            if button == self.pushButton_graph1:
                self.stackedWidget_in_visualize.setCurrentWidget(self.page_graph1)
                connection = pymysql.connect \
                    (host='localhost', port=3306, user='root', password='0000', db='headquarter', charset='utf8')
                cursor = connection.cursor()
                qy = """
                SELECT SUM(sales), ddate FROM dsinfo
                GROUP BY ddate ORDER BY DDATE DESC LIMIT 7;
                """
                cursor.execute(qy)
                iy = cursor.fetchall()
                connection.commit()
                connection.close()
                print(iy)
                sales, ddate = zip(*iy)
                x = list(ddate)
                x = list(reversed(x))
                y = list(sales)

                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)
                ax.plot(x, y, 'b--o', label='Max')
                # ax.set_xticklabels(x)
                ax.set_xlabel('Day', size = 10)
                ax.set_ylabel('Sales', size = 10)
                ax.set_title('The sales per day for the past week', size = 20) #fig.suptitle
                # ax.text(1,1,'STARBUCKS')
                ax.legend()
                ax.grid()

                canvas = FigureCanvasQTAgg(fig)
                canvas.draw()
                self.hLayout1.addWidget(canvas)
                canvas.show()
            else:
                self.stackedWidget_in_visualize.setCurrentWidget(self.page_graph2)
                ddate = self.dateEdit.text()
                connection = pymysql.connect \
                    (host='localhost', port=3306, user='root', password='0000', db='headquarter', charset='utf8')
                cursor = connection.cursor()
                qy = """
                SELECT country, bsname, sales, ddate FROM dsinfo
                WHERE ddate = '{}'
                ORDER BY sales DESC limit 10;
                """
                cursor.execute(qy.format(ddate))
                iy = cursor.fetchall()
                connection.commit()
                connection.close()
                print(iy)
                print(list(reversed(iy)))
                reversed_iy = list(reversed(iy))
                if iy == ():
                    self.label_main_noti.setText('조회할 데이터가 없습니다.')
                else:
                    reversed_iy = list(reversed(iy))
                    country, bsname, sales, ddate = zip(*reversed_iy)
                    x_bsname = list(bsname)
                    print(x_bsname)
                    y_sales = list(sales)
                    print(y_sales)
                    e_country = list(country)
                    iy = list(zip(country, bsname))
                    # x = []
                    # for i in iy:
                    #     x.append(i[0]+"\n"+i[1])
                    #     print(i[0]+"\n"+i[1])
                    ddate = list(set(ddate))

                    miny, maxy = str(min(y_sales)), str(max(y_sales))
                    miny, maxy = miny[:2], int(maxy[:2]) + 1
                    maxy = str(maxy)
                    zero = '0' * 6
                    miny, maxy = miny + zero, maxy + zero

                    fig = plt.figure()
                    ax = fig.add_subplot(1, 1, 1)
                    ax.barh(x_bsname, y_sales, 0.5, color=['c'], label='sales')
                    plt.yticks(rotation = 45)
                    plt.xlim(int(miny), int(maxy))
                    for i in range(len(reversed_iy)):
                        plt.text(y_sales[i], x_bsname[i], e_country[i])
                    plt.ylabel('Country / City', size = 10)
                    plt.xlabel('Sales per day', size = 10)
                    plt.title('Top 10 store on {}'.format(ddate[0]), size = 20)
                    plt.legend()

                    canvas = FigureCanvasQTAgg(fig)
                    canvas.draw()
                    self.hLayout2.addWidget(canvas)
                    canvas.show()
        except Exception as e:
            print(e)
            pass

    ####################################################################################################################
    ####################################################################################################################
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def quit(self):
        self.close()

app = QApplication(sys.argv)
ch = window()
ch.show()
app.exec_()