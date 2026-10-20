---
name: book-course
description: Raj's (Tech Samjho Raj) workflow for making an illustrated programming e-book (English + Hinglish editions, Chotu chai-cup mascot, every code output really run) and selling it with free teasers on techsamjhoraj.com, plus the plan for turning a series into a training course. Use when Raj asks for a book, notes PDF, e-book, workbook, course, training material, or "put my book on the site / sell it".
---

# Books and training courses (Tech Samjho Raj)

The reference build is `C:\samjhowithraj\vlog1\videos\python-chai-book\` ("Python with Chai: From Basic to Expert",
30 chapters × 10 A5 pages ≈ 330 pages). **Copy that folder for a new book and change only the content files.** Don't
invent a new layout (see the reuse-approved-templates rule).

## Raj's decisions (don't re-ask)
- Book structure:
  - Basic → Intermediate → Expert.
  - Topics follow a good trending book's order, not the channel playlist.
  - 30 chapters × 10 pages.
- Two editions: **English** and **Hinglish**. Same pages and same code; only the text differs.
- Look: a **hybrid** of a printed book and handwritten notes.
  - Body text: DM Sans.
  - Headings: Caveat. Bubbles and stickies: Patrick Hand.
  - Code: JetBrains Mono.
  - Mascot: **Chotu**, the chai cup, on every page (`mascot.py`, with poses that match the page kind).
- Every chapter includes:
  - 4 examples with child-like explanations
  - a "What if…?" box and a "Chotu's tip" box
  - 3 mistakes, each with the **real** error
  - 4 practice tasks plus a challenge
  - a cheat sheet and a "next chapter" pointer
- Back matter: answers at the back, plus an index and a contents page.
- Cover:
  - Author **Raj**, with his **half-body** photo from a thumbnail, and the logo.
  - Baloo 2 display font on a purple→pink→orange gradient (`book.py` COVER_CSS).
- Bio: "AI expert, Azure & Claude certified AI architect, coder and engineer, 20 years in tech, working at a tech
  company in Amsterdam, the Netherlands".
- Pricing (Indian market, 300-page illustrated e-book): ₹299 list, ₹199 launch, ₹399 for both editions (₹299 during the launch).
- Formats: PDF + EPUB in every purchase, at the same price. Store: Gumroad (later maybe Amazon/Flipkart and a UPI gateway).

## Build pipeline (python-chai-book)
- **Content.** `content_NN.py` / `content_A_B.py` are chapter dicts. Every text field is an `(en, hi)` tuple. The schema
  is in `build.py` (`topic_pages`): `n, level, title, hook, learn[4], story, idea[≤5], tip, syntax, labels[4], ex1…ex4,
  whatif, walk[≤5], mistakes[3]{t,wrong,fix,why}, practice[4], challenge, answers, cheat[5], next, terms`.
  Optional: `setup`, `files`, `ex*_in`, `ex*_pytest`.
- **Commands.**
  - `python build.py check` runs **every snippet for real** and fails on any surprise.
  - `python build.py topics N` builds one chapter.
  - `python build.py all` builds every chapter plus the teasers and both full books. It takes about 40 minutes, so
    run it in the background.
- **Rendering.** Headless Chrome (hyperframes chrome-headless-shell) prints A5 PDFs. JS auto-fit shrinks the text
  from 19px to 10.5px. The build ends with an **overflow report**: fix every listed page by shortening the text.
- **Outputs.**
  - Full books: `out/python-with-chai-{en,hi}-full.pdf`
  - Per-chapter PDFs: `out/notes/python-N-{en,hi}.pdf`
  - Teasers: `out/notes/python-N-{en,hi}-preview.pdf`
  - Covers: `out/cover-{en,hi}.png`
  - EPUBs: `videos/book-epub/out/` (see "EPUB" below). Ads and Gumroad images: `videos/book-ads/out/` (see "Ads").
- **Gotchas.**
  - Build any edit to a content file with an editor or a script file, not a bash heredoc: heredocs turn `\n` into
    real newlines. After editing, run an `ast.parse` check.
  - Fix seeds for `random`. Give each chapter its own data file names.
  - pytest runs from `.venv-tools`.
  - Fonts must be the **Latin** subset woff2 (DM Sans was once a 7 KB wrong subset, so all body text fell back to serif).
  - Overflow fixes: answers are packed by size (~40 lines a page). The contents page is split over 2 pages.
    `ex3_on_p7=True` gives a long ex4 page 8 to itself. `data-overflow` holds the overflow in pixels, so a 2px
    overflow just needs a shorter explanation.
  - The website's index.html is CRLF: after editing it with Python, check `git diff --stat` is small.
  - One session per book: never let two sessions edit python-chai-book at once.

## Selling: what goes public and what doesn't
- **Never** put a full-book or full-chapter PDF on the website or in a public repo. Only the `*-preview.pdf` teasers
  go public. A teaser is: the chapter title page, the story page, blurred locked thumbnails of the rest with an
  "inside the book" list, and a buy page. Make teasers only for chapters that match channel topics.
- Website (techsamjhoraj.com, `samjhowithrajwebsite/index.html`):
  - Set the `BOOK` config: prices, `buy:{en,hi,both}` links, `previews:[…]`. Empty buy links show "Coming soon"
    plus the email signup.
  - The `#book` page has a cover with a bobbing Chotu, a price box, buy buttons, teaser cards, the contents and an FAQ.
  - `bookBox()` on lesson pages uses the `BOOK_FOR_LESSON` map.
  - The book is the first entry in `PROMOS`.
  - Teasers are copied to `notes/book-chN-{en,hi}-preview.pdf`. Covers go to `media/book-cover-{en,hi}.jpg` and the
    banner to `media/book-promo.jpg`.
  - Bump `sw.js` VERSION, run the node parse check, push.
