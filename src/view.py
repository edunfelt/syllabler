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

        self.stack = QStackedWidget(self)  # stacked layout for multi-page form
        self.part1 = QWidget()
        self.part2 = QWidget()
        self.stack.addWidget(self.part1)
        self.stack.addWidget(self.part2)

        # Window properties
        self.setWindowTitle("Syllabler")
        self.setGeometry(500, 500, 600, 550)
        self.buttons = {}  # store buttons in dictionary
        self.fields = {}  # store fields in dictionary

        # Add UI elements
        self.create_header()
        self.main_layout.addWidget(self.stack)
        self.create_part1()
        self.create_part2()
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

    def create_part1(self):
        """
        Create form page 1
        """
        part1_layout = QFormLayout()

        # Basinformation
        swe_name = QLineEdit()
        swe_name.setPlaceholderText("Svenskt namn på kurs")
        self.fields["swe_name"] = swe_name
        part1_layout.addRow("Benämning:", swe_name)

        eng_name = QLineEdit()
        eng_name.setPlaceholderText("Engelskt namn på kurs")
        self.fields["eng_name"] = eng_name
        part1_layout.addRow("Engelsk benämning:", eng_name)

        course_code = QLineEdit()
        course_code.setPlaceholderText("Kurskod enligt XXYZZZ modellen")
        self.fields["course_code"] = course_code
        part1_layout.addRow("Kod:", course_code)

        # Högskolepoäng
        course_credits = QLineEdit()
        self.fields["course_credits"] = course_credits
        course_credits.setValidator(QDoubleValidator())
        part1_layout.addRow("Högskolepoäng:", course_credits)

        # Utbildningsnivå
        level_box = QComboBox()
        level_box.setPlaceholderText("-- Välj nivå --")
        self.fields["level"] = level_box
        level_box.addItem("Grundnivå")
        level_box.addItem("Avancerad nivå")
        part1_layout.addRow("Utbildningsnivå:", level_box)

        # Betygsskala
        grading_box = QComboBox()
        grading_box.setPlaceholderText("-- Ange betygsskala --")
        self.fields["grading_scale"] = grading_box
        grading_box.addItem("AF - sjugradig skala")
        grading_box.addItem("UV - Tregradig skala")
        grading_box.addItem("UG - Tvågradig skala")
        part1_layout.addRow("Betygsskala:", grading_box)

        # Huvudområde
        main_area = QHBoxLayout()
        main_area_true = QRadioButton("Huvudområde finns")
        main_area_true.setChecked(True)
        main_area_false = QRadioButton("Huvudområde saknas")
        self.fields["main_area_true"] = main_area_true
        self.fields["main_area_false"] = main_area_false
        main_area.addWidget(main_area_true)
        main_area.addWidget(main_area_false)
        part1_layout.addRow("Huvudområde:", main_area)

        area_box = QComboBox()
        area_box.setPlaceholderText("-- Ange huvudområde --")
        self.fields["main_area"] = area_box
        area_box.addItem("Område A")
        area_box.addItem("Område B")
        area_box.addItem("Område C")
        part1_layout.addRow("", area_box)

        # Fördjupning
        specialisation_box = QComboBox()
        specialisation_box.setPlaceholderText("-- Ange fördjupning --")
        self.fields["specialisation"] = specialisation_box
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
        part1_layout.addRow("Fördjupning", specialisation_box)

        # Ansvarig institution
        department = QLineEdit()
        department.setPlaceholderText("Ansvarig institution")
        self.fields["department"] = department
        part1_layout.addRow("Ges vid:", department)

        # Termin
        semester_box = QComboBox()
        semester_box.setPlaceholderText("-- Ange termin --")
        self.fields["semester"] = semester_box
        semester_box.addItem("HT20")
        semester_box.addItem("VT21")
        semester_box.addItem("ST21")
        semester_box.addItem("HT21")
        part1_layout.addRow("Giltig fr.o.m:", semester_box)

        # Behörighet
        eligibility = QVBoxLayout()

        eligibility_box = QComboBox()
        eligibility_box.setPlaceholderText("-- Ange behörighet --")
        self.fields["eligibility"] = eligibility_box
        eligibility_box.addItem("Särskild behörighet")
        eligibility_box.addItem("Självständigt arbete")
        eligibility.addWidget(eligibility_box)

        requirements = QLineEdit()
        requirements.setPlaceholderText("Lista de kurser/områden som krävs")
        self.fields["requirements"] = requirements
        requirements.setHidden(True)
        eligibility.addWidget(requirements)

        part1_layout.addRow("Behörighet:", eligibility)

        self.part1.setLayout(part1_layout)

    def create_part2(self):
        """
        Create form page 2
        """
        part2_layout = QFormLayout()
        self.part2.setLayout(part2_layout)

    def create_actions(self):
        """
        Create action buttons
        """
        action_btns = QDialogButtonBox()
        action_btns.setStandardButtons(
            QDialogButtonBox.Apply |
            QDialogButtonBox.Save |
            QDialogButtonBox.Discard |
            QDialogButtonBox.Close
        )

        # Swedish text on buttons
        action_btns.button(QDialogButtonBox.Apply).setText("Fortsätt")
        action_btns.button(QDialogButtonBox.Save).setText("Spara")
        action_btns.button(QDialogButtonBox.Discard).setText("Rensa")
        action_btns.button(QDialogButtonBox.Close).setText("Avsluta")

        # Add buttons to dictionary
        self.buttons["Nästa"] = action_btns.button(QDialogButtonBox.Apply)
        self.buttons["Spara"] = action_btns.button(QDialogButtonBox.Save)
        self.buttons["Rensa"] = action_btns.button(QDialogButtonBox.Discard)
        self.buttons["Avsluta"] = action_btns.button(QDialogButtonBox.Close)

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

    def warning(self, name):
        """
        Warning dialog if incompatible input
        :param name: name of field that is incorrect
        """
        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Warning)
        dialog.setWindowTitle("Felaktigt fält!")
        dialog.setText("Fältet '" + name + "' har felaktigt värde.")
        dialog.setInformativeText("Se den inbyggda manualen för mer information.")
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.show()

    def get_data(self):
        """
        Method for saving current form data to json file
        :return: dictionary of all the current form data
        """
        data = {}
        for name, field in self.fields.items():
            if isinstance(field, QLineEdit):
                data[name] = field.text()
            elif isinstance(field, QComboBox):
                data[name] = field.currentText()
        return data

    def reset_form(self):
        """
        Method for emptying all form fields without saving
        """
        for name, field in self.fields.items():
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(0)
            else:
                pass
        self.fields["main_area_true"].setChecked(True)

    def close_form(self):
        """
        Method for closing the form (with a warning)
        """
        self.close()

    def switch_page(self):
        """
        Method for switching page in form
        """
        if self.stack.currentWidget() is self.part1:
            self.stack.setCurrentIndex(1)
        elif self.stack.currentWidget() is self.part2:
            self.stack.setCurrentIndex(0)

    def main_area_switch(self):
        """
        Method for hiding the main area combo box if course has no main area
        """
        if self.fields["main_area_true"].isChecked():
            self.fields["main_area"].setEnabled(True)
        else:
            self.fields["main_area"].setEnabled(False)

    def eligibility_switch(self):
        """
        Method for removing the "Grundläggande" option if course is advanced
        """
        if self.fields["level"].currentIndex() == 0:
            self.fields["eligibility"].addItem("Grundläggande behörighet")
        elif self.fields["level"].currentIndex() == 1:
            self.fields["eligibility"].removeItem(2)

    def eligibility_list(self):
        """
        Method for showing input field for required courses only if necessary
        """
        if self.fields["eligibility"].currentText() == "Särskild behörighet":
            self.fields["requirements"].setHidden(False)
        else:
            self.fields["requirements"].setHidden(True)
            self.fields["requirements"].clear()
