from sys import argv
from PyQt6.QtWidgets import QApplication
from gui_new.GMainWindow import GMainWindow
from sortsubj.sort_subjs import SubSort

def main():
    app = QApplication(argv)
    g_main_window = GMainWindow(SubSort())
    g_main_window.show()

    app.exec()

if __name__ == "__main__":
    main()