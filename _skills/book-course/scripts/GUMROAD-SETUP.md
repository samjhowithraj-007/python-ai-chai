# Gumroad setup: Python with Chai

## Step 1: create the account (Raj does this; about 5 minutes)
1. Open **https://gumroad.com** → **Start selling** (or "Sign up").
2. Sign up with the email you want sales and payout emails sent to, plus a password you choose.
   Google sign-in is also fine. No Indian phone number is needed.
3. Confirm the email Gumroad sends you.
4. Choose your username, for example **samjhowithraj**. Your store becomes `samjhowithraj.gumroad.com`.
5. **Settings → Payments (Payouts):** country **India**, then add your bank account (an NRO account if you're an NRI)
   and your PAN / tax details when it asks. Do this before the first sale, so payouts aren't held back.
   Check the minimum payout and schedule shown there.
6. **Settings → Profile:** name "Raj · Tech Samjho Raj", logo `img/raj-mark.png` from the website folder, bio:
   "AI expert · Azure & Claude certified AI architect · 20 years in tech. Learn Python and AI in simple Hinglish."

Then tell me "account done". I'll help fill in the products in Chrome, but you'll need to be there to upload the PDFs
and click Publish.

## Step 2: products (copy and paste)
Images are in `C:\samjhowithraj\vlog1\videos\book-ads\out\gumroad\`. Upload **cover** as the Cover and **thumb** as the
Thumbnail. Book files are in `C:\samjhowithraj\vlog1\videos\python-chai-book\out\`.

Pricing: set the currency to **₹ INR** in the product's price field. Each product's price is the normal price.
The launch price comes from an **offer code** (Step 3), so the website can show ~~₹299~~ ₹199.

### Product A: English edition
- **Name:** Python with Chai: From Basic to Expert (English edition)
- **Price:** ₹299
- **File:** python-with-chai-en-full.pdf
- **URL slug:** python-with-chai-en
- **Images:** en-cover.png, en-thumb.png
- **Summary (the one-line "summary" field, if shown):** 30 illustrated chapters, from print() to asyncio. Every output really run.

### Product B: Hinglish edition
- **Name:** Python with Chai: Basic se Expert tak (Hinglish edition)
- **Price:** ₹299
- **File:** python-with-chai-hi-full.pdf
- **URL slug:** python-with-chai-hinglish
- **Images:** hi-cover.png, hi-thumb.png

### Product C: Both editions
- **Name:** Python with Chai: English + Hinglish (both editions)
- **Price:** ₹399
- **Files:** both PDFs
- **URL slug:** python-with-chai-both
- **Images:** both-cover.png, both-thumb.png

### Description (paste into all three; change the first line for B and C)
```
Learn Python the chai way: one cup, one chapter. ☕

Python with Chai takes you from your very first print() to decorators, asyncio and a real capstone project, in 30 illustrated chapters with Chotu the chai-cup buddy on every page.

WHAT'S INSIDE
• 30 chapters in 3 levels: Basic → Intermediate → Expert
• 336 illustrated A5 pages (PDF: reads well on phone, tablet or laptop, and prints nicely)
• Every chapter starts with a chai-shop story, then the idea, the syntax and 4 examples
• 120+ examples, and every output in the book was produced by really running the code
• "What if…?" boxes, Chotu's tips, and line-by-line walkthroughs
• Common mistakes with the real error messages, and how to fix them
• Practice tasks + a challenge per chapter, answers at the back
• Cheat sheet at the end of every chapter, full contents and index

WHO IT'S FOR
Complete beginners (Chapter 1 starts with installing Python), students, and anyone who started Python and got stuck. The expert chapters (decorators, context managers, type hints, pytest, threads, asyncio, APIs, performance) take you further when you're ready.

ABOUT THE AUTHOR
Raj is an AI expert, an Azure & Claude certified AI architect, coder and engineer with 20 years in tech, working at a tech company in Amsterdam, the Netherlands. He teaches Python and AI in simple Hinglish on YouTube (@SamjhowithRaj) and at techsamjhoraj.com.

Free preview chapters: https://www.techsamjhoraj.com/#book

Python is a trademark of the Python Software Foundation. This book is not affiliated with or endorsed by it.
```
- First line for B: `Python seekho chai ke saath: ek cup, ek chapter. ☕ (Same book, same code, explained in Hinglish.)`
- First line for C: `Get both editions: read in English, revise in Hinglish (or share with family). ☕`

### Other product settings
- **Receipt / thank-you message:** "Thank you! ☕ Your book is attached. Start with Chapter 1, type every example yourself, and tag @samjhowithraj when you finish your first chapter."
- Leave "Allow customers to pay what they want" off. Turn **Generate license keys** off. Turn "Limit product sales" off.
- Watermarking is optional (Gumroad can stamp the buyer's email on PDF pages, which discourages sharing). It's fine to turn it on.

## Step 3: launch offer code
**Checkout → Discounts (Offer codes) → New:**
- Code **LAUNCH**, ₹100 off, applies to products A and B
- Code **LAUNCHBOTH** is optional: the bundle at ₹399 is already the deal

A link with the code built in is `https://samjhowithraj.gumroad.com/l/python-with-chai-en/LAUNCH`, which shows ₹199 at checkout.

## Step 4: send these 3 links (the website gets them in BOOK.buy)
- en: `https://<username>.gumroad.com/l/python-with-chai-en/LAUNCH`
- hi: `https://<username>.gumroad.com/l/python-with-chai-hinglish/LAUNCH`
- both: `https://<username>.gumroad.com/l/python-with-chai-both`

Before launch: buy one copy yourself with the code (or use Gumroad's "test purchase" if it offers one) and check that
the PDF downloads.
