import sys
from PyQt5.QtWidgets import QApplication

from src.view import SyllablerUI
from src.controller import SyllablerCtrl


def main():
    syllabler = QApplication(sys.argv)
    view = SyllablerUI()
    view.show()
    SyllablerCtrl(view=view)
    sys.exit(syllabler.exec_())


if __name__ == '__main__':
    main()
