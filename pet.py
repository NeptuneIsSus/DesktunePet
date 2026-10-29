from PySide6.QtGui import QRegion, QPainter, QColor, QPixmap
import random
import math

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

    def process(self, delta:float, mouse:dict={}, screen:dict={}):
        pass

    def contains(self, x, y):
        return (
            self.x <= x < self.x + self.width
            and self.y <= y < self.y + self.height
        )

    def on_click(self, mouse:dict):
        print(f"Clicked rectangle named {self.name}")

class Pet(Rectangle):
    base_path:str = "assets/base/"

    gravity:float = 10.0

    def __init__(self, name:str):
        super().__init__(name, size=(100,100))

        self.x = random.randint(200,1720)
        self.y = random.randint(200,880)

        self.vx:float = 0
        self.vy:float = 0

        self.on_floor:bool = False

        self.head = QPixmap(self.base_path + "head.png")
        self.body = QPixmap(self.base_path + "body.png")
        self.back_leg = QPixmap(self.base_path + "back_leg.png")
        self.front_leg = QPixmap(self.base_path + "front_leg.png")
        self.back_arm = QPixmap(self.base_path + "back_arm.png")
        self.front_arm = QPixmap(self.base_path + "front_arm.png")

    def draw(self, painter: QPainter):
        self.draw_part(painter,self.back_arm)
        self.draw_part(painter,self.front_arm)
        self.draw_part(painter,self.back_leg)
        self.draw_part(painter,self.front_leg)
        self.draw_part(painter,self.body)
        self.draw_part(painter,self.head)

    def draw_part(self, painter:QPainter, image:QPixmap):
        painter.drawPixmap(
            self.x,
            self.y,
            self.width,
            self.height,
            image
        )

    def process(self, delta: float, mouse: dict = {}, screen: dict = {}):
        if self.selected:
            self.dragging(mouse)
        else:
            self.motion(delta,screen)

    def motion(self, delta:float, screen:dict):
        if self.on_floor:
            self.vx += (0.0 - self.vx) / 5
        self.vy += self.gravity * delta

        self.x += round(self.vx)
        self.y += round(self.vy)

        centerx:float = round(float(self.x) + float(self.width) / 2.0)

        bottom = self.y + self.height
        if bottom >= screen["bottom"]:
            self.y = screen["bottom"] - self.height
            self.vy = 0
            self.on_floor = True
        else:
            self.on_floor = False

        if centerx < screen["left"]:
            self.x = round(screen["left"] - (self.width / 2))
            self.vx = 0.0
        if centerx > screen["right"]:
            self.x = round(screen["right"] - (self.width / 2))
            self.vx = 0.0

        print(self.x,self.y)
    
    def dragging(self, mouse: dict):
        if self.selected and not mouse["down"]:
            self.selected = False
            return

        self.vx = (mouse["x"] - (self.x - self.mOffset[0])) /3
        self.vy = (mouse["y"] - (self.y - self.mOffset[1])) /3

        self.x = mouse["x"] + self.mOffset[0]
        self.y = mouse["y"] + self.mOffset[1]

    def on_click(self, mouse: dict):
        self.mOffset[0] = self.x - mouse["x"]
        self.mOffset[1] = self.y - mouse["y"]
        
        self.selected = True