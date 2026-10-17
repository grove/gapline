# Reservation intake

There are two public entry points. `submit(quantity)` accepts a request from
the web adapter and returns its queue message. `consume(message)` accepts
messages from that adapter or from independent partner producers and returns
an allocation record. Partner messages do not pass through `submit`.

Both entry points must reject quantities that are not integers from 1 through
100, inclusive. Booleans are not quantities. The queue payload is a mapping
with a `quantity` field; rejecting a missing field is acceptable.
