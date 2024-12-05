"""
Provides a DigitalClock widget that displays the current system time.
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, QTime


class DigitalClock(QLabel):
    """A QLabel-based digital clock widget that updates to show the current time."""

    def __init__(self, format='HH:mm:ss'):
        """
        Initialise the digital clock.

        Args:
            format (str): The time format string. Defaults to 'HH:mm:ss'.
        """

        super().__init__()
        self.format = format
        self.init_clock()


    def init_clock(self):
        """
        Set up a QTimer to update the clock's displayed time at regular intervals.
        """

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()


    def update_time(self):
        """
        Refresh the displayed time to reflect the current system time in the specified format.
        """

        current_time = QTime.currentTime().toString(self.format)
        self.setText(current_time)
