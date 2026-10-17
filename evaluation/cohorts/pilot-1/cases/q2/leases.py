"""A serially accessed queue for a bounded import batch."""

from copy import deepcopy


class BatchQueue:
    def __init__(self):
        self._keys = {}
        self._jobs = {}
        self._next_token = 0

    def enqueue(self, key, payload):
        if not isinstance(key, str) or not key:
            raise ValueError("key must be a nonempty string")
        if key in self._keys:
            job_id = self._keys[key]
            if self._jobs[job_id]["payload"] != payload:
                raise ValueError("key already identifies a different payload")
            return job_id
        job_id = len(self._jobs) + 1
        self._keys[key] = job_id
        self._jobs[job_id] = {
            "payload": deepcopy(payload),
            "state": "pending",
            "owner": None,
            "token": None,
            "deadline": None,
            "result": None,
        }
        return job_id

    def reserve(self, owner, now, ttl):
        if ttl <= 0:
            raise ValueError("lease duration must be positive")
        for job_id, job in self._jobs.items():
            eligible = job["state"] == "pending" or (
                job["state"] == "leased" and now >= job["deadline"]
            )
            if not eligible:
                continue
            self._next_token += 1
            job.update(
                state="leased",
                owner=owner,
                token=self._next_token,
                deadline=now + ttl,
            )
            return {
                "job_id": job_id,
                "token": job["token"],
                "payload": deepcopy(job["payload"]),
            }
        return None

    def finish(self, job_id, token, result, now):
        job = self._jobs[job_id]
        if (
            job["state"] != "leased"
            or job["token"] != token
            or now >= job["deadline"]
        ):
            return False
        job.update(state="done", result=deepcopy(result), owner=None)
        return True

    def inspect(self, job_id):
        job = self._jobs[job_id]
        return deepcopy({
            "state": job["state"],
            "payload": job["payload"],
            "result": job["result"],
        })
