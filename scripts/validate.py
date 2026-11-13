import json,sys
from pathlib import Path
p=Path("data/questions.json")
data=json.loads(p.read_text(encoding="utf-8"))
assert data.get("schema_version")==1
seen=set()
for q in data["questions"]:
    assert isinstance(q.get("id"),str) and q["id"] not in seen
    seen.add(q["id"])
    assert q.get("status") in ("unverified","verified","needs_review")
    assert isinstance(q.get("options"),list) and len(q["options"])==4
    assert q.get("answer") in (0,1,2,3,None)
    if q["status"]=="verified":
        assert q["answer"] is not None and q.get("verified_at") and q.get("source_url")
print(f"Validated {len(seen)} questions")
