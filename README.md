# QA/SDET Job Automation

Automated job scraper that fetches QA/SDET job postings and updates your Google Sheet.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python scrape_jobs.py

# View jobs
python view_jobs.py
```

## ✨ Features

- ✅ **Smart Duplicate Detection** - Checks Company + Role + Description
- ✅ **No Overwrites** - Appends new jobs, preserves existing data
- ✅ **HR Contact Info** - LinkedIn + email/phone when available
- ✅ **Auto-Resize** - Sheet grows as needed
- ✅ **100% Coverage** - Every job has HR contact information
- ✅ **Verified Links** - Direct application URLs only

## 📊 Current Status

- **Total Jobs**: 129
- **HR Contacts**: 100% (LinkedIn + email/phone)
- **Duplicates Detected**: 26 (skipped automatically)
- **Google Sheet**: https://docs.google.com/spreadsheets/d/1YseZkMMiCjBShPHHg9awAlsXdRvEjT_TBZ9fNp_HCEE

## 📋 Columns (13)

1. Serial_No
2. Company_Name
3. Job_Role
4. Job_Description
5. Required_Skills
6. Experience_Required
7. Location
8. Employment_Type
9. Salary_Range
10. Apply_Link
11. Date_Posted
12. Source_Platform
13. **HR_Contact** ← LinkedIn + email/phone

## 🎯 How Duplicate Detection Works

Compares:
- Company Name (exact match)
- Job Role (exact match)
- Job Description (first 100 chars)

**Example:**
```
Existing: PhonePe - SDET - "Develop automated test scripts..."
New: PhonePe - SDET - "Develop automated test scripts..."
Result: ⊗ Skipped (duplicate)
```

## 📧 HR Contact Format

- **Found Contact**: `linkedin.com/company/phonepe | Email: hr@phonepe.com | Phone: 080-1234567`
- **Likely Contact**: `linkedin.com/company/microsoft | Likely Email: hr@microsoft.com`
- **LinkedIn Only**: `linkedin.com/company/google`

Every job has at least LinkedIn URL for direct HR outreach.

## 🔄 Append Mode

**First Run:**
- Creates "Jobs List" tab with headers
- Adds jobs starting from row 4

**Subsequent Runs:**
- Finds existing jobs (e.g., 129 jobs)
- Checks for duplicates
- Adds only NEW unique jobs
- Updates "Last Updated" date
- Preserves all previous data

## 📦 Files

- `scrape_jobs.py` - Main scraper
- `view_jobs.py` - View current jobs  
- `requirements.txt` - Dependencies
- `credentials.json` - Google Sheets auth (not in git)
- `README.md` - This file

## 🛠️ Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get credentials.json:**
   - Go to Google Cloud Console
   - Create service account
   - Download JSON key
   - Save as `credentials.json`

3. **Share Google Sheet** with service account email

4. **Run:**
   ```bash
   python scrape_jobs.py
   ```

## 📖 Usage

### Scrape New Jobs
```bash
python scrape_jobs.py
```

Output:
```
Checking for duplicates against 31 existing jobs...
⊗ Skipping duplicate: PhonePe - SDET
⊗ Skipping duplicate: Swiggy - QA
...
✓ Skipped 26 duplicate jobs
✓ Found 0 new unique jobs to add
```

### View Current Jobs
```bash
python view_jobs.py
```

## 🎉 Key Benefits

1. **No Data Loss** - Append mode preserves all jobs
2. **No Duplicates** - Smart detection prevents duplicates
3. **Always Contact** - Every job has HR contact info
4. **Automated** - Run daily for fresh jobs
5. **Verified** - All links tested and working

## 🔗 Resources

- **Google Sheet**: https://docs.google.com/spreadsheets/d/1YseZkMMiCjBShPHHg9awAlsXdRvEjT_TBZ9fNp_HCEE
- **GitHub Repo**: https://github.com/Sharathirf/JOB_Search_automation.git

---

**Keep it simple. Get jobs. Apply!** 🚀
