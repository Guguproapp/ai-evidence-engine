# AI Evidence Engine 真人操作測試報告 023

測試日期：2026-08-17  
公開 Verifier：https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site  
Development/Test Evidence Black Box：https://aee-continuity-demo-856572888721.asia-east1.run.app  
測試方法：以瀏覽器實際點擊、選擇檔案、等待畫面結果並保存完整 viewport 截圖。未以 API、Log 或程式碼推論取代使用者畫面驗收。

## 結論

- 真人操作測試：**FAIL**。既有簽署 Demo 與 Black Box 流程可完成，但公開 Verifier 對錯誤檔案仍保留預設 Demo 的「已驗證修改版本」，可能造成誤解。
- 桌機完整操作：**PASS**。
- 手機完整操作：**PASS（有 P1 UX 問題）**。
- 未知來源圖片：**PASS**，均顯示「尚未驗證」，AI 參與程度為未知。
- 錯誤檔案：**FAIL**，錯誤訊息正確，但公開結果區仍顯示 Demo 的成功狀態。
- Evidence Black Box：**PASS**，畫面實際顯示 Generation、Retention、Retrieval、SHA-256、Signed Event 再驗證與 Continuity PASS。
- VIDEO READY：**NO**。

## 桌機完整操作紀錄

| 步驟 | 操作內容 | 預期結果 | 實際結果 | 狀態 | 截圖 | 等待時間 | 問題 |
|---|---|---|---|---|---|---:|---|
| 01 | 開啟 AEE 首頁 | 首頁完整顯示 | 標題、Demo、上傳入口與圖片完整 | PASS | `desktop/01-home.png` | 5.38 秒 | 無 |
| 02 | 前往圖片選擇區 | 可看見上傳入口 | 上傳區與 Evidence ID 入口可見 | PASS | `desktop/02-ready-select-image.png` | 3.42 秒 | 無 |
| 03 | 選擇內建簽署圖片 | 檔案被接受 | `aee-signed-ai.png` 被接受 | PASS | `desktop/03-image-selected.png` | <1 秒 | 無 |
| 04 | 查看實際圖片 | 圖片完整顯示 | 圖片與檔名顯示 | PASS | `desktop/04-image-displayed.png` | <1 秒 | 無 |
| 05 | 等待驗證 | 顯示處理狀態 | 處理快於截圖延遲，截圖時已完成 | PASS | `desktop/05-verification-started.png` | <1 秒 | 無 |
| 06 | 查看驗證結果 | 已驗證修改版本 | Registry 符合 `proofcart-v3` | PASS | `desktop/06-verification-result.png` | 1.02 秒 | 無 |
| 07 | 查看來源資料 | 顯示 Passport、Event、Hash | 全部顯示 | PASS | `desktop/07-source-record.png` | <1 秒 | 無 |
| 08 | 查看版本歷史 | Version 1／2／3 可見 | Parent 與三版履歷可見 | PASS | `desktop/08-version-history.png` | <1 秒 | 需向下捲動 |
| 09 | 點修改區域遮罩 | 顯示實測修改區 | 黑底白色變更區與 4.8% 顯示 | PASS | `desktop/09-modification-mask.png` | 0.35 秒 | 無 |
| 10 | 查看 C2PA | 3 個 Manifest 與狀態可見 | 已內嵌 3 個版本 | PASS | `desktop/10-c2pa-result.png` | <1 秒 | 無 |
| 11 | 查看數位簽章 | 簽章有效、身分界線清楚 | 有效；Development identity | PASS | `desktop/11-digital-signature.png` | <1 秒 | 無 |
| 12 | 點 Gemini 解釋 | 解釋既有事實，不改狀態 | Gemini 2.5 Flash 回覆，狀態維持 | PASS | `desktop/12-gemini-explanation.png` | 5.57 秒 | 無 |
| 13 | 進入 Black Box | 明確標示 Development/Test | 標示清楚 | PASS | `desktop/13-blackbox-entry.png` | <1 秒 | 無 |
| 14 | 選擇內建 Evidence | ProofCart V3 被選取 | 選取成功 | PASS | `desktop/14-blackbox-evidence-selected.png` | <1 秒 | 無 |
| 15 | 點完整 Continuity 測試 | 開始保存 | 按鈕實際點擊 | PASS | `desktop/15-blackbox-seal-start.png` | <1 秒 | 無 |
| 16 | 等待 Google 保存 | 顯示處理狀態 | 處理中畫面保存 | PASS | `desktop/16-google-saving-wait.png` | <1 秒 | 無 |
| 17 | Google 保存完成 | 顯示完成與 PASS | 真實服務完成 | PASS | `desktop/17-google-save-complete.png` | 1.08 秒 | 無 |
| 18 | 查看保存編號 | Generation 可見 | Object Generation 顯示 | PASS | `desktop/18-object-generation.png` | <1 秒 | 無 |
| 19 | 查看保存期限 | Retention Expiration 可見 | 約 10 分鐘 Test Retention 顯示 | PASS | `desktop/19-retention-expiration.png` | <1 秒 | 無 |
| 20 | 查看重新取得 | Retrieval PASS | Generation 一致 | PASS | `desktop/20-evidence-retrieval.png` | <1 秒 | 無 |
| 21 | 查看 SHA-256 | Reverification PASS | 完整 SHA-256 顯示 | PASS | `desktop/21-sha256-reverification.png` | <1 秒 | 無 |
| 22 | 查看原 Event 再驗證 | Signature/Event Hash 有效 | PASS | PASS | `desktop/22-signed-event-reverification.png` | <1 秒 | 無 |
| 23 | 查看 Continuity | 一對一連續性 PASS | IDs、Hash、Event 全部一致 | PASS | `desktop/23-evidence-continuity-result.png` | <1 秒 | 無 |
| 24 | 查看完整 PASS | 最終結果清楚 | FINAL RESULT PASS | PASS | `desktop/24-complete-pass.png` | <1 秒 | 需捲動看完所有欄位 |

