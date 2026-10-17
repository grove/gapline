def charge(approved, ledger):
    """Reject declined payments without recording a capture."""
    if not approved:
        return {"status": "declined"}
    ledger.append("captured")
    return {"status": "captured"}
