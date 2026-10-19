// Real screen recording of techsamjhoraj.com running Python (headless Chrome + CDP screencast).
// A drawn cursor shows every click. Output: rec/frames/*.jpg + rec/frames.txt (ffmpeg concat list) + rec/marks.json
import fs from "fs"; import path from "path"; import { createRequire } from "module";
const require = createRequire(import.meta.url);
const puppeteer = require("C:/Users/rajpr/AppData/Local/npm-cache/_npx/78b67a3578a558a1/node_modules/puppeteer-core");
const glob = p => fs.readdirSync(p);
const HF = path.join(process.env.USERPROFILE, ".cache/hyperframes/chrome/chrome-headless-shell");
const CHROME = path.join(HF, glob(HF)[0], "chrome-headless-shell-win64", "chrome-headless-shell.exe");
const OUT = path.resolve("rec"); fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(path.join(OUT, "frames"), { recursive: true });
const W = 860, H = 1000, SITE = "https://www.techsamjhoraj.com/";
const sleep = ms => new Promise(r => setTimeout(r, ms));

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: [`--window-size=${W},${H}`, "--hide-scrollbars"] });
const page = await browser.newPage();
await page.setViewport({ width: W, height: H, deviceScaleFactor: 2 });
await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: "dark" }]);

// cursor overlay (re-added after every navigation)
const CURSOR = () => { if (document.getElementById("__cur")) return; const c = document.createElement("div"); c.id = "__cur";
  c.innerHTML = '<svg width="34" height="34" viewBox="0 0 24 24"><path d="M4 2l15 9-7 1.5L8.5 20z" fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/></svg><i></i>';
  c.style.cssText = "position:fixed;left:430px;top:500px;z-index:99999;pointer-events:none;transition:left .55s cubic-bezier(.4,0,.2,1),top .55s cubic-bezier(.4,0,.2,1);filter:drop-shadow(0 2px 4px rgba(0,0,0,.5))";
  const st = document.createElement("style"); st.textContent = "#__cur i{position:absolute;left:-14px;top:-14px;width:36px;height:36px;border-radius:50%;background:rgba(127,209,185,.55);transform:scale(0);opacity:0}#__cur.clk i{animation:clk .45s ease-out}@keyframes clk{0%{transform:scale(.2);opacity:1}100%{transform:scale(1.4);opacity:0}}";
  document.head.appendChild(st); document.body.appendChild(c); };
async function cur() { await page.evaluate(CURSOR); }
async function moveTo(sel, dx = 0, dy = 0) {
  const r = await page.$eval(sel, e => { e.scrollIntoView({ block: "center", behavior: "smooth" }); return null; });
  await sleep(700);
  const b = await page.$eval(sel, e => { const r = e.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
  await page.evaluate((x, y) => { const c = document.getElementById("__cur"); c.style.left = x + "px"; c.style.top = y + "px"; }, b.x + dx, b.y + dy);
  await sleep(650); return b;
}
async function click(sel, dx = 0, dy = 0) {
  const b = await moveTo(sel, dx, dy);
  await page.evaluate(() => { const c = document.getElementById("__cur"); c.classList.remove("clk"); void c.offsetWidth; c.classList.add("clk"); });
  await page.mouse.click(b.x + dx, b.y + dy); await sleep(350);
}
async function waitDone(boxSel, max = 60000) {
  const t0 = Date.now();
  while (Date.now() - t0 < max) { const s = await page.$eval(boxSel + " .rstat", e => e.textContent); if (/Done|error|Stopped/.test(s)) return s; await sleep(200); }
}

// screencast
const cdp = await page.createCDPSession(); const frames = []; const marks = {}; let T0 = 0;
cdp.on("Page.screencastFrame", async f => {
  const t = f.metadata.timestamp; if (!T0) T0 = t; const name = `f${String(frames.length).padStart(5, "0")}.jpg`;
  fs.writeFileSync(path.join(OUT, "frames", name), Buffer.from(f.data, "base64")); frames.push([name, t - T0]);
  try { await cdp.send("Page.screencastFrameAck", { sessionId: f.sessionId }); } catch {}
});
const mark = k => { marks[k] = frames.length ? frames[frames.length - 1][1] : 0; console.log("mark", k, marks[k].toFixed(2)); };

// warm Python's CDN cache so the recorded first run is the real "second visit" speed? No: show the honest first load.
await page.goto(SITE + "#python-8", { waitUntil: "networkidle2" });
await page.evaluate(async () => { for (const r of await navigator.serviceWorker.getRegistrations()) await r.unregister(); try { localStorage.setItem("annc-book-1", "1"); } catch {} });
await page.reload({ waitUntil: "networkidle2" }); await cur();
await page.evaluate(() => document.querySelector(".codebox[data-run]").scrollIntoView({ block: "start" })); await page.evaluate(() => scrollBy(0, -90));
await cdp.send("Page.startScreencast", { format: "jpeg", quality: 85, everyNthFrame: 1 });
await sleep(1200); mark("lesson");
await click('.codebox[data-run] [data-act="run"]'); mark("run1");
await waitDone(".codebox[data-run]"); mark("out1"); await sleep(1800);
await click('.codebox[data-run] [data-act="edit"]'); mark("edit");
// change the price 20 -> 25 in the last line
await page.evaluate(() => { const ta = document.querySelector("textarea.ed"); const i = ta.value.lastIndexOf("20"); ta.focus(); ta.setSelectionRange(i, i + 2); });
await sleep(400); await page.keyboard.type("25", { delay: 160 }); await sleep(600);
await click('.codebox[data-run] [data-act="run"]'); mark("run2");
await waitDone(".codebox[data-run]"); mark("out2"); await sleep(1800);
// Playground
await page.evaluate(() => { location.hash = "playground"; }); await sleep(800); await cur(); await page.evaluate(() => scrollTo(0, 0)); mark("pg");
await sleep(800);
await page.select("#pg-ex", "9"); mark("class"); await sleep(900);
await click('#pg-box [data-act="run"]'); await waitDone("#pg-box"); mark("out3"); await sleep(1600);
await page.select("#pg-ex", "11"); mark("loop"); await sleep(900);
await click('#pg-box [data-act="run"]'); mark("run4"); await sleep(2600);
await click('#pg-box [data-act="stop"]'); mark("stop"); await sleep(2000);
await cdp.send("Page.stopScreencast"); await sleep(300);
await browser.close();

// concat list with real frame durations
const lines = ["ffconcat version 1.0"];
for (let i = 0; i < frames.length; i++) { const d = i + 1 < frames.length ? frames[i + 1][1] - frames[i][1] : 0.5; lines.push(`file 'frames/${frames[i][0]}'`, `duration ${Math.max(d, 0.001).toFixed(4)}`); }
lines.push(`file 'frames/${frames[frames.length - 1][0]}'`);
fs.writeFileSync(path.join(OUT, "frames.txt"), lines.join("\n")); fs.writeFileSync(path.join(OUT, "marks.json"), JSON.stringify(marks, null, 1));
console.log("frames", frames.length, "dur", frames[frames.length - 1][1].toFixed(1));
