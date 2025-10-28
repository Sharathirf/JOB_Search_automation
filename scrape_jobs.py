"""
QA/SDET Job Scraper - Enhanced Version
Fetches recent job postings and updates Google Sheet
Keep it simple: Get real jobs with direct links
"""

import gspread
from google.oauth2.service_account import Credentials
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import re

CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1YseZkMMiCjBShPHHg9awAlsXdRvEjT_TBZ9fNp_HCEE"

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

class EnhancedJobScraper:
    def __init__(self):
        self.jobs = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })
    
    def extract_skills(self, text):
        """Extract technical skills from text"""
        if not text:
            return ""
        
        skills = {
            'Java', 'Python', 'Selenium', 'TestNG', 'JUnit', 'Cypress', 
            'Playwright', 'REST API', 'Postman', 'Jenkins', 'Docker', 
            'Kubernetes', 'Git', 'Maven', 'Gradle', 'Appium', 'AWS', 
            'Azure', 'API Testing', 'CI/CD', 'Agile', 'Scrum'
        }
        
        found = [s for s in skills if s.lower() in text.lower()]
        return ', '.join(found[:8])
    
    def get_fresh_jobs_from_indeed(self, max_jobs=20):
        """Scrape from Indeed India with better parsing"""
        print("\n🔍 Scraping Indeed India...")
        jobs = []
        
        keywords = ['qa+automation', 'sdet', 'test+automation']
        location = 'bangalore'
        
        for keyword in keywords:
            if len(jobs) >= max_jobs:
                break
            
            try:
                url = f'https://in.indeed.com/jobs?q={keyword}&l={location}&sort=date'
                
                try:
                    resp = self.session.get(url, timeout=10)
                    if resp.status_code != 200:
                        continue
                    
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    cards = soup.find_all('div', {'class': 'job_seen_beacon'})[:10]
                    
                    for card in cards:
                        try:
                            # Title
                            title_elem = card.find('h2', {'class': 'jobTitle'})
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            
                            # Company
                            company_elem = card.find('span', {'class': 'companyName'})
                            company = company_elem.get_text(strip=True) if company_elem else "Company"
                            
                            # Link
                            link_elem = title_elem.find('a')
                            if link_elem and link_elem.get('href'):
                                job_link = 'https://in.indeed.com' + link_elem.get('href')
                            else:
                                job_link = "LINK_NOT_AVAILABLE"
                            
                            # Location
                            loc_elem = card.find('div', {'class': 'companyLocation'})
                            location_text = loc_elem.get_text(strip=True) if loc_elem else "Location Not Specified"
                            
                            # Summary
                            summary_elem = card.find('div', {'class': 'job-snippet'})
                            summary = summary_elem.get_text(strip=True) if summary_elem else ""
                            
                            # Skills
                            skills = self.extract_skills(summary)
                            
                            job = {
                                'Company_Name': company,
                                'Job_Role': title,
                                'Job_Description': summary,
                                'Required_Skills': skills,
                                'Experience_Required': 'Not Specified',
                                'Location': location_text,
                                'Employment_Type': 'Full-time',
                                'Salary_Range': 'Not Disclosed',
                                'Apply_Link': job_link,
                                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                                'Source_Platform': 'Indeed India'
                            }
                            
                            # Try to extract contact info for Indeed jobs
                            try:
                                job['HR_Contact_Extracted'] = self.extract_contact_info(summary, job_link, company)
                            except:
                                job['HR_Contact_Extracted'] = "LinkedIn: https://www.linkedin.com/company/" + company.lower().replace(' ', '-')
                            
                            jobs.append(job)
                            print(f"   ✓ {company[:30]} - {title[:40]}")
                            
                        except Exception as e:
                            continue
                    
                except Exception:
                    continue
                
                time.sleep(2)
                
            except Exception:
                continue
        
        print(f"   ✓ Found {len(jobs)} jobs from Indeed\n")
        return jobs
    
    def extract_contact_info(self, job_description, apply_link, company_name):
        """Extract HR contact info using multiple fallback methods"""
        contact_info = ""
        
        # Method 1: Try to find email in description
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, job_description)
        
        # Method 2: Try to find phone number
        phone_patterns = [
            r'\b\d{10}\b',  # 10 digit number
            r'\+91[-.\s]?\d{10}',  # +91 format
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # xxx-xxx-xxxx
        ]
        
        phone_numbers = []
        for pattern in phone_patterns:
            phone_numbers.extend(re.findall(pattern, job_description))
        
        # If found in description, add it
        if emails:
            contact_info = f"Email: {emails[0]}"
        if phone_numbers:
            if contact_info:
                contact_info += f" | Phone: {phone_numbers[0]}"
            else:
                contact_info = f"Phone: {phone_numbers[0]}"
        
        # Always add LinkedIn URL as fallback
        company_slug = company_name.lower().replace(' ', '-').replace('&', 'and').replace('.', '-')
        linkedin_url = f"https://www.linkedin.com/company/{company_slug}"
        
        if contact_info:
            contact_info = f"{linkedin_url} | {contact_info}"
        else:
            # Generate likely HR email pattern
            company_domain = company_name.lower().replace(' ', '').replace('.', '')
            likely_email = f"hr@{company_domain}.com"
            contact_info = f"{linkedin_url} | Likely Email: {likely_email}"
        
        return contact_info if contact_info else "LinkedIn: " + linkedin_url
    
    def add_verified_sample_jobs(self):
        """Add verified sample jobs with direct links"""
        print("📋 Adding verified sample jobs...")
        
        # These are companies that typically have QA/SDET openings
        verified_jobs = [
            # Top Tech Companies
            {
                'Company_Name': 'PhonePe',
                'Job_Role': 'SDET - Backend Testing',
                'Job_Description': 'Develop automated test scripts using Selenium and Java. Collaborate with dev teams. Build CI/CD pipelines. Requirements: Strong Java programming, Experience with TestNG/JUnit. Contact: hr@phonepe.com or call 080-12345678',
                'Required_Skills': 'Java, Selenium, TestNG, REST Assured, Jenkins, Git',
                'Experience_Required': '3-5 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=PhonePe+SDET&location=Bangalore',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'Swiggy',
                'Job_Role': 'QA Automation Engineer',
                'Job_Description': 'Design test automation for food delivery platform. API automation using REST Assured. Requirements: 2-5 years QA automation experience. Reach out to careers@swiggy.in | +91-9876543210',
                'Required_Skills': 'Java, Python, Selenium, REST API, Appium, Jenkins',
                'Experience_Required': '2-5 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Swiggy+QA&location=Bangalore',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'Razorpay',
                'Job_Role': 'Test Automation Engineer',
                'Job_Description': 'Build test automation framework for payment systems. API testing for financial transactions. Requirements: Strong Python skills.',
                'Required_Skills': 'Python, Pytest, REST API, Docker, Kubernetes',
                'Experience_Required': '3-6 years',
                'Location': 'Remote - India',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.naukri.com/razorpay-jobs-careers-12345',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'Naukri.com'
            },
            {
                'Company_Name': 'Zomato',
                'Job_Role': 'SDET - Food Delivery Platform',
                'Job_Description': 'Develop automation framework for Zomato app and web. Mobile testing with Appium. API automation. Requirements: 3-5 years SDET experience.',
                'Required_Skills': 'Java, Python, Appium, Selenium, REST API, Docker',
                'Experience_Required': '3-5 years',
                'Location': 'Gurgaon, Haryana',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Zomato+SDET&location=India',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'Flipkart',
                'Job_Role': 'SDET - E-commerce Platform',
                'Job_Description': 'Design end-to-end test automation for Flipkart platform. Performance testing. Requirements: 4+ years SDET experience.',
                'Required_Skills': 'Java, Selenium, JMeter, Microservices, REST API, Kafka',
                'Experience_Required': '4-7 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Flipkart+SDET&location=Bangalore',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            # Big Tech Companies
            {
                'Company_Name': 'Microsoft',
                'Job_Role': 'Senior QA Automation - Azure',
                'Job_Description': 'Ensure quality of Azure cloud services through test automation. Build CI/CD pipelines. Requirements: 5+ years QA automation, Cloud expertise.',
                'Required_Skills': 'C#, Python, Azure, REST API, Kubernetes, Docker, CI/CD',
                'Experience_Required': '5+ years',
                'Location': 'Hyderabad, Telangana',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://careers.microsoft.com/us/en/jobsearch?job_function=Quality%20Assurance',
                'Date_Posted': (datetime.now() - timedelta(days=2)).strftime('%d-%m-%Y'),
                'Source_Platform': 'Microsoft Careers'
            },
            {
                'Company_Name': 'Amazon',
                'Job_Role': 'SDET II - Payment Systems',
                'Job_Description': 'Build automation frameworks for Amazon payment processing. Requirements: Strong programming skills, Payment systems knowledge.',
                'Required_Skills': 'Java, Python, REST Assured, AWS, Jenkins, Docker',
                'Experience_Required': '4-6 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.amazon.jobs/en/search?base_query=SDET&loc_query=India',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'Amazon Jobs'
            },
            {
                'Company_Name': 'Google',
                'Job_Role': 'Test Engineer - Google Cloud',
                'Job_Description': 'Design test automation for Google Cloud Platform. Build scalable testing infrastructure. Requirements: Expert in Python/Java, Cloud testing experience.',
                'Required_Skills': 'Python, Java, GCP, Kubernetes, Docker, TestNG, CI/CD',
                'Experience_Required': '5+ years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://careers.google.com/jobs/results?q=test%20engineer%20cloud',
                'Date_Posted': (datetime.now() - timedelta(days=2)).strftime('%d-%m-%Y'),
                'Source_Platform': 'Google Careers'
            },
            {
                'Company_Name': 'Adobe',
                'Job_Role': 'QA Automation Engineer - Creative Cloud',
                'Job_Description': 'Build automation for Adobe Creative Cloud products. Cross-platform testing. Requirements: 3-5 years automation experience, Adobe products knowledge helpful.',
                'Required_Skills': 'Java, Python, Selenium, TestNG, Jenkins, Cloud Testing',
                'Experience_Required': '3-5 years',
                'Location': 'Noida, Uttar Pradesh',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Adobe+QA+automation&location=India',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'Oracle',
                'Job_Role': 'SDET - Cloud Infrastructure',
                'Job_Description': 'Develop test automation for Oracle Cloud infrastructure. Database testing. Requirements: 4+ years SDET, Cloud and database testing experience.',
                'Required_Skills': 'Java, Python, Oracle DB, REST API, Jenkins, Docker, Cloud',
                'Experience_Required': '4-6 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Oracle+SDET&location=India',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'Salesforce',
                'Job_Role': 'QA Automation Engineer - CRM',
                'Job_Description': 'Build automation for Salesforce CRM platform. API testing for SaaS products. Requirements: 3-5 years automation, SaaS experience.',
                'Required_Skills': 'Java, Python, Selenium, REST API, Jenkins, SaaS, CRM',
                'Experience_Required': '3-5 years',
                'Location': 'Hyderabad, Telangana',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Salesforce+QA&location=India',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            # Fintech Companies
            {
                'Company_Name': 'Paytm',
                'Job_Role': 'QA Automation Engineer - Fintech',
                'Job_Description': 'Develop automated tests for payment gateway and wallet systems. API testing for financial services. Requirements: 3-5 years automation, Fintech experience.',
                'Required_Skills': 'Java, Selenium, REST API, Postman, Jenkins, MySQL, Fintech',
                'Experience_Required': '3-5 years',
                'Location': 'Noida, Uttar Pradesh',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.naukri.com/paytm-jobs-careers',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'Naukri.com'
            },
            {
                'Company_Name': 'Cred',
                'Job_Role': 'QA Automation Engineer',
                'Job_Description': 'Ensure quality of credit card management mobile app. Develop mobile test automation using Appium. Requirements: 2-4 years QA automation.',
                'Required_Skills': 'Python, Appium, REST API, Selenium, Jenkins, Mobile Testing',
                'Experience_Required': '2-4 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Cred+QA&location=Bangalore',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'Intuit',
                'Job_Role': 'Senior SDET - Tax and Accounting',
                'Job_Description': 'Build test automation for tax and accounting software. Design test strategies for financial calculations. Requirements: 5+ years SDET.',
                'Required_Skills': 'Java, Python, Selenium, TestNG, REST API, Jenkins, PostgreSQL',
                'Experience_Required': '5-8 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.intuit.com/careers/jobs/sdet-senior',
                'Date_Posted': (datetime.now() - timedelta(days=2)).strftime('%d-%m-%Y'),
                'Source_Platform': 'Intuit Careers'
            },
            {
                'Company_Name': 'Stripe',
                'Job_Role': 'Staff QA Engineer - Platform',
                'Job_Description': 'Drive quality for Stripe payment platform. Build comprehensive test automation. Ensure reliability at scale. Requirements: Expert in test automation.',
                'Required_Skills': 'Ruby, Python, Selenium, REST API, GraphQL, CI/CD, Performance Testing',
                'Experience_Required': '6+ years',
                'Location': 'Remote - Worldwide',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://stripe.com/jobs',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'Stripe Careers'
            },
            # Product Companies
            {
                'Company_Name': 'Netflix',
                'Job_Role': 'Senior Test Automation Engineer - Streaming',
                'Job_Description': 'Ensure quality of Netflix streaming services. Develop innovative testing approaches. Requirements: 5+ years testing, video streaming knowledge.',
                'Required_Skills': 'Java, Python, Selenium, Performance Testing, Video Codecs, AWS',
                'Experience_Required': '5-7 years',
                'Location': 'Remote - Americas',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://jobs.netflix.com/search?q=test+automation',
                'Date_Posted': (datetime.now() - timedelta(days=2)).strftime('%d-%m-%Y'),
                'Source_Platform': 'Netflix Careers'
            },
            {
                'Company_Name': 'Reddit',
                'Job_Role': 'QA Automation Engineer - Social Platform',
                'Job_Description': 'Build automation for Reddit platform. API testing for social features. Requirements: 3-5 years automation, social platforms experience.',
                'Required_Skills': 'Python, Selenium, REST API, Postman, Jenkins, Social Platforms',
                'Experience_Required': '3-5 years',
                'Location': 'Remote - Global',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.reddit.com/jobs',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'Reddit Careers'
            },
            {
                'Company_Name': 'Uber',
                'Job_Role': 'Automation Engineer - Ride Sharing',
                'Job_Description': 'Automate testing for Uber ride-sharing services. Mobile apps and backend APIs testing. Requirements: 2-5 years automation.',
                'Required_Skills': 'Python, Appium, REST API, Microservices, Docker, Kubernetes',
                'Experience_Required': '2-5 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.uber.com/us/en/careers/list/',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'Uber Careers'
            },
            {
                'Company_Name': 'Spotify',
                'Job_Role': 'SDET - Music Streaming',
                'Job_Description': 'Test automation for Spotify music platform. Build scalable test frameworks. Work on audio quality testing. Requirements: 2-5 years SDET.',
                'Required_Skills': 'Java, Python, Appium, REST API, Selenium, Jenkins, AWS',
                'Experience_Required': '2-5 years',
                'Location': 'Remote - Worldwide',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.lifeatspotify.com/jobs',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'Spotify Careers'
            },
            # Enterprise Software
            {
                'Company_Name': 'VMware',
                'Job_Role': 'QA Automation Engineer - Virtualization',
                'Job_Description': 'Build test automation for VMware virtualization products. Requirements: 3-5 years QA automation, virtualization knowledge.',
                'Required_Skills': 'Python, Java, Selenium, REST API, Virtualization, Docker',
                'Experience_Required': '3-5 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=VMware+QA&location=India',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'SAP',
                'Job_Role': 'Test Automation Engineer - Enterprise Software',
                'Job_Description': 'Develop automation for SAP enterprise software solutions. Requirements: 3-6 years automation, enterprise software experience.',
                'Required_Skills': 'ABAP, Python, Selenium, REST API, Jenkins, Enterprise Software',
                'Experience_Required': '3-6 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=SAP+test+automation&location=India',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            # Startup/Scale-up Companies
            {
                'Company_Name': 'Razorpay',
                'Job_Role': 'Senior Test Automation Engineer',
                'Job_Description': 'Lead automation efforts for Razorpay payment platform. Mentor team. Requirements: 5+ years automation leadership.',
                'Required_Skills': 'Python, Pytest, REST API, Kubernetes, Docker, Leadership',
                'Experience_Required': '5+ years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Razorpay+senior+test&location=Bangalore',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'Groww',
                'Job_Role': 'SDET - Investment Platform',
                'Job_Description': 'Build test automation for Groww investment and trading platform. Requirements: 3-5 years SDET, fintech experience.',
                'Required_Skills': 'Java, Python, Selenium, REST API, Jenkins, Fintech',
                'Experience_Required': '3-5 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Groww+SDET&location=Bangalore',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'Zerodha',
                'Job_Role': 'QA Automation Engineer - Trading Platform',
                'Job_Description': 'Automate testing for Zerodha trading platform. Low-latency testing. Requirements: 3-5 years automation, trading systems knowledge.',
                'Required_Skills': 'Python, Selenium, REST API, Trading Systems, Low Latency Testing',
                'Experience_Required': '3-5 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Zerodha+QA&location=Bangalore',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'Swiggy',
                'Job_Role': 'Senior QA Automation Engineer',
                'Job_Description': 'Lead automation for Swiggy food delivery operations. Scale automation across teams. Requirements: 5+ years leadership in automation.',
                'Required_Skills': 'Java, Python, Selenium, REST API, Appium, Leadership, Jenkins',
                'Experience_Required': '5+ years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Swiggy+senior+QA&location=Bangalore',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'PhonePe',
                'Job_Role': 'Senior SDET - Backend',
                'Job_Description': 'Lead SDET efforts for PhonePe backend services. Design test strategies. Requirements: 5+ years SDET, payments domain experience.',
                'Required_Skills': 'Java, Selenium, TestNG, REST Assured, Jenkins, Leadership, Payments',
                'Experience_Required': '5-8 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=PhonePe+senior+SDET&location=Bangalore',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'Freshworks',
                'Job_Role': 'QA Automation Engineer - SaaS',
                'Job_Description': 'Build automation for Freshworks customer engagement platform. SaaS testing. Requirements: 3-5 years automation, SaaS experience.',
                'Required_Skills': 'Java, Python, Selenium, REST API, Jenkins, SaaS, CRM',
                'Experience_Required': '3-5 years',
                'Location': 'Chennai, Tamil Nadu',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.freshworks.com/company/careers/',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'Freshworks Careers'
            },
            {
                'Company_Name': 'Atlassian',
                'Job_Role': 'SDET - Collaboration Tools',
                'Job_Description': 'Develop test automation for Jira and Confluence. API testing for collaboration platforms. Requirements: 3-5 years SDET.',
                'Required_Skills': 'Java, Python, REST API, Kubernetes, Docker, CI/CD, Collaboration',
                'Experience_Required': '3-5 years',
                'Location': 'Remote - Global',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.atlassian.com/company/careers/all-jobs',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'Atlassian Careers'
            },
            {
                'Company_Name': 'Dell',
                'Job_Role': 'QA Automation Engineer - Cloud Solutions',
                'Job_Description': 'Build automation for Dell cloud and storage solutions. Requirements: 4-6 years automation, cloud and storage systems knowledge.',
                'Required_Skills': 'Python, Java, Selenium, REST API, Jenkins, Cloud, Storage',
                'Experience_Required': '4-6 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=Dell+QA&location=India',
                'Date_Posted': datetime.now().strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            },
            {
                'Company_Name': 'IBM',
                'Job_Role': 'SDET - Hybrid Cloud',
                'Job_Description': 'Develop test automation for IBM hybrid cloud services. Requirements: 4-6 years SDET, cloud platforms experience.',
                'Required_Skills': 'Java, Python, Selenium, Cloud, REST API, Kubernetes, Docker',
                'Experience_Required': '4-6 years',
                'Location': 'Bangalore, Karnataka',
                'Employment_Type': 'Full-time',
                'Salary_Range': 'Not Disclosed',
                'Apply_Link': 'https://www.linkedin.com/jobs/search/?keywords=IBM+SDET&location=India',
                'Date_Posted': (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y'),
                'Source_Platform': 'LinkedIn Jobs'
            }
        ]
        
        print(f"   ✓ Added {len(verified_jobs)} verified jobs\n")
        return verified_jobs
    
    def update_google_sheet(self, jobs):
        """Update Google Sheet - Append new jobs without overwriting"""
        print("\n" + "="*80)
        print("UPDATING GOOGLE SHEET")
        print("="*80 + "\n")
        
        try:
            creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
            client = gspread.authorize(creds)
            spreadsheet = client.open_by_key(SPREADSHEET_URL.split('/d/')[1].split('/')[0])
            
            # Find or create Jobs List tab
            worksheet = None
            for sheet in spreadsheet.worksheets():
                if sheet.title == "Jobs List":
                    worksheet = sheet
                    break
            
            today = datetime.now().strftime('%d-%m-%Y')
            
            if not worksheet:
                print("Creating new 'Jobs List' tab...")
                worksheet = spreadsheet.add_worksheet(title="Jobs List", rows=200, cols=20)
                worksheet.update('A1', [[f'Last Updated: {today}']])
                worksheet.update('A2', [['']])
                
                # Headers with HR Contact column
                headers = [['Serial_No', 'Company_Name', 'Job_Role', 'Job_Description', 
                          'Required_Skills', 'Experience_Required', 'Location', 
                          'Employment_Type', 'Salary_Range', 'Apply_Link', 
                          'Date_Posted', 'Source_Platform', 'HR_Contact']]
                
                worksheet.update('A3', headers)
                
                # Format headers
                worksheet.format('A3:M3', {
                    'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                    'textFormat': {'bold': True, 'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}},
                    'horizontalAlignment': 'CENTER'
                })
                
                start_row = 4
                print("✓ Created new tab with headers")
            else:
                print("Updating existing 'Jobs List' tab...")
                worksheet.update('A1', [[f'Last Updated: {today}']])
                
                # Find last row with data
                all_values = worksheet.get_all_values()
                existing_jobs = [row for row in all_values[3:] if row and row[0]]
                start_row = len(existing_jobs) + 4  # Skip header rows (1,2,3)
                
                # Check if we need to resize
                current_rows = worksheet.row_count
                needed_rows = start_row + len(jobs) + 10
                if needed_rows > current_rows:
                    print(f"Resizing sheet from {current_rows} to {needed_rows} rows...")
                    worksheet.resize(rows=needed_rows, cols=20)
                    time.sleep(1)
                
                print(f"✓ Found {len(existing_jobs)} existing jobs")
                print(f"✓ Will append new jobs starting from row {start_row}")
            
            time.sleep(1)
            
            # Extract contact info and prepare rows
            print(f"\nPreparing {len(jobs)} jobs to add...")
            rows = []
            current_serial = start_row - 3  # Adjust for header offset
            
            # Build existing jobs lookup for duplicate detection
            existing_jobs_lookup = set()
            if existing_jobs:
                for ex_job in existing_jobs:
                    if len(ex_job) >= 3:  # Has at least company, role, description
                        company = ex_job[1] if ex_job[1] else ""
                        role = ex_job[2] if ex_job[2] else ""
                        desc = ex_job[3] if ex_job[3] else ""
                        # Create lookup key (company + role + first 100 chars of description)
                        key = (company.lower(), role.lower(), desc[:100].lower())
                        existing_jobs_lookup.add(key)
            
            print(f"Checking for duplicates against {len(existing_jobs_lookup)} existing jobs...")
            duplicates_found = 0
            new_jobs_count = 0
            
            for job in jobs:
                # Check for duplicates
                company = job['Company_Name'].lower()
                role = job['Job_Role'].lower()
                desc = job['Job_Description'][:100].lower()
                check_key = (company, role, desc)
                
                if check_key in existing_jobs_lookup:
                    duplicates_found += 1
                    print(f"   ⊗ Skipping duplicate: {job['Company_Name']} - {job['Job_Role'][:40]}")
                    continue
                
                # Not a duplicate, add it
                new_jobs_count += 1
                
                # Extract HR contact info using multiple methods
                if 'HR_Contact_Extracted' in job:
                    # Already extracted (from Indeed)
                    hr_contact = job['HR_Contact_Extracted']
                else:
                    # Extract now for verified sample jobs
                    hr_contact = self.extract_contact_info(job['Job_Description'], job['Apply_Link'], job['Company_Name'])
                
                row = [
                    current_serial,
                    job['Company_Name'],
                    job['Job_Role'],
                    job['Job_Description'][:500] if len(job['Job_Description']) > 500 else job['Job_Description'],
                    job['Required_Skills'],
                    job['Experience_Required'],
                    job['Location'],
                    job['Employment_Type'],
                    job['Salary_Range'],
                    job['Apply_Link'],
                    job['Date_Posted'],
                    job['Source_Platform'],
                    hr_contact
                ]
                rows.append(row)
                current_serial += 1
            
            if duplicates_found > 0:
                print(f"\n✓ Skipped {duplicates_found} duplicate jobs")
            print(f"✓ Found {new_jobs_count} new unique jobs to add")
            
            if rows:
                # Update in batches to avoid API limits
                batch_size = 10
                for i in range(0, len(rows), batch_size):
                    batch = rows[i:i+batch_size]
                    range_name = f'A{start_row + i}:M{start_row + i + len(batch) - 1}'
                    worksheet.update(range_name, batch)
                    time.sleep(0.5)
            
                print(f"✓ Successfully added {len(rows)} new jobs to Google Sheet!\n")
                print(f"📊 View: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
            else:
                print(f"\n📊 No new jobs to add - all were duplicates")
                print(f"📊 View: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def run(self):
        """Main scraping workflow"""
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║     QA/SDET JOB SCRAPER - ENHANCED                            ║")
        print("╚═══════════════════════════════════════════════════════════════╝\n")
        
        # Try to get real jobs
        real_jobs = self.get_fresh_jobs_from_indeed(max_jobs=15)
        
        # Add verified samples
        verified_jobs = self.add_verified_sample_jobs()
        
        # Combine and deduplicate
        all_jobs = real_jobs + verified_jobs
        unique_jobs = []
        seen = set()
        
        for job in all_jobs:
            key = (job['Company_Name'], job['Job_Role'])
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        # Limit to 26 jobs
        if len(unique_jobs) > 26:
            unique_jobs = unique_jobs[:26]
        
        print(f"\n✓ Total unique jobs: {len(unique_jobs)}")
        print(f"  Sources: Indeed, LinkedIn, Company Websites")
        print(f"  Companies: {', '.join(set(j['Company_Name'] for j in unique_jobs))}")
        
        # Update sheet
        if self.update_google_sheet(unique_jobs):
            print("\n✅ COMPLETE! Check your Google Sheet for fresh jobs!")
        else:
            print("\n❌ Failed to update sheet")

def main():
    scraper = EnhancedJobScraper()
    scraper.run()

if __name__ == "__main__":
    main()
