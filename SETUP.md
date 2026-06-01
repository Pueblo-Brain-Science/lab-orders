# Lab Chemical Orders — Setup Guide

## Overview
- **Frontend:** GitHub Pages (free, your lab's URL)
- **Backend/Database:** Google Apps Script + Google Sheets (free, no server)

---

## Step 1 — Create the Google Sheet & Apps Script

1. Go to [sheets.google.com](https://sheets.google.com) and create a new blank spreadsheet.
   - Name it something like **"Lab Chemical Orders"**
2. Copy the Sheet URL from your browser — you'll need it later.
3. In the Sheet, go to **Extensions → Apps Script**
4. Delete the default code in the editor.
5. Open the file `Code.gs` from this folder and **paste the entire contents** into the Apps Script editor.
6. Click **Save** (floppy disk icon), then click **Deploy → New deployment**
7. Click the gear icon next to "Select type" → choose **Web app**
8. Fill in:
   - Description: `Lab Orders API`
   - Execute as: **Me**
   - Who has access: **Anyone** *(so lab members can submit without logging in)*
9. Click **Deploy** → Authorize when prompted → Copy the **Web App URL**

---

## Step 2 — Configure index.html

Open `index.html` and find these two lines near the bottom:

```js
var APPS_SCRIPT_URL = "";
var SHEET_URL = "";
```

Replace them with your actual URLs:

```js
var APPS_SCRIPT_URL = "https://script.google.com/macros/s/YOUR_ID_HERE/exec";
var SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit";
```

Save the file.

---

## Step 3 — Publish to GitHub Pages

1. Create a new **public** repository on [github.com](https://github.com)
   - Name it something like `lab-orders` or add it to your existing lab repo
2. Upload these files to the repo:
   - `index.html`
   - `README.md` (optional)
3. Go to the repo **Settings → Pages**
4. Under "Branch" select `main` (or `master`) and folder `/root`, then click **Save**
5. Your site will be live at:
   `https://YOUR-USERNAME.github.io/lab-orders/`

---

## Step 4 — Add to your lab website

Add a link wherever you want on your lab site:

```html
<a href="https://YOUR-USERNAME.github.io/lab-orders/">Chemical Order Requests</a>
```

Or embed it in an iframe:

```html
<iframe src="https://YOUR-USERNAME.github.io/lab-orders/" width="100%" height="800" frameborder="0"></iframe>
```

---

## How it works day-to-day

| Who | What they do |
|-----|-------------|
| Lab members | Open the site, fill in the form, click Submit |
| Lab manager | Open Google Sheet or the tracker table, update Status column |
| Anyone | Filter/search the tracker on the website |

The Google Sheet is always the source of truth — you can sort, filter, add notes, or share it with collaborators directly in Sheets.
