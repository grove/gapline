from .templates import Templates
from .worksheets import Worksheets


class Desk:
    def __init__(self):
        self.templates = Templates()
        self.worksheets = Worksheets()

    def approve(self, tasks):
        return self.templates.approve(tasks)

    def prepare(self, day, shift):
        return self.worksheets.generate(day, shift, self.templates.current())

    def mark(self, day, shift, task):
        self.worksheets.mark(day, shift, task)

    def finish(self, day, shift):
        self.worksheets.finish(day, shift)

    def view(self, day, shift):
        return self.worksheets.view(day, shift)
