import sys
from PySide6.QtCore import QLocale, QPoint, QRect, QSize, Qt
from PySide6.QtWidgets import QApplication, QSizePolicy, QWidget
from PySide6.QtGui import QCursor, QFont, QIcon, QPaintEvent, QPainter, QColor, QPalette, QRegion

class Rectangle:
    def __init__(self,name:str,x:int,y:int,width:int,height:int):
        self.name:str = name
        self.x:int = x
        self.y:int = y
        self.width:int = width
        self.height:int = height

    def get_region(self) -> QRegion:
        return QRegion(
            self.x, self.y,
            self.width, self.height
        )

    def draw(self, painter:QPainter):
        painter.fillRect(
            self.x,self.y,
            self.width,self.height,
            QColor(255,0,0,160)
        )

    def contains(self, x, y):
        return (
            self.x <= x < self.x + self.width
            and self.y <= y < self.y + self.height
        )

    def on_click(self,mx:int=0,my:int=0):
        print(f"Clicked rectangle named {self.name}")
        print(mx,my)

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

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        for r in self.rectangles:
            r.draw(painter)

    def mousePressEvent(self, event):
        pos = event.position()
        mx = pos.x()
        my = pos.y()

        for r in reversed(self.rectangles):
            if r.contains(mx,my):
                r.on_click(mx,my)
                break

app = QApplication(sys.argv)

overlay = Overlay()

rect1 = Rectangle("bob",100,100,150,150)
rect2 = Rectangle("bill",400,200,200,100)
rect3 = Rectangle("josh",700,400,120,120)

overlay.rectAdd(rect1)
overlay.rectAdd(rect2)
overlay.rectAdd(rect3)

overlay.show()

sys.exit(app.exec())

print("Activate")