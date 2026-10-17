# Notification deliveries

`recipients(primary, secondary)` combines two ordered lists of delivery
requests. Each occurrence is a separate requested delivery, even when the same
user ID occurs more than once. Preserve every occurrence and its input order,
with primary requests before secondary requests. Inputs contain non-empty
string IDs.
