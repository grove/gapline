class Catalog:
    def __init__(self):
        self._editions = {}
        self._next_number = 1

    def publish(self, draft):
        edition = draft.freeze(self._next_number)
        self._editions[edition.number] = edition
        self._next_number += 1
        return edition.number

    def get(self, number):
        return self._editions[number]

    def describe(self, number):
        edition = self.get(number)
        return {
            'number': number,
            'title': edition.title,
            'criteria': [
                {'key': row.key, 'name': row.name, 'maximum': row.maximum}
                for row in edition.criteria
            ],
        }
