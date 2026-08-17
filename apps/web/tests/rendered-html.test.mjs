import assert from "node:assert/strict";
import { access, readFile, stat } from "node:fs/promises";
import test from "node:test";

async function render(path = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request(`http://localhost${path}`, { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the Traditional Chinese default verifier", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);
  const html = await response.text();
  assert.match(html, /<title>AI Evidence Engine/);
  assert.match(html, /<html lang="zh-Hant-TW"/);
  assert.match(html, /驗證內容的來源履歷/);
  assert.match(html, /有紀錄的版本改了什麼/);
  assert.match(html, /沒有可信履歷時，系統會明確標示無法確認/);
  assert.match(html, /通用證據護照/);
  assert.match(html, /試用 60 秒示範/);
  assert.match(html, /上傳圖片/);
  assert.match(html, /官方 C2PA SDK/);
  assert.match(html, /ProofCart 示範/);
  assert.match(html, /記錄證據，不代替法律判決/);
  assert.match(html, />繁中</);
  assert.match(html, />EN</);
  assert.doesNotMatch(html, />Authentic</);
  assert.doesNotMatch(html, /可以辨識任何修過的圖片|可以掃陌生圖片判斷是否修圖|AI fake detector|Detects any edited image|Detects fake images|Finds modifications in any image/i);
  assert.doesNotMatch(html, /codex-preview|react-loading-skeleton|Your site is taking shape/i);
});

test("ships a bilingual privacy policy", async () => {
  const response = await render("/privacy");
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /隱私權政策/);
  assert.match(html, /只有你明確點選/);
  assert.match(html, /First-Seen/);
  assert.match(html, /Vertex AI Gemini/);
  assert.match(html, /OWNER INPUT REQUIRED/);
});

test("ships signed demo evidence and preserved C2PA reports", async () => {
  const publicRoot = new URL("../public/demo/", import.meta.url);
  const demo = JSON.parse(await readFile(new URL("demo-case.json", publicRoot), "utf8"));
  assert.equal(demo.versions.length, 3);
  assert.equal(demo.c2pa_tool, "c2patool 0.27.12");
  assert.ok(demo.registry_verification.every((item) => item.verified));
  assert.equal(demo.versions[2].c2pa.manifest_count, 3);
  assert.ok(demo.versions[2].modification_scope.changed_ratio > 0);
  for (let index = 1; index <= 3; index += 1) {
    const image = new URL(`version-${index}.png`, publicRoot);
    const report = new URL(`version-${index}-c2pa.json`, publicRoot);
    assert.ok((await stat(image)).size > 10_000);
    const c2pa = JSON.parse(await readFile(report, "utf8"));
    assert.equal(Object.keys(c2pa.manifests).length, index);
  }
  await assert.rejects(access(new URL("../app/_sites-preview", import.meta.url)));
});

