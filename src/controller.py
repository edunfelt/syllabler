class SyllablerCtrl:
    """Syllabler controller"""

    def __init__(self, view):
        self.view = view
        self.signals()

    def switch_page(self):
        """
        Method for switching to page 2 of the form
        """

    def save_data(self):
        """
        Method for saving current form data to json file
        """

    def reset_form(self):
        """
        Method for emptying all form fields without saving
        """

    def signals(self):
        """
        Method for connecting signals to viewer slots
        """
        self.view.buttons["Hjälp"].clicked.connect(self.view.handbook)
        self.view.buttons["Nästa"].clicked.connect(self.switch_page)
        self.view.buttons["Spara"].clicked.connect(self.save_data)
        self.view.buttons["Rensa"].clicked.connect(self.reset_form)
