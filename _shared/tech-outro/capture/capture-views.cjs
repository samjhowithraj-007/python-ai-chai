// Capture extra views of www.techsamjhoraj.com (hash routes) as 1440-wide 2x full-page PNGs + heading boxes.
const puppeteer = require(process.argv[2]);
const VIEWS = [["lesson", "#python-1"], ["chatbot", "#chatbot-1"], ["upcoming", "#upcoming"]];
(async () => {
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: "new" });
  const out = {};
  for (const [id, hash] of VIEWS) {
    const p = await b.newPage();
    await p.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
    await p.emulateMediaFeatures([{ name: "prefers-color-scheme", value: "dark" }]);
    await p.goto("https://www.techsamjhoraj.com/" + hash, { waitUntil: "networkidle0", timeout: 60000 });
    await new Promise(r => setTimeout(r, 1800));
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); });
    await new Promise(r => setTimeout(r, 600));
    out[id] = await p.evaluate(() => {
      const box = e => { const r = e.getBoundingClientRect(); return { x: Math.round(r.x + scrollX), y: Math.round(r.y + scrollY), w: Math.round(r.width), h: Math.round(r.height) }; };
      return { h: document.documentElement.scrollHeight,
        heads: [...document.querySelectorAll("h1,h2,h3,h4,pre,video,iframe,button")].filter(e => e.offsetParent).slice(0, 40)
          .map(e => ({ tag: e.tagName, t: (e.innerText || e.getAttribute("title") || "").trim().replace(/\s+/g, " ").slice(0, 60), ...box(e) })) };
    });
    await p.screenshot({ path: `view-${id}.png`, fullPage: true });
    await p.close();
  }
  require("fs").writeFileSync("views-boxes.json", JSON.stringify(out, null, 1));
  await b.close();
  for (const k in out) { console.log("==", k, out[k].h); out[k].heads.forEach(h => console.log(" ", h.tag, h.y, h.t)); }
})();
