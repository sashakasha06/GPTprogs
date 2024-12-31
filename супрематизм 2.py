import json
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QBrush, QColor, QPolygonF
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtCore import QRectF
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

messages = []


class Suprematism(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.object = ''

    def initUI(self):
        self.setGeometry(150, 150, 1000, 1000)
        self.setWindowTitle('Координаты')

    def paintEvent(self, event):
        qp = QPainter(self)
        try:
            if 'круг' in self.object:
                prompt = 'Необходимо изобразить ' + self.object +', также выбери случайный цвет для фигуры. Ответ должен содержать только JSON, без комментариев и дополнительной информации. Пример формата: {"Цвет": [255, 123, 0], "радиус": 34, "Центр": [148, 60]}'
                messages.append({"role": "user", "content": prompt})
                chat_completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=1000
                )
                response_text = chat_completion.choices[0].message.content
                print(response_text)
                messages.append({"role": "assistant", "content": response_text})
                modified_text = response_text.replace('```', '').replace('json', '')
                print(modified_text)

                try:
                    planets = json.loads(modified_text)
                except json.JSONDecodeError as e:
                    print("Ошибка декодирования JSON:", e)
                    return

                color = QColor(planets['Цвет'][0], planets['Цвет'][1], planets['Цвет'][2])
                radius = planets['радиус']
                center = QPointF(*planets['Центр'])
                qp.setBrush(QBrush(color))
                qp.drawEllipse(center, radius, radius)


            elif 'квадрат' in self.object:
                prompt = 'Необходимо изобразить ' + self.object + ', также выбери случайный цвет для фигуры и координаты верхней левой точки и правой нижней точки. Ответ должен содержать только JSON, без комментариев и дополнительной информации. Пример формата: {"Цвет": [255, 123, 0], "сторона": 48, "центр": [172, 84], "координаты": [[148, 60], [148, 108], [196, 108], [196, 60]]}'
                messages.append({"role": "user", "content": prompt})
                chat_completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=1000
                )
                response_text = chat_completion.choices[0].message.content
                print(response_text)
                messages.append({"role": "assistant", "content": response_text})
                modified_text = response_text.replace('```', '').replace('json', '')
                print(modified_text)

                try:
                    planets = json.loads(modified_text)
                except json.JSONDecodeError as e:
                    print("Ошибка декодирования JSON:", e)
                    return

                color = QColor(planets['Цвет'][0], planets['Цвет'][1], planets['Цвет'][2])
                qp.setBrush(QBrush(color))
                rect = [planets['координаты'][0], planets['координаты'][1], planets['координаты'][2], planets['координаты'][3]]
                qp.drawRect(rect[0], rect[1], rect[2], rect[3])


            elif 'треугольник' in self.object:
                prompt = 'Необходимо изобразить ' + self.object + ', также выбери случайный цвет для фигуры и координаты всех точек. Основание должно быть параллельно оси X, при этом третья точка должна находиться выше основания. Если координаты являются нецелым числом, то его стоит округлить до двух знаков после запятой по правилам математики. Ответ должен содержать только JSON, без комментариев и дополнительной информации. Пример формата: {"Цвет": [255, 123, 0], "радиус": 40, "центр": [50, 30], "координаты": [[50, 10], [15.36, 50], [84.64, 50]]}'
                messages.append({"role": "user", "content": prompt})
                chat_completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=1000
                )
                response_text = chat_completion.choices[0].message.content
                print(response_text)
                messages.append({"role": "assistant", "content": response_text})
                modified_text = response_text.replace('```', '').replace('json', '')
                print(modified_text)
                try:
                    planets = json.loads(modified_text)
                except json.JSONDecodeError as e:
                    print("Ошибка декодирования JSON:", e)
                    return

                color = QColor(planets['Цвет'][0], planets['Цвет'][1], planets['Цвет'][2])
                radius = planets['радиус']
                center = QPointF(*planets['Центр'])
                qp.setBrush(QBrush(color))
                qp.drawEllipse(center, radius, radius)
        except Exception as e:
            print("Произошла ошибка при отрисовке:", e)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.object = 'круг с центром в точке положения курсора и случайным радиусом в диапазоне от 20 до 100 пикселей'
            print(self.object)
            self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            self.object = "квадрат с центром в точке положения курсора и случайной длиной стороны в диапазоне от 20 до 100 пикселей"
            print(self.object)
            self.update()

    def keyPressEvent(self, event):
        self.object = 'треугольник, который должен быть равносторонним и вписанным в окружность со случайным радиусом длиной от 20 до 100 пикселей. В случае нецелых координат их следует округлить по правилам математики'
        print(self.object)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Suprematism()
    ex.show()
    sys.exit(app.exec())