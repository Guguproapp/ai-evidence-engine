# AI Evidence Engine｜最終操作影片 Runbook

公開網址：https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site

正式影片：https://youtu.be/HDG1qYo5hUg

狀態：`PASS`。1920×1080、2:43、英文字幕直接燒入、公開 Production 真實操作。舊版 `Fwu7yGUTVwo` 已被否決，不得提交。

目標：1920×1080、完整瀏覽器 Viewport、滑鼠可見、2 分 20 秒至 2 分 45 秒，硬限制低於 3 分鐘。必須真實操作 Production，不可用靜態截圖輪播。

## 錄影前檢查

1. 用公開網址開啟 Production，不使用 localhost。
2. 瀏覽器完整顯示在 1920×1080 畫布內，四邊不得裁切或留下巨大黑邊。
3. 準備新版 `version-3.png` 與實際遭竄改、會產生 `assertion.dataHash.mismatch` 的檔案。
4. 首頁與三個版本圖片都必須顯示 `GUGUPRO`。
5. 確認 `Explain with Gemini` 可呼叫 Production Cloud Run；Gemini 故障時仍保留密碼學結果。
6. 不宣稱開發簽章已進入正式 C2PA Trust List。
7. 不宣稱 Private Black Box 或 Mobile Authorization 已完成；畫面必須標示 `NEXT — NOT YET IMPLEMENTED`。

## 低於 3 分鐘正式流程

### 00:00–00:15｜問題與定位

畫面：AI Evidence Engine 首頁與 `UNIVERSAL EVIDENCE PASSPORT`。

旁白：

> How can we prove where digital content came from — without guessing whether AI made it? AI Evidence Engine is a Universal Evidence Passport for digital and physical creation.

### 00:15–00:45｜真正上傳並驗證

操作：點 `Upload an image`，在檔案選擇器選擇新版 `version-3.png`，等待結果。

必須看到：`Verified Modified`、Registry `Matched`、C2PA integrity `Valid`，不得只按 Try Demo 或捲動預設資料。

### 00:45–01:10｜圖片與 4.8% 修改範圍

操作：依序點 `Current image`、`Change overlay`、`Mask`，讓圖片主體清楚放大。

旁白重點：4.8% 是逐像素計算的 Spatial Change，不是 AI probability、copyright percentage 或 truth score。

### 01:10–01:35｜完整履歷

操作：依序點 Version 1、Version 2、Version 3，指向 Evidence Passport、History、Change Metrics 與 Trust。

必須展示：Parent、Timestamp、Tool / Model、Event ID、Hash、Signature、C2PA Manifest、每版修改範圍。

### 01:35–01:55｜真實竄改測試

操作：再次點上傳，選擇實際遭竄改的 Version 3。

必須看到：`Invalid Evidence` 與 `assertion.dataHash.mismatch`。不得展示預先寫死文字代替操作。

### 01:55–02:10｜Gemini Evidence Explanation

操作：點 `Explain with Gemini`，等待 Production 回應。

旁白重點：Gemini 只解釋 allowlist 後的驗證事實；`Verified Original`、`Verified Modified`、`Unverified`、`Invalid Evidence` 都由 Hash、Signature、C2PA、Registry 與 Event Chain 決定。

### 02:10–02:30｜Universal Evidence Passport

操作：捲到 `One evidence foundation. Many creation formats.`。

展示：Text、Image、Video、Audio、Documents、2D Design、3D Models、Manufacturing adapters，共用 Passport、Event Chain、Hash、Signature、Registry、Private Wallet。

### 02:30–02:45｜下一階段，不冒充完成

操作：顯示 `NEXT — NOT YET IMPLEMENTED` 區塊。

流程：Verifier requests evidence → phone shows requester/scope/purpose/expiry → owner approves or denies → phone signs single-use authorization → Black Box releases only authorized fields。

## 新版 Production Evidence 固定資料

- Version 1 Event ID：`7fcbfc61-fcdd-482e-98a8-047769747f32`
- Version 2 Event ID：`51b90c7b-8bcb-4df9-8e76-8f25f5c6539c`
- Version 3 Event ID：`1c3d4a0f-9e2a-4a18-a83f-0c982db4ef33`
- Version 1 SHA-256：`082cc812bb1720f7335e41da823706dc022aae1ded0daa1dfbc20b93717e0fee`
- Version 2 SHA-256：`02cb6fa502538e12a6f7dec66db75638d32efefe5a60ac2ed5848abc56783954`
- Version 3 SHA-256：`7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`
- Version 3 C2PA Active Manifest：`urn:c2pa:cd1f092b-94fe-4623-9e51-a8eacd50a762`
- Version 3 Event Hash：`262c794b7fa3077a52c0166617e6f2cbfedf47e335102fa02fdf8c39a8333ce6`
- Version 3 Spatial Change：`4.7743%`，介面顯示 `4.8% changed`

## 驗證狀態說法

- `Verified Original`：有效 C2PA、有效且匹配的 Registry、有效簽章／鏈，且無 Parent。
- `Verified Modified`：上述條件成立，且有 Parent。
- `Unverified`：證據不足，例如 valid C2PA 但 Registry No Match，或兩者皆無。
- `Invalid Evidence`：C2PA、Registry、簽章或鏈存在衝突／無效。
- `Trusted / Development / Unknown` 是身分信任狀態，與 Provenance State 分開。

## 誠實邊界

- C2PA Manifest 與內容完整性是真實官方工具結果，不是自製相似格式。
- Demo 使用 Development signer，並未宣稱正式 Trust List 身分。
- Modification Mask 是可解釋像素差異，不代表意圖、著作權比例、侵權或世界真相。
- Public Verifier 只有最低必要 Public Passport；完整 Prompt、原始私人素材與敏感輸入不公開。
- Private Black Box 與 Mobile Authorization 本輪只有規格與 Next Stage 畫面，尚未正式實作。
