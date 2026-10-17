# Cached lookup

`Lookup(fetch).get(key)` accepts string keys and returns the fetched value.
A successful value remains cached for the lifetime of the lookup: repeated
requests for a key must call the supplied `fetch` function only once. Different
keys are loaded independently. A failed fetch propagates its exception and
does not populate the cache, allowing the next request to retry.

Only the constructor and `get` are public. The small smoke test checks that
construction and one lookup finish without an exception; the other tests check
values and fetch interactions.
