from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from program.ui import *

WINDOW_START_X = 200
WINDOW_START_Y = 100
WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600


class PyQtGUI(QWidget):
    def __init__(self, ):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.navigator(0)

        self.setLayout(self.layout)
        self.setWindowTitle("PSI. Studento Atmintine")
        self.setGeometry(WINDOW_START_X, WINDOW_START_Y, WINDOW_SIZE_X, WINDOW_SIZE_Y)
        self.show()

    def navigator(self, message):
        if message == Message.home:
            self.clear_layout(self.layout)
            self.draw_home()
        elif message == Message.settings:
            self.clear_layout(self.layout)
            pass
        pass

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())

    def draw_home(self):
        Home(self.layout, self.navigator)
