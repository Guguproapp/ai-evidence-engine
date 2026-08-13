import hashlib
import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from ai_evidence.c2pa_adapter import C2paTool
from ai_evidence.image_diff import comparison_image, diff_mask, draw_text, fill_ellipse, fill_rect, solid_canvas, write_rgb_png
from ai_evidence.registry import Registry


WIDTH = 720
HEIGHT = 480


def build_pixels(version):
    background = (238, 243, 247) if version == 1 else (220, 235, 242)
    pixels = solid_canvas(WIDTH, HEIGHT, background)
    if version >= 2:
        for y in range(HEIGHT):
            shade = int(220 + 18 * y / HEIGHT)
            fill_rect(pixels, WIDTH, HEIGHT, 0, y, WIDTH, y + 1, (shade - 8, shade, min(255, shade + 7)))
    fill_ellipse(pixels, WIDTH, HEIGHT, 360, 390, 210, 30, (174, 184, 192))
    fill_rect(pixels, WIDTH, HEIGHT, 210, 105, 510, 375, (224, 135, 55))
    fill_rect(pixels, WIDTH, HEIGHT, 230, 125, 490, 355, (244, 165, 73))
    fill_rect(pixels, WIDTH, HEIGHT, 260, 165, 460, 305, (250, 246, 235))
    draw_text(pixels, WIDTH, HEIGHT, 292, 195, "GUGU", (24, 52, 72), 7)
    draw_text(pixels, WIDTH, HEIGHT, 309, 260, "V1" if version == 1 else ("V2" if version == 2 else "V3"), (67, 89, 103), 4)
    if version >= 2:
        fill_ellipse(pixels, WIDTH, HEIGHT, 520, 105, 54, 54, (31, 104, 89))
        draw_text(pixels, WIDTH, HEIGHT, 492, 88, "AI", (255, 255, 255), 5)
    if version >= 3:
        fill_rect(pixels, WIDTH, HEIGHT, 250, 245, 470, 320, (24, 52, 72))
        draw_text(pixels, WIDTH, HEIGHT, 270, 267, "PROOF", (255, 255, 255), 4)
    return pixels


def manifest_definition(event_id, version_id, parent_version_id, action):
    return {
        "claim_generator_info": [{"name": "gugupro AI Evidence Engine", "version": "0.2.0"}],
        "title": "ProofCart evidence image " + version_id,
        "assertions": [{
            "label": "org.gugupro.ai-evidence",
            "data": {
                "event_id": event_id,
                "version_id": version_id,
                "parent_version_id": parent_version_id,
                "action": action,
                "registry": "AI Evidence Engine",
            },
        }],
    }


