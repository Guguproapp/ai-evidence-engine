"use client";
/* eslint-disable @next/next/no-img-element -- Direct asset bytes preserve embedded C2PA data; image optimization could transform them. */

import { ChangeEvent, useEffect, useMemo, useRef, useState } from "react";
import { classifyEvidence } from "./evidence-classification.mjs";
import { DEFAULT_LOCALE, htmlLang, isLocale, Locale, LOCALE_STORAGE_KEY, translate } from "./i18n";

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

function humanAction(value: string, locale: Locale) {
  const action = ({
    digital_capture: "Original image captured",
    ai_background_and_badge_edit: "Background adjusted and AI badge added",
    ai_label_and_object_edit: "Product label area changed",
  } as Record<string, string>)[value] ?? value;
  return translate(locale, action);
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

function StatusPill({ value, locale }: { value: string; locale: Locale }) {
  const key = value.toLowerCase().replaceAll(" ", "-");
  return <span className={`status-pill ${key}`} data-canonical-value={value}>{translate(locale, value)}</span>;
}

export function EvidenceVerifier() {
  const [locale, setLocale] = useState<Locale>(DEFAULT_LOCALE);
  const [localeReady, setLocaleReady] = useState(false);
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
  const t = (key: string) => translate(locale, key);

  useEffect(() => {
    const saved = window.localStorage.getItem(LOCALE_STORAGE_KEY);
    const timer = window.setTimeout(() => {
      setLocale(isLocale(saved) ? saved : DEFAULT_LOCALE);
      setLocaleReady(true);
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (!localeReady) return;
    window.localStorage.setItem(LOCALE_STORAGE_KEY, locale);
    document.documentElement.lang = htmlLang(locale);
  }, [locale, localeReady]);

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
      action: humanAction(version.action_type, "en"),
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
        <a className="brand" href="#top" aria-label={t("AI Evidence Engine home")}>
          <span className="brand-mark">AE</span>
          <span><b>AI Evidence Engine</b><small>by GUGUPRO</small></span>
        </a>
        <div className="topbar-actions">
          <nav aria-label={t("Main navigation")}><a href="#verify">{t("Verify")}</a><a href="#proofcart">{t("ProofCart demo")}</a><a href="#details">{t("How it works")}</a></nav>
          <div className="language-switch" role="group" aria-label="Language / 語言">
            <button className={locale === "zh-TW" ? "active" : ""} onClick={() => setLocale("zh-TW")} aria-pressed={locale === "zh-TW"}>繁中</button>
            <span aria-hidden="true">|</span>
            <button className={locale === "en" ? "active" : ""} onClick={() => setLocale("en")} aria-pressed={locale === "en"}>EN</button>
          </div>
        </div>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <span className="eyebrow">{t("UNIVERSAL EVIDENCE PASSPORT")}</span>
          <h1>{t("Prove where a creation came from.")}<br /><em>{t("Without guessing.")}</em></h1>
          <p>{t("AI Evidence Engine records verifiable origin, tools, changes, and history across digital and physical creation. Image provenance is the first working modality.")}</p>
          <div className="hero-actions">
            <button className="primary" onClick={tryDemo}>{t("Try the 60-second demo")} <span>→</span></button>
            <label className="secondary upload-button">{t("Upload an image")}<input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleFile} /></label>
          </div>
          <div className="trust-strip"><span>✓ {t("Local verification")}</span><span>✓ {t("Official C2PA SDK")}</span><span>✓ {t("No image upload")}</span></div>
        </div>
        <div className="hero-proof">
          <div className="proof-card back-card"><span>{t("ORIGINAL")}</span><img src="/demo/version-1.png" alt={t("Original ProofCart product")} /></div>
          <div className="proof-card front-card"><span>{t("VERIFIED MODIFIED")}</span><img src="/demo/version-3-comparison.png" alt={t("Detected changed region")} /><div className="proof-stamp">✓ {t("Evidence chain verified")}</div></div>
        </div>
      </section>

      <section className="verify-entry" id="verify">
        <div><span className="section-number">01</span><h2>{t("Verify your evidence")}</h2><p>{t("The file stays in your browser. We reject unsupported formats and files over 10 MB before processing.")}</p></div>
        <div className="entry-grid">
          <label className={`drop-zone ${busy ? "busy" : ""}`}>
            <span className="upload-icon">↑</span><b>{t(busy ? "Checking C2PA and signature…" : "Choose an image to verify")}</b><small>{t("PNG, JPEG, or WebP · maximum 10 MB")}</small>
            <input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleFile} disabled={busy} />
          </label>
          <div className="evidence-lookup"><label htmlFor="evidence-id">{t("Or enter an Evidence ID")}</label><div><input id="evidence-id" value={evidenceQuery} onChange={(event) => setEvidenceQuery(event.target.value)} placeholder="proofcart-v3" /><button onClick={lookupEvidence}>{t("Verify")}</button></div>{queryMessage && <small>{queryMessage.startsWith("Registry record found:") ? `${t("Registry record found:")} ${queryMessage.split(": ")[1]}` : t(queryMessage)}</small>}</div>
        </div>
        {uploadError && <div className="alert error">{uploadError.startsWith("Verification failed:") ? `${t("Verification failed.")} ${uploadError.slice(20)}` : t(uploadError)}</div>}
        {upload && <div className="upload-result"><StatusPill value={upload.result} locale={locale} /><div><b>{upload.name}</b><small>SHA-256 {short(upload.hash, 16)} · {upload.manifestCount} C2PA Manifest</small></div>{upload.matchedVersion && <span>{t("Registry match:")} {upload.matchedVersion.version_id}</span>}</div>}
      </section>

      <section className="verification-section" ref={resultRef}>
        <div className="section-heading"><div><span className="section-number">02</span><h2>{t("Verification result")}</h2></div>{(upload || (version && verification)) && <StatusPill value={upload?.result ?? result} locale={locale} />}</div>
        {upload && !upload.matchedVersion ? <div className="standalone-result">
          <div><span>{t("Uploaded file")}</span><h3>{upload.name}</h3><p>{t(upload.result === "Invalid Evidence" ? "Evidence is present, but the asset bytes, C2PA claim, signature, or chain do not validate." : "This file is not proven original or modified because no matching AI Evidence Registry record was found.")}</p></div>
          <dl>
            <div><dt>{t("Provenance")}</dt><dd><StatusPill value={upload.result} locale={locale} /></dd></div>
            <div><dt>{t("Integrity")}</dt><dd>{t(upload.integrityState)}</dd></div>
            <div><dt>{t("C2PA integrity")}</dt><dd>{t(upload.c2paIntegrity)}</dd></div>
            <div><dt>{t("Registry")}</dt><dd>{t(upload.registryStatus)}</dd></div>
            <div><dt>{t("Identity trust")}</dt><dd>{t(upload.identityTrust)}</dd></div>
            <div><dt>{t("AI involvement")}</dt><dd>{upload.aiInvolvement === "UNKNOWN" ? t("Unknown — no signed Event level") : upload.aiInvolvement}</dd></div>
            <div><dt>{t("Content hash")}</dt><dd><code>{upload.hash}</code></dd></div>
            <div><dt>{t("C2PA manifests")}</dt><dd>{upload.manifestCount}</dd></div>
            <div><dt>{t("Active manifest")}</dt><dd><code>{upload.activeManifest ?? t("None")}</code></dd></div>
            <div><dt>{t("Validation")}</dt><dd>{upload.validation.map((item) => item.code).filter(Boolean).join(", ") || t("No C2PA validation record")}</dd></div>
            <div><dt>{t("Decision reasons")}</dt><dd>{upload.reasons.join(", ")}</dd></div>
          </dl>
          <details><summary>{t("Developer JSON")}</summary><pre>{JSON.stringify(upload.raw, null, 2)}</pre></details>
          <div className="gemini-explainer">
            <span>{t("AI EVIDENCE EXPLANATION")}</span>
            <h3>{t("Explain the verified facts in plain language")}</h3>
            {explanation ? <><p>{explanation.explanation}</p><small>{explanation.model} on Vertex AI · {t("Status remains")} {t(explanation.verification_status)}</small></> : explanationError ? <p className="explanation-fallback">{t(explanationError)}</p> : <p>{t("Gemini explains verified facts; it cannot assign or change the provenance state.")}</p>}
            <button className="secondary" onClick={explainUpload} disabled={explanationBusy}>{t(explanationBusy ? "Asking Gemini…" : explanation ? "Explain again" : "Explain with Gemini")}</button>
          </div>
          <button className="secondary" onClick={tryDemo}>{t("Return to signed demo")}</button>
        </div> : !demo || !version || !verification ? <div className="loading">{t("Loading signed evidence…")}</div> : <>
          <div className="verification-grid">
            <div className="image-panel">
              <div className="image-tabs">
                <button className={view === "image" ? "active" : ""} onClick={() => setView("image")}>{t("Current image")}</button>
                <button className={view === "comparison" ? "active" : ""} onClick={() => setView("comparison")} disabled={!version.comparison}>{t("Change overlay")}</button>
                <button className={view === "mask" ? "active" : ""} onClick={() => setView("mask")} disabled={!version.mask}>{t("Modification mask")}</button>
              </div>
              <img className="main-image" src={imageSource} alt={`${version.version_id} ${view}`} />
              {typeof version.modification_scope === "object" && <div className="mask-summary"><b>{Math.round((version.modification_scope.changed_ratio ?? 0) * 1000) / 10}% {t("Measured pixel change")}</b><span>{t("White/red areas are measured pixel changes, not AI probability, copyright percentage, or truth score.")}</span></div>}
            </div>
            <div className="facts-panel">
              <div className="plain-answer"><span>{t("What happened?")}</span><h3>{t(version.parent_version_id ? "This image was modified." : "This is the recorded original.")}</h3><p>{humanAction(version.action_type, locale)}</p></div>
              <dl>
                <div><dt>{t("Evidence signature")}</dt><dd className="good">✓ {t(verification.signature_status)}</dd></div>
                <div><dt>C2PA Manifest</dt><dd className="good">✓ {t("Embedded")} · {version.c2pa.manifest_count} {t("version(s)")}</dd></div>
                <div><dt>{t("Signer")}</dt><dd>{version.issuer}</dd></div>
                <div><dt>{t("Created")}</dt><dd>{new Date(version.timestamp).toLocaleString(locale)}</dd></div>
                <div><dt>{t("Content hash")}</dt><dd><code>{short(version.exact_hash, 18)}</code></dd></div>
                <div><dt>{t("Registry")}</dt><dd className="good">✓ {t("Signed record found")}</dd></div>
              </dl>
              <div className="trust-note"><b>{t("Integrity verified; development identity")}</b><p>{t("The C2PA bytes and evidence signature validate. The demo C2PA certificate is a development signer and is not on the official C2PA Trust List.")}</p></div>
              <div className="gemini-explainer">
                <span>{t("AI EVIDENCE EXPLANATION")}</span>
                <h3>{t("What this evidence means")}</h3>
                {explanation ? <><p>{explanation.explanation}</p><small>{explanation.model} on Vertex AI · {t("Status remains")} {t(explanation.verification_status)}</small></> : explanationError ? <p className="explanation-fallback">{t(explanationError)}</p> : <p>{t("Gemini can explain these verified facts in plain language. Hashes, signatures, C2PA, and the Registry remain the source of truth.")}</p>}
                <button className="secondary" onClick={explainVersion} disabled={explanationBusy}>{t(explanationBusy ? "Asking Gemini…" : explanation ? "Explain again" : "Explain with Gemini")}</button>
              </div>
            </div>
          </div>

          <section className="passport-sections" aria-label={t("Evidence Passport details")}>
            <article>
              <span>{t("EVIDENCE PASSPORT")}</span><h3>{t("What this asset is and where it came from")}</h3>
              <dl>
                <div><dt>{t("Passport ID")}</dt><dd><code>{demo.passport_id}</code></dd></div>
                <div><dt>{t("Asset / media")}</dt><dd>{version.asset_type ?? "digital-content"} · {version.media_type ?? "image/png"}</dd></div>
                <div><dt>{t("Evidence profile")}</dt><dd>{version.evidence_profile ?? "aee.image.c2pa.v1 (legacy event view)"}</dd></div>
                <div><dt>{t("Version ID")}</dt><dd>{version.version_id}</dd></div>
                <div><dt>{t("Created")}</dt><dd>{new Date(version.timestamp).toLocaleString(locale)}</dd></div>
                <div><dt>{t("Issuer")}</dt><dd>{version.issuer}</dd></div>
                <div><dt>{t("Creator / agent")}</dt><dd>{version.operator_type} · {version.provider}</dd></div>
                <div><dt>{t("Tool / model")}</dt><dd>{version.software ?? version.model}{version.software_version ? ` ${version.software_version}` : ""}</dd></div>
                <div><dt>{t("AI involvement")}</dt><dd>{version.involvement_level}</dd></div>
                <div><dt>{t("Evidence Event")}</dt><dd><code>{version.event_id}</code></dd></div>
                <div><dt>{t("Parent Event")}</dt><dd><code>{version.parent_event ?? t("Recorded original — no parent")}</code></dd></div>
              </dl>
            </article>
            <article>
              <span>{t("CHANGE METRICS")}</span><h3>{t("How much changed")}</h3>
              <dl>
                <div><dt>{t("Spatial change")}</dt><dd>{typeof version.modification_scope === "object" ? `${(100 * (version.change_metrics?.spatial_change_ratio ?? version.modification_scope.changed_ratio ?? 0)).toFixed(1)}% ${t("Measured pixel change")}` : `0.0% ${t("Measured pixel change")}`}</dd></div>
                <div><dt>{t("Changed region")}</dt><dd>{typeof version.modification_scope === "object" ? JSON.stringify(version.modification_scope.bounding_box ?? t("Not recorded")) : t("Original")}</dd></div>
                <div><dt>{t("Metric meaning")}</dt><dd>{t("Measured changed pixels — not AI probability, copyright percentage, or truth score.")}</dd></div>
              </dl>
            </article>
            <article>
              <span>{t("TRUST")}</span><h3>{t("Independent trust signals")}</h3>
              <dl>
                <div><dt>{t("Provenance")}</dt><dd>{t(result)}</dd></div>
                <div><dt>{t("Integrity")}</dt><dd>{t(decision?.integrityState ?? "UNVERIFIED")}</dd></div>
                <div><dt>{t("C2PA integrity")}</dt><dd>{t(version.c2pa.embedded ? "Valid bytes / manifest present" : "Not present")}</dd></div>
                <div><dt>{t("Signature")}</dt><dd>{t(verification.signature_status)}</dd></div>
                <div><dt>{t("Identity trust")}</dt><dd>{t(version.c2pa.development_signer ? "DEVELOPMENT" : (version.identity_trust ?? version.trust_status ?? "UNKNOWN").toUpperCase())}</dd></div>
                <div><dt>{t("AI involvement")}</dt><dd>{version.involvement_level} — {t("from signed Event evidence")}</dd></div>
                <div><dt>{t("Registry")}</dt><dd>{t(verification.verified ? "Matched" : "Invalid")}</dd></div>
              </dl>
            </article>
            <article>
              <span>{t("PRIVATE EVIDENCE")}</span><h3>{t("Owner-controlled by default")}</h3>
              <p><b>{t("Private Evidence Available:")}</b> {t(version.blackbox_available ? "Yes" : "No")}</p>
              <p>{t(version.blackbox_available ? "A private evidence commitment is available to the owner, but its contents are not disclosed by this public verifier." : "No complete Private Black Box is attached to this demo event.")}</p>
              <p><b>{t("Private disclosure architecture — not yet implemented.")}</b> {t("Mobile Authorization will let an owner approve selected fields, expiry, and purpose before any private evidence is released.")}</p>
            </article>
          </section>

          <div className="timeline-section">
            <div><span className="section-number">03</span><h2>{t("History")}</h2><p>{t("Each edit creates a child version with its own time, tool, Event ID, hash, signature, and C2PA manifest. Nothing silently overwrites the original.")}</p></div>
            <div className="timeline">
              {demo.versions.map((item, index) => <button key={item.version_id} className={selected === index ? "selected" : ""} onClick={() => { setSelected(index); setView(index === 0 ? "image" : "comparison"); clearExplanation(); }}>
                <span className="timeline-index">{index + 1}</span><img src={item.image} alt={item.version_id} /><span className="timeline-copy"><b>{index === 0 ? t("Original") : `${t("Edit")} ${index}`}</b><small>{humanAction(item.action_type, locale)} · {item.involvement_level} · {new Date(item.timestamp).toLocaleDateString(locale)}</small><code>{short(item.event_id)} · parent {short(item.parent_event ?? t("none"), 8)}</code></span><span className="timeline-check">✓</span>
              </button>)}
            </div>
          </div>

          <section className="proofcart" id="proofcart">
            <div className="proofcart-image"><span className="product-badge">{t("Evidence protected")}</span><img src="/demo/version-3.png" alt="ProofCart verified listing" /></div>
            <div className="proofcart-copy"><span className="eyebrow">{t("PROOFCART · VERTICAL DEMO")}</span><h2>{t("A buyer can verify the listing photo before trusting it.")}</h2><p>{t("The seller's original, both edits, exact changed region, C2PA chain, and registry signature are attached to one product photo.")}</p><button className="primary" onClick={tryDemo}>{t("Verify Evidence")} <span>→</span></button><div className="seller-proof"><span>{t("Seller image")}</span><b>{t("Signed by gugupro demo issuer")}</b><small>{t("Evidence ID")} {short(version.event_id, 14)}</small></div></div>
          </section>

          <section className="universal-architecture" aria-label={t("Universal Evidence Passport architecture")}>
            <div className="architecture-intro"><span className="eyebrow">{t("UNIVERSAL EVIDENCE PASSPORT")}</span><h2>{t("One evidence foundation. Many creation formats.")}</h2><p>{t("Images are the first working adapter. Every modality connects to the same signed Passport, Event Chain, Registry, and owner-controlled Private Wallet.")}</p></div>
            <div className="adapter-grid">
              {[
                ["Text", "Text DNA · source coverage"], ["Image", "C2PA · spatial change"], ["Video", "Timeline · frames · audio"], ["Audio", "Segments · spectral fingerprint"],
                ["Documents", "PDF · Office · embedded media"], ["2D Design", "Layers · geometry · print lineage"], ["3D Models", "Mesh · topology · dimensions"], ["Manufacturing", "CAD → G-code → physical output"],
              ].map(([name, detail]) => <div key={name}><b>{t(name)}</b><small>{t(detail)}</small></div>)}
            </div>
            <div className="shared-foundation"><b>{t("Shared foundation")}</b><span>Passport</span><span>Event Chain</span><span>Hash</span><span>Signature</span><span>Registry</span><span>Private Wallet</span></div>
          </section>

          <section className="next-stage" aria-label={t("Next stage private evidence authorization")}>
            <div><span className="eyebrow">{t("NEXT — NOT YET IMPLEMENTED")}</span><h2>{t("Private Black Box + Mobile Authorization")}</h2><p>{t("Private evidence stays encrypted and owner-controlled. A verifier receives only the fields the owner approves, for a limited purpose and time.")}</p></div>
            <ol>
              {["Verifier requests private evidence", "Phone shows requester, fields, purpose, and expiry", "Owner approves, denies, or selects fields", "Phone signs a single-use authorization", "Black Box releases only authorized evidence"].map((step, index) => <li key={step}><b>{index + 1}</b><span>{t(step)}</span></li>)}
            </ol>
          </section>

          <section className="developer-details" id="details">
            <button onClick={() => setDetailsOpen(!detailsOpen)} aria-expanded={detailsOpen}><span><b>{t("Advanced / Developer details")}</b><small>{t("Raw C2PA and registry evidence")}</small></span><span>{detailsOpen ? "−" : "+"}</span></button>
            {detailsOpen && <div className="details-body"><div><b>{t("C2PA tool")}</b><code>{demo.c2pa_tool}</code></div><div><b>{t("Active manifest")}</b><code>{version.c2pa.active_manifest}</code></div><div><b>{t("Evidence event")}</b><code>{version.event_id}</code></div><div><b>{t("Parent event")}</b><code>{version.parent_event ?? t("None")}</code></div><div><b>{t("Event hash")}</b><code>{version.event_hash}</code></div><a href={version.c2pa.raw_report} target="_blank" rel="noreferrer">{t("Open preserved raw C2PA JSON")} →</a></div>}
          </section>
        </>}
      </section>

      <footer><div className="brand"><span className="brand-mark">AE</span><span><b>AI Evidence Engine</b><small>{t("Evidence, not legal verdicts.")}</small></span></div><div className="footer-links"><a href="/privacy">{t("Privacy")}</a><p>{t("Records what happened. It does not decide copyright, infringement, or legality.")}</p></div></footer>
    </main>
  );
}
