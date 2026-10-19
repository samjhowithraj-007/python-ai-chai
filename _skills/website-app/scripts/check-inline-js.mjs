// Syntax-check every inline <script> in a page before pushing:  node <skill>/scripts/check-inline-js.mjs index.html
// Exits 1 on the first broken script, so it can gate a push:  node …/check-inline-js.mjs index.html && git push
// (19 Oct 2026: a // comment pasted mid-line cut off ") });" and broke paisasamjhoraj.com for 3 minutes.)
import { readFileSync } from "node:fs";

const file = process.argv[2] || "index.html";
const html = readFileSync(file, "utf8");
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)(?![^>]*type="application\/ld\+json")[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let bad = 0;
scripts.forEach((code, i) => {
  try { new Function(code); }
  catch (e) { bad++; console.error(`✗ ${file} inline script ${i + 1}: ${e.message}`); }
});
for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
  try { JSON.parse(m[1]); } catch (e) { bad++; console.error(`✗ ${file} JSON-LD: ${e.message}`); }
}
if (/\x08/.test(html)) { bad++; console.error(`✗ ${file} contains a backspace character (a "\\b" eaten by a shell heredoc)`); }
if (bad) process.exit(1);
console.log(`✓ ${file}: ${scripts.length} inline script(s) parse`);
