from PyQt6.QtWidgets import *
from sortsubj import Day

class GDay(QWidget):

    def __init__(self, model: Day, base_layout: QBoxLayout, base_window):
        super().__init__()
        self.model = model
        self.base_window = base_window
        self._is_selected = False
        self.separator = None
        self.vbox_subjects = QVBoxLayout()
        self.setLayout(self.vbox_subjects)
        self.mousePressEvent = self._mouse_event

        # TODO: make layout
        for b in [QPushButton(x) for x in self.base_window.subsort.subject]:
            self.vbox_subjects.addWidget(b)

        if base_layout.count() > 1:
            self.separator = QFrame()
            self.separator.setFrameShape(QFrame.Shape.VLine)
            self.separator.setFrameShadow(QFrame.Shadow.Sunken)
            base_layout.insertWidget(base_layout.count() - 1, self.separator)
        base_layout.insertWidget(base_layout.count() - 1, self)
    

    def _mouse_event(self, _):
        """ Reakce na udalost mysi """
        if self._is_selected:
            self.base_window.deselect_gday(self)
        else:
            self.base_window.select_gday(self)
        self.select(not self._is_selected)


    def select(self, value):
        """ 
        Meni hodnotu, ktera urcuje, zda je den vybran
        
        Parametry:
        value: bool - nova hodnota
        """
        self._is_selected = value
    
    def delete(self):
        """ Maze g-reprezentaci objektu z rozlozeni """
        if self.separator is not None:
            self.separator.setParent(None)
        self.setParent(None)