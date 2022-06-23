from sortsubj import *
from PyQt6.QtWidgets import *

class GStudent(QWidget):

    def __init__(self, model: tuple):
        super().__init__()
        self.model = model
        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)