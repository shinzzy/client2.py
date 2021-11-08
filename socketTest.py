import pandas as pd
from PyQt5.QtWidgets import *
import pyautogui as pg
import pymysql
from PyQt5 import uic
import sys, datetime
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import pyqtSlot, QTimer, QThread, pyqtSlot
from PyQt5 import QtCore
import socketio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from pandas import Series, DataFrame
from matplotlib.figure import Figure

page1 = uic.loadUiType("stock.ui")[0]

class SocketClient(QThread):
    add_chat = QtCore.pyqtSignal(str)
    sio = socketio.Client()

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.is_run = False
        self.ip = 5000
        self.localhost = 'localhost'

    def set_host(self, ip, port):
        self.ip = ip
        self.port = port

    def run(self):
        host = 'http://%s:%s' % (self.ip, self.port)

        self.connect(host)
        self.is_run = not self.is_run

    def connect(self, host):
        SocketClient.sio.on('receive', self.receive)
        SocketClient.sio.connect(host)
        self.add_chat.emit('채팅 서버와 접속 완료했습니다.')

    def send(self, msg):
        SocketClient.sio.emit('send', msg)
        self.add_chat.emit('[나]:%s' % (msg))

    def receive(self, msg):
        self.add_chat.emit('[상대방] %s' % (msg))

