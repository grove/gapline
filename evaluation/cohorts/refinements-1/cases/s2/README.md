# Listening room

This service manages timed exhibition audio licenses and visitor listening runs.
An exhibition license allows admission during `[opens_at, closes_at)` in UTC.
Staff can revoke a license to stop subsequent admissions. All public timestamps
must be timezone-aware; a caller may supply a different timezone for the same instant.

The exhibition's visitor policy guarantees uninterrupted playback after admission:
a run admitted while a license was valid may finish after the license closes or
is revoked. Admission captures the admitted track list and the visitor name.
Subsequent track-list edits affect later admissions only. Finishing a run does not
check the current license. Run IDs are unguessable capabilities delivered by the
front desk; this library is not an HTTP authorization layer. A completed run may
be queried repeatedly with the same result. No new admission may use a closed or
revoked license. Empty exhibitions and blank visitor names are rejected.

`listening/licenses.py` owns license changes; `listening/runs.py` admits runs and
records completion; `listening/clock.py` normalizes timestamps. Storage is in memory.
Run `python3 -m unittest discover -s tests -v` from this directory.
