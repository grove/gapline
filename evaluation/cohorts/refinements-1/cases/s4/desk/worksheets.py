from dataclasses import dataclass, field


@dataclass
class Worksheet:
    reference: int
    day: object
    shift: str
    revision: int
    tasks: tuple[tuple[str, str], ...]
    checked: set[str] = field(default_factory=set)
    complete: bool = False


class Worksheets:
    def __init__(self):
        self._items = {}

    def generate(self, day, shift, template):
        if shift not in ('morning', 'evening'):
            raise ValueError('unknown shift')
        key = (day, shift)
        if key not in self._items:
            self._items[key] = Worksheet(
                len(self._items) + 1, day, shift, template.revision, template.tasks
            )
        return self.view(day, shift)

    def mark(self, day, shift, task):
        sheet = self._items[(day, shift)]
        if sheet.complete:
            raise ValueError('worksheet is complete')
        if task not in dict(sheet.tasks):
            raise KeyError(task)
        sheet.checked.add(task)

    def finish(self, day, shift):
        sheet = self._items[(day, shift)]
        if sheet.checked != set(dict(sheet.tasks)):
            raise ValueError('worksheet has unchecked tasks')
        sheet.complete = True

    def view(self, day, shift):
        sheet = self._items[(day, shift)]
        return {
            'reference': sheet.reference, 'day': day, 'shift': shift,
            'revision': sheet.revision, 'tasks': sheet.tasks,
            'checked': frozenset(sheet.checked), 'complete': sheet.complete,
        }
