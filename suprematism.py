import json
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QBrush, QColor, QPolygonF
from PyQt6.QtCore import Qt, QPointF
from openai import OpenAI

client = OpenAI(
    api_key="sk-79GgdKZzhyOK8rvnpciFogWX3yA61T5W",
    base_url="https://api.proxyapi.ru/openai/v1",
)
messages = []


class Suprematism(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.do_paint = False
        self.setMouseTracking(True)
        self.object = ''

    def initUI(self):
        self.setGeometry(150, 150, 1000, 1000)
        self.setWindowTitle('Координаты')

    def gptprompt(self, promt):
        messages.append({"role": "user", "content": promt})
        print(messages)
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1000
        )
        response_text = chat_completion.choices[0].message.content
        messages.append({"role": "assistant", "content": response_text})
        modified_text = response_text.replace('```', '').replace('json', '')
        print(modified_text)
        result = json.loads(modified_text)
        messages.clear()
        print(result)
        return result

    def paintEvent(self, event):
        if self.do_paint:
            fincoords = []
            for x in self.coords:
                fincoords.append(QPointF(x[0], x[1]))

            qp = QPainter(self)
            color = QColor(234, 194, 23)
            qp.setBrush(QBrush(color))
            rect = QPolygonF(fincoords)
            qp.drawPolygon(rect)
            self.do_paint = False



    def mousePressEvent(self, event):
        center = event.pos()
        center = str(center.x()) + ', ' + str(center.y())
        if event.button() == Qt.MouseButton.RightButton:
            self.object = 'составь список точек - координат вершин солнышка с центром в точке (' + center + ') и случайной длиной стороны в диапазоне от 20 до 100 пикселей, в ответе дай ТОЛЬКО список JSON для фигуры Polygon, НИКАКОГО текста. Пример формата: [[100, 200], [200, 200], [200, 100], [100, 100]]'
            self.coords = self.gptprompt(self.object)
            print(self.coords)
            self.do_paint = True
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Suprematism()
    ex.show()
    sys.exit(app.exec())