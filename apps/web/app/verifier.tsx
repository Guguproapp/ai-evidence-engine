"use client";
/* eslint-disable @next/next/no-img-element -- Direct asset bytes preserve embedded C2PA data; image optimization could transform them. */

import { ChangeEvent, useEffect, useMemo, useRef, useState } from "react";

type Verification = {
  verified: boolean;
  signature_status: string;
  revocation_status: string;
  confidence_level: string;
};

type Version = {
  version_id: string;
  parent_version_id: string | null;
  parent_event: string | null;
  event_id: string;
  event_hash: string;
  exact_hash: string;
  timestamp: string;
  provider: string;
  issuer: string;
  model: string;
  action_type: string;
  operator_type: string;
  image: string;
  mask: string | null;
  comparison: string | null;
  modification_scope: string | { changed_ratio?: number; bounding_box?: unknown };
  c2pa: {
    tool: string;
    embedded: boolean;
    manifest_count: number;
    active_manifest: string;
    validation_status: Array<{ code: string; explanation?: string }>;
    raw_report: string;
    development_signer: boolean;
  };
};

type Demo = {
  generated_at: string;
  product: string;
  passport_id: string;
  content_id: string;
  c2pa_tool: string;
  versions: Version[];
  registry_verification: Verification[];
  mask_method: string;
};

type UploadResult = {
  name: string;
  hash: string;
  result: "Authentic" | "Modified" | "Unknown" | "Invalid Signature";
  manifestCount: number;
  activeManifest: string | null;
  validation: Array<{ code?: string; explanation?: string }>;
  raw: unknown;
  matchedVersion?: Version;
};

type ExplanationResult = {
  request_id: string;
  verification_status: "Authentic" | "Modified" | "Unknown" | "Invalid Signature";
  explanation: string;
  model: string;
  provider: string;
  decision_source: string;
};

const ALLOWED_TYPES = new Set(["image/png", "image/jpeg", "image/webp"]);
const MAX_UPLOAD = 10 * 1024 * 1024;
const EXPLAINER_URL = "https://ai-evidence-explainer-856572888721.asia-east1.run.app/v1/explain";

function short(value: string, size = 10) {
  return value ? `${value.slice(0, size)}…${value.slice(-6)}` : "—";
}

function humanAction(value: string) {
  return ({
    digital_capture: "Original image captured",
    ai_background_and_badge_edit: "Background adjusted and AI badge added",
    ai_label_and_object_edit: "Product label area changed",
  } as Record<string, string>)[value] ?? value;
}

function verificationLabel(version: Version, verification: Verification) {
  if (!verification.verified || verification.signature_status !== "valid") return "Invalid Signature";
  if (!version.parent_version_id) return "Authentic";
  return "Modified";
}

function StatusPill({ value }: { value: string }) {
  const key = value.toLowerCase().replaceAll(" ", "-");
  return <span className={`status-pill ${key}`}>{value}</span>;
}

