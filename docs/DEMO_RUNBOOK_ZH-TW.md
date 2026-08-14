# AI Evidence Engine｜黑客松 Demo 操作與講稿

公開網址：https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site

目標時間：2 分 30 秒。最長不要超過 3 分鐘。

## Demo 前 3 分鐘檢查

1. 使用無痕視窗開啟公開網址，確認不需要登入。
2. 等待首頁的 Verification Result 顯示 `Modified`。
3. 確認畫面顯示 `4.8% changed`、`3 version(s)` 與 `✓ valid`。
4. 點一次 `Mask`，確認黑白修改區域正常顯示。
5. 回到頁首，準備正式展示。
6. 不要在現場宣稱開發簽章已加入官方 C2PA Trust List。
7. 確認三張商品圖都顯示 `GUGUPRO`，不得使用舊的 `GUGUPROO`／`GUGU PROOF` 影片素材。

## 2～3 分鐘正式講稿

### 0:00–0:20｜問題

操作：停在首頁。

講稿：

> 現在我們看到一張網路商品照片，通常只能看到最後結果，卻不知道它從哪裡來、誰修改過、改了哪裡。AI Evidence Engine 不是 AI Detector；它保存的是可以驗證的來源與修改證據。

### 0:20–0:40｜一鍵開始

操作：點 `Try the 60-second demo`。

講稿：

> 評審不需要安裝程式，也不需要先準備圖片。按一次 Try Demo，就能看到一組真實簽章的商品照片證據。

### 0:40–1:05｜先回答最重要的問題

操作：指向 `Modified`、`Evidence signature ✓ valid`、`C2PA manifest` 與 `Registry`。

講稿：

> 系統先給人看得懂的結果：這張圖片修改過。Evidence 簽章有效，圖片內嵌三個 C2PA 版本，Registry 也找到對應的簽章紀錄。技術 JSON 被放在進階區，不會逼評審先讀 JSON。

### 1:05–1:25｜改了哪裡

操作：依序點 `Change overlay`、`Mask`。

講稿：

> 這不是固定畫上去的假框。系統逐像素比較前後版本，再產生 Modification Mask。這一版實際變更約 4.8%，集中在商品標籤區。這個比例只代表變更範圍，不是著作權比例。

### 1:25–1:50｜從哪裡演變而來

操作：依序點 Version 1、Version 2、Version 3。

講稿：

> 每次實質修改都建立 Child Version，不會覆蓋上一版。Version 1 是原始圖；Version 2 調整背景並加入標記；Version 3 修改商品標籤。每一版都有自己的內容雜湊、Event ID、Parent 關係與 C2PA Manifest。

### 1:50–2:10｜證據有沒有被竄改

操作：展開 `Advanced / Developer details`。

講稿：

> C2PA Event ID 與 AI Evidence Engine Registry 使用同一個事件識別碼。圖片位元、C2PA Claim 或 Event Chain 被修改時，驗證就會失敗。我們也保留原始 C2PA JSON，沒有只轉成自己的格式。

### 2:10–2:30｜ProofCart 商業情境

操作：捲到 ProofCart，點 `Verify Evidence`。

講稿：

> ProofCart 是第一個垂直應用。買家在商品頁點 Verify Evidence，就能知道賣家照片的原始來源、修改歷史、修改區域與簽章狀態。AI Evidence Engine 是核心平台，ProofCart 證明它能落地到真實交易場景。

### 2:30–2:40｜收尾

講稿：

> 我們不替法院判斷著作權，也不猜一個 AI 百分比。我們提供的是：發生過什麼、誰簽了、內容是否一致，以及證據有沒有被竄改。

## 評審追問時的實測項目

### Evidence ID

- Version 1：`0195e702-a549-455b-af94-f187ec416b50`（原始版本）。
- Version 2：`ae10e9fb-ad94-403b-a150-c3883aa32ef6`（第一次修改）。
- Version 3：`b56445dd-1530-4c69-93d1-6977120a9f40`（第二次修改）。
- 輸入不存在的 ID：顯示 `No registry record found for that Evidence ID.`。

### 上傳圖片

- 已簽章的 `version-3.png`：顯示 `Modified`、3 個 Manifest、Registry Match。
- 內容遭竄改但保留 C2PA 的圖片：顯示 `Invalid Signature` 與 `assertion.dataHash.mismatch`。
- 沒有 C2PA 的原始圖片：顯示 `Unknown` 與 0 個 Manifest。

## Production Version 3 固定資料

- Version 1 SHA-256：`b49c057203117efc75bde6c8c110641efffc31b415824fd2c39354bdc6fbb952`
- Version 2 SHA-256：`ab2993c35ddbbcd1aec128b4ee7ff1416ba8c137471275dfc10057f7d030f374`
- Version 3 SHA-256：`3b00f3ac87e58c5bf5ddb5e2dd021a0236bc3e3c5a02c082c1735867ea81bba9`
- Version 3 C2PA Active Manifest：`urn:c2pa:da19b9d8-4115-4708-95d1-de5763364a6d`
- Version 3 Event Hash：`e545c90fcd342fb753e3301509cdc5e048e5645d58e302144a99516b19bdee0d`

## 必須誠實說明的邊界

- C2PA Manifest 與內容完整性是真的，不是自製相似格式。
- Demo 目前使用開發簽章憑證，因此介面顯示 `Integrity verified; development identity`。
- 正式商業上線前仍要取得受信任的 C2PA 憑證，並用 KMS／HSM 保護私鑰。
- 網頁目前在瀏覽器本地驗證圖片，沒有伺服器上傳端點。
- Modification Mask 是像素變化證據，不等於修改意圖、侵權或法律結論。

## 現場備援

1. 若 C2PA WASM 第一次載入較慢，等待 3～5 秒，不要連續重按。
2. 若畫面停在 Loading，重新整理一次後點 Try Demo。
3. 若上傳自己的圖片顯示 Unknown，這是正確結果，代表沒有找到可驗證來源，不代表圖片一定是假。
4. 若網路不穩，先用首頁已內建的 Try Demo，不要依賴現場上傳。
5. 不要把 `signingCredential.untrusted` 說成簽章失敗；它代表 Demo 憑證身分尚未進入官方信任名單。
