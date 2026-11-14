#!/usr/bin/env python3
"""Conservative PDF importer. Never marks answers verified."""
import argparse, json, re, datetime
from pathlib import Path

SOURCES = {
 "1465": ("general_1465.pdf", 1465, "一般業（重要資料）重新排序版112.07.22(1465題).pdf"),
 "1000": ("reference_1000.pdf", 1000, "參考試題1000題.pdf"),
}
CIRCLED = "①②③④"
def clean(s):
 return re.sub(r"\\s+", " ", s).strip()

def parse_1465(path):
 import fitz
 doc=fitz.open(path)
 section="未分類"
 found=[]
 for page_index,page in enumerate(doc):
  lines=page.get_text(sort=True).splitlines()
  current=None
  for line in lines:
   s=line.strip()
   if not s: continue
   m=re.match(r"^(\\d{1,4})\\s*[.．、]\\s*[(（]\\s*([1-4])\\s*[)）]\\s*(.*)",s)
   if m:
    if current: found.append(current)
    current={"number":m.group(1),"answer":int(m.group(2))-1,"raw":m.group(3),"page":page_index+1,"category":section}
   elif current:
    current["raw"]+=" "+s
   elif len(s)<35 and not re.search(r"\\d+[.．]",s) and "題" not in s:
    section=s
  if current: found.append(current)
 out=[]
 for r in found:
  text=r["raw"]
  parts=re.split(r"([①②③④])",text)
  if len(parts)<9: continue
  question=clean(parts[0])
  opts=[clean(parts[i]) for i in (2,4,6,8)]
  # Ignore commentary following the fourth option: require human review of raw extraction.
  if question and all(opts):
   out.append((r,question,opts))
 return out

def parse_1000(path):
 import pdfplumber
 out=[]
 with pdfplumber.open(path) as pdf:
  for page_index,page in enumerate(pdf.pages):
   for table in page.extract_tables() or []:
    for cells in table:
     cells=[clean(x or "") for x in cells]
     joined=" ".join(cells)
     m=re.search(r"\\b(\\d{1,4})\\s*[.．]\\s*[(（]\\s*([1-4])\\s*[)）]",joined)
     if not m: continue
     opts=[]
     for c in cells:
      z=re.match(r"^[①②③④]\\s*(.*)",c)
      if z: opts.append(clean(z.group(1)))
     if len(opts)!=4: continue
     stem=clean(joined.split("①")[0])
     stem=re.sub(r"^.*?\\b"+re.escape(m.group(1))+r"\\s*[.．]\\s*[(（]\\s*[1-4]\\s*[)）]","",stem).strip()
     if stem:
      out.append(({"number":m.group(1),"answer":int(m.group(2))-1,"page":page_index+1,"category":"原檔未標示章節"},stem,opts))
 return out

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--source-dir",default="sources")
 ap.add_argument("--output",default="data/questions.json")
 ap.add_argument("--report",default="data/import_report.json")
 args=ap.parse_args()
 path=Path(args.output)
 data=json.loads(path.read_text(encoding="utf-8"))
 existing={q["id"]:q for q in data["questions"]}
 report={"date":datetime.date.today().isoformat(),"sources":{}}
 for code,(filename,expected,display) in SOURCES.items():
  source=Path(args.source_dir)/filename
  if not source.exists():
   report["sources"][code]={"status":"missing_source","expected":expected}
   continue
  parsed=parse_1465(source) if code=="1465" else parse_1000(source)
  added=0; conflicts=0; duplicates=0
  seen=set()
  for raw,stem,options in parsed:
   n=raw["number"]; key=f"{code}-{int(n):04d}"
   if key in seen: duplicates+=1; continue
   seen.add(key)
   if key in existing:
    old=existing[key]
    if clean(old["question"])!=stem or [clean(x) for x in old["options"]]!=options:
     conflicts+=1
    continue
   existing[key]={"id":key,"source_document":display,"source_page":raw["page"],"original_number":n,
    "category":raw["category"],"question":stem,"options":options,"original_answer":raw["answer"],
    "answer":raw["answer"],"status":"unverified","explanation":"原始題庫答案，尚未完成法規校正。",
    "verified_at":None,"source_url":None}
   added+=1
  report["sources"][code]={"status":"parsed","expected":expected,"extracted":len(parsed),
   "added":added,"conflicts":conflicts,"duplicate_numbers":duplicates,
   "warning":"PDF 擷取結果必須對照原稿檢查；未匯入或衝突題目不可視為完成"}
 data["questions"]=sorted(existing.values(),key=lambda q:(q["id"].split("-")[0],int(q["original_number"])))
 data["updated_at"]=datetime.date.today().isoformat()
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
 Path(args.report).parent.mkdir(parents=True,exist_ok=True)
 Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
