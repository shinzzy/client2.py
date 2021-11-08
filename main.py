import time

from PyQt5.QtWidgets import *
import pyautogui as pg
import pymysql
from PyQt5 import uic
import sys, datetime
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import pyqtSlot, QTimer
import pythreading



#
#
# page1 = uic.loadUiType("stock.ui")[0]
#
# class MainWindow(QMainWindow, page1):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.hour = 9
#         self.min = 0
#         self.day = 1
#         self.spinBox.setMaximum(100)
#         #self.search.clicked.connect(self.doge)
#         self.timer = QTimer(self)
#         self.timer.start(100)
#         self.timer.timeout.connect(self.timeout)
#         self.doge()  # price_record 테이블에 insert
#         conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
#         cur = conn.cursor()
#         sql = "select Name from market where Price > 100"
#         cur.execute(sql)
#         aa = cur.fetchall()
#
#         for i in aa:
#             self.comboBox.addItem("{}".format(i[0]))
#
#         self.tableWidget.setRowCount(10)
#         self.tableWidget.setColumnCount(4)
#         sql1 = "select * from market"
#         cur.execute(sql1)
#         bb = cur.fetchall()
#         print(bb[0][0])
#         j = 0
#         for i in bb:
#             cc = str(i[1])
#             dd = str(i[2])
#             ee = str(i[3])
#             self.tableWidget.setItem(j, 0, QTableWidgetItem(i[0]))
#             self.tableWidget.setItem(j, 1, QTableWidgetItem(cc))
#             self.tableWidget.setItem(j, 2, QTableWidgetItem(dd))
#             self.tableWidget.setItem(j, 3, QTableWidgetItem(ee))
#             j += 1
#
#         conn.commit()
#
#
#
#
#     @pyqtSlot()
#     def timeout(self):
#         vrtime = "{}일차 {}시 {}분".format(self.day, self.hour, self.min)
#         self.time.setText(vrtime)
#         self.min += 1
#
#
#
#         if self.min == 60:      #한시간이 지났을 때
#             self.min = 0
#             self.hour += 1
#             #graph, 주식 가격 변동 함수
#             self.musk()
#
#         if self.hour == 15 and self.min == 30:      #하루가 지났을 때
#             self.hour = 9
#             self.day += 1
#             a = pg.alert(text='주식시장이 마감했습니다. 1분간 휴식하세요', title='알림', button='OK')
#             self.musk2()
#             print(a)
#         # if self.day == 30:
#
#
#     def musk2(self):
#         conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
#         cur = conn.cursor()
#         sql = "select Name, Price from market"
#         cur.execute(sql)
#         Each = cur.fetchall()
#         for i in Each:
#             sql = "update price_record set Price9 = {} where date1 = {} and Name = '{}'".format(i[1], self.day, i[0])
#             cur.execute(sql)
#             conn.commit()
#
#         conn.close()
#
#     ## 주가변동 알고리즘
#     def musk(self):
#         conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
#         cur = conn.cursor()
#         sql = "select Name, each1, Now_each, Price from market"
#         cur.execute(sql)
#         Each = cur.fetchall()
#
#         for i in Each:
#             # 증감폭에 따른 변수
#             a = [1.1, 1.15, 1.2, 1.25, 1.3]  # 300이상
#             b = [1.05, 1.1, 1.15, 1.2, 1.25]  # 200개이상
#             c = [1, 1.05, 1.1, 1.15, 1.2]  # 100개 이상
#             d = [0.9, 0.95, 1, 1.05, 1.1]  # 0 ~ -100
#             e = [0.8, 0.85, 0.9, 1, 1.05]  # -100 ~ -200
#             f = [0.7, 0.75, 0.8, 0.85, 0.9]     # -300 ~ -200
#             name = i[0]
#             randomnum = random.randrange(0,5)
#             updown = i[1] - i[2]                #증감
#
#             ## 주가변동
#             if updown >= 300:
#                 sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(a[randomnum], name)
#                 cur.execute(sql)
#                 conn.commit()
#             elif updown >= 200:
#                 sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(b[randomnum], name)
#                 cur.execute(sql)
#                 conn.commit()
#             elif updown >= 100:
#                 sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(c[randomnum], name)
#                 cur.execute(sql)
#                 conn.commit()
#             elif updown <= 0:
#                 sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(d[randomnum], name)
#                 cur.execute(sql)
#                 conn.commit()
#             elif updown <= -100:
#                 sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(e[randomnum], name)
#                 cur.execute(sql)
#                 conn.commit()
#             elif updown <= -200:
#                 sql = "UPDATE market SET Price = Price * {} WHERE Name = '{}'".format(f[randomnum], name)
#                 cur.execute(sql)
#                 conn.commit()
#
#             # ## 개수를 현재개수로 바꾸는 쿼리
#             sql = "update market set each1 = Now_each where Name = '{}'".format(i[0])
#             cur.execute(sql)
#             conn.commit()
#
#
#             ## 변화된 가격을 price_record 에 기록
#             sql = "update price_record set Price{} = (select Price from market where name = '{}') where date1 = {} and name = '{}'".format(self.hour, name, self.day, name)
#             cur.execute(sql)
#             conn.commit()
#
#
#         conn.close()
#
#
#
#     def doge(self):         #price_record 에 테이블에 회사이름 날짜만 집어넣기
#         conn = pymysql.connect(host='10.10.21.108', user='root', password='1234', db='stock', charset='utf8')
#         cur = conn.cursor()
#         sql = "select Name, Price from market"
#         cur.execute(sql)
#         Each = cur.fetchall()
#
#         date = range(1, 31)
#         for j in date:                  #테이블에 데이터 만들기
#             for i in Each:
#                 sql = "insert into price_record(Name, date1) values ('{}',{})".format(i[0], j)
#                 cur.execute(sql)
#                 conn.commit()
#
#                 #첫째날아홉시는 강제로 넣기
#                 sql = "update price_record set Price9 = {} where Name = '{}' and date1 = 1".format(i[1], i[0])
#                 cur.execute(sql)
#                 conn.commit()
#
#
#         conn.close()
#
#
#
#
#
#     # def elon(self):
#     #     sql = "update market set Now_each"
#
#     # def refresh_prcie(self):
#
#     # def refresh_each(self):
#
#
#
#
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myWindow = MainWindow()
#     myWindow.show()
#     app.exec_()

