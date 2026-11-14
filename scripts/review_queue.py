#!/usr/bin/env python3
"""Generate a human-review queue; no automatic legal answer changes."""
import json,datetime,re
from pathlib import Path
p=Path("data/questions.json")
data=json.loads(p.read_text(encoding="utf-8"))
qs=data["questions"]
queue=[]
for q in qs:
 reasons=[]
 if q["status"]!="verified": reasons.append("尚未完成官方來源核對")
 if q["status"]=="verified" and (not q.get("source_url") or not q.get("verified_at") or not q.get("explanation")):
  reasons.append("已核對題目缺少證據")
 if re.search("職業災害勞工保護法|教育訓練|管理辦法|施行細則|修正|罰鍰|人數|時數",q["question"]):
  reasons.append("涉及法規版本、施行日期或數值，應查核現行官方法規")
 if reasons: queue.append({"id":q["id"],"source_page":q.get("source_page"),"status":q["status"],"reasons":reasons})
summary={"generated_at":datetime.date.today().isoformat(),"expected":2465,"imported":len(qs),
 "verified":sum(q["status"]=="verified" for q in qs),
 "needs_review":sum(q["status"]=="needs_review" for q in qs),
 "unverified":sum(q["status"]=="unverified" for q in qs),
 "remaining_import":max(0,2465-len(qs)),"review_queue":queue}
Path("data/review_report.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
print("Imported:",summary["imported"],"Verified:",summary["verified"],"Review queue:",len(queue))
