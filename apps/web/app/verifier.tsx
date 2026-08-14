"use client";
/* eslint-disable @next/next/no-img-element -- Direct asset bytes preserve embedded C2PA data; image optimization could transform them. */

import { ChangeEvent, useEffect, useMemo, useRef, useState } from "react";
import { classifyEvidence } from "./evidence-classification.mjs";

type Verification = {
  verified: boolean;
  signature_status: string;
  revocation_status: string;
  confidence_level: string;
  integrity_state?: "VALID" | "INVALID" | "UNVERIFIED";
  provenance_state?: "VERIFIED_ORIGINAL" | "VERIFIED_MODIFIED" | "UNVERIFIED" | "INVALID_EVIDENCE";
  identity_trust?: "TRUSTED" | "DEVELOPMENT" | "UNKNOWN" | "REVOKED";
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
  involvement_level: string;
  operator_type: string;
  human_approval: boolean;
  blackbox_available: boolean;
  asset_type?: string;
  media_type?: string;
  device_id?: string | null;
  software?: string | null;
  software_version?: string | null;
  trust_status?: string;
  public_disclosure_level?: string;
  schema_version?: string;
  evidence_profile?: string;
  identity_trust?: string;
  integrity_state?: string;
  provenance_state?: string;
  change_metrics?: { spatial_change_ratio?: number; changed_region?: unknown; bounding_box?: unknown };
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
  result: "Verified Original" | "Verified Modified" | "Unverified" | "Invalid Evidence";
  c2paIntegrity: "Valid" | "Invalid" | "Not Present";
  registryStatus: "Matched" | "Invalid" | "No Match";
  identityTrust: "Trusted" | "Development" | "Unknown" | "Revoked";
  integrityState: "VALID" | "INVALID" | "UNVERIFIED";
  aiInvolvement: string;
  reasons: string[];
  manifestCount: number;
  activeManifest: string | null;
  validation: Array<{ code?: string; explanation?: string }>;
  raw: unknown;
  matchedVersion?: Version;
};