class MainWindow(QMainWindow, page1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.send.clicked.connect(self.send_message)                    #메세지전송하기
        self.sc = SocketClient(self)                                    #통신
        self.sc.add_chat.connect(self.add_chat)                         #통신

        self.pushButton_2.clicked.connect(self.gotosignPage)        #회원가입클릭으로 회원가입페이지로 이동
        self.pushButton_idcheck.clicked.connect(self.idCheck)       #아이디 중복확인
        self.ID = ''                                                #아이디체크
        self.ID2 =''
        self.pushButton_signup.clicked.connect(self.signUp)         #회원가입버튼클릭
        self.pushButton_login.clicked.connect(self.login)           #로그인버튼 클릭시
        self.buy.clicked.connect(self.buy_1)                        ## 매수 버튼
        self.sell.clicked.connect(self.sell_1)                      ## 매도 버튼
        self.lcdNumber.setDigitCount(10)                            ## lcdnumber 자릿수 표현

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.graph.addWidget(self.canvas)
        self.ax = self.fig.add_subplot()
        self.ax.set_xlim([9, 15])

    def gotosignPage(self):         #회원가입페이지로 이동
        self.stackedWidget.setCurrentWidget(self.page_5)

    def idCheck(self):          #아이디 중복체크
        Id = self.textEdit_id.toPlainText()
        existId = []
        if len(Id) == 0:
            self.label_signUp.setText('아이디를 입력해주세요.')

        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
        cur = conn.cursor()
        sql = "select ID from member"
        cur.execute(sql)
        id2 = cur.fetchall()
        for i in id2:
            existId.append(i[0])
        if Id in existId:
            self.label_signUp.setText('사용할 수 없는 아이디입니다.')
            self.textEdit_id.clear()
        else:
            QMessageBox.information(self, '알림', '사용할 수 있는 아이디입니다~~~')
            self.label_signUp.setText('')
            self.ID = Id
        conn.close()

    def signUp(self):                   #회원가입
        if self.ID == self.textEdit_id.toPlainText():
            if len(self.textEdit_pw.toPlainText()) > 0:
                pw1 = self.textEdit_pw.toPlainText()
                pw2 = self.textEdit_pw2.toPlainText()
                if pw1 == pw2:
                    Id = self.textEdit_id.toPlainText()
                    QMessageBox.about(self, '알림', '회원가입이 완료되었습니다. 10만원이 자동충전됨')
                    conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock',
                                           charset='utf8')
                    cur = conn.cursor()
                    sql = "insert into member values('{}', '{}', '{}')".format(Id, pw1, 100000)
                    cur.execute(sql)
                    conn.commit()

                    sql = "select Name from market"
                    cur.execute(sql)
                    name1 =cur.fetchall()
                    for i in name1:
                        sql = "insert into bank values('{}', '{}', {})".format(self.ID, i[0], 0)
                        cur.execute(sql)
                        conn.commit()
                    conn.close()

                    self.stackedWidget.setCurrentWidget(self.page_2)
                else:
                    self.label_signUp.setText('비밀번호를 확인해주세요')

            else:
                self.label_signUp.setText('비밀번호를 입력해주세요')
        else:
            self.label_signUp.setText('아이디 중복체크를 해주세요.')

    def login(self):                #로그인
        id = self.textEdit.toPlainText()
        pw = self.textEdit_2.toPlainText()
        id2 = []
        pw2 = []
        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock',
                               charset='utf8')
        cur = conn.cursor()
        sql = "select ID from member"
        cur.execute(sql)
        idid = cur.fetchall()
        for i in idid:
            id2.append(i[0])
        if id in id2:
            sql2 = "select PW from member where ID = '{}'".format(id)
            cur.execute(sql2)
            pwpw = cur.fetchone()
            for i in pwpw:
                pw2.append(i)
            print(pw2)
            if pw == pw2[0]:
                self.ID2 = id

                ip = '127.0.0.1'
                port = 5000

                if (not ip) or (not port):
                    self.add_chat('ip 또는 port 번호가 비었습니다.')
                    return

                self.sc.set_host(ip, port)

                if not self.sc.is_run:
                    self.sc.start()
                self.stackedWidget.setCurrentWidget(self.page)
                #############로그인 완료. 시간세기 시작
                self.hour = 9
                self.min = 0
                self.day = 1
                self.spinBox.setMaximum(100)
                self.spinBox.setMinimum(1)
                # self.search.clicked.connect(self.doge)
                self.timer = QTimer(self)
                self.timer.start(100)
                self.timer.timeout.connect(self.timeout)
                self.deletetable()
                self.doge()  # price_record 테이블에 insert
                sql = "select Name from market"
                cur.execute(sql)
                aa = cur.fetchall()

                for i in aa:
                    self.comboBox.addItem("{}".format(i[0]))
                #self.draw()
                self.draw1()
                self.bank()
                conn.commit()
                conn.close()
            else:
                self.label_7.setText('비밀번호를 확인해주세요')
        else:
            self.label_7.setText('아이디를 확인해주세요')

    def send_message(self):                 #메세지 전송버튼
        if not self.sc.is_run:
            self.add_chat('서버와 연결이 끊겨 메세지를 전송할 수 없습니다.')
            return

        msg = self.lineEdit.text()
        self.sc.send(msg)
        #self.add_chat('[나] %s'%(msg))
        self.lineEdit.clear()

    @pyqtSlot(str)
    def add_chat(self, msg):                    #메세지를 채팅창에 띄우기
        self.listWidget.addItem(msg)

    @pyqtSlot()
    def timeout(self):
        vrtime = "{}일차 {}시 {}분".format(self.day, self.hour, self.min)
        self.time.setText(vrtime)
        self.min += 1

        if self.min == 60:      #한시간이 지났을 때
            self.min = 0
            self.hour += 1
            #graph, 주식 가격 변동 함수
            self.musk()
            self.draw()
            self.draw1()

        if self.hour == 15 and self.min == 30:      #하루가 지났을 때
            self.hour = 9
            self.day += 1
            a = pg.alert(text='주식시장이 마감했습니다. 1분간 휴식하세요', title='알림', button='OK')
            self.musk2()
            print(a)

    def musk2(self):
        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
        cur = conn.cursor()
        sql = "select Name, Price from market"
        cur.execute(sql)
        Each = cur.fetchall()
        for i in Each:
            sql = "update price_record set Price9 = {} where date1 = {} and Name = '{}'".format(i[1], self.day, i[0])
            cur.execute(sql)
            conn.commit()

        conn.close()

    ## 주가변동 알고리즘
    def musk(self):
        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
        cur = conn.cursor()
        sql = "select Name, each1, Now_each, Price from market"
        cur.execute(sql)
        Each = cur.fetchall()
        for i in Each:
            # 증감폭에 따른 변수
            a = [1.1, 1.15, 1.2, 1.25, 1.3]  # 300이상
            b = [1.05, 1.1, 1.15, 1.2, 1.25]  # 200개이상
            c = [1, 1.05, 1.1, 1.15, 1.2]  # 100개 이상
            d = [0.9, 0.95, 1, 1.05, 1.1]  # 0 ~ -100
            e = [0.8, 0.85, 0.9, 1, 1.05]  # -100 ~ -200
            f = [0.7, 0.75, 0.8, 0.85, 0.9]     # -300 ~ -200
            name = i[0]
            randomnum = random.randrange(0,5)
            updown = i[1] - i[2]                #증감

            ## 주가변동
            if updown >= 300:
                sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(a[randomnum], name)
                cur.execute(sql)
                conn.commit()
            elif updown >= 200:
                sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(b[randomnum], name)
                cur.execute(sql)
                conn.commit()
            elif updown >= 100:
                sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(c[randomnum], name)
                cur.execute(sql)
                conn.commit()
            elif updown <= 0:
                sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(d[randomnum], name)
                cur.execute(sql)
                conn.commit()
            elif updown <= -100:
                sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(e[randomnum], name)
                cur.execute(sql)
                conn.commit()
            elif updown <= -200:
                sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(f[randomnum], name)
                cur.execute(sql)
                conn.commit()

            # ## 개수를 현재개수로 바꾸는 쿼리
            sql = "update market set each1 = Now_each where Name = '{}'".format(i[0])
            cur.execute(sql)
            conn.commit()

            ## 변화된 가격을 price_record 에 기록
            sql = "update price_record set Price{} = (select Price from market where name = '{}') where date1 = {} and name = '{}'".format(self.hour, name, self.day, name)
            cur.execute(sql)
            conn.commit()
        conn.close()


    def doge(self):         #price_record 에 테이블에 회사이름 날짜만 집어넣기
        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
        cur = conn.cursor()
        sql = "select Name, Price from market"
        cur.execute(sql)
        Each = cur.fetchall()

        date = range(1, 31)
        for j in date:                  #테이블에 데이터 만들기
            for i in Each:
                sql = "insert into price_record(Name, date1) values ('{}',{})".format(i[0], j)
                # sql = "insert into price_record values ('{}',{},{},{},{},{},{},{},{})".format(i[0], 0,0,0,0,0,0,0, j)
                cur.execute(sql)
                conn.commit()

                #첫째날아홉시는 강제로 넣기
                # sql = "update price_record set Price9 = {} where Name = '{}' and date1 = 1".format(i[1], i[0])
                sql = "update price_record set Price9 = {} where Name = '{}' and date1 = 1".format(i[1], i[0])
                cur.execute(sql)
                conn.commit()
        conn.close()

    def draw(self): ## 그래프 그려주는 함수
        # # for draw graph
        self.ax.clear()
        self.ax.set_xlim([9, 15])
        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
        cur = conn.cursor()
        sql = "select Name, Price9, Price10, Price11, Price12, Price13, Price14, Price15 from price_record where date1 = {}".format(self.day)
        cur.execute(sql)

        Cname = cur.fetchall()
        df = pd.DataFrame()

        time = [9, 10, 11, 12, 13, 14, 15]
        time_a = []
        name = []
        price = []
        for i in Cname:

            self.ax.legend(['sanghee222', 'ryu', 'threestar', 'lifeisgood', 'jisu', 'pineapple', 'cosla', 'KT', 'nanosoft', 'mega'])
            for j in range(1,8):
                if i[j] == None:
                    break
                else:
                    price.append(int(i[j]))
            name.append(i[0])
            name_a = name*len(price)
            rangeaa = 0
            while True:
                if rangeaa < len(price):
                    time_a.append(time[rangeaa])
                    rangeaa += 1
                else:
                    break

            print(" 여기는 원형 데이터")
            print(name_a)
            print(price)
            print(time_a)
            df['time'] = time_a
            df['name'] = name_a
            df['price'] = price

            a = "time"
            b = "price"
            c = "name"

            row_data = {a : df['time'], b: df['price'], c: df['name']}
            data = DataFrame(row_data)
            print(" dictionarytyyyyyy ")
            print(data)

            a_price = data["price"]
            a_time = data["time"]
            print("a_xxxxxx ?")
            print(a_price)
            print(a_time)

            self.ax.plot(a_time, a_price, marker= 'o')
            plt.title("hihihihi")
            self.canvas.draw()
            price.clear()
            name.clear()
            time_a.clear()
        conn.commit()
        conn.close()

    def draw1(self): ## 주식시장 가격테이블
        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
        cur = conn.cursor()
        sql2 = "select Name, Price, Now_each from market"
        cur.execute(sql2)
        Each = cur.fetchall()
        num = 0
        self.tableWidget_2.setRowCount(5)
        self.tableWidget_3.setRowCount(5)
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        for i in Each:
            if num < 5:
                self.tableWidget_2.setItem(num, 0, QTableWidgetItem(str(i[0])))
                self.tableWidget_2.setItem(num, 1, QTableWidgetItem(str(i[1])))
                self.tableWidget_2.setItem(num, 2, QTableWidgetItem(str(i[2])))
            else:
                self.tableWidget_3.setItem(num-5, 0, QTableWidgetItem(str(i[0])))
                self.tableWidget_3.setItem(num-5, 1, QTableWidgetItem(str(i[1])))
                self.tableWidget_3.setItem(num-5, 2, QTableWidgetItem(str(i[2])))
            num += 1
        sql = "select money from member where id = '{}'".format(self.ID2)
        cur.execute(sql)
        money = cur.fetchone()
        print(money[0])
        int(money[0])
        self.lcdNumber.display(money[0])
        self.label_8.setText(money[0])
        conn.close()

    def deletetable(self):              ## price_record 테이블 데이터 삭제
        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
        cur = conn.cursor()
        sql = "delete from price_record"
        cur.execute(sql)
        conn.commit()
        conn.close()


    def buy_1(self): ## 주식 구매
        each = self.spinBox.value()     #내가 구매하려는 주식 양
        name = self.comboBox.currentText()      #내가 구매하려는 회사명
        price1 = self.label_8.text()           #내가 보유한 돈
        price = int(price1)
        # monHave = int(price)              #내가 보유한 돈
        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
        cur = conn.cursor()

        sql = "select Now_each, Price from market where Name = '{}'".format(name)
        cur.execute(sql)
        all1 = cur.fetchall()
        comHave = all1[0][0]            #회사가 보유한 주식
        comPrice = all1[0][1]           #그회사주식의 평균가격

        sum = comPrice * each
        if each < comHave:
            if sum < price:
                sql = "update market set Now_each = Now_each - {} where Name = '{}'".format(each, name)
                cur.execute(sql)
                conn.commit()

                sql = "update bank set Each1 = Each1 + {} where ID = '{}' and Name = '{}'".format(each, self.ID2, name)
                cur.execute(sql)
                conn.commit()

                sql = "update member set Money = Money - {} where ID = '{}'".format(sum, self.ID2)
                cur.execute(sql)
                conn.commit()
                conn.close()
            else:
                QMessageBox.about(self, '알림', '주식이 너무 비싸서 당신의 돈으로 살 수 없어요 양을 줄여보세요')
        else:
            QMessageBox.about(self,'알림','구매하려는 주식이 많습니다.')
        self.draw1()
        self.bank()

    def sell_1(self): ## 주식 판매
        each = self.spinBox.value()     #내가 판매하려는 주식 양
        name = self.comboBox.currentText()      #내가 판매하려는 회사명
        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
        cur = conn.cursor()
        sql = "select Each1 from bank where ID = '{}' and Name = '{}'".format(self.ID2, name)
        cur.execute(sql)
        MY1 = cur.fetchone()
        MY = MY1[0]     #내가가진 주식보유

        sql = "select Price, Now_each from market where Name = '{}'".format(name)
        cur.execute(sql)
        avg = cur.fetchall()
        print(avg)
        avgPrice = avg[0][0]
        Now_each = avg[0][1]

        sum = avgPrice * each
        if each <= MY:
            sql = "update bank set Each1 = Each1 - {} where ID = '{}' and Name = '{}'".format(each, self.ID2, name)
            cur.execute(sql)
            conn.commit()

            sql = "update member set Money = Money + {} where ID = '{}'".format(sum, self.ID2)
            cur.execute(sql)
            conn.commit()

            sql = "update market set Now_each = Now_each + {} where Name = '{}'".format(each, name)
            cur.execute(sql)
            conn.commit()
            conn.close()
        else:
            QMessageBox.about(self, '알림', '내가 보유한 주식보다 많이 판매하려고합니다')
        self.draw1()
        self.bank()


    def bank(self):     #주식보유량 테이블위젯 업데이트
        conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
        cur = conn.cursor()
        sql = "select Name, Each1 from bank where ID ='{}'".format(self.ID2)
        cur.execute(sql)
        stock = cur.fetchall()

        self.tableWidget_4.setRowCount(10)
        self.tableWidget_4.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_4.horizontalHeader().setStretchLastSection(True)
        num = 0
        for i in stock:
            self.tableWidget_4.setItem(num, 0, QTableWidgetItem(str(i[0])))
            self.tableWidget_4.setItem(num, 1, QTableWidgetItem(str(i[1])))
            num += 1
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()