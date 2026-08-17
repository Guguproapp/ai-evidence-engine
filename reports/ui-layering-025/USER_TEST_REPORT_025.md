# AEE 公開 UI 資訊分層驗收報告

- 日期：2026-08-17
- Production：https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site
- Sites Version：9
- Source Commit：`2842119e18758cd4a3c0a67b9654c88f5aa638b9`
- 修改範圍：資訊架構、顯示文案、錯誤訊息與 Developer Details；未修改驗證決策或證據資料。

## 驗收結果

| 項目 | 環境 | 結果 | 實際畫面行為 |
|---|---|---|---|
| Unverified 圖片 | Production Desktop | PASS | 顯示「無法確認來源」與安全說明，不顯示檔名、完整 SHA-256 或內部原因碼。 |
| Verified Modified | Production Desktop | PASS | 保留已驗證修改版本、C2PA、簽章、來源履歷及短內容指紋。 |
| Invalid Evidence | Production Desktop | PASS | 顯示「證據無法驗證」，內部 validation code 預設隱藏。 |
| 超過 10 MB | Production Desktop | PASS | 顯示「檔案太大，請選擇 10 MB 以下的圖片。」 |
| Corrupt Image | Production Desktop | PASS | 顯示可理解錯誤，SDK 錯誤碼僅在技術細節展開後顯示；結果區不殘留前一筆驗證。 |
| Developer Details | Production Desktop | PASS | 可展開／收合；完整 SHA-256、原始檔名、Manifest、Registry、Identity、AI evidence、Reason code、Canonical JSON 均保留。 |
| 繁體中文 | Production Desktop | PASS | 白話摘要與錯誤訊息完整。 |
| English | Production Desktop | PASS | 顯示 Unable to confirm source；內部檔名與 reason code 預設隱藏。 |
| Mobile | Production Responsive 390×844 | PASS | 無水平溢出；摘要與技術細節可正常閱讀。這是 responsive viewport 驗收，不冒充實體手機測試。 |
| Desktop | Production Chrome | PASS | 主要結果、摘要與技術細節分層正確。 |

## 修改前後證據

### 修改前

- `before/desktop-unverified.png`
- `before/desktop-oversize.png`

修改前一般畫面直接顯示測試檔名、完整 SHA-256、Registry、Manifest、Identity Trust、AI internal wording 與 reason code。

### 修改後（公開 Production）

- `after/desktop/unverified-summary-production.png`
- `after/desktop/unverified-developer-details-production.png`
- `after/desktop/verified-modified-production.png`
- `after/desktop/invalid-evidence-production.png`
- `after/desktop/unverified-english-production.png`
- `after/mobile/unverified-390x844-production.png`
- `after/mobile/developer-details-390x844-production.png`

## 自動測試

- Web Tests：14/14 PASS
- Lint：PASS
- Production Build：PASS
- `git diff --check`：PASS
- Secret / Private Key pattern scan（本輪程式檔）：PASS，未發現命中

## 不變項確認

- Verification Decision Engine：未修改
- Provenance State：未修改
- Integrity State：未修改
- C2PA 判定：未修改
- Registry 判定：未修改
- Hash 計算：未修改
- Event / Signed Payload：未修改
- Legacy Verification：未修改
