# 職業安全衛生行動題庫

本專案使用兩份參考 PDF 建立練習題庫。**匯入不等於校正**；未經人工核對官方現行法規的題目一律標示 `unverified`。

## 目前資料與流程

- `data/questions.json`：題目、原始答案、校正狀態、證據。
- `scripts/import_pdfs.py`：保守解析兩份 PDF，僅匯入能辨識完整題幹與四個選項的題目，保留已存在的人工校正內容；題號或文字衝突不會覆蓋。
- `scripts/review_queue.py`：產生 `data/review_report.json`，列出尚未核對及可能涉及法規版本的題目。**不會自動宣稱答案正確**。
- `data/import_report.json`：每份 PDF 擷取、衝突、缺來源狀態。
- `.github/workflows/import-review.yml`：每天台灣時間約 09:15 執行，亦可由 Actions 手動觸發。GitHub 排程可能延遲。
- `.github/workflows/validate.yml`：每次提交檢查基本資料結構。

## 必要設定：提供 PDF 來源

原始 PDF **沒有公開上傳至本儲存庫**。在 GitHub 儲存庫 Settings → Secrets and variables → Actions → New repository secret 建立：

1. `PDF_1465_URL`：可由 GitHub Actions 下載的 1,465 題 PDF 私密直連網址。
2. `PDF_1000_URL`：可由 GitHub Actions 下載的 1,000 題 PDF 私密直連網址。

請確保來源網址的權限及有效期限合適；**不要在公開儲存庫直接提交 PDF 或含權杖的網址**。未設定時，流程只產生缺少來源的報告，不會自動增加題目。

亦可在本機將 PDF 放入 `sources/general_1465.pdf` 與 `sources/reference_1000.pdf`，執行：

```bash
pip install pymupdf pdfplumber
python scripts/import_pdfs.py
python scripts/review_queue.py
python scripts/validate.py
```

`sources/` 已加入 `.gitignore`。

## 審核及完成標準

PDF 表格與換行可能造成漏題、誤切題幹或選項；匯入報告的擷取數量不能取代原始 PDF 的逐題對照。題庫預期共 2,465 題，兩份來源各自核對題號、選項及重複題號。法規題須查核正式來源、條文版本與施行日期，人工確認後才能設 `verified` 並附日期、來源連結與解析。自動化只準備待審清單，不會自行完成法律核對。

網站提供練習模式及答案解析模式，預設只顯示已核對題目。全部匯入、核對、部署及驗證完成前，**不得宣稱整個題庫完成**。
