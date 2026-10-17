# Notification recipients

`recipients(primary, secondary)` combines two ordered lists of user IDs. Each
user must receive at most one notification, even when present in both lists.
The result preserves the order of each user's first appearance. Inputs contain
non-empty string IDs; equality of the exact IDs identifies the same user.
