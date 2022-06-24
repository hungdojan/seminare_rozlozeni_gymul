from sortsubj import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from gui_new.globals import *
from gui_new.GLineEdit import GLineEdit

class GStudent(QFrame):

    def __init__(self, model: Student, base_layout: QBoxLayout, base_window):
        super().__init__()
        self.model = model
        self.base_window = base_window
        self._is_selected = False

        # rozlozeni jednoho radku
        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)
        self.id_lbl = QLabel(model.id)
        self.id_lbl.setFixedWidth(ID_WIDTH)
        self.id_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_name_lbl = QLabel(model.first_name)
        self.last_name_lbl = QLabel(model.last_name)
        self.class_lbl = QLabel(model.class_id)
        self.subjects_tf = [GLineEdit(s, self) for s in self.model.subjects]
        # nastaveni reakce na prijaty signal
        list(map(lambda x: x.contentChanged.connect(self.update_subjects), self.subjects_tf))

        self.hbox.setSpacing(1)
        self.hbox.setContentsMargins(10, 1, 10, 4)
        self.mousePressEvent = self._mouse_event
        self.hbox.addWidget(self.id_lbl, Qt.AlignmentFlag.AlignLeft)
        self.hbox.addWidget(self.first_name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.hbox.addWidget(self.last_name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.hbox.addWidget(self.class_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        list(map(lambda x: self.hbox.addWidget(x), self.subjects_tf))

        self.setContentsMargins(10, 0, 10, 0)
        self.separator = None

        # vlozit oddelovac mezi jednotlivymi studenty
        if base_layout.count() > 1:
            self.separator = QFrame(base_layout.parent())
            self.separator.setFrameShape(QFrame.Shape.HLine)
            self.separator.setFrameShadow(QFrame.Shadow.Sunken)
            self.separator.setContentsMargins(11, 0, 11, 0)
            base_layout.insertWidget(base_layout.count() - 1, self.separator)
        base_layout.insertWidget(base_layout.count() - 1, self)
    

    def _mouse_event(self, _):
        """ Reakce na udalost mysi """
        if self._is_selected:
            self.base_window.deselect_gstudent(self)
        else:
            self.base_window.select_gstudent(self)
        self.select(not self._is_selected)
    

    def update_subjects(self):
        """ Aktualizuje vybrane predmety studenta """
        print(self.model.subjects, end=' -> ')
        self.model.subjects = tuple(map(lambda x: x.text(), self.subjects_tf))
        print(self.model.subjects)


    def select(self, value: bool) -> None:
        """ 
        Meni hodnotu, ktera urcuje, zda je student oznacen
        
        Parametry:
        value: bool - Nova hodnota oznaceni
        """
        self._is_selected = value
        if self._is_selected:
            self.hbox.setContentsMargins(10, 0, 10, 3)
            self.setLineWidth(1)
            self.setFrameShape(QFrame.Shape.Box)
        else:
            self.hbox.setContentsMargins(10, 1, 10, 4)
            self.setLineWidth(0)
            self.setFrameShape(QFrame.Shape.NoFrame)


    def delete(self):
        """ Odstranuje g-reprezentaci z rozlozeni """
        if self.separator is not None:
            self.separator.setParent(None)
        self.setParent(None)