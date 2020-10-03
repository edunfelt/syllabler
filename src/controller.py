from functools import partial


class SyllablerCtrl:
    """Syllabler controller"""

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.signals()

    def save_course_data(self):
        """
        Method for saving current form data to json file
        """
        data = self.view.get_data()
        self.model.set_swe_name(data["swe_name"])
        self.model.set_eng_name(data["eng_name"])
        try:
            self.model.set_course_code(data["course_code"])
        except Exception:
            self.view.warning("Kod")
        else:
            self.model.set_course_credits(data["course_credits"])
            self.model.set_level(data["level"])
            self.model.set_grading_scale(data["grading_scale"])
            self.model.set_main_area(data["main_area"])
            self.model.set_specialisation(data["specialisation"])
            self.model.set_department(data["department"])
            self.model.set_semester(data["semester"])
            self.model.set_eligibility(data["eligibility"])
            self.model.set_requirements(data["requirements"])
            self.model.save_course()

    def signals(self):
        """
        Method for connecting signals to viewer slots
        """
        # Action buttons (on every page)
        self.view.buttons["Hjälp"].clicked.connect(self.view.handbook)
        self.view.buttons["Nästa"].clicked.connect(self.view.switch_page)
        self.view.buttons["Spara"].clicked.connect(partial(self.save_course_data))
        self.view.buttons["Rensa"].clicked.connect(self.view.reset_form)
        self.view.buttons["Avsluta"].clicked.connect(self.view.close_form)

        # Form part 1, huvudområde finns/saknas
        self.view.fields["main_area_false"].toggled.connect(self.view.main_area_switch)
        self.view.fields["main_area_true"].toggled.connect(self.view.main_area_switch)

        # Form part 1, utbildningsnivå grund/avancerad
        self.view.fields["level"].activated.connect(self.view.eligibility_switch)

        # Form part 1, särskild behörighet
        self.view.fields["eligibility"].currentIndexChanged.connect(self.view.eligibility_list)
