from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsTextItem
    )
from PySide6.QtGui import QPen, QFont
from PySide6.QtCore import Qt, QDate


class CalendarView(QGraphicsView):

    def __init__(self, view_mode='day', current_date=None):

        super().__init__()
        self.view_mode = view_mode
        self.current_date = current_date or QDate.currentDate()

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
            interval_hours = 0.5

        elif self.view_mode == 'week':
            total_hours = 24
            days = 7
            interval_hours = 6

        elif self.view_mode == 'month':
            total_hours = 24
            days = self.current_date.daysInMonth()
            interval_hours = 24

        else:
            total_hours = 24
            days = 1
            interval_hours = 0.5

        self.draw_grid(total_hours, days, interval_hours)


    def draw_grid(self, total_hours, days, interval_hours):
        
        intervals_per_day = int(total_hours / interval_hours)
        interval_width = 100
        day_width = interval_width * intervals_per_day
        day_height = 400
        label_padding = 20
        self.scene.setSceneRect(0, -label_padding, days * day_width, day_height + label_padding)

        font = QFont("Arial", 10)
        font.setBold(True)

        for day in range(days):

            day_x = day * day_width
            date = self.current_date.addDays(day)

            if self.view_mode == 'week':

                pen_day = QPen(Qt.SolidLine)
                pen_day.setWidth(2)
                pen_day.setColor(Qt.blue)
                self.scene.addLine(day_x, 0, day_x, day_height, pen_day)

            elif self.view_mode == 'month' and date.dayOfWeek() == 1:

                pen_week = QPen(Qt.SolidLine)
                pen_week.setWidth(2)
                pen_week.setColor(Qt.red)
                self.scene.addLine(day_x, 0, day_x, day_height, pen_week)

            if self.view_mode == 'week':
                
                day_name = date.toString('ddd')
                label = QGraphicsTextItem(day_name)
                label.setFont(font)
                label_width = label.boundingRect().width()
                label.setPos(
                        day_x + day_width / 2 - label_width / 2, -label_padding
                        )
                self.scene.addItem(label)

            elif self.view_mode == 'month':

                day_label = str(date.day())
                label = QGraphicsTextItem(day_label)
                label.setFont(font)
                label_width = label.boundingRect().width()
                label.setPos(
                        day_x + day_width / 2 - label_width / 2, -label_padding
                        )
                self.scene.addItem(label)

            for i in range(1, intervals_per_day):

                x = day_x + i * interval_width
                pen = QPen(Qt.DotLine)
                pen.setWidth(1)
                self.scene.addLine(x, 0, x, day_height, pen)

        num_horizontal_lines = 10
        horizontal_spacing = day_height / num_horizontal_lines

        for j in range(num_horizontal_lines + 1):
            y = j * horizontal_spacing
            pen = QPen(Qt.DotLine)
            pen.setWidth(1)
            self.scene.addLine(0, y, days * day_width, y, pen)


    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Right:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + 100)
        elif event.key() == Qt.Key_Left:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - 100)
        else:
            super().keyPressEvent(event)


    def wheelEvent(self, event):

        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        self.scale(zoom_factor, 1)