- Legal: it's his own original text and code, so selling is fine. Fonts are OFL (licence files are in `fonts/`).
  Add a "Python is a PSF trademark, not affiliated" line. Indian GST applies above the threshold, and the platform
  handles invoices. Raj lives in the Netherlands, so the income is likely taxed there: tell him to ask his tax adviser.

## EPUB for e-readers (included in every purchase, same price)
- `videos/book-epub/build_epub.py` builds a **reflowable EPUB 3** from the finished `out/python-with-chai-{en,hi}-full.html`
  (read only). Output is `book-epub/out/python-with-chai-{en,hi}.epub`, about 0.5 MB each. The folder has a `*` .gitignore
  because it's paid content.
- What it keeps and drops:
  - Kept: cover, front matter, 30 chapters (one XHTML each, Chotu on the chapter opener), answers, about the author.
  - Dropped: the contents pages (the reader's own TOC replaces them), the index (there are no page numbers), footers and
    per-page mascot bubbles.
  - Fonts: DM Sans, Caveat and JetBrains Mono are embedded (OFL allows it).
- XHTML gotchas: strip inline SVG, self-close `<br>` and `<img>`, turn `&nbsp;` into `&#160;`, escape bare `&`, and escape `<`
  not followed by a letter (e.g. `<__main__.Cup object>`). Check every file with `minidom`.
- Validate with **W3C epubcheck** (Java: `winget install Microsoft.OpenJDK.21`; the jar is from the w3c/epubcheck GitHub
  release). The target is 0 errors / 0 warnings. The nav must sit in the spine as a normal (linear) page.
- Tell buyers: the PDF is the designed print layout; the EPUB resizes for Kindle, Kobo and phones. **Same price**, both
  formats in every product. The Kindle (KDP) store can take this EPUB later.

## Gumroad shop (what was actually set up, Oct 2026)
- **Account and money (Raj only):**
  - Raj creates the account, enters bank/ID/KYC details himself, and clicks **Publish**. The safety check blocks Claude
    from publishing because it's a payments action.
  - Claude may fill product listings, upload files, create discount codes, and change settings Raj asks for (username,
    time zone, country).
- **Store and products:** samjhowithraj.gumroad.com, time zone Amsterdam. Three **E-book** products, currency **₹ (INR)**:
  - `/l/python-with-chai-en` ₹299
  - `/l/python-with-chai-hinglish` ₹299
  - `/l/python-with-chai-both` ₹399
- **Each product has:**
  - Cover 1280×720 and thumbnail 600×600 (`python book-ads/gumroad.py`).
  - A description: what's inside, who it's for, the author bio, the free preview link, the PSF line.
  - A summary, plus details "Pages 336 · Format PDF (A5) + EPUB".
  - Content tab: the PDF + EPUB, uploaded one file at a time and confirmed listed before **Save**.
  - Receipt: button "Download your book" and a thank-you message (Hinglish for the Hinglish edition).
- **Discount codes:**
  - **LAUNCH**: ₹100 off all products, ends 15 Nov 2026. It's built into the buy links (`/l/<slug>/LAUNCH` applies it and
    shows "₹100 off will be applied at checkout").
  - **A private 10% code** (its name is ONLY in Claude's local memory file book-project.md, never in this skill, git, the site, ads or captions).
  - Validity gotcha: untick **"No end date"**, then set the date with the native value setter + input event. Check that
    the list shows "Oct 18 – Nov 15".
- **Pricing strategy (Raj said "use the clever marketing one"):**
  - Keep the ₹299 list price as an anchor and run a time-boxed launch: ₹199, bundle ₹299.
  - The deadline is real (the code expires).
  - The bundle is the obvious best value, which also beats Gumroad's fixed per-sale fees.
- **Fees** (Gumroad direct sales): 10% + 50¢, plus 2.9% + 30¢ processing. Discover sales cost 30%. At ₹199 Raj keeps
  about half, at ₹299 about 64%, at ₹399 about 70%.
- **Payouts:**
  - With the account country set to **India** it's **PayPal only** ("new bank payout accounts cannot be set up in India"),
    with a $100 minimum.
  - Raj chose country **Netherlands**: the **Bank account (IBAN)** option appears, still with a $100 minimum, paid weekly.
  - The Country select sits far down the Payments page. Changing it asks to confirm and clears saved payout details.
- **Cheaper India option for later:** Instamojo or Razorpay (about 2%, UPI) need an Indian phone and KYC in Raj's name.
  It could be added as a second "Pay with UPI" button.
- **Website wiring** (owned by the website session):
  - `BOOK.buy` holds the plain product URLs.
  - The site works out `launchOn` from the date, appends `/LAUNCH` until 16 Nov 00:00 IST, and shows
    ~~₹299~~ ₹199 and Both ~~₹399~~ ₹299 with "Launch offer · ends 15 Nov".
  - After that it drops the code and hides the banner by itself.
  - The FAQ says "PDF + EPUB in every purchase".

## Ads and launch posts
- All scripts live in `videos/book-ads/` (outside the book folder):
  - `ads.py`: wide, post and story banners
  - `carousel.py`: the 5-slide pre-launch carousel
  - `carousel_live.py`: the "OUT NOW / ₹199 till 15 Nov" version
  - `gumroad.py`: product images
  - `CAPTIONS.md`: captions and the log of every post link
- Carousel slides (1080×1350):
  1. Hook: "Python boring lagta hai? 😴 Ab seekho chai ke saath", cover, badge, Chotu, price
  2. The chai-shop story page
  3. "Real code. Real output." with the example page
  4. "Galtiyan bhi sikhati hain" with the mistakes page
  5. The CTA: price, link, "Save karo / dost ko bhejo"
  
  Slides use **real book pages** captured with headless Chrome at 2× (each page is about 1587 px tall).
- Flow: pre-launch teaser ("coming", free preview) → after the products are published and the site's Buy buttons are
  verified live, the "Now available" carousel on YouTube Community, Instagram, Facebook page and X.
- Raj also announced "coming soon on Amazon, Flipkart and other online stores". That's his plan, not an error.
- **One session posts book ads:** the 📢 Book ads & sales session (since 19 Oct 2026). Check the platforms for existing posts before posting.
- Posting gotchas (Claude in Chrome):
  - **X:** click **Post by the dialog's `[data-testid=tweetButton]`**. A coordinate miss once sent the post without its
    images, and another "Post" ref was the wrong button. Check `[data-testid=tweetPhoto]` count = 4 on the status page,
    then clear any media left in the home composer.
  - **YouTube Community:** upload images, wait about 8 s, type, then click Post. The first try often silently does nothing.
    Re-check the Posts tab before retrying, so there's no duplicate.
  - **Facebook page:** Photo/video file input → text → Next → Post (Boost stays off) → "Not now" on "Add a Call Now
    button". Verify in Content Library → **Published**. One silent failure happened; check Drafts before retrying.
  - **Instagram:** a Meta "Choose if we process your data for ads" consent screen can block it. That's Raj's choice, so
    never click it. Crop **Original** (4:5). Type the caption with `computer.type`, check the line count, Share, then
    verify `og:description` with curl.
  - The site's service worker can show a stale page: call `registration.update()` and reload before judging the live site.

### Ad sets, tracker and approvals (worked and approved by Raj, 19 Oct 2026)
- **New ads = word swaps on the approved designs.** `adset_nov.py` imports `ads.py` / `carousel.py` and only replaces
  text (kicker, price line, link line, slide hooks), the same way `carousel_live.py` does. Never a new layout. Output goes to
  `out/set/`, and a contact sheet is checked before anything else.
- **One ad set per push, reviewed as one page.** Make every platform's version (YT community 4:5, IG/FB carousel 4:5,
  Story 9:16, X 16:9 or 4 images), then publish ONE review page with the exact images, captions and IST times
  (`ads-tracker/build_review.py`, plus `book-ads/POSTS-NOV.md` as the posting sheet). Raj approves the set with "OK ad set".
