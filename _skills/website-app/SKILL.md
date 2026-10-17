---
name: website-app
description: Create, move or update a Samjho with Raj website and its installable app. Covers a single-page site on GitHub Pages with a Namecheap domain, moving a domain (with an old-domain redirect that keeps https and #links working), DNS (A + AAAA + www CNAME), HTTPS enforcement, PWA install (manifest, offline service worker, icons, an "Install app" button with iPhone Safari / iPhone Chrome / in-app-browser guides), Google Search Console, profile links on YouTube / Instagram / Facebook, and the later App Store / Google Play path. Use when Raj says "new website", "move the website", "new domain", "make it an app", "install app not showing", "site not opening on phone", "add to Google", or "update links on social media".
---

# Website + app routine (Samjho with Raj)

Raj's live setup, as of 2026-10-17. Copy this pattern for any new site.

| Site | Repo (github.com/samjhowithraj-007/…) | Local folder | Icon bg |
|---|---|---|---|
| www.techsamjhoraj.com (Python, AI) | `samjhowithrajwebsite` | `C:\samjhowithraj\samjhowithrajwebsite` | `#202321` |
| www.paisasamjhoraj.com (money, calculators, Money Planner) | `paisasamjhorajwebsite` | `C:\samjhowithraj\paisasamjhorajwebsite` | `#1d6b4f` |
| www.samjhowithraj.online (old, forwards to tech) | `samjhowithraj-online-redirect` | `C:\samjhowithraj\samjhowithraj-online-redirect` | n/a |

**Identity.** Every repo uses `git config user.name samjhowithraj-007` and `user.email pragya.bigdata@gmail.com`. Never use the machine's global identity or the "richatiwary08" login. There is no `gh` CLI, so create repos in Chrome at github.com/new. **Creating a new public repo needs Raj's explicit yes.**

**Rules.** Website text is English (videos stay Hinglish). Finance pages keep the "educational only, not SEBI-registered advice" disclaimer in the footer, the About page and next to every result. One site per topic; each site links the other in its SOCIAL list and footer.

## 1. Build a site

- One static `index.html`: hash routes (`#learn/<id>`, `#calculators/<id>`, …), inline CSS with colour tokens on `:root` plus a dark mode, no build step. Reuse the shell of the existing sites: header with brand and tabs, `<main id="app">`, footer.
- Before publishing, check it in the browser pane at desktop width and with the `mobile` preset: no console errors, no sideways scroll at 375 px.
- Assets go in `img/` and `media/`. Videos are never precached.

## 2. Publish on GitHub Pages

1. In Chrome: github.com/new → owner samjhowithraj-007 → name → Public → Create. Then `git init -b main`, set the identity, `git remote add origin https://samjhowithraj-007@github.com/samjhowithraj-007/<repo>.git`, push.
2. Copy `templates/.github/workflows/pages.yml`. Edit the `cp -r …` line so it lists every published file: `index.html CNAME manifest.webmanifest sw.js robots.txt sitemap.xml google<token>.html img [media]`. **Any new top-level file must be added to that line, or it won't be published.**
3. Repo Settings → Pages → Source: **GitHub Actions** (choose this before the first deploy; otherwise the first run fails).
4. Settings → Pages → Custom domain `www.<domain>` → **click the Save button.** Pressing Enter does not save. With Actions deploys, the domain is set here; the CNAME file alone is not enough.
5. The workflow has `paths-ignore`, so **an empty commit does not deploy.** Push a real file change, or re-run the workflow.
6. Check deploys with `curl -s "https://api.github.com/repos/samjhowithraj-007/<repo>/actions/runs?per_page=3"`.

## 3. DNS at Namecheap

For each domain:
- `@` → A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- `@` → AAAA records `2606:50c0:8000::153` … `2606:50c0:8003::153`. Indian mobile networks prefer IPv6.
- `www` → CNAME `samjhowithraj-007.github.io.`
- Remove Namecheap's parking `URL Redirect` and the `parkingpage.namecheap.com` CNAME.

How to make the changes:
- **Adding records:** the Namecheap connector's `dns_records_save` adds records without touching existing ones. Use it for A, AAAA and CNAME.
- **Removing records:** use Chrome at `ap.www.namecheap.com/Domains/DomainControlPanel/<domain>/advancedns`:
  - Make the Chrome window large first (resize to 1100×850); a tiny window freezes typing.
  - Rows: Add New Record → type dropdown → Host → Value → ✓. Do one record per batch with a screenshot; chaining two rows broke once.
- **Don't touch:** other existing TXT records, such as `_cf-custom-hostname` and `_openai-site-verification`.

Once GitHub's DNS check passes: Settings → Pages → tick **Enforce HTTPS** (on every repo). Then verify:
```bash
for u in http://<d>/ https://<d>/ http://www.<d>/ https://www.<d>/; do curl -s -o /dev/null -w "$u %{http_code} %{redirect_url}\n" $u; done
```
Every form must end at `https://www.<d>/`.

## 4. Moving to a new domain

1. Set up the new domain as in steps 2–3 and change the custom domain in the repo.
2. Change the links in the site, the README, the youtube-edit skill, memory, the series plans and the teleprompter. Old video files keep the old text.
3. **Old domain:** don't use a Namecheap URL Redirect. It doesn't answer on https, so the links in posted videos time out. Instead, make a tiny Pages repo (`templates/redirect-index.html` as `index.html` and `404.html`, plus `CNAME` = old www domain, deployed from branch `main` root). Point the old domain's DNS at GitHub as in step 3. The page keeps `#lesson` links intact, so `https://www.samjhowithraj.online/#chatbot-3` opens the right lesson.
4. If a section moves to another site, keep its old hash working by forwarding it. Example: the tech site's `#tracker` → `location.replace("https://www.paisasamjhoraj.com/#planner")`.

## 5. Installable app (PWA)

1. Icons: `bash scripts/make-icons.sh <site-folder> 0x<bg-hex>`. The source is the 600 px logo `C:\samjhowithraj\logo-banner\samjhowithraj_watermark_600.png`; the 160 px `raj-mark.png` is too small.
2. Copy `templates/manifest.webmanifest`. Change `name` and `short_name` (app name = site name, e.g. "Paisa Samjho Raj"), `description`, `start_url`, `background_color` / `theme_color` (= icon bg), `categories` and `shortcuts`.
3. Copy `templates/sw.js`. Change the cache prefix and the precache list. **Bump `VERSION` every time sw.js or a precached file changes**, so phones update. Strategy: pages network-first, other files cache-first with a background refresh, `mp4/webm/m4a` never cached.
4. Paste the 5 parts of `templates/install-snippet.html`: head tags, header button, dialog, CSS, JS. Also add `@media (max-width:700px){.bar .social{display:none}}`, so the header fits next to the button.
5. What the Install button does:
   - **Android Chrome:** the real one-tap install (beforeinstallprompt). If Chrome isn't ready, it shows "⋮ → Install app".
   - **iPhone Safari:** numbered steps at the top, with a bouncing "Share is down here ⬇".
   - **iPhone Chrome:** "⬆ Share is up here" (Share is in the address bar; needs iOS 16.4+).
   - **WhatsApp, Instagram or Facebook in-app browsers:** "open in Chrome or Safari first".
   - **Hidden** when the site is already running as an installed app.
6. **Testing:**
   - The Claude browser pane can't register service workers, so test the PWA in Raj's Chrome on localhost (`python -m http.server <port>`), then unregister and clear caches.
   - For the iPhone dialogs, use a throwaway copy with `isIOS = true ||` or a fake CriOS `ua`. Delete it before committing, and check it returns 404 on the live site.
   - Use the browser pane's `mobile` preset for the Android path (reload after switching).

**Explaining it to Raj or viewers:** an iPhone never "downloads" from a website. Add to Home Screen *is* the install. Shared links open inside WhatsApp or Instagram, where installing is impossible. If a site "doesn't open when typed", the cause is usually a Google search box instead of the address bar, or a cached parking page.

## 6. Google Search Console (account raj.pragya84@gmail.com)

1. Add a property as **URL prefix** `https://www.<domain>/` (not "Domain": its TXT record write through the connector was blocked).
2. Verify with the HTML file. For Raj's account it is `googleef50f6b23d7dfe9f.html`, containing `google-site-verification: googleef50f6b23d7dfe9f.html`. Commit it (it's in the workflow `cp` list) and never delete it.
3. Add `robots.txt` (with a `Sitemap:` line) and `sitemap.xml`, then Sitemaps → submit `sitemap.xml`. A first "Couldn't fetch" is normal; Google retries.
4. In the URL inspection box at the top, enter the home page → **Request indexing**. Close the tip pop-ups first; they block the button.

