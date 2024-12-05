"""
Provides the CalendarView class for displaying day, week and month calendar layouts.
"""

from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsTextItem
    )
from PySide6.QtGui import QPen, QFont
from PySide6.QtCore import Qt, QDate


class CalendarView(QGraphicsView):
    """A graphical calendar view capable of displaying day, week or month layouts."""

    def __init__(self, view_mode='day', current_date=None):
        """
        Initialise the CalendarView.

        Sets up initial parameters, policies and the graphics scene.
        Draws the initial grid based on the selected view mode and date.

        Args:
            view_mode (str): The initial view mode ('day', 'week', 'month').
            current_date (QDate, optional): The starting date. Defaults to today's date.
        """

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
        """
        Clear the scene and redraw the calendar grid based on the current view mode and date.

        Determines the number of days and the interval hours based on 'view_mode' then calls 'draw_grid' to render the layout.
        """

        self.scene.clear()

        total_hours, days, interval_hours = self.get_grid_parameters()
        self.draw_grid(total_hours, days, interval_hours)


    def get_grid_parameters(self):
        """
        Determine grid parameters (total_hours, number of days, interval hours) based on the current view mode.

        Returns:
            tuple: A tuple (total_hours, days, interval_hours) appropriate for the view mode.
        """

        if self.view_mode == 'day':
            return 24, 1, 0.5

        elif self.view_mode == 'week':
            return 24, 7, 6

        elif self.view_mode == 'month':
            return 24, self.current_date.daysInMonth(), 24

        else:
            return 24, 1, 0.5


    def draw_grid(self, total_hours, days, interval_hours):
        """
        Draw the main calendar grid, including vertical and horizontal lines, day labels and intervals.

        Args:
            total_hours (float): Total hours per day.
            days (int): Number of days to display.
            interval_hours (float): The hour interval between vertical lines.
        """

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
            self.draw_day_lines(day_x, day_height, date)
            self.draw_labels(day_x, day_width, label_padding, font, date)
            self.draw_intervals(day_x, intervals_per_day, interval_width, day_height)

        self.draw_horizontal_lines(day_height, days * day_width)


    def draw_day_lines(self, day_x, day_height, date):
        """
        Draw vertical lines indicating day or week boundaries.

        Args:
            day_x (float): The x-position of the line.
            day_height (float): The height of the day area.
            date (QDate): The date corresponding to this column.
        """

        if self.view_mode == 'day':
            
            pass

        elif self.view_mode == 'week':

            pen_day = QPen(Qt.SolidLine)
            pen_day.setWidth(2)
            pen_day.setColor(Qt.blue)
            self.scene.addLine(day_x, 0, day_x, day_height, pen_day)

        elif self.view_mode == 'month' and date.dayOfWeek() == 1:

            pen_week = QPen(Qt.SolidLine)
            pen_week.setWidth(2)
            pen_week.setColor(Qt.red)
            self.scene.addLine(day_x, 0, day_x, day_height, pen_week)


    def draw_labels(self, day_x, day_width, label_padding, font, date):
        """
        Draw labels for days in week or month view (day names or day numbers).

        Args:
            day_x (float): The x-position of the day's column.
            day_width (float): The width of a single day column.
            label_padding (float): Space above the top line for labeling.
            font (QFont): The font used for day labels.
            date (QDate): The date corresponding to this column.
        """

        if self.view_mode == 'day':
            
            label_text = ''
            pass

        elif self.view_mode == 'week':

            day_name = date.toString('ddd')
            label_text = day_name

        elif self.view_mode == 'month':

            label_text = str(date.day())

        else:

            label_text = ''
            return

        label = QGraphicsTextItem(label_text)
        label.setFont(font)
        label_width = label.boundingRect().width()
        label.setPos(day_x + day_width / 2 - label_width / 2, -label_padding)
        self.scene.addItem(label)
        

    def draw_intervals(self, day_x, intervals_per_day, interval_width, day_height):
        """
        Draw vertical dotted lines that represent time intervals within each day.

        Args:
            day_x (float): The starting x-position for this day's intervals.
            intervals_per_day (int): Number of intervals to draw per day.
            interval_width (float): The width in pixels of each interval.
            day_height (float): The height of the day area.
        """

        for i in range(1, intervals_per_day):

            x = day_x + i * interval_width
            pen = QPen(Qt.DotLine)
            pen.setWidth(1)
            self.scene.addLine(x, 0, x, day_height, pen)


    def draw_horizontal_lines(self, day_height, total_width):
        """
        Draw horizontal dotted lines across all days, dividing the day height into sections.

        Args:
            day_height (float): The height of the day area.
            total_width (float): The total width covered by all days combined.
        """

        num_horizontal_lines = 10
        horizontal_spacing = day_height / num_horizontal_lines
        
        for j in range(num_horizontal_lines + 1):

            y = j * horizontal_spacing
            pen = QPen(Qt.DotLine)
            pen.setWidth(1)
            self.scene.addLine(0, y, total_width, y, pen)


    def keyPressEvent(self, event):
        """
        Handle keyboard navigation events to scroll the calendar horizontally.

        Pressing the right arrow key scrolls right, pressing the left arrow key scrolls left.

        Args:
            event (QKeyEvent): The key event triggered by the user input.
        """

        if event.key() == Qt.Key_Right:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + 100)

        elif event.key() == Qt.Key_Left:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - 100)

        else:
            super().keyPressEvent(event)


    def wheelEvent(self, event):
        """
        Handle mouse wheel events to zoom the calendar horizontally.

        Rolling the wheel up zooms in (wider intervals), rolling it down zooms out.

        Args:
            event (QWheelEvent): The wheel event triggered by the user input.
        """

        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor

        else:
            zoom_factor = zoom_out_factor

        self.scale(zoom_factor, 1)
