import os
import sys
import unittest
import psutil
from PyQt5.QtWidgets import *
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from src.controller import SyllablerCtrl
from src.model import Course
from src.view import SyllablerUI

app = QApplication(sys.argv)


# noinspection PyArgumentList
class TestCtrl(unittest.TestCase):
    def setUp(self):
        self.syllabler_ui = SyllablerUI()
        self.syllabler_ui.show()
        self.syllabler_model = Course()
        SyllablerCtrl(view=self.syllabler_ui, model=self.syllabler_model)

    def fill_form(self):
        """
        Fill out form, for testing purposes
        """
        for name, field in self.syllabler_ui.fields.items():
            if isinstance(field, QLineEdit):
                if name == "course_code":
                    field.setText("DA4002")
                else:
                    field.setText("Some text")
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(1)
            elif name == "main_area_false":
                field.setChecked(True)

    def test_save(self):
        """
        Test that save produces a json file as expected
        """
        save_btn = self.syllabler_ui.buttons["Spara"]

        # Assert that saving fails if course code is invalid
        QTest.mouseClick(save_btn, Qt.LeftButton)
        self.assertFalse(os.path.exists("course_fields.json"))

        # Assert success otherwise
        self.syllabler_ui.fields["course_code"].setText("DA4002")
        QTest.mouseClick(save_btn, Qt.LeftButton)
        self.assertTrue(os.path.exists("course_fields.json"))
        with open("course_fields.json", "r") as f:
            self.assertEqual(len(f.readlines()), 14)
        os.remove("course_fields.json")

    def test_clear(self):
        """
        Test that all fields are cleared when reset button is pressed
        """
        self.fill_form()
        clear_btn = self.syllabler_ui.buttons["Rensa"]
        QTest.mouseClick(clear_btn, Qt.LeftButton)
        for name, field in self.syllabler_ui.fields.items():
            if isinstance(field, QLineEdit):
                self.assertEqual(field.text(), "")
            elif isinstance(field, QComboBox):
                self.assertEqual(field.currentIndex(), 0)
            elif name == "main_area_true":
                self.assertTrue(field.isChecked())

    def test_exit(self):
        """
        Test that cancel button closes the form
        To fetch currently running processes and their pid's, the following thread was helpful:
        https://stackoverflow.com/questions/7787120/python-check-if-a-process-is-running-or-not
        """
        exit_btn = self.syllabler_ui.buttons["Avsluta"]

        for process in psutil.process_iter(attrs=["pid", "name"]):
            if process.info["name"] == "main.py":
                self.assertTrue(process.is_running())

        QTest.mouseClick(exit_btn, Qt.LeftButton)

        for process in psutil.process_iter(attrs=["pid", "name"]):
            if process.info["name"] == "main.py":
                self.assertFalse(process.is_running())

    def test_ok(self):
        """
        Test that the next button switches page and that the fields remain unchanged
        """
        self.fill_form()
        next_btn = self.syllabler_ui.buttons["Nästa"]

        QTest.mouseClick(next_btn, Qt.LeftButton)
        self.assertEqual(self.syllabler_ui.stack.currentIndex(), 1)

        QTest.mouseClick(next_btn, Qt.LeftButton)
        self.assertEqual(self.syllabler_ui.stack.currentIndex(), 0)
        for name, field in self.syllabler_ui.fields.items():
            if isinstance(field, QLineEdit):
                if name == "course_code":
                    self.assertEqual(field.text(), "DA4002")
                else:
                    self.assertEqual(field.text(), "Some text")
            elif isinstance(field, QComboBox):
                self.assertEqual(field.currentIndex(), 1)
            elif name == "main_area_false":
                self.assertTrue(field.isChecked)

    def test_level(self):
        """
        Test that level choice impacts eligibility options
        """
        level_box = self.syllabler_ui.fields["level"]

        level_box.setCurrentIndex(0)
        self.assertEqual(self.syllabler_ui.fields["eligibility"].count(), 2)

        level_box.setCurrentIndex(1)
        self.assertEqual(self.syllabler_ui.fields["eligibility"].count(), 2)

    def test_main_area(self):
        """
        Test that main area radio buttons changes available main area combo box
        """
        area_no = self.syllabler_ui.fields["main_area_false"]
        area_box = self.syllabler_ui.fields["main_area"]

        self.assertTrue(area_box.isEnabled())
        area_no.setChecked(True)
        self.assertFalse(area_box.isEnabled())

    def test_eligibility(self):
        """
        Test that the required line edit is visible if the eligibility status is "Särskild behörighet"
        """
        eligibility_box = self.syllabler_ui.fields["eligibility"]
        requirements = self.syllabler_ui.fields["requirements"]
        self.assertTrue(requirements.isHidden())
        eligibility_box.setCurrentIndex(0)
        self.assertFalse(requirements.isHidden())