## 7. Profile links (both sites everywhere)

- **YouTube Studio → Customisation:**
  - Links: "Tech lessons: Python + AI" and "Money lessons + calculators".
  - Description: a 🌐 line and a 💰 line. The description limit is 1000 characters, and `**` doesn't render on YouTube, so leave it out.
  - Publish, and check for "Changes published".
- **Instagram:**
  - accounts/edit bio is 150 characters at most. Type it with `computer.type` after selecting all, then Submit.
  - The clickable Website links can only be edited **in the phone app**; tell Raj.
- **Facebook page:**
  - About → Links: edit and add a link, then Save.
  - About → Intro → Bio: up to 255 characters; list both sites.
- Update memory `reference-socials.md` and `websites.md`.

## 8. App Store / Google Play (next step)

- Wrap each site with **Capacitor**: `com.techsamjhoraj.app` and `com.paisasamjhoraj.app`, with the same names as the sites.
- Raj does himself:
  - Apple Developer ($99 a year) and Google Play Console ($25), with ID verification.
  - Line up 12 Android testers for 14 days (Google's rule for new personal accounts).
  - Signing certificates.
- iOS builds go through a cloud Mac (Codemagic), since Raj is on Windows.
- Apple guideline 4.2 rejects plain web wrappers. The app needs offline use, notifications for new lessons and episodes, saved progress, and native share.
- Play's **financial features declaration** for Paisa: education and calculators only, no loans, trading or advice.
- Each site hosts a privacy policy page; there's no data collection.

## Backup

After any change to this skill, copy it to `C:\samjhowithraj\vlog1\.claude\skills\website-app` and `C:\samjhowithraj\vlog1\videos\_skills\website-app`. Then commit and push python-ai-chai, with the same rule as youtube-edit.
