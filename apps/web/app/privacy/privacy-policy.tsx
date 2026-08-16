"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { DEFAULT_LOCALE, htmlLang, isLocale, Locale, LOCALE_STORAGE_KEY } from "../i18n";

const copy = {
  "zh-TW": {
    title: "隱私權政策",
    updated: "最後更新：2026 年 8 月 16 日",
    intro: "本政策說明 AI Evidence Engine by GUGUPRO 如何處理你在公開 Verifier 與未來 Android 應用程式中使用的資料。",
    localTitle: "本機圖片驗證",
    local: "你選擇的 PNG、JPEG 或 WebP 圖片會在裝置瀏覽器內計算 SHA-256 並解析 C2PA。公開 Verifier 的現行流程不會把原始圖片傳送到 AI Evidence Engine、Google Cloud Run 或 Gemini。",
    cloudTitle: "Gemini 證據說明",
    cloud: "只有在你按下「使用 Gemini 解釋」時，系統才會把經過白名單限制的結構化驗證事實傳送至 Google Cloud Run，再由 Vertex AI Gemini 產生白話說明。資料可能包含驗證狀態、版本 ID、Evidence ID、修改比例、C2PA 狀態、Registry 狀態、簽章狀態與公開簽發者；不包含原始圖片、Prompt、私人來源檔案或 Private Black Box 內容。Gemini 不會決定或改變驗證狀態。",
    logsTitle: "紀錄與保存",
    logs: "Google Cloud 可能為資安、錯誤排查、限流與服務可靠性保存標準請求紀錄，例如時間、HTTP 狀態、服務版本與技術診斷。Production 不刻意記錄原始圖片；結構化說明請求可能短暫出現在受控服務紀錄中。實際保存期限依 GUGUPRO 的 Google Cloud 日誌設定與 Google Cloud 服務政策為準。",
    browserTitle: "裝置端資料",
    browser: "網站使用 localStorage 保存語言偏好 aee_locale。此偏好留在你的裝置，可由你清除瀏覽器網站資料刪除。第一版不要求帳號，不使用廣告，不要求聯絡人、位置、簡訊、通話紀錄、相機或麥克風權限。",
    thirdTitle: "第三方服務",
    third: "本產品使用 Google Cloud Run、Vertex AI Gemini 與 Content Authenticity Initiative 的 C2PA 開源工具。第三方服務依其各自條款與隱私政策處理必要技術資料。",
    rightsTitle: "你的選擇與權利",
    rights: "你可以不使用 Gemini 說明，密碼學與 C2PA 驗證仍可繼續運作。你可以清除本機語言偏好，也可以就資料處理提出查詢、更正或刪除要求。",
    contactTitle: "聯絡方式",
    contact: "正式支援信箱在 Google Play 上架前仍需由擁有者確認（OWNER INPUT REQUIRED）。在此之前可透過公開專案頁提出一般技術問題。請勿公開提交身分證件、API Key、私人金鑰或敏感證據。",
    back: "返回 Verifier",
  },
  en: {
    title: "Privacy Policy",
    updated: "Last updated: August 16, 2026",
    intro: "This policy explains how AI Evidence Engine by GUGUPRO handles data used in the public Verifier and planned Android application.",
    localTitle: "On-device image verification",
    local: "PNG, JPEG, or WebP images you select are hashed with SHA-256 and parsed for C2PA inside your device browser. The current public Verifier does not send the original image to AI Evidence Engine, Google Cloud Run, or Gemini.",
    cloudTitle: "Gemini Evidence Explanation",
    cloud: "Only when you select “Explain with Gemini” does the app send allowlisted structured verification facts to Google Cloud Run and Vertex AI Gemini. Facts may include verification state, version ID, Evidence ID, change ratio, C2PA status, Registry status, signature status, and public issuer. They do not include the original image, prompts, private source files, or Private Black Box contents. Gemini cannot decide or change verification states.",
    logsTitle: "Logging and retention",
    logs: "Google Cloud may retain standard request logs for security, debugging, rate limiting, and reliability, such as timestamps, HTTP status, service revision, and technical diagnostics. Production does not intentionally log original images. Structured explanation requests may appear temporarily in controlled service logs. Retention follows GUGUPRO's Google Cloud logging configuration and applicable Google Cloud service policies.",
    browserTitle: "On-device data",
    browser: "The site uses localStorage to save the aee_locale language preference. You can remove it by clearing site data. Version 1 requires no account, uses no ads, and requests no contacts, location, SMS, call log, camera, or microphone permission.",
    thirdTitle: "Third-party services",
    third: "The product uses Google Cloud Run, Vertex AI Gemini, and open-source C2PA tooling from the Content Authenticity Initiative. Each provider handles necessary technical data under its own terms and privacy policy.",
    rightsTitle: "Your choices and rights",
    rights: "You may decline Gemini explanation; cryptographic and C2PA verification still work. You may clear local language preferences and request information, correction, or deletion concerning processed data.",
    contactTitle: "Contact",
    contact: "The final support email requires owner confirmation before Google Play submission (OWNER INPUT REQUIRED). Until then, general technical questions may be submitted through the public project page. Do not publicly submit identity documents, API keys, private keys, or sensitive evidence.",
    back: "Back to Verifier",
  },
} as const;

export function PrivacyPolicy() {
  const [locale, setLocale] = useState<Locale>(DEFAULT_LOCALE);
  useEffect(() => {
    const saved = window.localStorage.getItem(LOCALE_STORAGE_KEY);
    const next = isLocale(saved) ? saved : DEFAULT_LOCALE;
    document.documentElement.lang = htmlLang(next);
    const timer = window.setTimeout(() => setLocale(next), 0);
    return () => window.clearTimeout(timer);
  }, []);
  const c = copy[locale];
  function choose(next: Locale) {
    setLocale(next);
    window.localStorage.setItem(LOCALE_STORAGE_KEY, next);
    document.documentElement.lang = htmlLang(next);
  }
  return <>
    <header className="topbar"><Link className="brand" href="/"><span className="brand-mark">AE</span><span><b>AI Evidence Engine</b><small>by GUGUPRO</small></span></Link><div className="language-switch" role="group" aria-label="Language / 語言"><button className={locale === "zh-TW" ? "active" : ""} onClick={() => choose("zh-TW")}>繁中</button><span>|</span><button className={locale === "en" ? "active" : ""} onClick={() => choose("en")}>EN</button></div></header>
    <main className="privacy-page"><span className="eyebrow">AI EVIDENCE ENGINE</span><h1>{c.title}</h1><p className="policy-note">{c.updated}<br />{c.intro}</p>
      <h2>{c.localTitle}</h2><p>{c.local}</p><h2>{c.cloudTitle}</h2><p>{c.cloud}</p><h2>{c.logsTitle}</h2><p>{c.logs}</p><h2>{c.browserTitle}</h2><p>{c.browser}</p><h2>{c.thirdTitle}</h2><p>{c.third}</p><h2>{c.rightsTitle}</h2><p>{c.rights}</p><h2>{c.contactTitle}</h2><p>{c.contact}</p><p><Link href="/">← {c.back}</Link></p>
    </main>
  </>;
}
