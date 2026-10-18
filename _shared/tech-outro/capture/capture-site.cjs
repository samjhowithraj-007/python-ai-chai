// Capture www.techsamjhoraj.com for the Tech Explainer outro walkthrough.
// Usage (from this folder): node capture-site.cjs <path to puppeteer-core>
// Writes site-full.png (1440-wide page at 2x), site-top.png and site-boxes.json (nav links, headings, cards in page CSS px).
const puppeteer = require(process.argv[2]);
(async () => {
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: "new" });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
  await p.emulateMediaFeatures([{ name: "prefers-color-scheme", value: "dark" }]);
  await p.goto("https://www.techsamjhoraj.com/", { waitUntil: "networkidle0", timeout: 60000 });
  await new Promise(r => setTimeout(r, 1500));
  // scroll through once so lazy content loads
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); });
  await new Promise(r => setTimeout(r, 800));
  const boxes = await p.evaluate(() => {
    const box = e => { const r = e.getBoundingClientRect(); return { x: Math.round(r.x + scrollX), y: Math.round(r.y + scrollY), w: Math.round(r.width), h: Math.round(r.height) }; };
    const vis = e => e.offsetParent || getComputedStyle(e).position === "fixed";
    const nav = [...document.querySelectorAll("nav a, header a")].filter(vis).map(e => ({ t: e.innerText.trim().slice(0, 40), href: e.getAttribute("href"), ...box(e) }));
    const heads = [...document.querySelectorAll("h1,h2,h3")].filter(vis).map(e => ({ tag: e.tagName, t: e.innerText.trim().slice(0, 70), ...box(e) }));
    const cards = [...document.querySelectorAll("a[href]")].filter(e => vis(e) && e.getBoundingClientRect().height > 80).slice(0, 40)
      .map(e => ({ t: e.innerText.trim().replace(/\s+/g, " ").slice(0, 70), href: e.getAttribute("href"), ...box(e) }));
    return { title: document.title, page: { w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight }, nav, heads, cards };
  });
  require("fs").writeFileSync("site-boxes.json", JSON.stringify(boxes, null, 1));
  await p.screenshot({ path: "site-top.png" });
  await p.screenshot({ path: "site-full.png", fullPage: true });
  await b.close();
  console.log(boxes.title, boxes.page, "nav", boxes.nav.length, "heads", boxes.heads.length, "cards", boxes.cards.length);
})();
