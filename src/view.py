from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class SyllablerUI(QMainWindow):
    """Syllabler UI"""

    def __init__(self):
        """Initialize view"""
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Window properties
        self.setWindowTitle("Syllabler")
        self.setGeometry(500, 500, 600, 550)
        self.buttons = {}  # store buttons in dictionary

        # Add UI elements
        self.create_header()
        self.create_form()
        self.create_actions()
        self.setLayout(self.main_layout)

    def create_header(self):
        """
        Create form header for page 1
        """
        header_layout = QHBoxLayout()

        # Title
        title = QLabel("<h1>Basinformation (kan ej revideras)</h1>")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # User handbook
        handbook_btn = QPushButton()
        self.buttons["Hjälp"] = handbook_btn
        handbook_btn.setText("Hjälp")
        header_layout.addWidget(handbook_btn)

        self.main_layout.addLayout(header_layout)

    def create_form(self):
        """
        Create form page 1
        """
        form_layout = QFormLayout()

        # Basinformation
        form_layout.addRow("Benämning:", QLineEdit())
        form_layout.addRow("Engelsk benämning:", QLineEdit())
        form_layout.addRow("Kod:", QLineEdit())

        # Högskolepoäng
        course_credits = QLineEdit()
        course_credits.setValidator(QDoubleValidator())
        form_layout.addRow("Högskolepoäng:", course_credits)

        # Utbildningsnivå
        level_box = QComboBox()
        level_box.addItem("Grundnivå")
        level_box.addItem("Avancerad nivå")
        form_layout.addRow("Utbildningsnivå:", level_box)

        # Betygsskala
        grading_box = QComboBox()
        grading_box.addItem("AF - sjugradig skala")
        grading_box.addItem("UV - Tregradig skala")
        grading_box.addItem("UG - Tvågradig skala")
        form_layout.addRow("Betygsskala:", grading_box)

        # Huvudområde
        main_area = QHBoxLayout()
        main_area_true = QRadioButton("Huvudområde finns")
        main_area_true.setChecked(True)
        main_area_false = QRadioButton("Huvudområde saknas")
        main_area.addWidget(main_area_true)
        main_area.addWidget(main_area_false)
        form_layout.addRow("Huvudområde:", main_area)

        area_box = QComboBox()
        area_box.addItem("Område A")
        area_box.addItem("Område B")
        area_box.addItem("Område C")
        form_layout.addRow("", area_box)

        # FÖrdjupning
        specialisation_box = QComboBox()
        specialisation_box.addItem("G1N")
        specialisation_box.addItem("G1F")
        specialisation_box.addItem("G1E")
        specialisation_box.addItem("G2F")
        specialisation_box.addItem("G2E")
        specialisation_box.addItem("A1N")
        specialisation_box.addItem("A1F")
        specialisation_box.addItem("A1E")
        specialisation_box.addItem("A2E")
        specialisation_box.addItem("GXX")
        specialisation_box.addItem("AXX")
        form_layout.addRow("Fördjupning", specialisation_box)

        # Ansvarig institution
        form_layout.addRow("Ges vid:", QLineEdit())

        # Termin
        semester_box = QComboBox()
        semester_box.addItem("HT20")
        semester_box.addItem("VT21")
        semester_box.addItem("ST21")
        semester_box.addItem("HT21")
        form_layout.addRow("Giltig fr.o.m:", semester_box)

        # Behörighet
        eligibility_box = QComboBox()
        eligibility_box.addItem("Grundläggande behörighet")
        eligibility_box.addItem("Särskild behörighet")
        eligibility_box.addItem("Självständigt arbete")
        form_layout.addRow("Behörighet:", eligibility_box)

        self.main_layout.addLayout(form_layout)

    def create_actions(self):
        """
        Create action buttons
        """
        action_btns = QDialogButtonBox()
        action_btns.setStandardButtons(
            QDialogButtonBox.Apply |
            QDialogButtonBox.Save |
            QDialogButtonBox.Discard
        )

        # Add buttons to dictionary
        self.buttons["Nästa"] = action_btns.button(QDialogButtonBox.Apply)
        self.buttons["Spara"] = action_btns.button(QDialogButtonBox.Save)
        self.buttons["Rensa"] = action_btns.button(QDialogButtonBox.Discard)

        self.main_layout.addWidget(action_btns)

    def handbook(self):
        """
        User handbook window
        """
        handbook = QMessageBox(self)
        handbook.setIcon(QMessageBox.Question)
        handbook.setText("<h1>Användarmanual</h1>")
        handbook.setWindowTitle("Syllabler manual")
        handbook.setInformativeText("Manual kommer snart...")
        handbook.setStandardButtons(
            QMessageBox.Ok |
            QMessageBox.Close
        )
        handbook.show()
