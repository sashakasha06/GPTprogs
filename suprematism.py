import json
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QCursor, QPolygonF
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtCore import QRectF
import random
import math
from openai import OpenAI

client = OpenAI(
    api_key="sk-79GgdKZzhyOK8rvnpciFogWX3yA61T5W",
    base_url="https://api.proxyapi.ru/openai/v1",
)
messages = []
fl = 0

class Suprematism(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.circles = []
        self.squares = []
        self.triangs = []
        self.object = ''

    def initUI(self):
        self.setGeometry(150, 150, 1000, 1000)
        self.setWindowTitle('Координаты')

    def paintEvent(self, event):
        qp = QPainter(self)
        if 'круг' in self.object:
            fl = 1
            promt = 'Необходимо изобразить ' + self.object + ', также выбери случайный цвет для фигуры. Ответ должен содержать только JSON, без комментариев и дополнительной информации. Пример формата: {"Цвет": [255, 123, 0], "радиус": 34, "Центр": [148, 60]}'
            color = QColor(planets['цвет'][0], planets['цвет'][1], planets['цвет'][2])
            radius = planets['радиус']
            center = planets['Центр']
            qp.setBrush(QBrush(color))
            print(qp.setBrush())
            qp.drawEllipse(center, radius, radius)

        elif 'квадрат' in self.object:
            fl = 2
            promt = 'Необходимо изобразить ' + self.object + ', также выбери случайный цвет для фигуры и координаты верхней левой точки и правой нижней точки. Ответ должен содержать только JSON, без комментариев и дополнительной информации. Пример формата: {"Цвет": [255, 123, 0], "сторона": 48, "центр": [172, 84], "координаты": [[148, 60], [196, 108], 48]}'

            color = QColor(planets['цвет'][0], planets['цвет'][1], planets['цвет'][2])
            coords = [planets["координаты"][0], planets["координаты"][1], planets["координаты"][2], planets["координаты"][3]]
            qp.setBrush(QBrush(color))
            print(qp.setBrush())
            rect = QRectF(coords[0], coords[1], coords[2], coords[2])
            qp.drawRect(rect)

        elif 'треугольник' in self.object:
            fl = 3
            promt = 'Необходимо изобразить ' + self.object + ', также выбери случайный цвет для фигуры и координаты всех точек. Основание должно быть параллельно оси X, при этом третья точка должна находиться выше основания. Если координаты являются нецелым числом, то его стоит округлить до двух знаков после запятой по правилам математики. Ответ должен содержать только JSON, без комментариев и дополнительной информации. Пример формата: {"Цвет": [255, 123, 0], "радиус": 40, "центр": [50, 30], "координаты": [[50, 10], [15.36, 50], [84.64, 50]]}'

            messages.append({"role": "user", "content": promt})
            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1000
            )
            response_text = chat_completion.choices[0].message.content
            messages.append({"role": "assistant", "content": response_text})
            modified_text = response_text.replace('```', '').replace('json', '')
            planets = json.loads(modified_text)
            print(response_text)
            for key, value in planets.items():
                print(key, ': ', value)
            color = QColor(planets['цвет'][0], planets['цвет'][1], planets['цвет'][2])
            coords = [planets["координаты"][0], planets["координаты"][1], planets["координаты"][2]]
            qp.setBrush(QBrush(color))
            print(qp.setBrush())
            rect = QRectF(coords[0], coords[1], coords[2])
            polygon = QPolygonF(rect)
            qp.drawPolygon(polygon)
            self.triangs.clear()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.object = 'круг с центром в точке положения курсора и случайным радиусом в диапазоне от 20 до 100 пикселей'
            self.update()

        elif event.button() == Qt.MouseButton.RightButton:
            self.object = "квадрат с центром в точке положения курсора и случайной длиной стороны в диапазоне от 20 до 100 пикселей"
            self.update()

    def keyPressEvent(self, event):
        self.object = 'треугольник, который должен быть равносторонним и вписанным в окружность с центром в точке нажатия и радиусом в диапазоне от 20 до 100 пикселей'
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Suprematism()
    ex.show()
    sys.exit(app.exec())