type ExplanationResult = {
  request_id: string;
  verification_status: "Verified Original" | "Verified Modified" | "Unverified" | "Invalid Evidence";
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

function verificationDecision(version: Version, verification: Verification) {
  const validation = version.c2pa.validation_status ?? [];
  const c2paValid = !validation.some((item) => item.code && !item.code.endsWith(".untrusted"));
  return classifyEvidence({
    hasC2pa: version.c2pa.embedded && version.c2pa.manifest_count > 0,
    c2paValid,
    registryMatched: true,
    registryValid: verification.verified && verification.signature_status === "valid",
    hasParent: Boolean(version.parent_version_id),
    identityTrust: version.c2pa.development_signer ? "DEVELOPMENT" : "UNKNOWN",
  });
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
  const decision = version && verification ? verificationDecision(version, verification) : null;
  const result = decision?.provenanceState ?? "Unverified";
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
      action: upload.result === "Invalid Evidence" ? "Uploaded bytes or evidence do not validate" : "No matching registry record found",
      changed_ratio: 0,
      c2pa_manifest_count: upload.manifestCount,
      c2pa_status: upload.validation.map((item) => item.code).filter(Boolean).join(", ") || "no validation record",
      registry_status: "not found",
      signature_status: upload.result === "Invalid Evidence" ? "invalid" : "unknown",
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
      const matchedIndex = matchedVersion && demo ? demo.versions.indexOf(matchedVersion) : -1;
      const registryVerification = matchedIndex >= 0 ? demo?.registry_verification[matchedIndex] : undefined;
      if (matchedIndex >= 0) setSelected(matchedIndex);
      const { createC2pa } = await import("@contentauth/c2pa-web/inline");
      const sdk = await createC2pa();
      const reader = await sdk.reader.fromBlob(file.type, file);
      if (!reader) {
        sdk.dispose();
        const classification = classifyEvidence({
          hasC2pa: false,
          c2paValid: false,
          registryMatched: Boolean(matchedVersion),
          registryValid: Boolean(registryVerification?.verified),
          requiredProfileEvidenceValid: false,
          hasParent: Boolean(matchedVersion?.parent_version_id),
        });
        setUpload({
          name: file.name,
          hash,
          result: classification.provenanceState,
          c2paIntegrity: classification.c2paIntegrity,
          registryStatus: classification.registryStatus,
          identityTrust: "Unknown",
          integrityState: classification.integrityState,
          aiInvolvement: matchedVersion?.involvement_level ?? "UNKNOWN",
          reasons: classification.reasons,
          manifestCount: 0,
          activeManifest: null,
          validation: [],
          raw: null,
          matchedVersion,
        });
        return;
      }
      const store = await reader.manifestStore();
      const raw = await reader.json();
      const record = store as unknown as { manifests?: Record<string, unknown>; active_manifest?: string; validation_status?: Array<{ code?: string; explanation?: string }> };
      const validation = record.validation_status ?? [];
      const invalid = validation.some((item) => item.code && !item.code.endsWith(".untrusted"));
      const manifestCount = Object.keys(record.manifests ?? {}).length;
      const identityTrust = matchedVersion?.c2pa.development_signer ? "Development" : "Unknown";
      const classification = classifyEvidence({
        hasC2pa: manifestCount > 0,
        c2paValid: !invalid,
        registryMatched: Boolean(matchedVersion),
        registryValid: Boolean(registryVerification?.verified),
        hasParent: Boolean(matchedVersion?.parent_version_id),
        identityTrust,
        requiredProfileEvidenceValid: Boolean(matchedVersion && registryVerification?.verified && manifestCount > 0 && !invalid),
      });
      await reader.free();
      sdk.dispose();
      setUpload({
        name: file.name,
        hash,
        result: classification.provenanceState,
        c2paIntegrity: classification.c2paIntegrity,
        registryStatus: classification.registryStatus,
        identityTrust,
        integrityState: classification.integrityState,
        aiInvolvement: matchedVersion?.involvement_level ?? "UNKNOWN",
        reasons: classification.reasons,
        manifestCount,
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
          <span className="eyebrow">UNIVERSAL EVIDENCE PASSPORT</span>
          <h1>Prove where a creation came from.<br /><em>Without guessing.</em></h1>
          <p>AI Evidence Engine records verifiable origin, tools, changes, and history across digital and physical creation. Image provenance is the first working modality.</p>
          <div className="hero-actions">
            <button className="primary" onClick={tryDemo}>Try the 60-second demo <span>→</span></button>
            <label className="secondary upload-button">Upload an image<input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleFile} /></label>
          </div>
          <div className="trust-strip"><span>✓ Local verification</span><span>✓ Official C2PA SDK</span><span>✓ No image upload</span></div>
        </div>
        <div className="hero-proof">
          <div className="proof-card back-card"><span>ORIGINAL</span><img src="/demo/version-1.png" alt="Original ProofCart product" /></div>
          <div className="proof-card front-card"><span>VERIFIED MODIFIED</span><img src="/demo/version-3-comparison.png" alt="Detected changed region" /><div className="proof-stamp">✓ Evidence chain verified</div></div>
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
          <div><span>Uploaded file</span><h3>{upload.name}</h3><p>{upload.result === "Invalid Evidence" ? "Evidence is present, but the asset bytes, C2PA claim, signature, or chain do not validate." : "This file is not proven original or modified because no matching AI Evidence Registry record was found."}</p></div>
          <dl>
            <div><dt>Provenance</dt><dd><StatusPill value={upload.result} /></dd></div>
            <div><dt>Integrity</dt><dd>{upload.integrityState}</dd></div>
            <div><dt>C2PA integrity</dt><dd>{upload.c2paIntegrity}</dd></div>
            <div><dt>Registry</dt><dd>{upload.registryStatus}</dd></div>
            <div><dt>Identity trust</dt><dd>{upload.identityTrust}</dd></div>
            <div><dt>AI involvement</dt><dd>{upload.aiInvolvement === "UNKNOWN" ? "Unknown — no signed Event level" : upload.aiInvolvement}</dd></div>
            <div><dt>Content hash</dt><dd><code>{upload.hash}</code></dd></div>
            <div><dt>C2PA manifests</dt><dd>{upload.manifestCount}</dd></div>
            <div><dt>Active manifest</dt><dd><code>{upload.activeManifest ?? "None"}</code></dd></div>
            <div><dt>Validation</dt><dd>{upload.validation.map((item) => item.code).filter(Boolean).join(", ") || "No C2PA validation record"}</dd></div>
            <div><dt>Decision reasons</dt><dd>{upload.reasons.join(", ")}</dd></div>
          </dl>
          <details><summary>Developer JSON</summary><pre>{JSON.stringify(upload.raw, null, 2)}</pre></details>
          <div className="gemini-explainer">
            <span>AI EVIDENCE EXPLANATION</span>
            <h3>Explain the verified facts in plain language</h3>
            {explanation ? <><p>{explanation.explanation}</p><small>{explanation.model} on Vertex AI · Status remains {explanation.verification_status}</small></> : explanationError ? <p className="explanation-fallback">{explanationError}</p> : <p>Gemini explains verified facts; it cannot assign or change the provenance state.</p>}
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
              {typeof version.modification_scope === "object" && <div className="mask-summary"><b>{Math.round((version.modification_scope.changed_ratio ?? 0) * 1000) / 10}% measured pixel change</b><span>White/red areas are measured pixel changes, not AI probability, copyright percentage, or truth score.</span></div>}
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

          <section className="passport-sections" aria-label="Evidence Passport details">
            <article>
              <span>EVIDENCE PASSPORT</span><h3>What this asset is and where it came from</h3>
              <dl>
                <div><dt>Passport ID</dt><dd><code>{demo.passport_id}</code></dd></div>
                <div><dt>Asset / media</dt><dd>{version.asset_type ?? "digital-content"} · {version.media_type ?? "image/png"}</dd></div>
                <div><dt>Evidence profile</dt><dd>{version.evidence_profile ?? "aee.image.c2pa.v1 (legacy event view)"}</dd></div>
                <div><dt>Version ID</dt><dd>{version.version_id}</dd></div>
                <div><dt>Created</dt><dd>{new Date(version.timestamp).toLocaleString()}</dd></div>
                <div><dt>Issuer</dt><dd>{version.issuer}</dd></div>
                <div><dt>Creator / agent</dt><dd>{version.operator_type} · {version.provider}</dd></div>
                <div><dt>Tool / model</dt><dd>{version.software ?? version.model}{version.software_version ? ` ${version.software_version}` : ""}</dd></div>
                <div><dt>AI involvement</dt><dd>{version.involvement_level}</dd></div>
                <div><dt>Evidence Event</dt><dd><code>{version.event_id}</code></dd></div>
                <div><dt>Parent Event</dt><dd><code>{version.parent_event ?? "Recorded original — no parent"}</code></dd></div>
              </dl>
            </article>
            <article>
              <span>CHANGE METRICS</span><h3>How much changed</h3>
              <dl>
                <div><dt>Spatial change</dt><dd>{typeof version.modification_scope === "object" ? `${(100 * (version.change_metrics?.spatial_change_ratio ?? version.modification_scope.changed_ratio ?? 0)).toFixed(1)}% measured pixel change` : "0.0% measured pixel change"}</dd></div>
                <div><dt>Changed region</dt><dd>{typeof version.modification_scope === "object" ? JSON.stringify(version.modification_scope.bounding_box ?? "Not recorded") : "Original"}</dd></div>
                <div><dt>Metric meaning</dt><dd>Measured changed pixels — not AI probability, copyright percentage, or truth score.</dd></div>
              </dl>
            </article>
            <article>
              <span>TRUST</span><h3>Independent trust signals</h3>
              <dl>
                <div><dt>Provenance</dt><dd>{result}</dd></div>
                <div><dt>Integrity</dt><dd>{decision?.integrityState ?? "UNVERIFIED"}</dd></div>
                <div><dt>C2PA integrity</dt><dd>{version.c2pa.embedded ? "Valid bytes / manifest present" : "Not present"}</dd></div>
                <div><dt>Signature</dt><dd>{verification.signature_status}</dd></div>
                <div><dt>Identity trust</dt><dd>{version.c2pa.development_signer ? "DEVELOPMENT" : (version.identity_trust ?? version.trust_status ?? "UNKNOWN").toUpperCase()}</dd></div>
                <div><dt>AI involvement</dt><dd>{version.involvement_level} — from signed Event evidence</dd></div>
                <div><dt>Registry</dt><dd>{verification.verified ? "Matched" : "Invalid"}</dd></div>
              </dl>
            </article>
            <article>
              <span>PRIVATE EVIDENCE</span><h3>Owner-controlled by default</h3>
              <p><b>Private Evidence Available:</b> {version.blackbox_available ? "Yes" : "No"}</p>
              <p>{version.blackbox_available ? "A private evidence commitment is available to the owner, but its contents are not disclosed by this public verifier." : "No complete Private Black Box is attached to this demo event."}</p>
              <p><b>Private disclosure architecture — not yet implemented.</b> Mobile Authorization will let an owner approve selected fields, expiry, and purpose before any private evidence is released.</p>
            </article>
          </section>

          <div className="timeline-section">
            <div><span className="section-number">03</span><h2>History</h2><p>Each edit creates a child version with its own time, tool, Event ID, hash, signature, and C2PA manifest. Nothing silently overwrites the original.</p></div>
            <div className="timeline">
              {demo.versions.map((item, index) => <button key={item.version_id} className={selected === index ? "selected" : ""} onClick={() => { setSelected(index); setView(index === 0 ? "image" : "comparison"); clearExplanation(); }}>
                <span className="timeline-index">{index + 1}</span><img src={item.image} alt={item.version_id} /><span className="timeline-copy"><b>{index === 0 ? "Original" : `Edit ${index}`}</b><small>{humanAction(item.action_type)} · {item.involvement_level} · {new Date(item.timestamp).toLocaleDateString()}</small><code>{short(item.event_id)} · parent {short(item.parent_event ?? "none", 8)}</code></span><span className="timeline-check">✓</span>
              </button>)}
            </div>
          </div>

          <section className="proofcart" id="proofcart">
            <div className="proofcart-image"><span className="product-badge">Evidence protected</span><img src="/demo/version-3.png" alt="ProofCart verified listing" /></div>
            <div className="proofcart-copy"><span className="eyebrow">PROOFCART · VERTICAL DEMO</span><h2>A buyer can verify the listing photo before trusting it.</h2><p>The seller&apos;s original, both edits, exact changed region, C2PA chain, and registry signature are attached to one product photo.</p><button className="primary" onClick={tryDemo}>Verify Evidence <span>→</span></button><div className="seller-proof"><span>Seller image</span><b>Signed by gugupro demo issuer</b><small>Evidence ID {short(version.event_id, 14)}</small></div></div>
          </section>

          <section className="universal-architecture" aria-label="Universal Evidence Passport architecture">
            <div className="architecture-intro"><span className="eyebrow">UNIVERSAL EVIDENCE PASSPORT</span><h2>One evidence foundation. Many creation formats.</h2><p>Images are the first working adapter. Every modality connects to the same signed Passport, Event Chain, Registry, and owner-controlled Private Wallet.</p></div>
            <div className="adapter-grid">
              {[
                ["Text", "Text DNA · source coverage"],
                ["Image", "C2PA · spatial change"],
                ["Video", "Timeline · frames · audio"],
                ["Audio", "Segments · spectral fingerprint"],
                ["Documents", "PDF · Office · embedded media"],
                ["2D Design", "Layers · geometry · print lineage"],
                ["3D Models", "Mesh · topology · dimensions"],
                ["Manufacturing", "CAD → G-code → physical output"],
              ].map(([name, detail]) => <div key={name}><b>{name}</b><small>{detail}</small></div>)}
            </div>
            <div className="shared-foundation"><b>Shared foundation</b><span>Passport</span><span>Event Chain</span><span>Hash</span><span>Signature</span><span>Registry</span><span>Private Wallet</span></div>
          </section>

          <section className="next-stage" aria-label="Next stage private evidence authorization">
            <div><span className="eyebrow">NEXT — NOT YET IMPLEMENTED</span><h2>Private Black Box + Mobile Authorization</h2><p>Private evidence stays encrypted and owner-controlled. A verifier receives only the fields the owner approves, for a limited purpose and time.</p></div>
            <ol>
              <li><b>1</b><span>Verifier requests private evidence</span></li>
              <li><b>2</b><span>Phone shows requester, fields, purpose, and expiry</span></li>
              <li><b>3</b><span>Owner approves, denies, or selects fields</span></li>
              <li><b>4</b><span>Phone signs a single-use authorization</span></li>
              <li><b>5</b><span>Black Box releases only authorized evidence</span></li>
            </ol>
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
