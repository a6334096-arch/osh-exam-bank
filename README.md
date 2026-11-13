# 職業安全衛生行動題庫

手機版職安題庫專案。**目前只有基礎架構，尚未匯入完整題庫，也尚未完成法規答案校正。**

- `data/questions.json`：題目資料；目前為空陣列。
- `scripts/validate.py`：檢查題號、選項、答案及法規核對資訊。
- `.github/workflows/validate.yml`：每次推送及 PR 自動檢查。
- `index.html`：手機版網站起始頁。

核對狀態：`unverified` 待核對、`needs_review` 有疑義、`verified` 已核對。已核對題目必須附日期及官方法規來源。

GitHub Pages 啟用：Settings → Pages → Deploy from a branch → main → /(root) → Save。

原始 PDF 暫不公開上傳；法規異動未來僅自動標記待審，不會未經人工核對就改答案。
