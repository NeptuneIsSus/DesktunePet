import sys

from PySide6.QtCore import QLocale, QPoint, QRect, QSize, Qt, QTimer, QElapsedTimer
from PySide6.QtWidgets import QApplication, QSizePolicy, QWidget
from PySide6.QtGui import QCursor, QFont, QIcon, QPaintEvent, QPainter, QColor, QPalette, QRegion

import win32api
import win32con

from pet import Rectangle, Pet


# ===============================================       Globals     ==========================================================


screen = {
    "x": 0,
    "y": 0,
    "width": 0,
    "height": 0,
    "left": 0,
    "right": 0,
    "top": 0,
    "bottom": 0
}

mouse = {
    "x": 0,
    "y": 0,
    "down": False
}


# ===============================================       Classes     ==========================================================




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
        global mouse

        pos = QCursor.pos()
        mouse["x"] = pos.x()
        mouse["y"] = pos.y()
        mouse["down"] = (win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000) != 0

        # regular rectangle function:
        delta = self.clock.restart() / 1000.0

        for r in self.rectangles:
            r.process(delta, mouse, screen)

        self.update_regions()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        for r in self.rectangles:
            r.draw(painter)

    def mousePressEvent(self, event):
        global mouse

        for r in reversed(self.rectangles):
            if r.contains(mouse["x"],mouse["y"]):
                r.on_click(mouse)
                break


# ===============================================       Activation      ==========================================================


app = QApplication(sys.argv)

scr = QApplication.primaryScreen()
bounds = scr.geometry()

screen["x"] = bounds.x()
screen["y"] = bounds.y()
screen["width"] = bounds.width()
screen["height"] = bounds.height()
screen["left"] = bounds.left()
screen["right"] = bounds.right()
screen["top"] = bounds.top()
screen["bottom"] = bounds.bottom()

print(screen)

overlay = Overlay()

rect1 = Rectangle("rect",position=(500,500),color=QColor(255,255,255,255))
pet = Pet("bubby")
overlay.rectAdd(rect1)
overlay.rectAdd(pet)

overlay.show()

sys.exit(app.exec())

print("Activate") 