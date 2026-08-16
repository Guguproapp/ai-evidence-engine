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
  assert.match(html, /看見內容從哪裡來/);
  assert.match(html, /通用證據護照/);
  assert.match(html, /試用 60 秒示範/);
  assert.match(html, /上傳圖片/);
  assert.match(html, /官方 C2PA SDK/);
  assert.match(html, /ProofCart 示範/);
  assert.match(html, /記錄證據，不代替法律判決/);
  assert.match(html, />繁中</);
  assert.match(html, />EN</);
  assert.doesNotMatch(html, />Authentic</);
  assert.doesNotMatch(html, /codex-preview|react-loading-skeleton|Your site is taking shape/i);
});

test("ships a bilingual privacy policy", async () => {
  const response = await render("/privacy");
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /隱私權政策/);
  assert.match(html, /不會把原始圖片傳送/);
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
  assert.match(verifier, /MAX_UPLOAD = 10 \* 1024 \* 1024/);
  assert.match(verifier, /image\/png/);
  assert.match(verifier, /image\/jpeg/);
  assert.match(verifier, /image\/webp/);
  assert.match(verifier, /crypto\.subtle\.digest\("SHA-256"/);
  assert.match(verifier, /@contentauth\/c2pa-web\/inline/);
  assert.match(verifier, /verificationAttempts\.current\.length >= 8/);
  assert.doesNotMatch(verifier, /fetch\([^)]*file|FormData|innerHTML|eval\(/);
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
  assert.match(verifier, /Hashes, signatures, C2PA, and the Registry remain the source of truth/);
  assert.match(verifier, /ai-evidence-explainer-856572888721\.asia-east1\.run\.app/);
  assert.match(verifier, /payload\.verification_status !== status/);
  assert.match(verifier, /cryptographic verification result above is unchanged/);
  assert.match(verifier, /measured pixel change/);
  assert.match(verifier, /Private disclosure architecture — not yet implemented/);
  assert.match(verifier, /AI involvement/);
});
