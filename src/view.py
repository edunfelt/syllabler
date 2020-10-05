import json

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def code_check(course_code: str):
    """
    Check if a course code is of the form XXYZZZ
    :param course_code: Code to check
    :return: True if course code is valid, False otherwise
    """
    if len(course_code) != 6:
        raise Exception("Provided code is too short")

    if not course_code[0].isupper() and course_code[1].isupper():
        raise Exception
    elif not course_code[2:].isdigit():
        raise Exception


def get_data(field):
    """
    Get data from form field
    :param field: field to get data from
    :return: input data
    """
    if isinstance(field, QLineEdit):
        return field.text()
    elif isinstance(field, QComboBox):
        return field.currentText()
    elif isinstance(field, dict):
        data = {}
        for key, value in field.items():
            data[key] = get_data(value)
        return data
    elif isinstance(field, QSpinBox):
        return field.value()
    elif isinstance(field, QRadioButton):
        if field.isChecked():
            return field.text()
        else:
            return ""
    elif isinstance(field, QCheckBox):
        if field.isChecked():
            return field.text()
        else:
            return ""


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
        self.part3 = QWidget()
        self.part3_layout = QVBoxLayout()

        self.part2_layout = QFormLayout()
        self.part2.setLayout(self.part2_layout)
        self.part2_part_list = QListWidget()  # list for course parts
        self.part2_part_stack = QStackedWidget()  # form for each course part

        self.stack.addWidget(self.part1)
        self.stack.addWidget(self.part2)

        # Window properties
        self.setWindowTitle("Syllabler")
        self.setGeometry(500, 500, 600, 550)

        # Keep track of UI elements
        self.buttons = {}  # store buttons in dictionary
        self.fields = {}  # store fields in dictionary
        self.parts = 0  # count number of course parts

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
        title = QLabel("<h1>Basinformation för kursplaner</h1>")
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
        part2_form = QFormLayout()

        # Beskrivning
        description = QLineEdit()
        description.setPlaceholderText("Lista de områden som kursen behandlar")
        self.fields["description"] = description
        part2_form.addRow("Kursbeskrivning:", description)

        # Kursmoment
        parts_info = QHBoxLayout()
        parts = QSpinBox()
        self.fields["parts"] = parts
        parts_info.addWidget(parts)

        pass_all = QCheckBox()
        pass_all.setText("Godkänt på alla delar krävs")
        self.fields["pass_all"] = pass_all
        parts_info.addWidget(pass_all)

        weighted_grade = QCheckBox()
        weighted_grade.setText("Slutbetyget sammanvägs")
        self.fields["weighted"] = weighted_grade
        parts_info.addWidget(weighted_grade)
        part2_form.addRow("Antal delmoment:", parts_info)
        self.part2_layout.addRow(part2_form)

        course_parts = QHBoxLayout()
        course_parts.addWidget(self.part2_part_list)
        course_parts.addWidget(self.part2_part_stack)
        self.part2_layout.addRow(course_parts)

        # Undervisningsformer
        teaching_forms = QHBoxLayout()
        teaching = ["teaching_Föreläsningar", "teaching_Gruppundervisning", "teaching_Seminarier", "teaching_Övningar",
                    "teaching_Projektarbeten", "teaching_Handledning", "teaching_Exkursioner", "teaching_Laborationer"]
        vert1 = QVBoxLayout()
        vert2 = QVBoxLayout()
        for option in teaching[:4]:
            item = QCheckBox()
            item.setText(option.lstrip("teaching_"))
            self.fields[option] = item
            vert1.addWidget(item)
        for option in teaching[4:]:
            item = QCheckBox()
            item.setText(option.lstrip("teaching_"))
            self.fields[option] = item
            vert1.addWidget(item)
        teaching_forms.addItem(vert1)
        teaching_forms.addItem(vert2)
        self.part2_layout.addRow("Undervisningsformer:", teaching_forms)

        online = QComboBox()
        online.setPlaceholderText("-- Ange undervisningsform --")
        online.addItem("Ja")
        online.addItem("Nej")
        self.fields["online_course"] = online
        self.part2_layout.addRow("Distansundervisning:", online)

        # Kursdeltagande
        mandatory = QHBoxLayout()
        tasks = ["task_Föreläsningar", "task_Gruppundervisning", "task_Seminarier", "task_Övningar",
                 "task_Projektarbeten", "task_Handledning", "task_Exkursioner", "task_Laborationer"]
        mandatory1 = QVBoxLayout()
        mandatory2 = QVBoxLayout()
        for option in tasks[:4]:
            item = QCheckBox()
            item.setText(option.lstrip("task_"))
            self.fields[option] = item
            mandatory1.addWidget(item)
        for option in tasks[4:]:
            item = QCheckBox()
            item.setText(option.lstrip("task_"))
            self.fields[option] = item
            mandatory1.addWidget(item)
        mandatory.addItem(mandatory1)
        mandatory.addItem(mandatory2)
        self.part2_layout.addRow("Kursdeltagande:", mandatory)

        # Kompletteringsalternativ
        completion_box = QComboBox()
        completion_box.setPlaceholderText("-- Välj komplettering --")
        self.fields["completion"] = completion_box
        completion_box.addItem("Komplettering Fx till E")
        completion_box.addItem("Komplettering Fx till A-E")
        completion_box.addItem("Komplettering U till G")
        completion_box.addItem("Ej komplettering Fx till E")
        completion_box.addItem("Ej komplettering U till G")
        self.part2_layout.addRow("Komplettering:", completion_box)

        # Ej tillåtna huvudområden/kurser
        forbidden_main = QLineEdit()
        forbidden_main.setPlaceholderText("Huvudområde")
        self.fields["forbidden_main"] = forbidden_main
        self.part2_layout.addRow("Kan ej ingå i examen inom:", forbidden_main)

        forbidden_courses = QLineEdit()
        forbidden_courses.setPlaceholderText("Lista kurser här")
        self.fields["forbidden_course"] = forbidden_courses
        self.part2_layout.addRow("Kan ej ingå i examen med:", forbidden_courses)

        # Programtillhörighet
        program = QLineEdit()
        program.setPlaceholderText("Utblidningsprogram")
        self.fields["program"] = program
        self.part2_layout.addRow("Ingår i program:", program)

        # Övriga
        relations = QComboBox()
        relations.setPlaceholderText("-- Ange hur kursen ges --")
        relations.addItem("Fristående")
        relations.addItem("Ingår i program")
        relations.addItem("Program och fristående")
        self.fields["relations"] = relations
        self.part2_layout.addRow("Kursen ges som:", relations)

    def create_part3(self, file):
        self.stack.addWidget(self.part3)
        part3_text = QTextEdit(self.part3)
        part3_text.setReadOnly(True)
        display_text = open(file)
        part3_text.setHtml(display_text.read())
        display_text.close()
        self.part3_layout.addWidget(part3_text)
        self.part3.setLayout(self.part3_layout)

    def remove_part3(self):
        self.part3_layout.removeItem(self.part3_layout.itemAt(0))

    def create_part(self):
        """
        Create a form for a course part
        :return: course part form layout
        """
        layout = QFormLayout()
        part_info = {}
        # Namn
        part_desc = QHBoxLayout()
        part_name = QLineEdit()
        part_name.setPlaceholderText("Namn på moment")
        part_info["part_name"] = part_name
        part_desc.addWidget(part_name)

        # Generell information: betygsinformation, beskrivning
        part_required = QRadioButton()
        part_required.setText("Betygsavgörande")
        part_info["part_required"] = part_required
        part_desc.addWidget(part_required)
        layout.addRow("Information:", part_desc)

        # Betygsättning
        part_grading = QComboBox()
        part_grading.setPlaceholderText("-- Ange betygsskala --")
        part_info["part_grading"] = part_grading
        part_grading.addItem("AF - sjugradig")
        part_grading.addItem("UV - tregradig")
        part_grading.addItem("UG - tvågradig")
        layout.addRow("Betygsskala:", part_grading)

        # Högskolepoäng
        part_credits = QLineEdit()
        part_info["part_credits"] = part_credits
        part_credits.setValidator(QDoubleValidator())
        layout.addRow("Högskolepoäng:", part_credits)

        # Examinationsform
        part_exam = QComboBox()
        part_exam.setPlaceholderText("-- Examinationsform --")
        part_info["part_exam"] = part_exam
        part_exam.addItem("Skriftligt prov")
        part_exam.addItem("Muntligt prov")
        part_exam.addItem("Skriftligt och mutligt prov")
        part_exam.addItem("Skriftliga redovisningar")
        part_exam.addItem("Muntliga redovisningar")
        part_exam.addItem("Övningar")
        part_exam.addItem("Laborationsrapporter")
        part_exam.addItem("Rapporter från exkursioner")
        part_exam.addItem("Praktik")
        part_exam.addItem("Opposion på andras uppgifter")
        part_exam.addItem("Aktivitet på seminarier")
        layout.addRow("Examinationsform:", part_exam)

        # Förväntade kunskaper
        part_goal = QLineEdit()
        part_goal.setPlaceholderText("Lista förväntade kunskaper")
        part_info["part_goal"] = part_goal
        layout.addRow("Förväntade kunskaper:", part_goal)

        self.fields["part_" + str(self.parts)] = part_info
        return layout

    def create_actions(self):
        """
        Create action buttons
        """
        action_btns = QDialogButtonBox()
        action_btns.setStandardButtons(
            QDialogButtonBox.Apply |
            QDialogButtonBox.Discard |
            QDialogButtonBox.Close
        )

        # Swedish text on buttons
        action_btns.button(QDialogButtonBox.Apply).setText("Fortsätt")
        action_btns.button(QDialogButtonBox.Discard).setText("Rensa")
        action_btns.button(QDialogButtonBox.Close).setText("Tillbaka")

        # Add buttons to dictionary
        self.buttons["Nästa"] = action_btns.button(QDialogButtonBox.Apply)
        self.buttons["Rensa"] = action_btns.button(QDialogButtonBox.Discard)
        self.buttons["Tillbaka"] = action_btns.button(QDialogButtonBox.Close)

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

    def warning(self):
        """
        Warning dialog if incompatible input
        :param name: name of field that is incorrect
        """
        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Warning)
        dialog.setWindowTitle("Felaktigt fält!")
        dialog.setText("Det finns fält med felaktiga värden.")
        dialog.setInformativeText("Se den inbyggda manualen för mer information.")
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.show()

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

    def new_part(self):
        """
        Method for creating required number of course parts
        """
        while self.parts < self.fields["parts"].value():    # using < here to avoid hanging if user decreases value
            if self.parts < self.fields["parts"].value():
                course_part = self.create_part()
                self.part2_part_list.insertItem(self.parts, "Kursmoment " + str(self.parts + 1))
                course_stack = QWidget()
                course_stack.setLayout(course_part)
                self.part2_part_stack.addWidget(course_stack)
                self.parts += 1

    def part_switch(self, part):
        """
        Switch between course parts in list menu
        :param: index of course part to switch to
        """
        self.part2_part_stack.setCurrentIndex(part)

    def check_invalid(self, fields):
        """
        Check if a form field is invalid before proceeding.
        """
        invalid_fields = False
        for name, field in fields.items():
            if name == "course_code":
                try:
                    code_check(fields["course_code"].text())
                except Exception:
                    field.setStyleSheet("QLineEdit" "{ background: pink; }")
                    invalid_fields = True
                else:
                    field.setStyleSheet("QLineEdit" "{ background: lightgreen; }")
            elif name == "forbidden_main" or name == "forbidden_course" or name == "program":
                field.setStyleSheet("QLineEdit" "{ background: lightgreen; }")
            elif name == "requirements" and self.fields["eligibility"] != "Särskild behörighet":
                field.setStyleSheet("QLineEdit" "{ background: lightgreen; }")
            elif isinstance(field, QLineEdit) and field.text() == "":
                field.setStyleSheet("QLineEdit" "{ background: pink; }")
                invalid_fields = True
            elif isinstance(field, QComboBox) and field.currentText()[0] == "-":
                field.setStyleSheet("QComboBox" "{ background: pink; }")
                invalid_fields = True
            elif isinstance(field, dict):
                invalid_fields = self.check_invalid(field)
            elif isinstance(field, QLineEdit):
                field.setStyleSheet("QLineEdit" "{ background: lightgreen; }")
            elif isinstance(field, QComboBox):
                field.setStyleSheet("QComboBox" "{ background: lightgreen; }")

        return invalid_fields
