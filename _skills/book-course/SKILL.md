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
  - **RAJTECH84**: 10% off, PRIVATE (only for people Raj chooses). Never put it on the site, in ads or captions.
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
- **One session posts book ads** (this payments/ads session). Check the platforms for existing posts before posting.
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
