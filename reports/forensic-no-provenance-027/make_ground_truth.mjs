import sharp from "../../apps/web/node_modules/sharp/lib/index.js";
import { writeFile } from "node:fs/promises";
import path from "node:path";

const [source, originalOutput, modifiedOutput] = process.argv.slice(2);
if (!source || !originalOutput || !modifiedOutput) {
  throw new Error("usage: node make_ground_truth.mjs SOURCE ORIGINAL_OUTPUT MODIFIED_OUTPUT");
}

const original = await sharp(source).rotate().resize({ width: 1500, height: 2000 }).png().toBuffer();
const metadata = await sharp(original).metadata();
if (metadata.width !== 1500 || metadata.height !== 2000) {
  throw new Error(`unexpected canonical dimensions: ${metadata.width}x${metadata.height}`);
}

const edit = Buffer.from(`
  <svg width="1500" height="2000" xmlns="http://www.w3.org/2000/svg">
    <rect x="1100" y="1425" width="260" height="180" rx="14"
      fill="#e32636" stroke="#ffffff" stroke-width="12"/>
    <path d="M1145 1470 L1315 1560 M1315 1470 L1145 1560"
      stroke="#ffffff" stroke-width="19" stroke-linecap="round"/>
  </svg>
`);

await sharp(original).toFile(originalOutput);
await sharp(original).composite([{ input: edit, top: 0, left: 0 }]).removeAlpha().png().toFile(modifiedOutput);

const before = await sharp(originalOutput).removeAlpha().raw().toBuffer();
const after = await sharp(modifiedOutput).removeAlpha().raw().toBuffer();
const mask = Buffer.alloc(metadata.width * metadata.height * 3);
let changedPixels = 0;
let minX = metadata.width;
let minY = metadata.height;
let maxX = -1;
let maxY = -1;
for (let index = 0; index < metadata.width * metadata.height; index += 1) {
  const offset = index * 3;
  const delta = Math.max(
    Math.abs(before[offset] - after[offset]),
    Math.abs(before[offset + 1] - after[offset + 1]),
    Math.abs(before[offset + 2] - after[offset + 2]),
  );
  if (delta >= 12) {
    mask.fill(255, offset, offset + 3);
    changedPixels += 1;
    const x = index % metadata.width;
    const y = Math.floor(index / metadata.width);
    minX = Math.min(minX, x);
    minY = Math.min(minY, y);
    maxX = Math.max(maxX, x);
    maxY = Math.max(maxY, y);
  }
}

const outputDirectory = path.dirname(originalOutput);
const boundingBox = changedPixels === 0 ? null : {
  x: minX,
  y: minY,
  width: maxX - minX + 1,
  height: maxY - minY + 1,
};
const metrics = {
  method: "ground_truth_pair_pixel_diff",
  pixel_threshold: 12,
  changed_pixels: changedPixels,
  total_pixels: metadata.width * metadata.height,
  spatial_change_ratio: Number((changedPixels / (metadata.width * metadata.height)).toFixed(6)),
  bounding_box: boundingBox,
  warning: "Offline A/B ground truth only; not a single-image AEE Production forensic result.",
};
await sharp(mask, { raw: { width: metadata.width, height: metadata.height, channels: 3 } })
  .png()
  .toFile(path.join(outputDirectory, "ground-truth-mask.png"));
await writeFile(path.join(outputDirectory, "ground-truth-metrics.json"), `${JSON.stringify(metrics, null, 2)}\n`);
