import unittest

from changes import ChangeFeed, CursorExpired


class ChangeTests(unittest.TestCase):
    def test_pages_include_repeated_keys_and_tombstones(self):
        feed = ChangeFeed()
        feed.put("note/1", {"text": "draft"})
        feed.put("note/1", {"text": "ready"})
        feed.delete("note/1")
        first = feed.begin(0, 2)
        last = feed.resume(first.continuation, 2)
        self.assertEqual(first.events, (
            (1, "note/1", {"text": "draft"}),
            (2, "note/1", {"text": "ready"}),
        ))
        self.assertEqual(last.events, ((3, "note/1", None),))
        self.assertIsNone(last.continuation)
        self.assertEqual(last.checkpoint, 3)

    def test_compaction_rejects_old_cursor(self):
        feed = ChangeFeed()
        feed.put("note/1", {})
        feed.delete("note/1")
        feed.compact(1)
        with self.assertRaises(CursorExpired):
            feed.begin(0, 1)
        self.assertEqual(feed.begin(1, 1).events, ((2, "note/1", None),))

    def test_returned_values_do_not_change_history(self):
        feed = ChangeFeed()
        value = {"tags": ["work"]}
        feed.put("note/1", value)
        value["tags"].append("changed")
        page = feed.begin(0, 10)
        page.events[0][2]["tags"].clear()
        self.assertEqual(feed.begin(0, 10).events[0][2], {"tags": ["work"]})


if __name__ == "__main__":
    unittest.main()
