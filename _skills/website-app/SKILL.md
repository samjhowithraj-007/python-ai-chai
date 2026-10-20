---
name: website-app
description: Create, move or update a Samjho with Raj website and its installable app. Covers a single-page site on GitHub Pages with a Namecheap domain, moving a domain (with an old-domain redirect that keeps https and #links working), DNS (A + AAAA + www CNAME), HTTPS enforcement, PWA install (manifest, offline service worker, icons, an "Install app" button with the app icon and colour, desktop and iPhone / in-app-browser guides), Google Search Console, social icons (YouTube / Instagram / Facebook / X), email sign-up with Brevo (lists, double opt-in forms, privacy page, sending-domain DNS and senders), the "Ask Raj" rule-based chat helper, the Series page's live-episode list, profile links, and the later App Store / Google Play path. Use when Raj says "new website", "move the website", "new domain", "make it an app", "install app not showing", "site flickers", "add icons", "email sign-up / notify subscribers", "Brevo", "chatbot", "episode is live", "site not opening on phone", "add to Google", or "update links on social media".
---

# Website + app routine (Samjho with Raj)

Raj's live setup, as of 2026-10-18. Copy this pattern for any new site.

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
- **Don't touch:** other existing TXT records, such as `_cf-custom-hostname` and `_openai-site-verification`, the Brevo records (§10: `brevo-code` TXT on `@`, `brevo1/2._domainkey` CNAMEs, `_dmarc` TXT), and the `v=spf1 include:spf.efwd.registrar-servers.com` SPF that Namecheap's email forwarding adds (it doesn't show in the connector's record list, only in public DNS).

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
   - **Desktop (since 2026-10-18):** always shown. Chrome/Edge with a prompt install in one click; otherwise it opens browser steps (Chrome: install icon in the address bar or ⋮ → Cast, save and share → Install page as app; Edge: ⋯ → Apps → Install this site as an app; Safari: File → Add to Dock; Firefox: can't, use Chrome/Edge). Before this it only appeared when Chrome fired `beforeinstallprompt`, so Raj "didn't see it".
   - **Hidden** when the site is already running as an installed app.
6. **How the button looks (Raj's choices):**
   - The app icon (`img/icon-192.png`, 28 px round) + "Install app"; on ≤420 px the label shortens to "Install" (`<span class="install-x"> app</span>`).
   - Background = the site's app colour (tech `#202321`, paisa `#1d6b4f`), white text, faint white outline in dark mode. Never `var(--ink)`: that turns white in dark mode.
   - A pop + accent ring, **3 times** after load (`animation: … 3`), then still; pauses on hover; off for reduced-motion. Raj first asked for it to "keep popping", then said the site flickered, so don't make it infinite.
   - **No `hidden` attribute in the HTML.** It is visible from the first paint and hidden only by `@media (display-mode:standalone){.install{display:none!important}}`. Showing it from JS after load shifted the header on every page load (the "flicker").
7. **Testing:**
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
- Each site hosts a privacy page at `#privacy` (§10). The only data collected is an email address a visitor chooses to give, stored in Brevo.

## 9. Social icons

- `SOCIAL` entries have `icon` (key into an `ICONS` map of 24×24 SVG paths) and an optional `color`. `fillSocial()` renders round icon buttons with `aria-label` + `title`; entries without `icon` stay text pills.
- Icons: YouTube `#ff0000`, Instagram `#e1306c`, Facebook `#1877f2`, X (no colour, follows the theme, `https://x.com/samjhowithraj`). The cross-site link is an icon too: tech site → ₹ coin (`money`, `var(--green)`), money site → violet AI sparkle (`tech`, `#8b5cf6`), with the site name in the title.
- Pass the colour as `--sb`, **not `--brand`**: the money site already defines `--brand` on `:root`, which turned the X icon green.
- The header hides `.social` under 700 px (the Install button needs the room); the footer and About page still show them.

## 10. Email sign-up (Brevo)

Raj chose sign-up boxes, **not** a login wall: a login wall would block Google indexing and video viewers. MailerLite was dropped because its free plan shrank to about 250 subscribers (2026). Brevo started on the free plan (300 emails a day, "Sent by Brevo" footer). **Since 20 Oct 2026 Raj has a paid Brevo subscription**: use it fully for marketing (campaigns, automations, segments by list), and check the plan's send limit and footer setting in the account before quoting them. Raj's standing rule: every new launch (website feature, book or video) gets a Brevo campaign, plus Shorts and Reels posted on all platforms by the Campaigns team. The website session's part: tell Campaigns the live link and the facts (prices, dates).
- **Account:** Brevo org "techsamjhoraj", Raj's login, used for both sites. Lists: **Paisa lessons** (#3), **Tech lessons** (#4). Forms: "Paisa lessons sign-up" and "Tech lessons sign-up" (Marketing → Forms), Full page/embedded, **double confirmation email** with the default DOI template.
- **On the site:** `const SIGNUP = { action: "<sibforms URL>" }` and `signup(lead)` returns the box (empty string while `action` is empty, so the box can ship switched off). The submit handler posts `FormData` with `EMAIL`, `email_address_check` (empty honeypot), `locale=en`, `html_type=simple` via `fetch(..., { mode: "no-cors" })`, then shows "check your inbox". The action URL comes from the form's Share → Simple HTML code (`action="https://b84d134c.sibforms.com/serve/…"`).
- **Where the box sits:** home/classroom page, inside `<article class="lesson">` at the end of every lesson (outside the article it lands in the page grid under the sidebar), and the Series/Upcoming list.
- **Privacy page `#privacy`** on both sites, linked in the footer: no account needed, progress stays in local storage, email only if you sign up, stored by Brevo, opens/clicks may be counted, unsubscribe link, deletion via samjhowithraj@gmail.com, no analytics/cookies, GitHub Pages logs. Footer wording changed from "No sign-up" to "No tracking · Privacy".
- **Never put a Brevo API key in the site** (anyone could read the list or send mail). Raj once pasted one in chat; it wasn't in the account, but if one appears, have it deleted (Settings → SMTP & API → API keys). Forms don't need a key.
- Seeing subscribers: Brevo → Contacts → Lists (count per list), or the form's stats.

## 11. Brevo sending domains and senders

- Settings → Senders, domains, IPs → Domains → Add a domain → skip the branded subdomain → **Manual** (not Automatic, which wants Namecheap access). Brevo shows 4 records; read the values with JS from the page's inputs (the DMARC value is masked in tool output: swap `=@:;` for words to read it).
- Add them with the Namecheap connector `dns_records_save` (it only adds): TXT `@` `brevo-code:8294604a05e2c479ad174e3ddcf0afed` (same code for both domains), CNAME `brevo1._domainkey` → `b1.<domain-with-dash>-com.dkim.brevo.com`, CNAME `brevo2._domainkey` → `b2.…`, TXT `_dmarc` `v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com`. Public DNS (`https://dns.google/resolve?name=…&type=…`) showed them in about 40 s; then click **Authenticate domain** (the records page text stays stale; check the Domains list). Both domains are Authenticated.
- Senders (all Verified): **techsamjhoraj** <updates@techsamjhoraj.com>, **Paisa Samjho Raj** <updates@paisasamjhoraj.com>, **Samjho with Raj** <samjhowithraj@gmail.com> (Brevo's default; Raj asked for these names). The updates@ addresses have no inbox: set reply-to samjhowithraj@gmail.com on campaigns. Brevo warns that freemail senders go to spam; use the updates@ senders for announcements.
- Brevo's Add sender page often freezes when typing with `computer.type`; use `form_input` for the fields, and reload if a screenshot times out. Skip the "Brand your domain" pop-up.
- **Why mail went to spam (fixed 2026-10-18):** campaigns and the double opt-in template were sending from the Gmail sender (Brevo rewrites it to @brevosend.com). New campaigns still **default to the Gmail sender** (Brevo has no "set default"), so always switch it.
- **Branded confirmation emails (2026-10-18):** Brevo's default DOI design (one line + button) landed in spam even from the right sender, so #3 and #8 were replaced (Content ⋮ → Reset design → Add content → Create from scratch → HTML custom code) with `emails/confirm-paisa.html` / `emails/confirm-tech.html`: logo header, why you got it, a **`{{ doubleoptin }}`** button (required), "ignore if you didn't sign up", and an "add updates@… to your contacts" tip. After saving, the template turns Inactive: use **Save → Save & activate**. Transactional → Logs shows each confirmation's sender and opens.
- **Gmail Primary vs Promotions (tested 2026-10-18):** the showcase emails (big image, cards, many buttons, ₹ in the subject) landed in Promotions; letter-style versions landed in **Primary** for both sites. Use the letter style for welcome and personal notes: `emails/welcome-letter-tech.html` / `welcome-letter-paisa.html` (plain text look, no images, 2 links, "just hit reply" ask, "drag to Primary" line, unsubscribe; money version keeps a one-line not-advice note), sender name **"Raj from Samjho with Raj"** / **"Raj from Paisa Samjho Raj"** (still the updates@ addresses), subject "Welcome, and where to start". Brevo drafts: #11 "Tech welcome (letter)", #12 "Finance welcome (letter)" (no recipients yet). Keep the showcase design for big announcements, where Promotions is fine.
- **Tech letter tuning (2026-10-18):** the first Tech letter (two links in a numbered list, "I'll send you one short email each time", "drag to Primary") went to Promotions for a real subscriber while Finance stayed in Primary. Rewritten as a personal note with **one link**, no list, no email-frequency promise, a reply question, and the newest lesson named in text (Python with Chai, 15 lessons, latest range()): Primary again. Keep welcome letters to one or two links and refresh the "newest lesson / next part" line as videos come out (edit both the automation step message and the template).
- **Welcome automations (live since 2026-10-18):** Automations → Workflows: **"Tech welcome letter"** (#1: Contact added to list *Tech lessons* → Send an email) and **"Finance welcome letter"** (#2: *Paisa lessons* → Send an email), both Active, re-entry off. Contacts join a list only after the double opt-in click, so the welcome goes out right after confirmation. Emails come from templates #13 "Tech welcome letter (automation)" / #14 "Finance welcome letter (automation)" (letter HTML, "Raj from …" sender, reply-to Gmail); the automation keeps its own copy (#15 / #16), so to change the text later, edit the step's message in the workflow. Builder tips: clicking a trigger/action in the side panel adds it (drag-and-drop doesn't work through automation); Send an email → Add message → Create new message → pick the saved template → "Use this design in automation" → Save; rename via the title at the top left; Activate automation → Activate. A free-plan limit applies to automation contacts.
- **Sending only to new sign-ups (manual, before automations existed):** Duplicate the campaign with **Recipients unticked**, then Recipients → Send to → Individual contacts (or "Recently used") → pick the new addresses, Save, Schedule → Send now. Check each new contact's Lists tab first (Contacts → contact → Lists) so nobody gets a site they didn't sign up for. The list pages sometimes render empty; the Lists overview and the contact page are reliable.
- First real campaigns sent 2026-10-18 (#6 Tech, #7 Finance, 2 recipients each). An earlier attempt at Send now was blocked by the session's safety classifier until Raj said "you can do it".
- **Confirmation emails:** template #3 renamed "Paisa double opt-in" (sender Paisa Samjho Raj <updates@paisasamjhoraj.com>, subject "Confirm your subscription to Paisa Samjho Raj"), used by the Paisa form; #8 "Tech double opt-in" (techsamjhoraj <updates@techsamjhoraj.com>), used by the Tech form (Form → Settings → template). Dropdowns may show the old names (#8 = "…confirmation_copy").
- **Campaigns (drafts):** #6 "Tech lessons: welcome" → list Tech lessons, sender techsamjhoraj <updates@techsamjhoraj.com>; #7 "Finance lessons: welcome" → list Paisa lessons, sender Paisa Samjho Raj <updates@paisasamjhoraj.com>; both reply-to samjhowithraj@gmail.com (Additional settings → Use a different Reply-to address). #5 is an old test draft. Tests of #6 and #7 reached Raj's Gmail inbox/Promotions, not spam. Sending to real subscribers needs Raj's go.
- **Design:** course-showcase HTML emails kept in the repos (`samjhowithrajwebsite/emails/welcome-tech.html`, `paisasamjhorajwebsite/emails/welcome-paisa.html`; not published): header, featured video (tech `media/chatbot-3.jpg`, paisa YouTube thumbnail `i.ytimg.com/vi/<id>/maxresdefault.jpg`), course/tool cards (copy a card block for new courses or books), coming-next box, footer with `{{ unsubscribe }}` and privacy link; money emails keep the educational-only disclaimer. Put them in Brevo via Design → Create from scratch → **HTML custom code**: the editor is a plain `<textarea>`, so set it with the native value setter + `input` event in JS (`String.raw` template; the HTML has no backticks), type one space and delete it, then Save & Quit.
- Campaign editing tips: the subject/preview fields accept `computer.type`; in the list picker, tick the list then press Escape (clicking elsewhere can untick it); Escape in Preview & Test closes the whole dialog, so tick the test address, click the dialog heading, then Send Test.

## 12. "Ask Raj" chat helper

- Raj chose a **rule-based** helper (no AI, no keys, nothing sent anywhere) on both sites, named **Ask Raj** with the ☕ icon (earlier "SamjhoBot"). The header says "Automated helper" and the greeting says it is not Raj himself; keep that.
- Code: `askRaj(BOT)` builds a floating button (`.cb-fab`, app colour, "☕ Ask Raj" on phones too) and a chat panel (`.cb-panel`; bottom sheet under 480 px; tapping an internal link closes it on phones). `BOT = { tagline, foot, hello, chips, rules: [[keywords[], reply | fn(t)]], fallback }`; replies may be `{ text, chips }`. Matching lowercases the text; the **first matching rule wins**.
- Tech brain: chai shop (menu, order masala/adrak/elaichi/tulsi, bill with the Lesson 7 ₹5 discount over ₹50) plus course guide (Python, chatbot, Agentic AI, Upcoming, install, email, contact; "how are you built" → dictionary + if-else, chatbot Parts 2–3; "bye" → Lesson 10 break).
- Money brain: maps topics to `L(id)` lesson and `C(id)` calculator links; the **advice rule comes first** ("which fund", "best stock", "recommend", "tips", "crypto"…) and refuses (not SEBI-registered, points to the costs/index/allocation lessons). Every topic reply ends with "Educational only, not advice."
- Rule-order gotchas found in testing: "where do i start" matched the order rule via "do" (removed "do", "one", "ek", "give"; start rule placed before order/bill); "expense ratio" matched budget via "expense" (fees rule placed before budget). Test new keywords with a quick script that sends messages and reads the last bot reply.

## 13. Series page: mark an episode live

On paisasamjhoraj.com `#series`, `EP_LIVE = { "01": "https://youtu.be/GyPQ-RxBRi8" }` drives it: live parts get a linked title and a green "▶ Watch" chip; the first not-live part says "Coming next". When a new part goes public, add its long-video link (check it with `https://www.youtube.com/oembed?url=…`), bump sw, commit, ask Raj, push. This is also step 7 of the publish checklist in memory.

## 14. Featured slot, sponsors and books (monetising)

- Raj chose his own ad space over AdSense (AdSense: tiny earnings at his traffic, approval risk for a script-rendered single page, tracking cookies + consent banner, and loan/trading/crypto ads next to the money site's "not advice" message).
- `PROMOS = [{ label, title, text, image, link, cta }]` and `promo(here)` render one card (`.promo`) on the home/classroom page (first promo) and at the end of every lesson (rotates, never promotes the page you're on), just above the email box. `label` is "From Raj" for his own things and **"Sponsored"** for a paid sponsor (external sponsored links get `rel="noopener sponsored"`). To run a sponsor: add an entry at the top with label "Sponsored", bump sw, ask, push.
- Money-site sponsors: education-friendly only, no loan apps, trading tips, crypto or anything that reads like advice (stated on the About page). The privacy pages say featured spots are plain links, not an ad network.
- Tech site "Recommended books" (`books()`, `BOOKS`, `id="books"`, on the classroom page): Amazon India search links; set `AMAZON_TAG` to Raj's Amazon Associates ID (he signs up himself) and the links and the disclosure line switch to affiliate wording automatically. No cover images (copyright); emoji tiles instead. Ask Raj answers "books".

## 15. Editing and shipping checklist

- Raj approves every push ("Push both sites live?"). Commit each repo separately with the samjhowithraj-007 identity.
- **Before every push:** `node ~/.claude/skills/website-app/scripts/check-inline-js.mjs index.html` must print ✓ (see "Lessons from 19 Oct 2026 (paisasamjhoraj.com session)").
- **Line endings differ by repo and can change** (paisasamjhoraj.com `index.html` was LF on 19 Oct 2026, techsamjhoraj.com CRLF; check with `git ls-files --eol index.html`). Patch with Python in binary mode, detect the newline (`"\r\n" if b.count(b"\r\n") > 100 else "\n"`) and keep the file's newline (Git Bash `sed -i` and text-mode Python rewrote whole files once). Long Python heredocs can break in Git Bash: write the script to the scratchpad and run it.
- Bump `VERSION` in each `sw.js` for every change to `index.html`.
- Test locally with `python -m http.server` via a temporary `.claude/launch.json` in the working folder (delete it after), at desktop and the `mobile` preset, light and dark. A hidden browser pane can't screenshot: read computed styles with JS instead. The browser caches `index.html`; add `?v=N` to the URL.
- After pushing, poll the live page for a string from the change (`curl -s "https://www.<d>/?nc=$RANDOM" | grep -q …`); deploys take 10–40 s. Tell Raj to press Ctrl + Shift + R if he still sees the old version.

## Backup

After any change to this skill, copy it to `C:\samjhowithraj\vlog1\.claude\skills\website-app` and `C:\samjhowithraj\vlog1\videos\_skills\website-app`. Then commit and push python-ai-chai, with the same rule as youtube-edit.

## Lessons from 19 Oct 2026 (Content Planner)
- **Push only with Raj's OK, and only what he OK'd.** A single urgent page (e.g. tonight's lesson `#chatbot-4`) can go
  out alone while a redesign waits; bump `sw` on every push. A follow-up bug fix to an OK'd page is fine; say so.
- **Before/after first:** show phone + desktop snapshots (folder `C:\samjhowithraj\website-snapshots\<date>\`) for any
  redesign, then push after OK. Aim Lighthouse ≥ 90, accessibility 100, `prefers-reduced-motion` respected.
- **Design direction (Raj, 19 Oct: "professional and high-tech"):** tech site = dev-tool/AI-product look (dark-first, glow,
  animated code hero, Ctrl+K search that opens Ask Raj); money site = fintech look (slider calculators, instant charts,
  trust blocks: sources, "checked on" dates, bylines). Ideas only from benchmark sites; never copy design, text or assets.
- **Weekly ideas:** scheduled task `weekly-website-polish-ideas` (Wed 9 AM) adds ranked ideas to each repo's IMPROVEMENTS.md.
- **Ask Raj:** Step 1 = hand-written replies first, then `site-index.json` (built before each push: `node tools/build-index.mjs`)
  searched in the browser with a passage + link. Step 2 = one shared Cloudflare Worker (`C:\samjhowithraj\ask-raj-worker\`,
  model claude-haiku-5-5, CORS for both domains, rate limit + daily cap, key only as a Worker secret Raj sets himself);
  falls back to Step 1 on error or after 8 s. Money answers always carry "Educational, not advice".
- **Earning features:** Shop (books + templates + packs), Workshops page with an enquiry form, cohort waitlist. Until Raj
  OKs Brevo forms, forms open an email to samjhowithraj@gmail.com. No investment/insurance/credit-card affiliates (SEBI,
  AMFI, IRDAI) and no AdSense for now.
- **Money facts on the site** carry a source and "checked on" date (e.g. card interest "up to about 45% a year",
  checked 19 Oct 2026).
- **Approvals:** every push or Raj step also goes as one line to the Content Planner; "done: <what>" after.

## Lessons from 19 Oct 2026 (techsamjhoraj.com session, technical)
- **Lesson-only push while a redesign is uncommitted:** build the file from the live code (`git show HEAD:index.html > tmp`),
  apply the same patch script to it, then `git hash-object -w tmp` + `git update-index --cacheinfo 100644,<hash>,index.html`
  (and sw.js with its bump), commit, push. The working copy keeps the redesign; its own push needs the next `sw` VERSION.
- **Run box + chat loops:** lesson code that loops on `input()` with no `break` ends with EOFError when the preloaded input
  runs out. Keep the code exactly as in the video; the site treats that case as a normal finish ("Done in N s" + a grey
  "No more lines in the Input box…" note). The status next to Run shows in screen captures, so check it before telling the
  video session a page is ready (it said "Finished with an error" once).
- **Speed (phones):** a header `backdrop-filter` over a fixed, masked grid/glow layer cost ~900 ms of layout; a long
  font-family list (Segoe UI Variable, SF Pro…) doubled layout time. Use `system-ui,-apple-system,"Segoe UI",Roboto,sans-serif`,
  a near-solid header, `content-visibility:auto` on lower blocks, and `main{min-height:100svh}` so the footer doesn't shift
  (CLS) when the page renders from JS. Local Lighthouse on this PC swings 75–92 while other sessions render: alternate
  old/new runs, compare traces (`Layout` time per pass), then confirm on PageSpeed Insights after the push.
- **Screenshots:** plain headless Chrome clips widths under ~500 px. Use puppeteer-core + the hyperframes
  chrome-headless-shell (as in `videos/python-chai-live-demo/record.mjs`), one browser context per shot (localStorage leaks
  between pages otherwise). `content-visibility` blocks look blank in full-page shots; scroll them into view to check.
- **Ask Raj build details:** `tools/build-index.mjs` runs the page's own script in a Node `vm` with a do-nothing DOM stub and
  calls the view functions (sign-up/promo boxes stubbed out). A local `.git/hooks/pre-push` refuses a push when
  `site-index.json` is stale. The Worker looks up passage text by id in the site's published index; it never trusts text from
  the browser (that would make it a free Claude proxy). Test with `test/fake-claude.mjs` + `wrangler dev` (no key, no cost).
  `wrangler.toml` changes need a full restart (`--var` and `.dev.vars` did not override `[vars]`), and old `workerd`
  processes can keep port 8787: stop them by command line before restarting.
- **Patching index.html (CRLF):** write patch scripts to files with raw strings. Inline Python in a bash heredoc once
  turned the regex word boundary (backslash + b) into a backspace character; after a patch, search the file for byte 0x08.

## Lessons from 19 Oct 2026 (paisasamjhoraj.com session)
- **Syntax-check before EVERY push (paisasamjhoraj.com was broken for about 3 minutes).** A `// comment` pasted into the
  middle of a one-line `fetch(…, { body: … }) });` commented out the closing `});`, so the whole page script stopped.
  It got pushed because the build step was chained as `node tools/build-index.mjs | grep -v ERROR && git push`: the
  `grep` succeeded, which hid the build's failure. Rules:
  - `node ~/.claude/skills/website-app/scripts/check-inline-js.mjs index.html` parses every inline script and the
    JSON-LD and flags backspace bytes; gate the push on it: `check && build && git push`. Never pipe a check through
    `grep`/`tail` before `&&` (the pipe's exit code is the last command's).
  - Put comments on their own line, never in the middle of a line of code.
  - After the LAST edit, reload and do one real action again (e.g. ask Ask Raj a question). A test done before a "tiny"
    edit doesn't count.
  - After pushing, poll the live page for a string from the change, then open it once in the browser pane and check
    the console for errors.
- **Grid columns holding long unbreakable content** (formula boxes with `white-space:nowrap`) need
  `grid-template-columns:minmax(0,1fr)`, not `1fr`, or the column widens and the phone page scrolls sideways.
- **Money site redesign (live 19 Oct, Raj: "same kind as the tech site"):** reuse the tech site's look, not new ideas:
  dark-first, faint grid + glow on `body::before`, bold system-ui headings with a gradient `<em>`, one big gold CTA
  (`.btn.cta`) + a ghost button, byline + stats row, a live widget on the right of the hero (money: mini SIP slider
  with the SIP calculator's own maths), a 4-card trust strip, footer columns, and a moon button (`#theme`,
  `localStorage psr-theme`). Money colours: gold `#F5B83D` + green `#3ccf8e` (dark), `#137a4f` (light).
  - Make it dark-first by setting `data-theme="dark"` in a tiny `<head>` script before paint, so all the older
    `:root[data-theme="dark"]` rules keep working; the light theme is the base `:root`.
  - Put the redesign as an override block at the END of `<style>` (later rules win) instead of editing 60 old rules.
  - A new header button can push the wordmark onto two lines on phones: `.brand{white-space:nowrap}` and smaller
    sizes at ≤440 px / ≤370 px (as on the tech site).
  - `html{overflow-x:clip}` makes `scrollWidth` always equal the screen width, so a "no sideways scroll" check by
    `scrollWidth` proves nothing. Check elements instead: any `getBoundingClientRect().right > innerWidth`.
  - Lighthouse runs locally from the npx cache: `node ~/AppData/Local/npm-cache/_npx/<hash>/node_modules/lighthouse/cli/index.js
    <url> --form-factor=mobile --only-categories=performance,accessibility,best-practices,seo --chrome-flags=--headless=new`
    with `CHROME_PATH` set. Compare old (live) vs new (localhost) in the same run.
