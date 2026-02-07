from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Optional


class LinkedInJobScraper:
    """LinkedIn Job Scraper using Selenium."""
    
    def __init__(self, headless: bool = True, chromedriver_path: str = None):
        """
        Initialize the scraper.
        
        Args:
            headless: Run browser in headless mode
            chromedriver_path: Path to chromedriver executable
        """
        self.options = Options()
        
        if headless:
            self.options.add_argument("--headless")
        
        # Common options to avoid detection
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # Disable automation flags
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize driver
        if chromedriver_path:
            service = Service(chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=self.options)
        else:
            self.driver = webdriver.Chrome(options=self.options)
        
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self, email: str, password: str) -> bool:
        """
        Login to LinkedIn.
        
        Args:
            email: LinkedIn email
            password: LinkedIn password
            
        Returns:
            True if login successful
        """
        try:
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for login form
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_field = self.driver.find_element(By.ID, "password")
            
            # Fill credentials
            email_field.send_keys(email)
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for feed to load (indicates successful login)
            time.sleep(3)
            
            if "feed" in self.driver.current_url or "checkpoint" not in self.driver.current_url:
                print("✅ Login successful!")
                return True
            else:
                print("⚠️  Login might require verification (2FA/captcha)")
                return False
                
        except TimeoutException:
            print("❌ Login timeout - check credentials or LinkedIn blocks login")
            return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def search_jobs(
        self, 
        keywords: str, 
        location: str = "", 
        limit: int = 25
    ) -> List[Dict]:
        """
        Search for jobs on LinkedIn.
        
        Args:
            keywords: Job title or keywords
            location: Job location
            limit: Maximum number of jobs to scrape
            
        Returns:
            List of job dictionaries
        """
        jobs = []
        
        try:
            # Build search URL
            search_url = f"https://www.linkedin.com/jobs/search?keywords={keywords.replace(' ', '%20')}"
            if location:
                search_url += f"&location={location.replace(' ', '%20')}"
            
            self.driver.get(search_url)
            time.sleep(3)
            
            # Scroll to load more jobs
            job_cards = self._scroll_and_load_jobs(limit)
            
            print(f"🔍 Found {len(job_cards)} job cards")
            
            for i, card in enumerate(job_cards[:limit]):
                try:
                    job = self._extract_job_data(card)
                    if job:
                        jobs.append(job)
                        print(f"✅ Scraped job {i+1}/{min(len(job_cards), limit)}: {job.get('title', 'Unknown')}")
                    
                    time.sleep(1)  # Be nice to LinkedIn
                    
                except Exception as e:
                    print(f"⚠️  Error extracting job {i+1}: {e}")
                    continue
            
        except Exception as e:
            print(f"❌ Search error: {e}")
        
        return jobs
    
    def _scroll_and_load_jobs(self, limit: int) -> list:
        """Scroll page to load more job cards."""
        job_cards = []
        last_count = 0
        scroll_attempts = 0
        max_attempts = 10
        
        while len(job_cards) < limit and scroll_attempts < max_attempts:
            # Find job cards
            cards = self.driver.find_elements(By.CLASS_NAME, "job-card-container")
            
            if len(cards) > last_count:
                job_cards = cards
                last_count = len(cards)
                scroll_attempts = 0
            else:
                scroll_attempts += 1
            
            # Scroll down
            self.driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(2)
        
        return job_cards
    
    def _extract_job_data(self, card) -> Optional[Dict]:
        """Extract data from a job card."""
        try:
            # Click card to load details
            card.click()
            time.sleep(2)
            
            job_data = {
                "title": self._safe_find_text(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title"),
                "company": self._safe_find_text(By.CLASS_NAME, "job-details-jobs-unified-top-card__company-name"),
                "location": self._safe_find_text(By.CLASS_NAME, "job-details-jobs-unified-top-card__bullet"),
                "url": self.driver.current_url,
                "scraped_at": datetime.now().isoformat()
            }
            
            # Try to get description
            try:
                description_elem = self.driver.find_element(
                    By.CLASS_NAME, "jobs-description__content"
                )
                job_data["description"] = description_elem.text[:500]  # First 500 chars
            except:
                job_data["description"] = ""
            
            # Try to get posting info
            try:
                insights = self.driver.find_elements(
                    By.CLASS_NAME, "job-details-jobs-unified-top-card__job-insight"
                )
                job_data["insights"] = [i.text for i in insights]
            except:
                job_data["insights"] = []
            
            return job_data
            
        except Exception as e:
            print(f"Error extracting job: {e}")
            return None
    
    def _safe_find_text(self, by: By, value: str) -> str:
        """Safely find element and get text."""
        try:
            elem = self.driver.find_element(by, value)
            return elem.text.strip()
        except:
            return ""
    
    def save_to_json(self, jobs: List[Dict], filename: str):
        """Save jobs to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({"jobs": jobs, "count": len(jobs)}, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(jobs)} jobs to {filename}")
    
    def save_to_csv(self, jobs: List[Dict], filename: str):
        """Save jobs to CSV file."""
        if not jobs:
            print("No jobs to save")
            return
        
        # Get all possible fields
        fieldnames = set()
        for job in jobs:
            fieldnames.update(job.keys())
        fieldnames = sorted(fieldnames)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs)
        
        print(f"💾 Saved {len(jobs)} jobs to {filename}")
    
    def close(self):
        """Close the browser."""
        self.driver.quit()
        print("👋 Browser closed")
