import random
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication
from Game.GameWindow import Ui_MainWindow

class Player:
    dir = [[-1, 0], [1, 0], [0, 1], [0, -1]]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

    def move(self, type):
        xp = self.x + self.dir[type][0]
        yp = self.y + self.dir[type][1]
        if xp < 0 or xp > 9 or yp < 0 or yp > 9:
            return
        else:
            self.x = xp
            self.y = yp

    def updateSpeed(self):
        self.speed +=1

    def getSpeedLayer(self):
        return self.speed

    def getSpeed(self):
        return int(1000 // self.speed)

    def getPos(self):
        return [self.x, self.y]


class Bomb:
    def __init__(self, num, bobRange, interval):
        self.num = num
        self.bombRange = bobRange
        self.interval = interval
        self.bombs = []

    def updateNum(self):
        self.num +=1

    def updateBobRange(self):
        self.bombRange+= 1

    def updateBobRange(self):
        self.interval -=50


    def upDate(self):
        self.bombs = []
        for i in range(self.num):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            z = random.randint(1, self.bombRange)
            self.bombs.append([x, y, z])

    def getBombs(self):
        return self.bombs

    def getBombNum(self):
        return self.num

    def getBombRange(self):
        return self.bombRange

    def getInterval(self):
        return int(self.interval)


class Board:
    mat = [[0 for i in range(10)] for j in range(10)]

    def __init__(self):
        self.start()

    def start(self):
        for i in range(10):
            for j in range(10):
                self.mat[i][j] = 0

    def placeBombs(self, p):
        for u in p:
            self.mat[u[0]][u[1]] = 1

    def bang(self, p):
        for k in p:
            for i in range(k[0] - k[2], k[0] + k[2] + 1):
                if i >= 0 and i <= 9:
                    self.mat[i][k[1]] = 2
            for i in range(k[1] - k[2], k[1] + k[2] + 1):
                if i >= 0 and i <= 9:
                    self.mat[k[0]][i] = 2

    def getState(self, x, y):
        return self.mat[x][y]

    def getMat(self):
        return self.mat


class GameController(QMainWindow, Ui_MainWindow):
    mat = [[0 for i in range(10)] for j in range(10)]

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dataIni()
        self.buildGraph()
        self.start()

    def dataIni(self):
        self.score = 0
        self.case = 0
        self.bombCounter = 0
        self.buildBomb()
        self.buildPlayer()

    def buildBomb(self):
        self.bombs = Bomb(5, 2, 2000)
        self.bombs.upDate()

    def buildPlayer(self):
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        self.player = Player(x, y)

        x = random.randint(0, 9)
        y = random.randint(0, 9)
        self.playerPlus = Player(x, y)


    def buildGraph(self):
        self.board = Board()
        for i in range(10):
            for j in range(10):
                t = QtWidgets.QLabel(self.centralwidget)
                t.setPixmap(QtGui.QPixmap("./Game/image/bot.png"))
                t.setGeometry(QtCore.QRect(70 + 40 * i, 50 + 40 * j, 40, 40))
                self.mat[i][j] = t

        self.gg = QtWidgets.QLabel(self.centralwidget)
        self.gg.setPixmap(QtGui.QPixmap("./Game/image/person.png"))

        self.ggg = QtWidgets.QLabel(self.centralwidget)
        self.ggg.setPixmap(QtGui.QPixmap("./Game/image/person1.png"))

        self.personUpdate()
        self.numShowUpdate()
        self.rangeShowUpdate()
        self.speedShowUpdate()

    def start(self):

        self.flag = True
        self.timer = QTimer()
        self.timer.timeout.connect(self.playerClk)
        self.timer.setInterval(self.player.getSpeed())
        self.timer.start()

        self.bombTimer = QTimer()
        self.bombTimer.timeout.connect(self.bombTime)
        self.bombTimer.setInterval(100)
        self.bombTimer.start()

        self.scoreTimer = QTimer()
        self.scoreTimer.timeout.connect(self.updateScore)
        self.scoreTimer.setInterval(50)
        self.scoreTimer.start()

    def restart(self):
        self.dataIni()
        self.personUpdate()
        self.numShowUpdate()
        self.rangeShowUpdate()
        self.speedShowUpdate()
        self.start()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Space:
            self.recover()
            self.mapShowUpdate()
            self.restart()
            return

        if self.flag == False:
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
        self.personUpdate()
        self.timer.start()
        self.flag = False

    def updateScore(self):
        self.score += 1
        self.scoreLabel.setText(str(self.score))

    def playerClk(self):
        self.flag = True
        self.timer.stop()

    def bombTime(self):
        self.bombCounter += 1
        if self.bombCounter == 12:
            self.placeBombs()
            self.mapShowUpdate()
        elif self.bombCounter == 22:
            self.bang()
            self.mapShowUpdate()
        elif self.bombCounter == 23:
            if self.check() == False:
                self.recover()
                self.mapShowUpdate()
                self.case +=1
                if self.case %3 == 0:
                    self.bombs.updateNum()
                    self.numShowUpdate()
                elif self.case %7== 0:
                    self.bombs.updateBobRange()
                    self.rangeShowUpdate()
                elif self.case %16==0:
                    self.player.updateSpeed()
                    self.speedShowUpdate()
                self.bombs.upDate()
                self.bombCounter = 0

    def placeBombs(self):
        p = self.bombs.getBombs()
        self.board.placeBombs(p)

    def recover(self):
        self.board.start()

    def bang(self):
        self.board.bang(self.bombs.getBombs())

    def check(self):
        x, y = self.player.getPos()
        if self.board.getState(x, y) == 2:
            self.scoreTimer.stop()
            self.bombTimer.stop()
            self.timer.stop()
            self.flag = False
            return True
        return False

    def personUpdate(self):
        x, y = self.player.getPos()
        self.gg.setGeometry(QtCore.QRect(70 + 40 * x, 50 + 40 * y, 40, 40))

    def mapShowUpdate(self):
        p = self.board.getMat()
        for i in range(10):
            for j in range(10):
                t = self.mat[i][j]
                if p[i][j] == 0:
                    t.setPixmap(QtGui.QPixmap("./Game/image/bot.png"))
                elif p[i][j] == 1:
                    t.setPixmap(QtGui.QPixmap("./Game/image/bomb.png"))
                elif p[i][j] == 2:
                    t.setPixmap(QtGui.QPixmap("./Game/image/after.png"))

    def speedShowUpdate(self):
        self.speedLabel.setText(str(self.player.getSpeedLayer()))

    def numShowUpdate(self):
        self.numLabel.setText(str(self.bombs.getBombNum()))

    def rangeShowUpdate(self):
        self.rangeLabel.setText(str(self.bombs.getBombRange()))


if __name__ == '__main__':
    app = QApplication([])
    game = GameController()
    game.show()
    sys.exit(app.exec_())
