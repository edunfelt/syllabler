import unittest
from src.model import Course
from src.model import code_check


class TestCourse(unittest.TestCase):
    def setUp(self):
        data = {}
        self.course = Course(data, "Course Name")

    def test_course_code(self):
        self.course.set_course_code("DA4002")
        self.assertTrue(code_check(self.course.get_course_code()))

        with self.assertRaises(Exception):
            self.course.set_course_code("DA")

        with self.assertRaises(Exception):
            self.course.set_course_code("DA40002")

        with self.assertRaises(TypeError):
            self.course.set_course_code("xxyzzz")


if __name__ == '__main__':
    unittest.main()
