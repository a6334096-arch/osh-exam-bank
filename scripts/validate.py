import json
from pathlib import Path

path = Path("data/questions.json")
data = json.loads(path.read_text(encoding="utf-8"))
assert data.get("schema_version") == 1, "Unsupported schema version"
questions = data.get("questions")
assert isinstance(questions, list) and questions, "Missing questions"
seen = set()
counts = {"verified": 0, "unverified": 0, "needs_review": 0}
for q in questions:
    qid = q.get("id")
    assert isinstance(qid, str) and qid and qid not in seen, f"Invalid/duplicate ID: {qid}"
    seen.add(qid)
    assert isinstance(q.get("question"), str) and q["question"].strip(), f"Empty question: {qid}"
    opts = q.get("options")
    assert isinstance(opts, list) and len(opts) == 4, f"Not four options: {qid}"
    assert all(isinstance(o, str) and o.strip() for o in opts), f"Empty option: {qid}"
    assert q.get("status") in counts, f"Invalid status: {qid}"
    assert q.get("answer") in (0, 1, 2, 3, None), f"Invalid answer: {qid}"
    assert q.get("source_document") and isinstance(q.get("source_page"), int) and q["source_page"] > 0, f"Missing source reference: {qid}"
    if q["status"] == "verified":
        assert q["answer"] is not None and q.get("verified_at") and q.get("source_url"), f"Missing verification evidence: {qid}"
    if q["status"] == "needs_review":
        assert q.get("extraction_status") and q.get("raw_extracted_text"), f"Missing review context: {qid}"
    counts[q["status"]] += 1
print(f"Validated {len(seen)} questions: {counts}")
