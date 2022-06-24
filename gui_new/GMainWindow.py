from PyQt6.QtWidgets import *
from PyQt6.QtGui import QKeySequence
from gui_new.GStudent import GStudent
from gui_new.GDay import GDay
from sortsubj.sort_subjs import SubSort
from PyQt6.QtCore import pyqtSlot, Qt

class GMainWindow(QMainWindow):
    def __init__(self, subsort: SubSort=None):
        super(GMainWindow, self).__init__()
        self.subsort = subsort
        self.subsort.load_file_student(r'C:\Users\hungd\Documents\GitHub\seminare_rozlozeni_gymul\input_zaci-2R-anonym.csv')
        self.subsort.load_file_subjects(r'C:\Users\hungd\Documents\GitHub\seminare_rozlozeni_gymul\input_predmety.csv')
        self.lof_gstudents = []
        self.lof_gdays = []
        self.selected_gstudents = set()
        self.selected_gdays = set()
        self.__setup()

    def __setup(self):
        # nastaveni hlavniho okna
        self.setWindowTitle("Seminare")

        # hlavni pracovni plocha
        main_widget = QWidget(self)
        self.horizontalLayout = QHBoxLayout(main_widget)
        self.horizontalLayout.addStretch()
        main_widget.setLayout(self.horizontalLayout)
        self.setCentralWidget(main_widget)

        self.__setup_menu_bar()
        self.__setup_left_panel()
        self.__setup_mid_panel()
        self.__setup_right_panel()

        self.showMaximized()


    def __setup_menu_bar(self):
        """ Vygeneruje horni listu """
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # tovarni funkce
        def add_action(name, action_slt, parent: QMenu, shortcut=None):
            """ Vytvari polozku v menu """
            if parent is None or action_slt is None:
                raise Exception("add_action failed")
            action = parent.addAction(name)
            action.triggered.connect(action_slt)
            if shortcut is not None:
                action.setShortcut(QKeySequence(shortcut))
                action.setShortcutVisibleInContextMenu(True)
            return action

        # soubor menu
        file_menu = self.menu_bar.addMenu("Soubor")
        add_action('Otevřít soubor', self._slt_open_file, file_menu, 'Ctrl+O')
        add_action('Uložit', self._slt_save, file_menu, 'Ctrl+S')
        file_menu.addSeparator()
        add_action('Exportovat data', self._slt_export, file_menu, 'Ctrl+E')

        file_menu.addSeparator()
        add_action('Zavřít', self.close, file_menu)

        # student menu
        student_menu = self.menu_bar.addMenu('Student')
        add_action('Přidat studenta', self._slt_add_student, student_menu)
        add_action('Smazat studenta', self._slt_delete_student, student_menu)
        student_menu.addSeparator()
        add_action('Načíst studenty', self._slt_import_students, student_menu)

        # dny menu
        day_menu = self.menu_bar.addMenu('Dny')
        add_action('Přidat den', self._slt_add_day, day_menu)
        add_action('Odstranit dny', self._slt_remove_days, day_menu)
        day_menu.addSeparator()
        add_action('Načíst předměty', self._slt_import_subjects, day_menu)

        # trideni
        add_action('AKTUALIZACE', self._slt_sort, self.menu_bar)
    
    
    def __setup_left_panel(self):
        """ Vygeneruje levy panel se studenty """
        lof_students_scrar = QScrollArea(self)
        lof_students_scrar.setLineWidth(2)
        lof_students_scrar.setFrameShape(QFrame.Shape.Box)
        lof_students_scrar.setFrameShadow(QFrame.Shadow.Plain)
        frame = QFrame(lof_students_scrar)
        self.student_vbox = QVBoxLayout(frame)
        self.student_vbox.setContentsMargins(3, 3, 3, 3)
        self.student_vbox.setSpacing(1)
        self.student_vbox.addStretch()

        frame.setLayout(self.student_vbox)
        lof_students_scrar.setWidgetResizable(True)
        lof_students_scrar.setWidget(frame)
        self.horizontalLayout.insertWidget(self.horizontalLayout.count() - 1, lof_students_scrar)

        self.lof_gstudents = [GStudent(self.subsort.students[student], self.student_vbox, self) 
                              for student in self.subsort.students]
    

    def __setup_mid_panel(self):
        lof_days_scrar = QScrollArea()
        frame = QFrame()
        self.days_hbox = QHBoxLayout()

        frame.setLayout(self.days_hbox)
        lof_days_scrar.setWidget(frame)
        
        # TODO: add days
        self.lof_gdays = [GDay]


    def __setup_right_panel(self):
        # TODO:
        pass


    def select_gstudent(self, gstudent):
        self.selected_gstudents.add(gstudent)


    def deselect_gstudent(self, gstudent):
        self.selected_gstudents.remove(gstudent)
    

    def select_gday(self, gday):
        self.selected_gdays.add(gday)
    

    def deselect_gday(self, gday):
        self.selected_gday.remove(gday)


    @pyqtSlot()
    def _slt_delete_student(self):
        for gs in self.selected_gstudents:
            student = gs.model
            gs.delete()
            self.subsort.delete_student(student)

    @pyqtSlot()
    def _slt_open_file(self):
        # TODO:
        print("open file")


    @pyqtSlot()
    def _slt_save(self):
        # TODO:
        print('save')


    @pyqtSlot()
    def _slt_import_subjects(self):
        # TODO:
        print('import subjects')


    @pyqtSlot()
    def _slt_export(self):
        # TODO:
        print('export data')
    

    @pyqtSlot()
    def _slt_import_students(self):
        # TODO:
        print('import students')


    @pyqtSlot()
    def _slt_close_app(self):
        # TODO:
        print('close app')
    

    @pyqtSlot()
    def _slt_add_student(self):
        # TODO:
        print('add student')

    
    @pyqtSlot()
    def _slt_add_day(self):
        # TODO:
        new_day = self.subsort.add_day([])
        self.lof_gdays.append(GDay(new_day, self.horizontalLayout, self))
        print('add day')
    

    @pyqtSlot()
    def _slt_remove_days(self):
        # TODO:
        for gd in self.selected_gdays:
            student = gd.model
            gd.delete()
            self.subsort.delete_student(student)
        print('remove days')
    

    @pyqtSlot()
    def _slt_sort(self):
        # TODO:
        print('sort')