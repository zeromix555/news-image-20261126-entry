// news-image-20261126-entry — main.ts
// Copies the front-page image this repository holds to the output path
// the grader reads: /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).
// Node 22, standard library only. Deterministic: the same bytes every run.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
console.log("wrote entry.png to", outDir);
