import hashlib
import json

def compute_hash(previous_hash, timestamp, actor, action, details):
    payload = json.dumps(
        {
            "pvh" : previous_hash,
            "tms" : timestamp.isoformat(),
            "actor" : actor,
            "action" : action,
            "details" : details,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()