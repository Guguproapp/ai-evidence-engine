const button = document.querySelector("#run");
const message = document.querySelector("#message");
const result = document.querySelector("#result");
const stages = document.querySelector("#stages");
const asset = document.querySelector("#asset");
const firstSeenButton = document.querySelector("#first-seen-run");
const firstSeenFile = document.querySelector("#first-seen-file");
const firstSeenMessage = document.querySelector("#first-seen-message");
const firstSeenResult = document.querySelector("#first-seen-result");

function value(id, text) {
  document.querySelector(`#${id}`).textContent = text || "—";
}

button.addEventListener("click", async () => {
  button.disabled = true;
  message.textContent = "正在建立Signed Event並呼叫IAM保護的Remote Black Box…";
  result.hidden = true;
  try {
    const response = await fetch("/v1/demo/continuity", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ asset_id: asset.value }),
    });
    const payload = await response.json();
    if (!response.ok || payload.evidence_continuity !== "PASS") throw new Error(payload.error || `HTTP ${response.status}`);
    stages.replaceChildren(...payload.stages.map((stage) => {
      const row = document.createElement("div");
      const copy = document.createElement("span");
      const status = document.createElement("strong");
      copy.innerHTML = `<b>${stage.name}</b><small></small>`;
      copy.querySelector("small").textContent = stage.detail;
      status.textContent = stage.status;
      row.append(copy, status);
      return row;
    }));
    value("final-status", payload.evidence_continuity);
    value("passport", payload.signed_event.passport_id);
    value("event", payload.signed_event.event_id);
    value("generation", payload.remote_seal.generation);
    value("retention", payload.remote_seal.retention_expiration);
    value("hash", payload.retrieval.retrieved_sha256);
    result.hidden = false;
    message.textContent = "完整流程已由真實服務執行完成。";
  } catch (error) {
    message.textContent = `執行失敗：${error.message}`;
  } finally {
    button.disabled = false;
  }
});

firstSeenButton.addEventListener("click", async () => {
  const file = firstSeenFile.files[0];
  if (!file) {
    firstSeenMessage.textContent = "請先選擇圖片。";
    return;
  }
  firstSeenButton.disabled = true;
  firstSeenResult.hidden = true;
  firstSeenMessage.textContent = "正在建立First-Seen Signed Event、Google封存並重新取回驗證…";
  try {
    const form = new FormData();
    form.append("evidence_file", file, file.name);
    const response = await fetch("/v1/demo/first-seen", { method: "POST", body: form });
    const payload = await response.json();
    if (!response.ok || payload.evidence_continuity !== "PASS") throw new Error(payload.error || `HTTP ${response.status}`);
    value("first-seen-status", payload.registration_status);
    value("first-seen-prior", payload.prior_provenance);
    value("first-seen-passport", payload.signed_event.passport_id);
    value("first-seen-event", payload.signed_event.event_id);
    value("first-seen-generation", payload.remote_seal.generation);
    value("first-seen-retention", payload.remote_seal.retention_expiration);
    value("first-seen-hash", `${payload.retrieval.stored_sha256} = ${payload.retrieval.retrieved_sha256} · MATCH ${payload.retrieval.hash_match ? "YES" : "NO"}`);
    firstSeenResult.hidden = false;
    firstSeenMessage.textContent = "AEE已從這個時間點開始保存可驗證履歷；更早來源仍為未知。";
  } catch (error) {
    firstSeenMessage.textContent = `執行失敗：${error.message}`;
  } finally {
    firstSeenButton.disabled = false;
  }
});
