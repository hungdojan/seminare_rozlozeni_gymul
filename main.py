from sys import argv
from PyQt6.QtWidgets import QApplication
from gui_new.GMainWindow import GMainWindow

def main():
    app = QApplication(argv)
    g_main_window = GMainWindow()
    g_main_window.show()

    app.exec()

if __name__ == "__main__":
    main()