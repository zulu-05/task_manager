from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, QTime


class DigitalClock(QLabel):

    def __init__(self, format='HH:mm:ss.zzz'):

        super().__init__()
        self.format = format
        self.init_clock()


    def init_clock(self):

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1)
        self.update_time()


    def update_time(self):

        current_time = QTime.currentTime().toString(self.format)
        self.setText(current_time)