def main():
    root = Path(__file__).resolve().parents[1]
    output = root / "demo-output" / "image-demo"
    if output.exists():
        shutil.rmtree(output)
    raw_dir = output / "raw"
    signed_dir = output / "signed"
    mask_dir = output / "masks"
    c2pa_dir = output / "c2pa"
    public_dir = root / "apps" / "web" / "public" / "demo"
    for directory in (raw_dir, signed_dir, mask_dir, c2pa_dir):
        directory.mkdir(parents=True, exist_ok=True)

    tool = C2paTool()
    registry = Registry(output / "registry", output / "registry-keys", issuer_id="gugupro-demo-issuer")
    passport_id = str(uuid.uuid4())
    content_id = "proofcart-product-photo"
    pixels = {version: build_pixels(version) for version in (1, 2, 3)}
    for version in (1, 2, 3):
        write_rgb_png(raw_dir / f"version-{version}.png", WIDTH, HEIGHT, pixels[version])

    masks = {}
    for version in (2, 3):
        mask, stats = diff_mask(pixels[version - 1], pixels[version], WIDTH, HEIGHT)
        comparison = comparison_image(pixels[version - 1], pixels[version], mask, WIDTH, HEIGHT)
        write_rgb_png(mask_dir / f"version-{version}-mask.png", WIDTH, HEIGHT, mask)
        write_rgb_png(mask_dir / f"version-{version}-comparison.png", WIDTH, HEIGHT, comparison)
        masks[version] = stats

    actions = {1: "digital_capture", 2: "ai_background_and_badge_edit", 3: "ai_label_and_object_edit"}
    events = []
    c2pa_reports = []
    parent_event = None
    parent_version = None
    parent_signed = None
    for version in (1, 2, 3):
        event_id = str(uuid.uuid4())
        version_id = f"proofcart-v{version}"
        manifest_path = c2pa_dir / f"version-{version}-manifest.json"
        manifest_path.write_text(json.dumps(manifest_definition(event_id, version_id, parent_version, actions[version]), ensure_ascii=False, indent=2), encoding="utf-8")
        signed_path = signed_dir / f"version-{version}.png"
        sign_report = tool.sign(
            raw_dir / f"version-{version}.png",
            signed_path,
            manifest_path,
            parent=parent_signed,
            create_type="digitalCapture" if version == 1 else None,
        )
        read_report = tool.read(signed_path)
        (c2pa_dir / f"version-{version}-sign-report.json").write_text(json.dumps(sign_report, ensure_ascii=False, indent=2), encoding="utf-8")
        (c2pa_dir / f"version-{version}-read-report.json").write_text(json.dumps(read_report, ensure_ascii=False, indent=2), encoding="utf-8")
        event = registry.register_file(
            signed_path,
            event_id=event_id,
            passport_id=passport_id,
            content_id=content_id,
            parent_event=parent_event,
            provider="gugupro",
            model="deterministic-image-demo",
            model_version="0.2.0",
            action_type=actions[version],
            involvement_level="L0" if version == 1 else "L4",
            modification_scope="original" if version == 1 else masks[version],
            operator_type="Human" if version == 1 else "AI/Program",
            human_approval=True,
            blackbox_available=True,
        )
        events.append({
            **event,
            "version_id": version_id,
            "parent_version_id": parent_version,
            "image": f"/demo/version-{version}.png",
            "mask": None if version == 1 else f"/demo/version-{version}-mask.png",
            "comparison": None if version == 1 else f"/demo/version-{version}-comparison.png",
            "c2pa": {
                "tool": tool.version(),
                "embedded": True,
                "manifest_count": len(read_report.get("manifests", {})),
                "active_manifest": read_report.get("active_manifest"),
                "validation_status": read_report.get("validation_status", []),
                "raw_report": f"/demo/version-{version}-c2pa.json",
                "development_signer": True,
            },
        })
        c2pa_reports.append(read_report)
        parent_event = event_id
        parent_version = version_id
        parent_signed = signed_path

    verification = [registry.verify_event(event) for event in events]
    demo = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "product": "ProofCart verified product photo",
        "passport_id": passport_id,
        "content_id": content_id,
        "c2pa_tool": tool.version(),
        "versions": events,
        "registry_verification": verification,
        "mask_method": "Per-pixel RGB maximum-channel difference with threshold 12; white pixels are observed changes.",
        "security": {"private_key_deployed": False, "client_side_upload_processing": True, "max_upload_bytes": 10485760, "allowed_types": ["image/png", "image/jpeg", "image/webp"]},
    }
    output.joinpath("demo-case.json").write_text(json.dumps(demo, ensure_ascii=False, indent=2), encoding="utf-8")
    public_dir.mkdir(parents=True, exist_ok=True)
    for version in (1, 2, 3):
        shutil.copy2(signed_dir / f"version-{version}.png", public_dir / f"version-{version}.png")
        shutil.copy2(c2pa_dir / f"version-{version}-read-report.json", public_dir / f"version-{version}-c2pa.json")
        if version > 1:
            shutil.copy2(mask_dir / f"version-{version}-mask.png", public_dir / f"version-{version}-mask.png")
            shutil.copy2(mask_dir / f"version-{version}-comparison.png", public_dir / f"version-{version}-comparison.png")
    public_dir.joinpath("demo-case.json").write_text(json.dumps(demo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "c2pa_tool": tool.version(), "versions": len(events), "all_registry_signatures_valid": all(item["verified"] for item in verification), "mask_stats": masks}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

