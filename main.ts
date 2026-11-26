// news-image-20261126 entry: copies the poster image beside this file
// to the output directory as entry.png, after validating it is a whole
// PNG within the competition limits (at most 1024x1024, at most 1 MiB).
// The image is the program's own drawing of Thursday 26 November 2026's
// world news, produced by news-image-20261126-draw.py.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const srcPath = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(srcPath);

// PNG magic bytes.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG (bad magic bytes)');
}
// IHDR: width and height are big-endian uint32 at offsets 16 and 20.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(srcPath, dest);

const sha256 = createHash('sha256').update(bytes).digest('hex');
console.log(`entry.png: ${width}x${height}, ${bytes.length} bytes, sha256 ${sha256}`);
console.log(`wrote ${dest}`);