test("declares upload limits and client-side validation", async () => {
  const verifier = await readFile(new URL("../app/verifier.tsx", import.meta.url), "utf8");
  const dictionary = await readFile(new URL("../app/i18n.ts", import.meta.url), "utf8");
  assert.match(verifier, /MAX_UPLOAD = 10 \* 1024 \* 1024/);
  assert.match(verifier, /image\/png/);
  assert.match(verifier, /image\/jpeg/);
  assert.match(verifier, /image\/webp/);
  assert.match(verifier, /crypto\.subtle\.digest\("SHA-256"/);
  assert.match(verifier, /@contentauth\/c2pa-web\/inline/);
  assert.match(verifier, /verificationAttempts\.current\.length >= 8/);
  assert.match(verifier, /!uploadError && \(upload \|\| \(version && verification\)\)/);
  assert.match(verifier, /uploadError \? <div className="loading">/);
  assert.match(verifier, /setUploadError\(""\)/);
  assert.match(dictionary, /所選檔案無法處理，因此不顯示任何驗證結果。/);
  assert.match(dictionary, /檔案太大，請選擇 10 MB 以下的圖片。/);
  assert.match(verifier, /new FormData\(\)/);
  assert.match(verifier, /Start a verified history from now/);
  assert.doesNotMatch(verifier, /innerHTML|eval\(/);
});

test("uses a static bilingual dictionary and persistent locale without changing canonical enums", async () => {
  const verifier = await readFile(new URL("../app/verifier.tsx", import.meta.url), "utf8");
  const dictionary = await readFile(new URL("../app/i18n.ts", import.meta.url), "utf8");
  const decision = await readFile(new URL("../app/evidence-classification.mjs", import.meta.url), "utf8");
  assert.match(dictionary, /DEFAULT_LOCALE: Locale = "zh-TW"/);
  assert.match(dictionary, /LOCALE_STORAGE_KEY = "aee_locale"/);
  assert.match(dictionary, /"Verified Original": "已驗證原始版本"/);
  assert.match(dictionary, /"Invalid Evidence": "證據無效"/);
  assert.match(verifier, /localStorage\.getItem\(LOCALE_STORAGE_KEY\)/);
  assert.match(verifier, /localStorage\.setItem\(LOCALE_STORAGE_KEY, locale\)/);
  assert.match(verifier, /changeLocale\("en"\)/);
  assert.match(verifier, /changeLocale\("zh-TW"\)/);
  assert.match(verifier, /localStorage\.setItem\(LOCALE_STORAGE_KEY, nextLocale\)/);
  assert.match(decision, /VERIFIED_ORIGINAL: "VERIFIED_ORIGINAL"/);
  assert.match(decision, /VERIFIED_MODIFIED: "VERIFIED_MODIFIED"/);
  assert.match(decision, /INVALID_EVIDENCE: "INVALID_EVIDENCE"/);
  assert.doesNotMatch(decision, /已驗證原始版本|已驗證修改版本|證據無效/);
});

test("exposes the bounded Gemini evidence explainer", async () => {
  const verifier = await readFile(new URL("../app/verifier.tsx", import.meta.url), "utf8");
  assert.match(verifier, /EVIDENCE PASSPORT/);
  assert.match(verifier, /CHANGE METRICS/);
  assert.match(verifier, /PRIVATE EVIDENCE/);
  assert.match(verifier, /NEXT — NOT YET IMPLEMENTED/);
  assert.match(verifier, /One evidence foundation\. Many creation formats\./);
  assert.match(verifier, /Explain with Gemini/);
  assert.match(verifier, /AI only helps interpret the result\. It does not participate in verification decisions\./);
  assert.match(verifier, /ai-evidence-explainer-856572888721\.asia-east1\.run\.app/);
  assert.match(verifier, /payload\.verification_status !== status/);
  assert.match(verifier, /cryptographic verification result above is unchanged/);
  assert.match(verifier, /measured pixel change/);
  assert.match(verifier, /Private disclosure architecture — not yet implemented/);
  assert.match(verifier, /AI involvement/);
});

test("separates plain-language verification results from developer evidence", async () => {
  const verifier = await readFile(new URL("../app/verifier.tsx", import.meta.url), "utf8");
  const dictionary = await readFile(new URL("../app/i18n.ts", import.meta.url), "utf8");
  assert.match(verifier, /className="plain-result-facts"/);
  assert.match(verifier, /className="technical-details"/);
  assert.match(verifier, /View technical details/);
  assert.match(verifier, /Full SHA-256/);
  assert.match(verifier, /Copy hash/);
  assert.match(verifier, /Reason codes/);
  assert.match(verifier, /Canonical JSON/);
  assert.match(dictionary, /無法確認來源/);
  assert.match(dictionary, /這不代表圖片是假的，也不代表圖片由 AI 生成/);
  assert.match(dictionary, /AEE 來源履歷/);
  assert.match(dictionary, /C2PA 來源憑證/);
  assert.match(dictionary, /簽署者身分/);
  assert.match(dictionary, /AI 參與/);
  assert.match(dictionary, /AI 僅協助解讀，不參與驗證判定/);
  assert.doesNotMatch(verifier, /<h3>\{upload\.name\}<\/h3>/);
});

test("offers an opt-in First-Seen bridge without changing canonical provenance states", async () => {
  const verifier = await readFile(new URL("../app/verifier.tsx", import.meta.url), "utf8");
  const dictionary = await readFile(new URL("../app/i18n.ts", import.meta.url), "utf8");
  const decision = await readFile(new URL("../app/evidence-classification.mjs", import.meta.url), "utf8");
  assert.match(verifier, /upload\.result === "Unverified"/);
  assert.match(verifier, /LEGACY CONTENT BRIDGE · DEVELOPMENT \/ TEST/);
  assert.match(verifier, /registration_status: "FIRST_SEEN_SEALED"/);
  assert.match(verifier, /Provenance before this AEE record is unknown/);
  assert.match(verifier, /This is not proof of originality, authorship, copyright, or earlier history/);
  assert.match(verifier, /\/v1\/demo\/first-seen/);
  assert.match(dictionary, /從現在開始建立證據履歷/);
  assert.match(dictionary, /不是原創、作者、著作權或先前歷史的證明/);
  assert.doesNotMatch(decision, /FIRST_SEEN_SEALED/);
});
