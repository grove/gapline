from dataclasses import dataclass


@dataclass(frozen=True)
class Template:
    revision: int
    tasks: tuple[tuple[str, str], ...]


class Templates:
    def __init__(self):
        self._approved = None
        self._next_revision = 1

    def approve(self, tasks):
        tasks = tuple((key, text) for key, text in tasks)
        if not tasks or any(not key.strip() or not text.strip() for key, text in tasks):
            raise ValueError('named tasks are required')
        if len({key for key, text in tasks}) != len(tasks):
            raise ValueError('duplicate task key')
        self._approved = Template(self._next_revision, tasks)
        self._next_revision += 1
        return self._approved.revision

    def current(self):
        if self._approved is None:
            raise ValueError('no approved template')
        return self._approved
