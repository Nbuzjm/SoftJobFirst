from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, random

from GameWindow import Ui_MainWindow

class Player:
    dir=[[-1,0],[1,0],[0,1],[0,-1]]
    def __init__(self, x, y, p):
        self.x = x
        self.y = y
        self.speed = 5
        self.t = QtWidgets.QLabel(p)
        self.t.setPixmap(QtGui.QPixmap(r"C:\Users\zhenxs\PycharmProjects\SoftProjectDemo\Game\image\person.png"))
        self.t.setGeometry(QtCore.QRect(70 + 40 * x, 50 + 40 * y, 40, 40))

    def move(self, type):
        xp = self.x+ self.dir[type][0]
        yp = self.y+ self.dir[type][1]
        if xp < 0 or xp > 9 or yp < 0 or yp >  9:
            return
        else:
            self.x=xp
            self.y=yp
            self.t.setGeometry(QtCore.QRect(70 + 40 * self.x, 50 + 40 * self.y, 40, 40))

    def getSpeed(self):
        return int(1000//self.speed)

    def getPos(self):
        return [self.x,self.y]


class bomb:
    def __init__(self, num, bobRange, interval):
        self.num = num
        self.bombRange=bobRange
        self.interval =interval
        self.bombs =[]

    def upDate(self):
        self.bombs=[]
        for i in range(self.num):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            z = random.randint(1,self.bombRange)
            self.bombs.append([x,y,z])

    def getBombs(self):
        # print(self.bombs)
        return self.bombs

    def getInterval(self):
        return int(self.interval)

class GameBoard(QMainWindow,Ui_MainWindow):
    mat = [[0 for i in range(10)] for j in range(10)]
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.score = 0
        self.bombCounter =0
        self.buildBomb()
        self.buildGraph()
        self.buildPlayer()
        self.buildTimer()

    def buildBomb(self):
        self.bombs=bomb(10,3,2000)
        self.bombs.upDate()

    def buildGraph(self):
        for i in range(10):
            for j in range(10):
                t = QtWidgets.QLabel(self.centralwidget)
                t.setPixmap(QtGui.QPixmap(r"C:\Users\zhenxs\PycharmProjects\SoftProjectDemo\Game\image\bot.png"))
                t.setGeometry(QtCore.QRect(70+40*i, 50+40*j, 40, 40))
                t.setObjectName("block"+str(i)+str(j))
                self.mat[i][j]=t

    def buildPlayer(self):
        x=random.randint(0,9)
        y=random.randint(0,9)
        self.player=Player(x,y,self.centralwidget)

    def buildTimer(self):
        self.flag=True

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.setInterval(self.player.getSpeed())
        self.timer.start()

        self.bombTimer=QTimer()
        self.bombTimer.timeout.connect(self.bombTime)
        self.bombTimer.setInterval(100)
        self.bombTimer.start()

        self.scoreTimer = QTimer()
        self.scoreTimer.timeout.connect(self.updateScore)
        self.scoreTimer.setInterval(50)
        self.scoreTimer.start()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Space:
            self.scoreTimer.start()
            self.bombTimer.start()
            self.timer.start()
            self.recover()
            self.bombCounter=0
            self.score = 0
            self.flag = True
            return

        if self.flag==False :
            return
        if key == Qt.Key_Left:
            self.player.move(0)
        elif key == Qt.Key_Right:
            self.player.move(1)
        elif key == Qt.Key_Down:
            self.player.move(2)
        elif key == Qt.Key_Up:
            self.player.move(3)
        else:
            return
        self.timer.start()
        self.flag=False

    def updateScore(self):
        self.score += 1
        self.scoreLabel.setText(str(self.score))

    def showTime(self):
        self.flag=True
        self.timer.stop()

    def bombTime(self):
        self.bombCounter += 1
        if self.bombCounter==12:
            self.placeBombs()
        elif self.bombCounter==22:
            self.bang()
        elif self.bombCounter==23:
            if self.check()== False:
                self.recover()
                self.bombs.upDate()
                self.bombCounter=0

    def placeBombs(self):
        p = self.bombs.getBombs()
        for u in p:
            self.mat[u[0]][u[1]].setPixmap(QtGui.QPixmap(r"C:\Users\zhenxs\PycharmProjects\SoftProjectDemo\Game\image\bomb.png"))
        self.temp = [[0 for i in range(10)] for j in range(10)]
        for k in p:
            for i in range(k[0]-k[2],k[0]+k[2]+1):
                if i>=0 and i<=9:
                    self.temp[i][k[1]]=1
            for i in range(k[1]-k[2],k[1]+k[2]+1):
                if i>=0 and i<=9:
                    self.temp[k[0]][i]=1

    def recover(self):
        for u in self.mat:
            for v in  u:
                v.setPixmap(QtGui.QPixmap(r"C:\Users\zhenxs\PycharmProjects\SoftProjectDemo\Game\image\bot.png"))

    def bang(self):
        for i in range(10):
            for j in range(10):
                if self.temp[i][j]==1:
                    self.mat[i][j].setPixmap(QtGui.QPixmap(r"C:\Users\zhenxs\PycharmProjects\SoftProjectDemo\Game\image\after.png"))

    def check(self):
        x,y = self.player.getPos()
        if self.temp[x][y]==1:
            self.scoreTimer.stop()
            self.bombTimer.stop()
            self.timer.stop()
            self.flag = False
            return True
        return False


if __name__ == '__main__':
    app = QApplication([])
    game = GameBoard()
    game.show()
    sys.exit(app.exec_())