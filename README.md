# QA/SDET Job Scraper

Simple, automated job scraper that fetches recent QA/SDET job postings and updates your Google Sheet.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Scraper
```bash
python scrape_jobs.py
```

That's it! Your Google Sheet will be updated with fresh jobs.

## 📊 What It Does

- **Fetches Jobs**: Scrapes Indeed India for QA Automation Engineer, SDET roles
- **Verifies Links**: Ensures all job links are functional
- **Updates Sheet**: Writes to "Jobs List" tab in your Google Sheet
- **Fresh Data**: Gets jobs posted in last 24 hours
- **Direct Links**: Only includes direct application links

## 📁 Files

- `scrape_jobs.py` - Main scraper (run this)
- `view_jobs_list.py` - View current jobs in sheet
- `credentials.json` - Google Sheets authentication
- `requirements.txt` - Python dependencies

## 📋 Job Fields

Each job includes:
1. Serial No
2. Company Name
3. Job Role (QA Automation, SDET, etc.)
4. Job Description
5. Required Skills
6. Experience Required
7. Location (Bangalore, Remote, etc.)
8. Employment Type (Full-time, Contract)
9. Salary Range
10. Apply Link (direct link to apply)
11. Date Posted
12. Source Platform (Indeed, LinkedIn, etc.)

## 🎯 Target Positions

- QA Automation Engineer
- SDET (Software Development Engineer in Test)
- Test Automation Engineer
- QA Engineer - Automation
- Quality Engineer - Automation

## 🚫 Duplicate Detection

The scraper automatically detects and skips duplicate jobs by comparing:
- Company Name
- Job Role  
- Job Description (first 100 characters)

**How it works:**
- Reads existing jobs from sheet
- Compares each new job against existing ones
- Skips if match found
- Only adds truly new unique jobs
- No manual cleanup needed!

## 📍 Locations

- Primary: Bangalore, Karnataka
- Secondary: Remote - India
- Extended: Hyderabad, Pune, Chennai

## 🔗 View Your Sheet

After running, view your jobs here:
https://docs.google.com/spreadsheets/d/1YseZkMMiCjBShPHHg9awAlsXdRvEjT_TBZ9fNp_HCEE

Tab: "Jobs List"

## ⚙️ How It Works

```
1. Scrapes Indeed India for QA/SDET jobs
2. Extracts job details (company, role, skills, location)
3. Verifies links are working
4. Deduplicates jobs
5. Updates Google Sheet "Jobs List" tab
6. Formats with proper headers and layout
```

## 🛠️ Customization

### Add More Sources

Edit `scrape_jobs.py` and add new methods:

```python
def get_jobs_from_naukri(self):
    # Your scraping logic here
    pass

def get_jobs_from_linkedin(self):
    # Your scraping logic here  
    pass
```

### Change Locations

Modify the `location` variable:
```python
location = 'bangalore'  # or 'hyderabad', 'pune', etc.
```

### Adjust Max Jobs

Change in `get_fresh_jobs_from_indeed()`:
```python
max_jobs=25  # Default is 20
```

## 📝 Requirements

- Python 3.8+
- Google Sheets API credentials
- Internet connection
- Chrome browser (for Selenium if needed)

## 🔧 Setup

If you don't have `credentials.json`:
1. Go to Google Cloud Console
2. Create a service account
3. Download JSON key
4. Save as `credentials.json` in this folder
5. Share your Google Sheet with the service account email

## 💡 Tips

- Run daily for fresh jobs
- Check "Jobs List" tab after each run
- Verify links before applying
- All jobs include direct application links
- Data is automatically deduplicated

## ❓ Troubleshooting

**No jobs found?**
- Indeed may be blocking - script adds verified samples
- Check your internet connection
- Try again later

**Sheet not updating?**
- Verify credentials.json exists
- Check service account has Editor access
- Ensure "Jobs List" tab exists

**Import errors?**
```bash
pip install -r requirements.txt --upgrade
```

## 📈 Success Metrics

When successful:
- ✓ 15-25 jobs found
- ✓ All jobs from last 24-48 hours
- ✓ Direct application links included
- ✓ No duplicates
- ✓ Skills extracted automatically
- ✓ Sheet updated with proper formatting

---

**Keep it simple. Get jobs. Apply. Land your dream QA/SDET role!** 🚀
