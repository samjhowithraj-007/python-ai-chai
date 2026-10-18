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
- Pricing (Indian market, 300-page illustrated e-book): ₹299 list, ₹199 launch, ₹399 for both editions.

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
  - Ads live OUTSIDE the book folder: `videos/book-ads/ads.py` (reads the book's fonts and cover only) gives
    `book-ads/out/book-ad-{wide,post,story}.jpg` + CAPTIONS.md. Check the wide one by eye before using it as the
    site's `media/book-promo.jpg`.
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
- Payments:
  - **Raj creates the seller account himself** (Gumroad, Instamojo or Razorpay Payment Pages, with KYC and bank
    details). Claude never does this.
  - Raj uploads the full PDFs there and sends Claude the product links. Claude pastes them into `BOOK.buy` and
    then makes the ad post.
- Legal: it's his own original text and code, so selling is fine. Fonts are OFL (licence files are in `fonts/`).
  Add a "Python is a PSF trademark, not affiliated" line. Indian GST applies above the threshold, and the platform
  handles invoices.
- Launch ad: post the banner and a short caption to YouTube (Community), Instagram, Facebook and X, linking to
  techsamjhoraj.com/#book. After Meta flags, post to Meta slowly, or let Raj post there by hand.

## Training course (next product, same assets)
- Plan:
  - Turn each book chapter into one module: a 10–15 min lesson video (reuse the Shorts / tech-explainer templates),
    the chapter's teaser as a handout, a quiz (the chapter's practice tasks), and the assignment (the challenge).
  - Add 3 capstone projects: Ch 20 Chai Shop app, Ch 29 API + regex, Ch 30 expert capstone.
  - Add a certificate at the end.
- Tiers: book (₹199–399) → self-paced course (videos + book + quizzes) → live cohort / doubt sessions.
- Host on Graphy, TagMango or Teachable, or on the website's classroom tab with paid unlock links. Payments and
  accounts are Raj's to set up.
