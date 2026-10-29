import sys

from PySide6.QtCore import QLocale, QPoint, QRect, QSize, Qt, QTimer, QElapsedTimer
from PySide6.QtWidgets import QApplication, QSizePolicy, QWidget
from PySide6.QtGui import QCursor, QFont, QIcon, QPaintEvent, QPainter, QColor, QPalette, QRegion

import win32api
import win32con


# ===============================================       Globals     ==========================================================


mx:int
my:int
mdown:bool


# ===============================================       Classes     ==========================================================


class Rectangle:
    def __init__(self,name:str,position:tuple[int,int]=(0,0),size:tuple[int,int]=(100,100),color:QColor=QColor(255,0,0,255)):
        self.name:str = name
        self.x:int = position[0]
        self.y:int = position[1]
        self.width:int = size[0]
        self.height:int = size[1]
        self.selected:bool = False
        self.color:QColor = color
        self.mOffset:list[int] = [0,0]

    def get_region(self) -> QRegion:
        return QRegion(
            self.x, self.y,
            self.width, self.height
        )

    def draw(self, painter:QPainter):
        painter.fillRect(
            self.x,self.y,
            self.width,self.height,
            self.color
        )

    def process(self, delta:float):
        if self.selected: self.moving()

    def contains(self, x, y):
        return (
            self.x <= x < self.x + self.width
            and self.y <= y < self.y + self.height
        )

    def on_click(self):
        global mx
        global my

        print(f"Clicked rectangle named {self.name}")

        self.mOffset[0] = self.x - mx
        self.mOffset[1] = self.y - my
        
        self.selected = True

    def moving(self):
        if self.selected and not mdown:
            self.selected = False
            return

        global mx
        global my

        self.x = mx + self.mOffset[0]
        self.y = my + self.mOffset[1]

class Overlay(QWidget):
    def rectAdd(self, r:Rectangle):
        self.rectangles.append(r)
        self.update_regions()

    def rectRemove(self, r:Rectangle):
        self.rectangles.append(r)
        self.update_regions()

    def update_regions(self) -> None:
        mask = QRegion()

        for r in self.rectangles:
            mask = mask.united(r.get_region())

        self.setMask(mask)
        self.update()

    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        self.rectangles:list[Rectangle] = []

        self.clock = QElapsedTimer()
        self.clock.start()

        self.timer = QTimer(self)
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.timeout.connect(self.process)
        self.timer.start(16)

    def process(self):
        # calculate mouse position
        global mx
        global my
        global mdown

        pos = QCursor.pos()
        mx = pos.x()
        my = pos.y()
        mdown = (win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000) != 0

        # regular rectangle function:
        delta = self.clock.restart() / 1000.0

        for r in self.rectangles:
            r.process(delta)

        self.update_regions()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        for r in self.rectangles:
            r.draw(painter)

    def mousePressEvent(self, event):
        global mx
        global my

        for r in reversed(self.rectangles):
            if r.contains(mx,my):
                r.on_click()
                break


# ===============================================       Activation      ==========================================================


app = QApplication(sys.argv)

overlay = Overlay()

rect1 = Rectangle("bob",(100,100),(150,150),QColor(255,0,0,200))
rect2 = Rectangle("bill",(400,200),(200,100),QColor(0,255,0,200))
rect3 = Rectangle("josh",(700,400),(120,120),QColor(0,0,255,200))

overlay.rectAdd(rect1)
overlay.rectAdd(rect2)
overlay.rectAdd(rect3)

overlay.show()

sys.exit(app.exec())

print("Activate") 