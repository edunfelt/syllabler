import sys
import unittest
from src.view import SyllablerUI
from PyQt5.QtWidgets import *
from PyQt5.QtTest import QTest

app = QApplication(sys.argv)


class TestView(unittest.TestCase):
    """
    This is inspired by the following article: http://johnnado.com/pyqt-qtest-example/
    """

    def setUp(self):
        """
        Set up Syllabler GUI
        """
        self.syllabler = SyllablerUI()

    def test_defaults(self):
        """
        Test the default values of the form
        """
        for name, field in self.syllabler.fields.items():
            if isinstance(field, QLineEdit):
                self.assertEqual(field.text(), "")
            elif isinstance(field, QComboBox):
                self.assertEqual(field.currentText()[0], "-")
            elif name == "main_area_true":
                self.assertTrue(field.isChecked())

    def test_credits(self):
        """
        Test that only doubles are allowed in the credits field
        """
        course_credits = self.syllabler.fields["course_credits"]
        QTest.keyClicks(course_credits, "abc")
        self.assertEqual(course_credits.text(), "")

        course_credits.clear()
        QTest.keyClicks(course_credits, "a1b2c")
        self.assertEqual(course_credits.text(), "12")

        course_credits.clear()
        QTest.keyClicks(course_credits, "7.5")
        self.assertEqual(course_credits.text(), "7.5")
