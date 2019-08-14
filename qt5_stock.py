# coding=utf-8

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QCursor, QIcon, QColor, QPalette
import ctypes
import requests
import datetime

def getStock(stockName):
    response = requests.get('http://hq.sinajs.cn/list='+stockName)
    listdata = []
    for item in response.text.split(";"):
        if item.isspace():
            continue
        index0 = item.index("\"")
        item = item[index0+1:len(item)-1]
        itemList = item.split(",")
        stock = {}
        stock["name"] = itemList[0]
        oldPrice = float(itemList[2])
        price = float(itemList[3])
        zdfv = float('%.3f' % (price - oldPrice))
        zdf = float('%.2f' % (zdfv / oldPrice * 100))
        stock["oldPrice"] = oldPrice
        stock["price"] = price
        stock["zdfv"] = zdfv
        stock["zdf"] = zdf
        listdata.append(stock)
    return listdata

def getStockList():
    fo = open("stock.list", "r")
    return ",".join(fo.readlines()).replace("\n", "")

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.stockList = getStockList()
        l = len(self.stockList.split(","))
        height = l * 5
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(180, height)  # 悬浮窗宽/高设置
        self.move(1650, 100)  # 悬浮窗坐标, 以屏幕左上角为原点
        self.initUI()
    
    def initUI(self):
        self.label = QLabel()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.first = True
       
        self.stockData()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.stockData)
        self.timer.start(3000)  # 3秒定时刷新
        self.show()
        
    def stockData(self):
        if not self.checkInTime() and not self.first:
            return
        str = ""
        for item in getStock(self.stockList):
            name = item["name"]
            price = item["price"]
            zdfv = item["zdfv"]
            zdf = item["zdf"]
            str_n = '{0} {1} {2}({3}%)\n'.format(name, price, zdfv, zdf)
            str += str_n
        self.label.setText(str)
        self.first = False
    
    def checkInTime(self):
        amTimeStart = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:15', '%Y-%m-%d%H:%M')
        amTimeEnd =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'11:30', '%Y-%m-%d%H:%M')
        pmTimeStart = datetime.datetime.strptime(str(datetime.datetime.now().date())+'13:00', '%Y-%m-%d%H:%M')
        pmTimeEnd =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'15:00', '%Y-%m-%d%H:%M')
        nowTime = datetime.datetime.now()
        if amTimeStart <= nowTime and nowTime <= amTimeEnd or pmTimeStart <= nowTime and nowTime <= pmTimeEnd:
            return True
        return False

    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my = MyApp()
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    sys.exit(app.exec_())
