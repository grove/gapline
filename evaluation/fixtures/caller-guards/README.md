# Caller guards teaching fixture

Only register_user is the public API. Blank names are invalid; the internal
formatter intentionally relies on its caller to validate input.

Evaluator expectation (do not share with the audit agent): REFUTED /
WITHDRAWN public API defect after inspecting caller preconditions.
