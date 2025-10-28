"""
View Jobs in Google Sheet
Simple script to check current jobs
"""

import gspread
from google.oauth2.service_account import Credentials

CREDENTIALS_FILE = "credentials.json"
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def main():
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║              CURRENT JOB LISTINGS                               ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key('1YseZkMMiCjBShPHHg9awAlsXdRvEjT_TBZ9fNp_HCEE')
        worksheet = spreadsheet.worksheet('Jobs List')
        
        all_values = worksheet.get_all_values()
        
        if len(all_values) < 4:
            print("❌ No jobs found in sheet!")
            return
        
        print(f"📅 {all_values[0][0]}")
        print(f"📊 Total Jobs: {len(all_values) - 3}\n")
        print("="*90 + "\n")
        
        # Show jobs
        for idx, row in enumerate(all_values[3:], start=4):
            if not row[0]:
                break
            
            print(f"Job #{idx-3}")
            print(f"  Company: {row[1]}")
            print(f"  Role: {row[2]}")
            print(f"  Skills: {row[4]}")
            print(f"  Location: {row[6]}")
            print(f"  Posted: {row[10]}")
            if len(row) > 12 and row[12]:
                print(f"  HR Contact: {row[12]}")
            print(f"  Apply: {row[9]}")
            print("-" * 90)
        
        print(f"\n✅ Found {len([r for r in all_values[3:] if r[0]])} jobs")
        print(f"\n🔗 View full sheet:")
        print(f"   https://docs.google.com/spreadsheets/d/1YseZkMMiCjBShPHHg9awAlsXdRvEjT_TBZ9fNp_HCEE")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()

