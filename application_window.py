"""
Defines the main application window for the Task Manager application.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
    )
from PySide6.QtCore import Qt, QDate, QPropertyAnimation
from calendar_view import CalendarView
from digital_clock import DigitalClock


class ApplicationWindow(QMainWindow):
    """The main window of the Task Manager application."""

    def __init__(self):
        """
        Initialise the ApplicationWindow.

        Sets up the window properties and triggers the UI setup.
        """
        
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.resize(800, 600)
        self.init_ui()


    def init_ui(self):
        """
        Initialise all UI components and layout them within the main window.

        This method delegates the creation and organisation of widgets and layouts to separate helper methods for clarity and maintainability.
        """

        self.setup_central_widget()
        self.create_calendar_view()
        self.create_buttons()
        self.create_digital_clock()
        self.create_date_range_label()
        self.layout_widgets()


    def setup_central_widget(self):
        """
        Set up the central widget for the main window.

        Creates a central widget that will act as the parent for all other UI components.
        """

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)


    def create_calendar_view(self):
        """
        Create and initialise the calendar view widget.

        The CalendarView displays a day, week or month-based calendar layout.
        """

        self.calendar_view = CalendarView('day')


    def create_buttons(self):
        """
        Create the navigation buttons for switching between day, week and month views.

        Connects the buttons to the 'switch_view' method to update the calendar layout dynamically.
        """

        self.btn_day = QPushButton("Day View")
        self.btn_week = QPushButton("Week View")
        self.btn_month = QPushButton("Month View")

        self.btn_day.clicked.connect(lambda: self.switch_view('day'))
        self.btn_week.clicked.connect(lambda: self.switch_view('week'))
        self.btn_month.clicked.connect(lambda: self.switch_view('month'))

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.btn_day)
        self.button_layout.addWidget(self.btn_week)
        self.button_layout.addWidget(self.btn_month)


    def create_digital_clock(self):
        """
        Create and initialise the digital clock widget.

        The DigitalClock displays the current time and updates every second.
        """

        self.digital_clock = DigitalClock(format='HH:mm:ss.zzz')
        self.digital_clock.setStyleSheet("font-size: 16px; color: blue;")
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.digital_clock)
        self.top_layout.addStretch()


    def create_date_range_label(self):
        """
        Create the date range label which displays the currently viewed date range.

        This label is typically updated when the view mode changes (e.g., for the week view).
        """

        self.date_range_label = QLabel()
        self.date_range_label.setAlignment(Qt.AlignCenter)
        self.date_range_label.setStyleSheet("font-size: 14px; font-weight: bold;")


    def update_date_range_label(self):
        """
        Update the date range label based on the current view mode.

        For the week view, displays the start and end dates of the displayed week.
        For other views, clears the label.

        Args:
            view_mode (str): The current view mode of the calendar.
        """

        if view_mode == 'day':
            pass
        
        elif view_mode == 'week':
            start_date = self.calendar_view.current_date
            end_date = start_date.addDays(6)
            date_range = f"{start_date.toString('MMM dd')} - {end_date.toString('MMM dd')}"
            self.date_range_label.setText(date_range)

        elif view_mode == 'month':
            pass

        else:
            self.date_range_label.setText('')


    def layout_widgets(self):
        """
        Organise all created widgets and layouts into the central widget's main layout.
        """

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.date_range_label)
        self.main_layout.addWidget(self.calendar_view)
        self.central_widget.setLayout(self.main_layout)


    def animate_calendar_view(self, start_rect, end_rect, duration=500, callback=None):
        """
        Animate calendar view to the specified mode.
        
        Starts an animation that slightly enlarges the calendar view before changing the mode, creating a visual transition effect.
        """

        self.animation = QPropertyAnimation(self.calendar_view, b"geometry")
        self.animation.setDuration(duration)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)

        if callback:
            self.animation.finished.connect(callback)
        
        self.animation.start()


    def switch_view(self, view_mode):
        """
        Animate and switch the calendar view to the specified mode.

        Starts an animation that slightly enlarges the calendar view before changing the mode, creating a visual transition effect.

        Args:
            view_mode (str): The desired view mode ('day', 'week' or 'month').
        """
        
        start_rect = self.calendar_view.geometry()
        end_rect = start_rect.adjusted(0, 0, start_rect.width() * 0.05, start_rect.height() * 0.05)
        self.animate_calendar_view(start_rect, end_rect, callback=lambda: self.finish_switch_view(view_mode))


    def finish_switch_view(self, view_mode):
        """
        Complete the view switch by updating the calendar and playing a reverse animation.

        Resets the calendar date to the current date, updates the view mode and redraws the grid.
        Plays another animation to revert the calendar to its original size.
        Updates the date range label if needed.

        Args:
            view_mode (str): The newly selected view mode.
        """

        self.calendar_view.update_view(view_mode)
        start_rect = self.calendar_view.geometry()
        end_rect = start_rect.adjusted(0, 0, -start_rect.width() * 0.05, -start_rect.height() * 0.05)
        self.animate_calendar_view(start_rect, end_rect)
        self.update_date_range_label(view_mode)
