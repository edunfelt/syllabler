from functools import partial
from src.view import *


class SyllablerCtrl:
    """Syllabler controller"""

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.signals()

    def save_course(self):
        """
        Method for saving current form data to json file
        :return: dictionary of all the current form data
        """
        data = {}
        if self.view.check_invalid(self.view.fields):
            self.view.warning()
        else:
            for name, field in self.view.fields.items():
                data[name] = get_data(field)
            with open("course_fields.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        self.model.read_data("course_fields.json")
        self.model.human_readable()

    def reset_form(self):
        """
        Method for emptying all form fields without saving
        """
        for name, field in self.view.fields.items():
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(0)
            else:
                pass
        self.view.fields["main_area_true"].setChecked(True)

    def close_form(self):
        """
        Method for closing the form (with a warning)
        """
        self.view.close()

    def next_page(self):
        """
        Method for moving to the next page of the form
        """
        if self.view.stack.currentWidget() is self.view.part1:
            self.view.stack.setCurrentIndex(1)
        elif self.view.stack.currentWidget() is self.view.part2:
            if self.view.check_invalid(self.view.fields):
                self.view.warning()
            else:
                self.save_course()
                self.view.create_part3("hr_texts.html")
                self.view.stack.setCurrentIndex(2)

    def prev_page(self):
        """
        Method for moving to the previous page
        """
        if self.view.stack.currentWidget() is self.view.part2:
            self.view.stack.setCurrentIndex(0)
        elif self.view.stack.currentWidget() is self.view.part3:
            self.view.remove_part3()
            self.view.stack.setCurrentIndex(1)

    def signals(self):
        """
        Method for connecting signals to viewer slots
        """
        # Action buttons (on every page)
        self.view.buttons["Hjälp"].clicked.connect(self.view.handbook)
        self.view.buttons["Nästa"].clicked.connect(partial(self.next_page))
        self.view.buttons["Rensa"].clicked.connect(partial(self.reset_form))
        self.view.buttons["Tillbaka"].clicked.connect(partial(self.prev_page))

        # Form part 1, huvudområde finns/saknas
        self.view.fields["main_area_false"].toggled.connect(self.view.main_area_switch)
        self.view.fields["main_area_true"].toggled.connect(self.view.main_area_switch)

        # Form part 1, utbildningsnivå grund/avancerad
        self.view.fields["level"].activated.connect(self.view.eligibility_switch)

        # Form part 1, särskild behörighet
        self.view.fields["eligibility"].currentIndexChanged.connect(self.view.eligibility_list)

        # Form part 2, kursmoment
        self.view.fields["parts"].valueChanged.connect(self.view.new_part)
        self.view.part2_part_list.currentRowChanged.connect(self.view.part_switch)
