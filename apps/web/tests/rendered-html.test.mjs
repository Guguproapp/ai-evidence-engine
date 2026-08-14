import assert from "node:assert/strict";
import { access, readFile, stat } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the judge-facing verifier", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);
  const html = await response.text();
  assert.match(html, /<title>AI Evidence Engine/);
  assert.match(html, /Prove where a creation came from/);
  assert.match(html, /UNIVERSAL EVIDENCE PASSPORT/);
  assert.match(html, /Try the 60-second demo/);
  assert.match(html, /Upload an image/);
  assert.match(html, /Official C2PA SDK/);
  assert.match(html, /ProofCart demo/);
  assert.match(html, /Evidence, not legal verdicts/);
  assert.doesNotMatch(html, />Authentic</);
  assert.doesNotMatch(html, /codex-preview|react-loading-skeleton|Your site is taking shape/i);
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
});