桌機主流程含逐步截圖保存共 **71.33 秒**。

## 任意圖片真人操作紀錄

每一類都從新的公開 Verifier 頁面，實際打開檔案選擇器、選擇檔案並查看畫面結果。檔案上傳後會自動開始驗證，沒有另一個需要點擊的「開始驗證」按鈕。

| 類型 | 讀取 | C2PA | Registry | 畫面結果 | AI 等級 | 狀態 | 截圖 | 時間 |
|---|---|---|---|---|---|---|---|---:|
| 公開領域手機照片 | 成功 | 0 | No Match | 尚未驗證 | 未知 | PASS | `unknown-images/01-normal-phone-photo.png` | 1.80 秒 |
| 公開領域網路圖 | 成功 | 0 | No Match | 尚未驗證 | 未知 | PASS | `unknown-images/02-unknown-web-image.png` | 1.98 秒 |
| 無來源 AI 圖 | 成功 | 0 | No Match | 尚未驗證 | 未知 | PASS | `unknown-images/03-ai-no-source.png` | 1.71 秒 |
| AEE 完整來源 AI 圖 | 成功 | 3 | `proofcart-v3` | 已驗證修改版本 | L4 | PASS | `unknown-images/04-ai-with-evidence.png` | 2.13 秒 |
| 裁切修改圖 | 成功 | 0 | No Match | 尚未驗證 | 未知 | PASS | `unknown-images/05-modified-crop.png` | 8.07 秒 |
| 瀏覽器實際截圖 | 成功 | 0 | No Match | 尚未驗證 | 未知 | PASS | `unknown-images/06-screenshot.png` | 2.96 秒 |
| 縮放轉 JPEG | 成功 | 0 | No Match | 尚未驗證 | 未知 | PASS | `unknown-images/07-resized-converted.png` | 1.71 秒 |
| 損壞 PNG | 拒絕 | 無結果 | 無結果 | 顯示驗證失敗，但下方仍有 Demo 成功狀態 | 不適用 | FAIL | `unknown-images/08-corrupt-png.png` | 1.84 秒 |
| 不支援 TXT | 拒絕 | 無結果 | 無結果 | 顯示格式拒絕，但下方仍有 Demo 成功狀態 | 不適用 | FAIL | `unknown-images/09-unsupported-txt.png` | 1.53 秒 |

未知圖片沒有被宣稱為 AI、非 AI、真實、虛假或驗證成功。畫面使用的安全說法是：「因找不到相符的 AI Evidence Registry 紀錄，無法證明此檔案是原始版本或修改版本。」

## 手機 390 × 844 真人操作

