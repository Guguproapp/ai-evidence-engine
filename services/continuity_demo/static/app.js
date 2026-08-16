const button = document.querySelector("#run");
const message = document.querySelector("#message");
const result = document.querySelector("#result");
const stages = document.querySelector("#stages");
const asset = document.querySelector("#asset");

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