import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series, DataFrame

# df = pd.DataFrame()
# df['days'] = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']*3 ## 요일
# df['visits'] = [32,23,14,14,27,40,35,37,28,9,41,29,33,21,45,33,9,11,10,12,27] ## 방문 고객수
# df['corp'] = ['A']*7 + ['B']*7 + ['C']*7 ## 회사명
#
# ## 3개 데이터 분리
# a_df = df.query('corp =="A"')
# a_visits = a_df['visits']
# days = a_df['days']
#
# print('-----------------------')
# print(type(a_df), " , ", a_df)
# print(type(a_visits), " , ", a_visits)
# print(type(days), " , ", days)
# b_df = df.query('corp =="B"')
# b_visits = b_df['visits']
#
# c_df = df.query('corp =="C"')
# c_visits = c_df['visits']
#
# fig = plt.figure(figsize=(8, 8))  ## 캔버스 생성
# fig.set_facecolor('white')  ## 캔버스 색상 설정
# ax = fig.add_subplot()  ## 그림 뼈대(프레임) 생성
#
# ax.plot(days, a_visits, marker='o', label='A')  ## 선그래프 생성
# ax.plot(days, b_visits, marker='o', label='B')
# ax.plot(days, c_visits, marker='o', label='C')
#
# ax.legend()  ## 범례
#
# plt.title('Sales for last weekdays', fontsize=20)  ## 타이틀 설정
# plt.show()
#
# a = 'col1'
# b = 'col2'
# c = [1,2,3,4]
# d = [1,2,3,4]
#
# row_data = {a : c, b : d}
# data = DataFrame(row_data)
# print("----------------------!-------------=")
# print(data)


list = [9,10,11,12,13,14,15]
a = 3
list_a = []
print(list_a)
b = 0
while True:
    if b < a:
        list_a.append(list[b])
        b += 1
    else:
        break

print(list_a)