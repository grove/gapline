# Shift worksheet desk

An assembly workshop maintains approved inspection templates and generates dated
worksheets for morning and evening shifts. Supervisors can prepare worksheets in
advance. Operators tick tasks and keep the completed worksheet as the shift record.

The governing product requirements are in `POLICY.md`. `desk/templates.py` stores
approved revisions, `desk/worksheets.py` owns generated sheets, and `desk/service.py`
coordinates approval and generation. Storage is in memory for a single desk.
Public APIs accept ISO date objects, shift names `morning` and `evening`, and named
tasks. Generated references are sequential local identifiers. A template's task
keys are unique, and worksheets expose task text and revision for operators.

Run `python3 -m unittest discover -s tests -v` from this directory.