export function EvidenceVerifier() {
  const [demo, setDemo] = useState<Demo | null>(null);
  const [selected, setSelected] = useState(2);
  const [view, setView] = useState<"image" | "mask" | "comparison">("comparison");
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [upload, setUpload] = useState<UploadResult | null>(null);
  const [uploadError, setUploadError] = useState("");
  const [busy, setBusy] = useState(false);
  const [evidenceQuery, setEvidenceQuery] = useState("");
  const [queryMessage, setQueryMessage] = useState("");
  const [explanation, setExplanation] = useState<ExplanationResult | null>(null);
  const [explanationError, setExplanationError] = useState("");
  const [explanationBusy, setExplanationBusy] = useState(false);
  const resultRef = useRef<HTMLElement | null>(null);
  const verificationAttempts = useRef<number[]>([]);

  useEffect(() => {
    fetch("/demo/demo-case.json")
      .then((response) => response.json())
      .then(setDemo)
      .catch(() => setUploadError("Demo evidence could not be loaded."));
  }, []);

  const version = demo?.versions[selected] ?? null;
  const verification = demo?.registry_verification[selected] ?? null;
  const result = version && verification ? verificationLabel(version, verification) : "Unknown";
  const imageSource = useMemo(() => {
    if (!version) return "";
    if (view === "mask") return version.mask ?? version.image;
    if (view === "comparison") return version.comparison ?? version.image;
    return version.image;
  }, [version, view]);

  function clearExplanation() {
    setExplanation(null);
    setExplanationError("");
  }

  async function requestExplanation(
    status: ExplanationResult["verification_status"],
    facts: Record<string, string | number | boolean | null>,
  ) {
    clearExplanation();
    setExplanationBusy(true);
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 15_000);
    try {
      const response = await fetch(EXPLAINER_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status, facts }),
        signal: controller.signal,
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json() as ExplanationResult;
      if (payload.verification_status !== status || !payload.explanation) {
        throw new Error("Explanation response did not preserve the verified status.");
      }
      setExplanation(payload);
    } catch {
      setExplanationError("AI explanation is temporarily unavailable. The cryptographic verification result above is unchanged.");
    } finally {
      window.clearTimeout(timeout);
      setExplanationBusy(false);
    }
  }

  function explainVersion() {
    if (!version || !verification) return;
    const status = (upload?.result ?? result) as ExplanationResult["verification_status"];
    const changedRatio = typeof version.modification_scope === "object" ? version.modification_scope.changed_ratio ?? 0 : 0;
    void requestExplanation(status, {
      version_id: version.version_id,
      parent_version_id: version.parent_version_id,
      evidence_id: version.event_id,
      action: humanAction(version.action_type),
      changed_ratio: changedRatio,
      c2pa_manifest_count: version.c2pa.manifest_count,
      c2pa_status: version.c2pa.development_signer ? "valid development identity" : "valid",
      registry_status: verification.verified ? "matched" : "not verified",
      signature_status: verification.signature_status,
      signer: version.issuer,
    });
  }

  function explainUpload() {
    if (!upload) return;
    void requestExplanation(upload.result, {
      version_id: `uploaded-${upload.hash.slice(0, 16)}`,
      parent_version_id: null,
      evidence_id: null,
      action: upload.result === "Invalid Signature" ? "Uploaded bytes do not match the signed C2PA claim" : "No matching registry record found",
      changed_ratio: 0,
      c2pa_manifest_count: upload.manifestCount,
      c2pa_status: upload.validation.map((item) => item.code).filter(Boolean).join(", ") || "no validation record",
      registry_status: "not found",
      signature_status: upload.result === "Invalid Signature" ? "invalid" : "unknown",
      signer: null,
    });
  }

  function tryDemo() {
    setSelected(2);
    setView("comparison");
    setUpload(null);
    clearExplanation();
    setTimeout(() => resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 50);
  }

  async function handleFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;
    setUploadError("");
    setUpload(null);
    clearExplanation();
    const now = Date.now();
    verificationAttempts.current = verificationAttempts.current.filter((value) => now - value < 60_000);
    if (verificationAttempts.current.length >= 8) {
      setUploadError("Verification rate limit reached. Please wait one minute and try again.");
      return;
    }
    verificationAttempts.current.push(now);
    if (!ALLOWED_TYPES.has(file.type)) {
      setUploadError("Only PNG, JPEG, and WebP images are accepted.");
      return;
    }
    if (file.size > MAX_UPLOAD) {
      setUploadError("File is larger than the 10 MB safety limit.");
      return;
    }
    setBusy(true);
    try {
      const digest = await crypto.subtle.digest("SHA-256", await file.arrayBuffer());
      const hash = Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
      const matchedVersion = demo?.versions.find((item) => item.exact_hash === hash);
      if (matchedVersion && demo) setSelected(demo.versions.indexOf(matchedVersion));
      const { createC2pa } = await import("@contentauth/c2pa-web/inline");
      const sdk = await createC2pa();
      const reader = await sdk.reader.fromBlob(file.type, file);
      if (!reader) {
        sdk.dispose();
        setUpload({ name: file.name, hash, result: "Unknown", manifestCount: 0, activeManifest: null, validation: [], raw: null, matchedVersion });
        return;
      }
      const store = await reader.manifestStore();
      const raw = await reader.json();
      const record = store as unknown as { manifests?: Record<string, unknown>; active_manifest?: string; validation_status?: Array<{ code?: string; explanation?: string }> };
      const validation = record.validation_status ?? [];
      const invalid = validation.some((item) => item.code && !item.code.endsWith(".untrusted"));
      await reader.free();
      sdk.dispose();
      setUpload({
        name: file.name,
        hash,
        result: invalid ? "Invalid Signature" : matchedVersion?.parent_version_id ? "Modified" : "Authentic",
        manifestCount: Object.keys(record.manifests ?? {}).length,
        activeManifest: record.active_manifest ?? null,
        validation,
        raw,
        matchedVersion,
      });
    } catch (error) {
      setUploadError(error instanceof Error ? `Verification failed: ${error.message}` : "Verification failed.");
    } finally {
      setBusy(false);
    }
  }

  function lookupEvidence() {
    const query = evidenceQuery.trim().toLowerCase();
    if (!demo || !query) return;
    const found = demo.versions.find((item) => item.event_id.toLowerCase() === query || item.version_id.toLowerCase() === query) || (demo.passport_id.toLowerCase() === query ? demo.versions.at(-1) : undefined);
    if (!found) {
      setQueryMessage("No registry record found for that Evidence ID.");
      return;
    }
    setSelected(demo.versions.indexOf(found));
    clearExplanation();
    setQueryMessage(`Registry record found: ${found.version_id}`);
    setTimeout(() => resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 50);
  }

  return (
    <main>
      <header className="topbar">
        <a className="brand" href="#top" aria-label="AI Evidence Engine home">
          <span className="brand-mark">AE</span>
          <span><b>AI Evidence Engine</b><small>by gugupro</small></span>
        </a>
        <nav aria-label="Main navigation"><a href="#verify">Verify</a><a href="#proofcart">ProofCart demo</a><a href="#details">How it works</a></nav>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <span className="eyebrow">VERIFIABLE IMAGE HISTORY</span>
          <h1>See where an image came from.<br /><em>And exactly what changed.</em></h1>
          <p>Upload an image or try a signed product-photo demo. The verifier checks its content hash, C2PA manifest, signed evidence chain, and changed regions.</p>
          <div className="hero-actions">
            <button className="primary" onClick={tryDemo}>Try the 60-second demo <span>→</span></button>
            <label className="secondary upload-button">Upload an image<input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleFile} /></label>
          </div>
          <div className="trust-strip"><span>✓ Local verification</span><span>✓ Official C2PA SDK</span><span>✓ No image upload</span></div>
        </div>
        <div className="hero-proof">
          <div className="proof-card back-card"><span>ORIGINAL</span><img src="/demo/version-1.png" alt="Original ProofCart product" /></div>
          <div className="proof-card front-card"><span>VERIFIED EDIT</span><img src="/demo/version-3-comparison.png" alt="Detected changed region" /><div className="proof-stamp">✓ Evidence chain verified</div></div>
        </div>
      </section>

      <section className="verify-entry" id="verify">
        <div><span className="section-number">01</span><h2>Verify your evidence</h2><p>The file stays in your browser. We reject unsupported formats and files over 10 MB before processing.</p></div>
        <div className="entry-grid">
          <label className={`drop-zone ${busy ? "busy" : ""}`}>
            <span className="upload-icon">↑</span><b>{busy ? "Checking C2PA and signature…" : "Choose an image to verify"}</b><small>PNG, JPEG, or WebP · maximum 10 MB</small>
            <input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleFile} disabled={busy} />
          </label>
          <div className="evidence-lookup"><label htmlFor="evidence-id">Or enter an Evidence ID</label><div><input id="evidence-id" value={evidenceQuery} onChange={(event) => setEvidenceQuery(event.target.value)} placeholder="proofcart-v3" /><button onClick={lookupEvidence}>Verify</button></div>{queryMessage && <small>{queryMessage}</small>}</div>
        </div>
        {uploadError && <div className="alert error">{uploadError}</div>}
        {upload && <div className="upload-result"><StatusPill value={upload.result} /><div><b>{upload.name}</b><small>SHA-256 {short(upload.hash, 16)} · {upload.manifestCount} C2PA manifest(s)</small></div>{upload.matchedVersion && <span>Registry match: {upload.matchedVersion.version_id}</span>}</div>}
      </section>

      <section className="verification-section" ref={resultRef}>
        <div className="section-heading"><div><span className="section-number">02</span><h2>Verification result</h2></div>{(upload || (version && verification)) && <StatusPill value={upload?.result ?? result} />}</div>
        {upload && !upload.matchedVersion ? <div className="standalone-result">
          <div><span>Uploaded file</span><h3>{upload.name}</h3><p>{upload.result === "Invalid Signature" ? "C2PA evidence is present, but the asset bytes no longer match the signed claim." : "No matching AI Evidence Registry record was found for this file."}</p></div>
          <dl><div><dt>Result</dt><dd><StatusPill value={upload.result} /></dd></div><div><dt>Content hash</dt><dd><code>{upload.hash}</code></dd></div><div><dt>C2PA manifests</dt><dd>{upload.manifestCount}</dd></div><div><dt>Active manifest</dt><dd><code>{upload.activeManifest ?? "None"}</code></dd></div><div><dt>Validation</dt><dd>{upload.validation.map((item) => item.code).filter(Boolean).join(", ") || "No C2PA validation record"}</dd></div></dl>
          <details><summary>Developer JSON</summary><pre>{JSON.stringify(upload.raw, null, 2)}</pre></details>
          <div className="gemini-explainer">
            <span>AI EVIDENCE EXPLANATION</span>
            <h3>Explain the verified facts in plain language</h3>
            {explanation ? <><p>{explanation.explanation}</p><small>{explanation.model} on Vertex AI · Status remains {explanation.verification_status}</small></> : explanationError ? <p className="explanation-fallback">{explanationError}</p> : <p>Gemini explains the result; it does not decide whether the image is authentic or modified.</p>}
            <button className="secondary" onClick={explainUpload} disabled={explanationBusy}>{explanationBusy ? "Asking Gemini…" : explanation ? "Explain again" : "Explain with Gemini"}</button>
          </div>
          <button className="secondary" onClick={tryDemo}>Return to signed demo</button>
        </div> : !demo || !version || !verification ? <div className="loading">Loading signed evidence…</div> : <>
          <div className="verification-grid">
            <div className="image-panel">
              <div className="image-tabs">
                <button className={view === "image" ? "active" : ""} onClick={() => setView("image")}>Current image</button>
                <button className={view === "comparison" ? "active" : ""} onClick={() => setView("comparison")} disabled={!version.comparison}>Change overlay</button>
                <button className={view === "mask" ? "active" : ""} onClick={() => setView("mask")} disabled={!version.mask}>Mask</button>
              </div>
              <img className="main-image" src={imageSource} alt={`${version.version_id} ${view}`} />
              {typeof version.modification_scope === "object" && <div className="mask-summary"><b>{Math.round((version.modification_scope.changed_ratio ?? 0) * 1000) / 10}% changed</b><span>White/red areas are measured pixel changes, not copyright percentages.</span></div>}
            </div>
            <div className="facts-panel">
              <div className="plain-answer"><span>What happened?</span><h3>{version.parent_version_id ? "This image was modified." : "This is the recorded original."}</h3><p>{humanAction(version.action_type)}</p></div>
              <dl>
                <div><dt>Evidence signature</dt><dd className="good">✓ {verification.signature_status}</dd></div>
                <div><dt>C2PA manifest</dt><dd className="good">✓ Embedded · {version.c2pa.manifest_count} version(s)</dd></div>
                <div><dt>Signer</dt><dd>{version.issuer}</dd></div>
                <div><dt>Created</dt><dd>{new Date(version.timestamp).toLocaleString()}</dd></div>
                <div><dt>Content hash</dt><dd><code>{short(version.exact_hash, 18)}</code></dd></div>
                <div><dt>Registry</dt><dd className="good">✓ Signed record found</dd></div>
              </dl>
              <div className="trust-note"><b>Integrity verified; development identity</b><p>The C2PA bytes and evidence signature validate. The demo C2PA certificate is a development signer and is not on the official C2PA Trust List.</p></div>
              <div className="gemini-explainer">
                <span>AI EVIDENCE EXPLANATION</span>
                <h3>What this evidence means</h3>
                {explanation ? <><p>{explanation.explanation}</p><small>{explanation.model} on Vertex AI · Status remains {explanation.verification_status}</small></> : explanationError ? <p className="explanation-fallback">{explanationError}</p> : <p>Gemini can explain these verified facts in plain language. Hashes, signatures, C2PA, and the Registry remain the source of truth.</p>}
                <button className="secondary" onClick={explainVersion} disabled={explanationBusy}>{explanationBusy ? "Asking Gemini…" : explanation ? "Explain again" : "Explain with Gemini"}</button>
              </div>
            </div>
          </div>

          <div className="timeline-section">
            <div><span className="section-number">03</span><h2>Where this image came from</h2><p>Each edit creates a child version. Nothing silently overwrites the original.</p></div>
            <div className="timeline">
              {demo.versions.map((item, index) => <button key={item.version_id} className={selected === index ? "selected" : ""} onClick={() => { setSelected(index); setView(index === 0 ? "image" : "comparison"); clearExplanation(); }}>
                <span className="timeline-index">{index + 1}</span><img src={item.image} alt={item.version_id} /><span className="timeline-copy"><b>{index === 0 ? "Original" : `Edit ${index}`}</b><small>{humanAction(item.action_type)}</small><code>{short(item.event_id)}</code></span><span className="timeline-check">✓</span>
              </button>)}
            </div>
          </div>

          <section className="proofcart" id="proofcart">
            <div className="proofcart-image"><span className="product-badge">Evidence protected</span><img src="/demo/version-3.png" alt="ProofCart verified listing" /></div>
            <div className="proofcart-copy"><span className="eyebrow">PROOFCART · VERTICAL DEMO</span><h2>A buyer can verify the listing photo before trusting it.</h2><p>The seller&apos;s original, both edits, exact changed region, C2PA chain, and registry signature are attached to one product photo.</p><button className="primary" onClick={tryDemo}>Verify Evidence <span>→</span></button><div className="seller-proof"><span>Seller image</span><b>Signed by gugupro demo issuer</b><small>Evidence ID {short(version.event_id, 14)}</small></div></div>
          </section>

          <section className="developer-details" id="details">
            <button onClick={() => setDetailsOpen(!detailsOpen)} aria-expanded={detailsOpen}><span><b>Advanced / Developer details</b><small>Raw C2PA and registry evidence</small></span><span>{detailsOpen ? "−" : "+"}</span></button>
            {detailsOpen && <div className="details-body"><div><b>C2PA tool</b><code>{demo.c2pa_tool}</code></div><div><b>Active manifest</b><code>{version.c2pa.active_manifest}</code></div><div><b>Evidence event</b><code>{version.event_id}</code></div><div><b>Parent event</b><code>{version.parent_event ?? "None"}</code></div><div><b>Event hash</b><code>{version.event_hash}</code></div><a href={version.c2pa.raw_report} target="_blank" rel="noreferrer">Open preserved raw C2PA JSON →</a></div>}
          </section>
        </>}
      </section>

      <footer><div className="brand"><span className="brand-mark">AE</span><span><b>AI Evidence Engine</b><small>Evidence, not legal verdicts.</small></span></div><p>Records what happened. It does not decide copyright, infringement, or legality.</p></footer>
    </main>
  );
}