| 步驟 | 操作 | 結果 | 狀態 | 截圖 | 問題 |
|---|---|---|---|---|---|
| M01 | 開啟首頁 | 圖片、標題與主要按鈕完整 | PASS | `mobile/01-home-390x844.png` | 無水平溢出 |
| M02 | 尋找驗證入口 | Header 沒有桌機版「驗證」連結；首頁「上傳圖片」可用 | PASS | `mobile/02-ready-select.png` | P2：手機Header無驗證捷徑 |
| M03 | 從首頁上傳圖片 | 驗證成功，但畫面仍停留首頁位置 | PASS | `mobile/03-verification-result.png` | P1：沒有自動帶到結果 |
| M04 | 手動找到結果並點遮罩 | 遮罩、4.8%與解釋完整 | PASS | `mobile/04-modification-mask.png` | 需要大量捲動 |
| M05 | 查看 Passport／Trust | Change Metrics與Trust完整 | PASS | `mobile/05-evidence-passport.png` | 長Hash／JSON閱讀較吃力 |
| M06 | 查看 History | 三版歷史可操作 | PASS | `mobile/06-version-history.png` | 每版卡片很高 |
| M07 | 點 Gemini | 真實回覆顯示 | PASS | `mobile/07-gemini-explanation.png` | 部分回覆為英文 |
| M08 | 開啟 Black Box | Development/Test標示清楚 | PASS | `mobile/08-blackbox-entry.png` | 無水平溢出 |
| M09 | 選擇 Evidence | 選單可操作 | PASS | `mobile/09-blackbox-selected.png` | 無 |
| M10 | 點完整測試 | 流程開始 | PASS | `mobile/10-blackbox-running.png` | 無 |
| M11 | 查看 Generation／Retention | PASS與數值可讀 | PASS | `mobile/11-blackbox-generation-retention.png` | 需捲動 |
| M12 | 查看 Retrieval／Hash | Hash結果可讀 | PASS | `mobile/12-blackbox-retrieval-hash.png` | 64字元Hash換行 |
| M13 | 查看最終 PASS | Continuity與邊界文字可見 | PASS | `mobile/13-blackbox-final-pass.png` | 全頁高度約2,823px |

手機頁面寬度 390px、文件寬度 390px，未發現水平溢出或主要按鈕被裁切。

## 錯誤證據

### ERROR_01 — 損壞 PNG 後保留 Demo 成功結果

- 發生步驟：任意圖片第 8 類。
- 使用者操作：選擇副檔名為 PNG、內容不是 PNG 的損壞檔。
- 畫面：顯示 `InvalidFileSignature`，但下方仍有「已驗證修改版本」與 ProofCart Demo 結果。
- 可重現：是，每次以新的公開頁面可重現。
- 重新整理：回到預設 Demo；沒有解決公開版本的錯誤狀態設計。
- 是否阻止後續：不阻止操作，但可能造成錯誤理解。
- 嚴重度：**P0**。
- 截圖：`errors/ERROR_01-corrupt-png-stale-demo-result.png`。

### ERROR_02 — 不支援 TXT 後保留 Demo 成功結果

- 發生步驟：任意圖片第 9 類。
- 使用者操作：透過檔案選擇器選擇 TXT。
- 畫面：顯示「只接受 PNG、JPEG 與 WebP 圖片」，但下方仍有「已驗證修改版本」。
- 可重現：是。
- 重新整理：回到預設 Demo。
- 是否阻止後續：不阻止操作，但可能造成錯誤理解。
- 嚴重度：**P0**，與 ERROR_01 同一根因。
- 截圖：`errors/ERROR_02-unsupported-file-stale-demo-result.png`。

### ERROR_03 — 手機 Header 沒有驗證導覽連結

- 發生步驟：手機 M02。
- 使用者操作：嘗試使用桌機相同的 Header「驗證」入口。
- 畫面：手機 Header 只顯示品牌與語言；仍可改用首頁「上傳圖片」。
- 可重現：是。
- 重新整理：不變。
- 是否阻止後續：否。
- 嚴重度：**P2**。
- 截圖：`errors/ERROR_03-mobile-verify-nav-hidden.png`。

## Bug 分類

### P0

1. 公開Production在損壞或不支援檔案錯誤後，仍顯示預設Demo的「已驗證修改版本」。核心引擎沒有把錯誤檔判成PASS，但一般使用者可能誤讀畫面。

### P1

1. 手機從首頁「上傳圖片」選檔並完成驗證後，畫面不會自動移到驗證結果；第一次使用者仍停留在Hero，可能以為沒有反應。

### P2

1. 手機Header隱藏「驗證／ProofCart／運作方式」導覽，只剩品牌與語言切換。
2. 手機頁面需要大量垂直捲動；版本卡片、Passport、Hash及Black Box結果分散在多個畫面。
3. Gemini中文介面回覆仍可能是英文，雖不影響證據狀態。

## 修改與部署界線

P0最小修正已在 Commit `764089dfcaf7a4f2bb853345b1326f3e73804638` 完成並Push；本機實際操作確認錯誤檔不再顯示任何Verified狀態。

但目前登入的Sites帳號無法存取既有公開Site專案，連線結果為 `Sites project not found`，所以本輪真人公開測試仍如實呈現舊Production問題。沒有建立第二個Site，也沒有宣稱已部署。

## VIDEO READY

**NO**

阻塞正式錄影的必要問題：公開Production尚未取得並部署P0修正。P1手機自動定位問題不阻止桌機影片，但必須由產品驗收決定是否另行修正。
