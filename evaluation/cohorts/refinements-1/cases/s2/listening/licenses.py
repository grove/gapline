from dataclasses import dataclass
from .clock import utc


@dataclass(frozen=True)
class Admission:
    exhibition: str
    tracks: tuple[str, ...]


@dataclass
class License:
    opens_at: object
    closes_at: object
    tracks: tuple[str, ...]
    revoked: bool = False


class Licenses:
    def __init__(self):
        self._items = {}

    def add(self, key, opens_at, closes_at, tracks):
        start, stop = utc(opens_at), utc(closes_at)
        tracks = self._tracks(tracks)
        if key in self._items or not key.strip() or stop <= start:
            raise ValueError('invalid or duplicate license')
        self._items[key] = License(start, stop, tracks)

    def _tracks(self, tracks):
        tracks = tuple(tracks)
        if not tracks or any(not track.strip() for track in tracks):
            raise ValueError('at least one named track is required')
        return tracks

    def replace_tracks(self, key, tracks):
        self._items[key].tracks = self._tracks(tracks)

    def revoke(self, key):
        self._items[key].revoked = True

    def admit(self, key, now):
        now = utc(now)
        item = self._items[key]
        if item.revoked or not item.opens_at <= now < item.closes_at:
            raise PermissionError('exhibition is not admitting visitors')
        return Admission(key, item.tracks)
