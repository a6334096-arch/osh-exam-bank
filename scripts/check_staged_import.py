#!/usr/bin/env python3
"""Gate a staged PDF extraction before replacing the live question bank.

Usage: python scripts/check_staged_import.py data/staging/questions_candidate.json
No writes are performed. Extraction is not legal verification.
"""
import json, sys, collections
from pathlib import Path

candidate = Path(sys.argv[1] if len(sys.argv)>1 else "data/staging/questions_candidate.json")
live = Path("data/questions.json")
data = json.loads(candidate.read_text(encoding="utf-8"))
existing = json.loads(live.read_text(encoding="utf-8"))
questions = data["questions"]
ids = [q["id"] for q in questions]
assert data.get("schema_version")==1, "Unexpected schema"
assert len(ids)==len(set(ids)), "Duplicate IDs"
assert len(questions)>=len(existing["questions"]), "Candidate would remove questions"
by_id = {q["id"]:q for q in questions}
for old in existing["questions"]:
    new = by_id.get(old["id"])
    assert new, f"Missing existing ID: {old['id']}"
    if old["status"]=="verified":
        for key in ("status","answer","verified_at","source_url","explanation"):
            assert new.get(key)==old.get(key), f"Verified evidence changed: {old['id']} {key}"
for q in questions:
    assert isinstance(q.get("question"),str) and q["question"].strip(), q.get("id")
    assert isinstance(q.get("options"),list) and len(q["options"])==4, q.get("id")
    assert all(isinstance(o,str) and o.strip() for o in q["options"]), q.get("id")
    assert q.get("answer") in (0,1,2,3,None), q.get("id")
    assert q.get("status") in ("verified","unverified","needs_review"), q.get("id")
    assert isinstance(q.get("source_page"),int) and q["source_page"]>0, q.get("id")
    if q["status"]=="verified":
        assert q.get("source_url") and q.get("verified_at") and q.get("explanation"), q.get("id")
print("STAGED IMPORT FORMAT PASS:",len(questions),"questions")
print("BY SOURCE:",dict(collections.Counter(q["id"].split("-")[0] for q in questions)))
print("STATUS:",dict(collections.Counter(q["status"] for q in questions)))
print("NOTE: Format validation does not confirm original PDF accuracy or current law.")
