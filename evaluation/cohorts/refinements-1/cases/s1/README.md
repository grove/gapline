# Studio assessment rubrics

A small in-memory service used by an art school to draft marking rubrics,
publish numbered editions, and calculate assessment percentages.

Teachers may continue editing a draft after publishing it. Publication freezes
the title, criterion order, criterion names, and maximum points for that edition.
An assessment always uses the edition recorded when it was submitted, so an
already recorded assessment has the same percentage after later draft edits.
A new publication picks up the current draft values.

Scores must supply exactly one entry for every published criterion, with each
score between zero and its maximum. Criterion keys are unique within a draft.
Removing the final criterion is allowed in a draft, but an empty draft cannot be
published. The service uses integral points and rounds percentages to two digits.

`rubrics/editor.py` handles authoring, `rubrics/catalog.py` stores editions, and
`rubrics/assessment.py` records and calculates results. All storage is local to
one service instance. Callers use these methods rather than mutating model fields.

Run the checks with `python3 -m unittest discover -s tests -v` from this directory.
