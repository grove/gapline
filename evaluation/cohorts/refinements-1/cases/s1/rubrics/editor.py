from dataclasses import dataclass


@dataclass
class Criterion:
    key: str
    name: str
    maximum: int


@dataclass(frozen=True)
class Edition:
    number: int
    title: str
    criteria: tuple[Criterion, ...]


class Draft:
    def __init__(self, title):
        if not title.strip():
            raise ValueError('title is required')
        self.title = title
        self._criteria = []

    def add(self, key, name, maximum):
        if not key or not name.strip() or type(maximum) is not int or maximum <= 0:
            raise ValueError('invalid criterion')
        if any(item.key == key for item in self._criteria):
            raise ValueError('duplicate criterion')
        self._criteria.append(Criterion(key, name, maximum))

    def revise(self, key, *, name=None, maximum=None):
        item = next((item for item in self._criteria if item.key == key), None)
        if item is None:
            raise KeyError(key)
        if name is not None and not name.strip():
            raise ValueError('name is required')
        if maximum is not None and (type(maximum) is not int or maximum <= 0):
            raise ValueError('maximum must be a positive integer')
        if name is not None:
            item.name = name
        if maximum is not None:
            item.maximum = maximum

    def remove(self, key):
        for index, item in enumerate(self._criteria):
            if item.key == key:
                del self._criteria[index]
                return
        raise KeyError(key)

    def freeze(self, number):
        if not self._criteria:
            raise ValueError('cannot publish an empty rubric')
        return Edition(number, self.title, tuple(self._criteria))
