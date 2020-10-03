import json


def code_check(course_code: str):
    """
    Check if a course code is of the form XXYZZZ
    :param course_code: Code to check
    :return: True if course code is valid, False otherwise
    """
    if len(course_code) != 6:
        raise Exception("Provided code is too short")

    if not course_code[0].isupper() and course_code[1].isupper():
        return False
    elif not course_code[2:].isdigit():
        return False
    else:
        return True


class Course(object):
    """Syllabler course model"""

    def __init__(self):
        """
        Create new course object
        """
        self.course_data = {}

    def set_swe_name(self, swe_name):
        self.course_data["swe_name"] = swe_name

    def get_swe_name(self):
        return self.course_data["swe_name"]

    def set_eng_name(self, eng_name: str):
        self.course_data["eng_name"] = eng_name

    def get_eng_name(self):
        return self.course_data["eng_name"]

    def set_course_code(self, course_code: str):
        if not code_check(course_code):
            raise TypeError("Course code is not of valid form")
        self.course_data["course_code"] = course_code

    def get_course_code(self):
        return self.course_data["course_code"]

    def set_course_credits(self, course_credits: float):
        self.course_data["course_credits"] = course_credits

    def get_course_credits(self):
        return self.course_data["course_credits"]

    def set_level(self, level: str):
        self.course_data["level"] = level

    def get_level(self):
        return self.course_data["level"]

    def set_grading_scale(self, grading_scale: str):
        self.course_data["grading_scale"] = grading_scale

    def get_grading_scale(self):
        return self.course_data["grading_scale"]

    def set_main_area(self, main_area: str):
        self.course_data["main_area"] = main_area

    def get_main_area(self):
        return self.course_data["main_area"]

    def set_specialisation(self, specialisation: str):
        self.course_data["specialisation"] = specialisation

    def get_specialisation(self):
        return self.course_data["specialisation"]

    def set_department(self, department: str):
        self.course_data["department"] = department

    def get_department(self):
        return self.course_data["department"]

    def set_semester(self, semester: str):
        self.course_data["semester"] = semester

    def get_semester(self):
        return self.course_data["semester"]

    def set_parts_number(self, parts: int):
        self.course_data["parts"] = parts

    def get_parts_number(self):
        return self.course_data["parts"]

    def set_part(self, part, part_name: str):
        self.course_data[part_name] = part

    def set_eligibility(self, eligibility: str):
        self.course_data["eligibility"] = eligibility

    def get_eligibility(self):
        return self.course_data["eligibility"]

    def set_requirements(self, requirements):
        self.course_data["requirements"] = requirements

    def get_requirements(self):
        return self.course_data["requirements"]

    def set_description(self, description: str):
        self.course_data["description"] = description

    def get_description(self):
        return self.course_data["description"]

    def set_teaching_form(self, teaching_form: str):
        self.course_data["teaching_form"] = teaching_form

    def get_teaching_form(self):
        return self.course_data["teaching_form"]

    def set_location(self, location: str):
        self.course_data["location"] = location

    def get_location(self):
        return self.course_data["location"]

    def set_mandatory(self, mandatory: str):
        self.course_data["mandatory"] = mandatory

    def get_mandatory(self):
        return self.course_data["mandatory"]

    def set_completion_options(self, completion_option: str):
        self.course_data["completion_option"] = completion_option

    def get_completion_option(self):
        return self.course_data["completion_option"]

    def set_main_forbidden(self, main_forbidden: str):
        self.course_data["main_forbidden"] = main_forbidden

    def get_main_forbidden(self):
        return self.course_data["main_forbidden"]

    def set_course_forbidden(self, course_forbidden: str):
        self.course_data["course_forbidden"] = course_forbidden

    def get_course_forbidden(self):
        return self.course_data["course_forbidden"]

    def set_program(self, program: str):
        self.course_data["program"] = program

    def get_program(self):
        return self.course_data["program"]

    def set_relations(self, relations: str):
        self.course_data["relations"] = relations

    def get_relations(self):
        return self.course_data["relations"]

    def save_course(self):
        with open("course_fields.json", "w", encoding="utf-8") as data:
            json.dump(self.course_data, data, indent=4, ensure_ascii=False)

    def get_course(self):
        return self.course_data


class CoursePart(object):
    def __init__(self, part_data: dict, part_name: str):
        """
        Create  course part
        :param part_data: Dictionary in which course part data should be stored
        :param part_name: Name of course part
        """
        self.part_data = part_data
        self.part_data["part_name"] = part_name

    def set_part_grading(self, grading_scale: str):
        self.part_data["part_grading"] = grading_scale

    def get_part_grading(self):
        return self.part_data["part_grading"]

    def set_part_credits(self, part_credits: float):
        self.part_data["part_credits"] = part_credits

    def get_part_credits(self):
        return self.part_data["part_credits"]

    def set_part_exam(self, exam_form: str):
        self.part_data["part_exam"] = exam_form

    def get_part_exam(self):
        return self.part_data["part_exam"]

    def set_part_goal(self, goal: str):
        self.part_data["part_goal"] = goal

    def get_part_goal(self):
        return self.part_data["part_goal"]

    def get_part(self):
        return self.part_data
