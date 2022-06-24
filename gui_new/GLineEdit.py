from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal
from gui_new.globals import SUBJECTS_WIDTH

class GLineEdit(QLineEdit):
    contentChanged = pyqtSignal()
    
    def __init__(self, text: str, parent):
        super().__init__(text)
        self.base_parent = parent
        self.content = text
        self.setFixedWidth(SUBJECTS_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.base_parent.hbox.addWidget(self)

        self.returnPressed.connect(self.returnEvent)

    
    def focusOutEvent(self, event):
        """ Reakce na udalost ukonceni upravy LineEdit """
        self.setText(self.content)
        super().focusOutEvent(event)
    
    
    def returnEvent(self):
        """ Reakce na Enter klavesu """
        if self.content != self.text().strip():
            self.content = self.text()
            self.contentChanged.emit()
        self.clearFocus()
    

    def keyPressEvent(self, event):
        """ Reakce na udalost stisknuti klavesy """
        if event.key() == Qt.Key.Key_Escape:
            self.clearFocus()
        return super().keyPressEvent(event)