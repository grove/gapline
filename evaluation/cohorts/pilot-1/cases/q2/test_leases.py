import unittest

from leases import BatchQueue


class QueueTests(unittest.TestCase):
    def test_completion_keeps_the_operation_identity(self):
        queue = BatchQueue()
        job = queue.enqueue("invoice/17", {"row": 17})
        lease = queue.reserve("worker-a", 0, 10)
        self.assertTrue(queue.finish(job, lease["token"], {"imported": 1}, 2))
        self.assertEqual(queue.enqueue("invoice/17", {"row": 17}), job)
        self.assertEqual(queue.inspect(job)["result"], {"imported": 1})
        self.assertIsNone(queue.reserve("worker-b", 3, 10))
        with self.assertRaises(ValueError):
            queue.enqueue("invoice/17", {"row": 18})

    def test_reissued_lease_fences_old_worker(self):
        queue = BatchQueue()
        job = queue.enqueue("page/1", [1])
        old = queue.reserve("slow", 0, 10)
        new = queue.reserve("replacement", 10, 10)
        self.assertNotEqual(old["token"], new["token"])
        self.assertFalse(queue.finish(job, old["token"], "late", 11))
        self.assertTrue(queue.finish(job, new["token"], "ok", 12))
        self.assertFalse(queue.finish(job, new["token"], "twice", 13))

    def test_values_are_detached(self):
        queue = BatchQueue()
        payload = {"rows": [1]}
        job = queue.enqueue("page/1", payload)
        payload["rows"].append(2)
        lease = queue.reserve("worker", 0, 10)
        lease["payload"]["rows"].append(3)
        result = {"accepted": [1]}
        queue.finish(job, lease["token"], result, 1)
        result["accepted"].append(4)
        self.assertEqual(queue.inspect(job), {
            "state": "done", "payload": {"rows": [1]},
            "result": {"accepted": [1]},
        })


if __name__ == "__main__":
    unittest.main()
