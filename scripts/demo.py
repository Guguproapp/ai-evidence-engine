import json
from pathlib import Path

from ai_evidence.registry import Registry
from ai_evidence.text_dna import compare_text


ORIGINAL = """人工智慧內容需要可驗證的來源。系統記錄每一次實質修改，並保留父版本與子版本的關係。這些證據只描述發生過什麼，不替法院判斷著作權、侵權或抄襲。\n\n詳細提示詞保存在使用者的私人證據錢包，全球登錄中心只保存必要的雜湊、簽章與查驗位置。"""


def main():
    output = Path("demo-output")
    output.mkdir(exist_ok=True)
    data = output / "data"
    keys = output / "keys"
    registry = Registry(data, keys)
    event = registry.register_text(
        ORIGINAL,
        content_id="demo-article",
        provider="gugupro",
        model="recorded-demo-model",
        model_version="0.1",
        action_type="generate",
        involvement_level="L5",
        modification_scope="entire_document",
        human_approval=True,
        blackbox_available=True,
    )
    variants = {
        "A_retyped_exact": ORIGINAL,
        "B_about_10_percent": ORIGINAL.replace("可驗證的來源", "能被查驗的來源").replace("全球登錄中心", "公開登錄中心"),
        "C_about_30_percent": ORIGINAL.replace("系統記錄每一次實質修改", "每次內容被改動時都建立事件").replace("只描述發生過什麼", "只保存客觀過程").replace("必要的雜湊、簽章與查驗位置", "最低限度的證明資料"),
        "D_heavy_rewrite": "可信任的數位內容需要留下歷程，但權利歸屬仍應交由有權機關判斷。敏感資訊不宜集中上傳。",
    }
    report = {
        "passport": event,
        "signature_verification": registry.verify_event(event),
        "text_dna_tests": {name: compare_text(ORIGINAL, text) for name, text in variants.items()},
        "truth_boundary": {
            "c2pa": "NOT RUN - official tool not installed in this environment",
            "google_synthid": "NOT INTEGRATED - no public general-purpose third-party verification API confirmed",
            "openai_verify_api": "NOT INTEGRATED - no public third-party Verify API confirmed",
        },
    }
    (output / "demo-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
