import sys
from PyQt5.QtWidgets import QApplication
from src.view import SyllablerUI
from src.controller import SyllablerCtrl
from src.model import Course


def main():
    syllabler = QApplication(sys.argv)
    view = SyllablerUI()
    view.show()
    model = Course()
    SyllablerCtrl(view=view, model=model)
    sys.exit(syllabler.exec_())


if __name__ == '__main__':
    main()
