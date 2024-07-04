import sys

from PyQt5.QtWidgets import QApplication
from programm import Main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())