- **Calendar per book:** launch week → mid-month push (chapter peek with real pages) → festival tie-in if one falls in the
  window → "3 din baaki" → "aaj last day". Don't repeat a feed post within ~3 days; use a Story instead.
- **Posting rules:** one platform at a time (~30 min apart), at least 3 h from that day's Shorts, full caption always,
  never re-upload, at most 5 book comments per platform per day. Stories with link stickers are Raj's (phone app only).
  Check dates with 📣 Campaigns so promos don't land on the same day.
- **Codes:** only the public launch code goes in ads, and only for the products it covers (LAUNCH = the Python with Chai
  books only; not the ₹149/₹199 sheets and packs, since ₹100 off leaves nothing after fees). No buy link in an ad until
  💳 Payments sends a live one; planned slugs are never posted.
- **Money products** always carry "Financial education, advice nahi" and never promise returns.
- **Mascot by product (Raj, 19 Oct 2026):** money products (money book, Family Money Planner, tracker) use **Gullak Bhai**,
  a clay piggy bank (kit: `C:\samjhowithraj\brand\mascots\gullak-bhai\`, used once Raj approves the design). Chotu stays on
  tech books and the AI prompts pack. Money ads swap the `chotu(...)` call for the Gullak Bhai kit; the layout stays the same.
- **Raj's view:** Raj can't read .md files. `ADS-TRACKER.md` is the data, and `ads-tracker/build_page.py` turns it into the
  "Book Ads" Artifact page (live / drafts / calendar / ended / ideas). Republish to the SAME URL after every change.
- **Posting days** run from one-time reminder tasks that follow `ads-tracker/POSTING-DAY.md` and ask Raj "Post now?" first.
- **Raj's list:** every approval, Raj-only step or change to review also goes as one line to the Content Planner
  (what · where Raj answers · review link), then "done: <what>".

## Training course (next product, same assets)
- Plan:
  - Turn each book chapter into one module: a 10–15 min lesson video (reuse the Shorts / tech-explainer templates),
    the chapter's teaser as a handout, a quiz (the chapter's practice tasks), and the assignment (the challenge).
  - Add 3 capstone projects: Ch 20 Chai Shop app, Ch 29 API + regex, Ch 30 expert capstone.
  - Add a certificate at the end.
- Tiers: book (₹199–399) → self-paced course (videos + book + quizzes) → live cohort / doubt sessions.
- Host on Graphy, TagMango or Teachable, or on the website's classroom tab with paid unlock links. Payments and
  accounts are Raj's to set up.

## Script backups
`scripts/` holds copies of the ad, carousel, Gumroad-image and EPUB builders (no book text). The working copies live in
`videos/book-ads/` and `videos/book-epub/`; copy them back from here if those folders are lost.

## Lessons from 19 Oct 2026 (Content Planner)
- **A book after every 20 Shorts** of a series: "AI Chatbot with Chai" Vol 1 (chatbot Parts 1–20; `vlog1/videos/ai-chatbot-book/`),
  "Paisa Samjho: Salary se Savings tak" (money Shorts 1–20; `financial planning/money-book/`), one per AI Jobs sector.
  Draft a chapter as soon as its Short script exists; build the full book after Part 20.
- **Money-book adaptation** of this pipeline (same look, Chotu): code examples become worked Verma-family rupee examples
  whose arithmetic the build's check step really verifies; "real error" becomes a real money mistake; every chapter ends
  with a worksheet + the matching paisasamjhoraj.com calculator; "Financial education, advice nahi" on the cover page and
  every chapter; every rate, tax or RBI/SEBI rule checked on a primary source with a date, listed in the back.
- **Small paid products:** templates (Google Sheet "Make a copy" link + .xlsx, formulas tested, "Illustrative" note per tab)
  and PDF packs. Price floor ₹149: at ₹99 Gumroad fees leave about ₹16 a sale (₹149 ≈ ₹60). Family Money Planner ₹199.
- **Codes:** LAUNCH (public, ₹100 off) is meant only for the 3 Python with Chai products; Raj limits it in Gumroad.
  Never put the private 10% code anywhere.
- **API keys for running examples:** never ask Raj to paste a key in chat. Use `C:\samjhowithraj\tools\save-anthropic-key.ps1`
  (hidden prompt, saves to the private `.anthropic_key` the runner reads), started in a Terminal tab; confirm only that
  the file exists. Sandboxed checks may not see it; check with a command outside the sandbox.
- **Track every PDF:** `python C:\samjhowithraj\tools\pdf_catalog.py` rebuilds the PDF Library page
  (https://claude.ai/artifact/Hks2tq4VEAJNeRMQCb1XT5). Add a PRODUCTS rule when a new book or pack is made or goes on sale.
- **Sales numbers:** read Gumroad → Sales (read only); its prices are in ₹ (the Products list shows $). Count real buyers
  only: leave out Raj's own test purchases and refunds. A Sunday task (gumroad-weekly-sales) writes
  `reports/pdf-sales.json` and republishes the PDF Library.
- **Listing text comes from the real file:** write the Gumroad description from the maker session's hand-over (tabs,
  formula counts, what's really inside), never ahead of the file. A draft written before the sheets existed promised a
  PDF how-to and progress bars that weren't there.
- **Google Sheets copy link:** Raj uploads the .xlsx to his Drive, saves it as a Google Sheet, shares it as Viewer, and
  ends the link with `/copy`. It goes only in the receipt message, so only buyers see it.
- **Free gifts stay off Gumroad:** the Python with Chai cheat sheets are a free gift for email subscribers (status
  "subscriber gift" in the PDF Library), not part of the paid download.
- **Filling Gumroad in Chrome (20 Oct):** the Gumroad tab only responds while Chrome is the front window, so ask Raj
  to keep it in front and not switch away. Typing long text key by key freezes the tab: put the description in with
  one `document.execCommand('insertHTML', …)` on the focused editor, and set short fields with form_input. Currency
  option value is `inr`. Cover = "Upload images or videos" → "Computer files" file input; thumbnail has its own file
  input; product files use the Content tab's file input (an .xlsx may sit at 0% for ~20 s, then finish). Save each tab,
  reload and read the values back. Create products as drafts; Raj limits codes and clicks Publish.
- **Hand-offs:** files + description + price → 💳 Payments & Gumroad (Raj publishes); teasers → the website session; ads →
  📢 Book ads & sales. Every review or Raj step also goes as one line to the Content Planner.

## Lessons from 19 Oct 2026 (📗 Money Plan books: build gotchas)
- **A space in the folder path breaks the fonts without any error.** The CSS `url(file:///C:/.../financial planning/...)` is
  unquoted, so a path with a space fails and every heading falls back to serif. Encode it: `.replace(" ", "%20")` for the
  fonts in `doc()`, for `book.py` image paths and for cover pages. After the first build, look at a page to check Caveat headings.
- **Money check step (money-book/build.py):**
  - Examples, mistakes and answers are "hisaab" dicts: `steps=[(name, label, expr[, unit])]`, `out` templates with `{name}`, and an `expect`.
  - `check` fails on:
    - a wrong `expect`
    - any ₹ amount in the text that no hisaab produces (listed in `given` for the rare plain inputs)
    - rule words (RBI, SEBI, repo, GST, tax…) in a chapter with no `facts`
    - a `**` (compounding) step without `projection=True`
    - a missing worksheet or tool
  - Match amounts with `₹\d+(?:,\d+)*`. `₹[\d,]+` grabs the comma after "₹39,000," and fails.
  - Test the checker by breaking one total and one amount on purpose.
- **Money chapter = 11 pages.** It's the 10 Python-book page kinds (syntax → "rule") plus a worksheet page (blank table +
  calculator link). Teasers still thumb pages 3–10.
- **Looking at pages:** a headless-Chrome `--screenshot` of a CSS grid of pages came out blank. Open the PDF in the browser
  pane instead (the first screenshot may still be loading; take another).
- **.xlsx templates on Windows:**
  - The xlsx skill's `recalc.py` fails here (`socket.AF_UNIX`). Instead, recalculate a copy with
    `soffice --headless --calc --convert-to xlsx --outdir test out/*.xlsx`, then scan it with openpyxl `data_only=True` for `#` errors
    and hand-check the key cells.
  - Don't put `LibreOffice/program` FIRST on PATH: its own python.exe shadows the real one (no openpyxl). Append it, or
    call `C:\Python314\python.exe`.
  - Deliver the openpyxl file, not the LibreOffice copy, with `wb.calculation.fullCalcOnLoad = True`.
  - Status formulas on blank tabs must handle empty input (say "Start with your income" instead of a false "OK").
- **Template covers:** reuse the book's COVER_CSS gradient, Baloo 2, Chotu and a small "sheet" card with the example
  numbers. Make 1280×720 + 600×600 (the square one needs its own layout, or it looks empty). Generator scripts stay in the
  private `money-book/templates/`, since they would give the product away.
- **Two sessions editing one skill at once lose each other's text.** Append, then re-read with grep and confirm the
  section is there after the push.

## Lessons from 19 Oct 2026 (📘 Tech books: "50 AI Prompts" pack)
- **Prompt packs with real AI replies** (`vlog1/videos/ai-prompts-pdf/`, private `*` .gitignore):
  - `prompts_data.py` holds every prompt as an (en, hi) pair. `[brackets]` mark what the reader changes.
  - `run_prompts.py` sends each prompt exactly as printed (brackets removed, no system prompt) and saves the replies in
    `outputs.json`. It skips the ones already saved, and `--redo N` reruns one.
  - `make_pdf.py` refuses to build if a reply is missing (`draft` = layout only, never sell).
  - The Hinglish prompt is run separately, so the Hinglish book shows a real Hinglish reply.
  - Cost: 100 calls on `claude-haiku-5-5` with effort `low` is cents. Haiku has no server-side `fallbacks`, so leave that
    parameter out.
- **Never trim a real reply to fit.** If the overflow report lists a page, give that reply the next page to itself
  (`SPLIT` set: prompt + tip + "reply on next page", then the reply), and add the extra pages to the contents numbers.
- **Render the reply's markdown.** Raw output in a mono `<pre>` showed `|` pipes, backticks and tiny text. Convert
  code fences to code blocks, `|` rows to a table, and `**`, `*` and backticks to bold, italic and code. Keep the words
  exactly as the AI wrote them.
- **Heredoc gotcha, part 2:** `r"\1"` inside a bash heredoc'd Python edit was saved as the control character chr(1), so
  `<b>\1</b>` printed nothing. Write regex edits with the Write/Edit tool, then check `ast.parse` and `s.count(chr(1)) == 0`.
- **Key steps: trust the disk, not the report.** Five times a "saved"/"ran it" report didn't match the disk. Check the
  file (outside the sandbox) before doing anything. Never read a terminal where a plain `Read-Host` was used, because it
  shows the key. Use the hidden-prompt `save-anthropic-key.ps1`.
- **Page screenshots that work:** put the chosen pages (stacked, not a grid) in one HTML file via `B.doc`, then run Chrome
  `--screenshot --window-size=559,<794 × pages>`.
- **Selling a pack:** files + description + price → 💳 Payments & Gumroad. Raj asked (19 Oct) that once a PDF is live,
  📢 Book ads & sales makes the ad and posts it on all his platforms (book and product ads are theirs, not 📣 Campaigns'), so send them the request at hand-off time too.

## Lessons from 20 Oct 2026 (📗 Money Plan books: Gullak Bhai)
- **Money content has its own mascot: Gullak Bhai** (Raj OK, 20 Oct 2026). He's a clay gullak with a coin slot on his head who
  fills up as savings grow. Catchphrase "Chhota-chhota daalo, bada-bada banao!". Chotu stays on tech/Python only.
- **Shared kit, one source:** `C:\samjhowithraj\brand\mascots\gullak-bhai\`
  - `gullak.py`: `gullak(pose, cls)` with 8 poses (happy, think, warn, party, point, worried, full, read)
  - `svg/`, plus transparent `png/512` and `png/256`
  - README with colours and usage
  - `sheet.py` builds the character sheet (Artifact https://claude.ai/artifact/Ey8j3HGmNybjKr32QZdpLq)
  - The money book's `mascot.py` imports the kit, so a fix to the kit reaches the book on the next build.
- **How a new mascot was made and approved:**
  1. Draw it in code in Chotu's house style: 6px ink outline, flat fills, round hands, the same eyes and cheeks.
  2. Use a square viewBox (here -2 -8 212 212) so PNGs export at exact 512/256.
  3. Export with headless Chrome `--default-background-color=00000000` for transparent PNGs. Check the PNG is colour type 6 (RGBA).
  4. Check a contact sheet, fix what reads wrong (a cobweb read as a feather; the belly band needed a clipPath), then show Raj ONE sheet page.
- **Swapping a mascot without touching the layout:** keep the CSS classes (`chotu`, `withchotu`) and the page kinds. Only map
  `PAGE_POSE` to the new poses (mistakes → warn, practice → full, ex34 → party). Change the SAYS lines and the "tip" label.
  Rebuild and confirm 0 overflow. Re-make the product covers and tell Payments to replace the images in its Gumroad drafts.
- **Raj's photo goes on every book and paid product** (Raj, 20 Oct 2026: "put my image on all the book like how it is for tech").
  - **Book:** the cover keeps the tech layout (`#raj` half-body cutout bottom-right, mascot bottom-left, logo top-left). The title
    page and "About the author" use the cutout too, and the back cover uses the round logo.
  - **Product covers:** the cutout goes bottom-right with the mascot beside it. The square thumbnail needs its own sizes so the
    photo doesn't cover the sheet card or the disclaimer line.
- **Money book.py** (adapted 20 Oct 2026):
  - 11-page chapters, so page numbers are `(n-1)*NPAGES + k + 1`
  - levels 1–7 / 8–14 / 15–20
  - a "Sources and checks" page built from every chapter's `facts`
  - the disclaimer and "Verma family is fictional" in the copyright page, the cover chip and every footer
  - outputs `paisa-samjho-{en,hi}-full.pdf` + `cover-{en,hi}.png`

## Lessons from 20 Oct 2026 (📙 Exam puzzle book: "Reasoning Samjho")
- **Puzzle-book adaptation** (`vlog1/videos/exam-puzzle-book/`, private `*` .gitignore): same page frame, fonts, auto-fit and
  Chrome PDF as python-chai-book. Only `topic_pages` changes: title · story · method + rule · "Draw it like this" · 4 worked
  puzzles (easy → hard) · 3 traps · 2 practice pages · boss puzzle + cheat sheet · worked answers. About 16 pages a chapter.
- **The check step = a brute-force solver.** `solver.py` tries every arrangement (rows, round tables, two facing rows, mixed
  facing). `build.py check` fails unless each puzzle has exactly ONE arrangement and every printed option equals the solver's.
  Tune clues against the solver (0 solutions → loosen, 2+ → add one clue) before writing the steps.
- **Draw diagrams from the solver's answer** (`diagram.py`), never by hand, so a picture can't disagree with the answer.
- **Left/right traps:** if everyone faces the same way, mirroring keeps every relative answer the same, so a "left/right"
  trap only bites with mixed facings. Use mixed facings (or a direction-of-counting question) for those traps.
- **Mascot by product:** exam/puzzle content uses **Dimaag Dada** (kit `videos/exam-puzzles/mascot.py`, loaded by path with
  importlib because the book's own file is also called mascot.py). Raj stays the author and the face on the cover.
- **One puzzle bank for book + Shorts:** `python build.py bank` → `bank/bank.json` + `BANK.md`. Puzzle IDs are chapter.number;
  each Short names its puzzle ID, and the book logs it.
- **Looking at pages without PIL/pdftoppm:** split the chapter HTML into groups of 4 `<section>` pages and Chrome `--screenshot`
  each at 559 × (794 × 4).
- Book headings follow the brand pattern ("Paisa Samjho: Salary se Savings tak" → "Reasoning Samjho: Puzzle se Selection tak").
