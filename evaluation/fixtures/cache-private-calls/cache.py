class Lookup:
    def __init__(self, fetch):
        self._fetch = fetch
        self._values = {}

    def _load(self, key):
        return self._fetch(key)

    def get(self, key):
        if key not in self._values:
            self._values[key] = self._load(key)
        return self._values[key]
