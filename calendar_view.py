from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGraphicsView,
    QGraphicsScene,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel
    )
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt, QTimer, QTime


class CalendarView(QGraphicsView):

    def __init__(self, view_mode='day'):

        super().__init__()
        self.view_mode = view_mode
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.init_grid()


    def init_grid(self):

        self.scene.clear()
        if self.view_mode == 'day':
            total_hours = 24
            days = 1
        elif self.view_mode == 'week':
            total_hours = 24
            days = 7
        elif self.view_mode == 'month':
            total_hours = 24
            days = 30
        else:
            total_hours = 24
            days = 1

        self.draw_grid(total_hours, days)


    def draw_grid(self, total_hours, days):
        
        interval_width = 50
        day_width = interval_width * total_hours * 2
        day_height = 400
        num_horizontal_lines = 10

        for day in range(days):
            for i in range(total_hours * 2 + 1):
                x = day * day_width + i * interval_width
                pen = QPen(Qt.DotLine if i % 2 else Qt.SolidLine)
                self.scene.addLine(x, 0, x, day_height, pen)

        horizontal_spacing = day_height / num_horizontal_lines
        for j in range(num_horizontal_lines + 1):
            y = j * horizontal_spacing
            pen = QPen(Qt.DotLine)
            self.scene.addLine(0, y, days * day_width, y, pen)

        self.scene.setSceneRect(0, 0, days * day_width, day_height)


    def key_press_event(self, event):

        if event.key() == Qt.Key_Right:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + 100)
        elif event.key() == Qt.Key_Left:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - 100)
        else:
            super().key_press_event(event)


