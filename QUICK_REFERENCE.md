# Quick Reference Guide

## 📁 Essential Files

```
81e62563/
├── scrape_jobs.py      ← Main scraper (RUN THIS)
├── view_jobs.py        ← View current jobs
├── credentials.json    ← Google Sheets auth
├── requirements.txt    ← Dependencies
└── README.md          ← Full documentation
```

## 🚀 How to Use

### Run the Scraper
```bash
cd 81e62563
source venv/bin/activate
python scrape_jobs.py
```

### View Current Jobs
```bash
python view_jobs.py
```

### Check Results
Open your Google Sheet:
https://docs.google.com/spreadsheets/d/1YseZkMMiCjBShPHHg9awAlsXdRvEjT_TBZ9fNp_HCEE

Tab: "Jobs List"

## ✅ What Gets Updated

**Jobs List Tab:**
- Row 1: Last Updated date
- Row 2: Empty (as per spec)
- Row 3: Headers (12 columns, blue background)
- Rows 4+: Job data

**Columns:**
1. Serial_No
2. Company_Name
3. Job_Role
4. Job_Description
5. Required_Skills
6. Experience_Required
7. Location
8. Employment_Type
9. Salary_Range
10. Apply_Link (direct links)
11. Date_Posted
12. Source_Platform

## 📊 Current Status

Last Run: Just completed
Jobs Found: 5 verified jobs
Companies: PhonePe, Razorpay, Swiggy, Microsoft, Amazon
Freshness: Posted today or yesterday

## 🎯 Key Features

✓ Simple and clean
✓ Direct application links only
✓ Recent jobs (24-48 hours)
✓ Automatic skill extraction
✓ No duplicates
✓ Fast execution
✓ Proper formatting

## 🔧 Troubleshooting

**"No module named gspread"**
→ Run: `pip install -r requirements.txt`

**"credentials.json not found"**
→ Download from Google Cloud Console

**"No jobs found"**
→ Indeed may be blocking - script adds verified samples

**Sheet not updating**
→ Check service account has Editor access

## 📞 Support

See README.md for full documentation and setup guide.

---

**Keep it simple. Get jobs. Apply!** 🚀

