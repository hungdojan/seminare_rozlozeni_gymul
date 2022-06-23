# from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QKeySequence, QStandardItemModel, QStandardItem
from gui_new.GStudent import GStudent

class GMainWindow(QMainWindow):
    def __init__(self):
        super(GMainWindow, self).__init__()
        self.__setup()

    def __setup(self):
        # nastaveni hlavniho okna
        self.setWindowTitle("Seminare")

        self.__setup_menu_bar()

        # hlavni pracovni plocha
        self.horizontalLayout = QHBoxLayout()
        main_widget = QWidget(self)
        main_widget.setLayout(self.horizontalLayout)
        self.setCentralWidget(main_widget)

        self.showMaximized()


    def __setup_menu_bar(self):
        """ Vygeneruje horni listu """
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        def add_action(name, action_sg, parent: QMenu, shortcut=None):
            """ Vytvari polozku v menu """
            if parent is None or action_sg is None:
                raise Exception("add_action failed")
            action = parent.addAction(name)
            action.triggered.connect(action_sg)
            if shortcut is not None:
                action.setShortcut(QKeySequence(shortcut))
                action.setShortcutVisibleInContextMenu(True)
            return action

        # soubor menu
        file_menu = self.menu_bar.addMenu("Soubor")
        add_action('Otevřít soubor', self._sg_open_file, file_menu, 'Ctrl+O')
        add_action('Uložit', self._sg_save, file_menu, 'Ctrl+S')
        file_menu.addSeparator()
        add_action('Načíst předměty', self._sg_import_subjects, file_menu, 'Ctrl+G')
        add_action('Načíst žáky', self._sg_import_students, file_menu, 'Ctrl+H')
        add_action('Exportovat data', self._sg_export, file_menu, 'Ctrl+E')

        file_menu.addSeparator()
        add_action('Zavřít', self.close, file_menu)


    def _sg_open_file(self):
        # TODO:
        print("open file")


    def _sg_save(self):
        # TODO:
        print('save')


    def _sg_import_subjects(self):
        # TODO:
        print('import subjects')


    def _sg_export(self):
        # TODO:
        print('export data')
    
    def _sg_import_students(self):
        # TODO:
        print('import students')


    def _sg_close_app(self):
        # TODO:
        print('close app')