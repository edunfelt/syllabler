from functools import partial


class SyllablerCtrl:
    """Syllabler controller"""

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.signals()

    def signals(self):
        """
        Method for connecting signals to viewer slots
        """
        # Action buttons (on every page)
        self.view.buttons["Hjälp"].clicked.connect(self.view.handbook)
        self.view.buttons["Nästa"].clicked.connect(self.view.switch_page)
        self.view.buttons["Spara"].clicked.connect(partial(self.view.save_data))
        self.view.buttons["Rensa"].clicked.connect(self.view.reset_form)
        self.view.buttons["Avsluta"].clicked.connect(self.view.close_form)

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
