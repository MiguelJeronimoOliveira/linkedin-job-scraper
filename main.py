import argparse
import os
from dotenv import load_dotenv
from linkedin_scraper import LinkedInJobScraper


def main():
    # Load environment variables
    load_dotenv()
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="LinkedIn Job Scraper")
    parser.add_argument("--keywords", "-k", required=True, help="Job keywords to search")
    parser.add_argument("--location", "-l", default="", help="Job location")
    parser.add_argument("--limit", "-n", type=int, default=25, help="Number of jobs to scrape")
    parser.add_argument("--output", "-o", default="linkedin_jobs", help="Output filename (without extension)")
    parser.add_argument("--format", "-f", choices=["json", "csv", "both"], default="json", help="Output format")
    parser.add_argument("--email", "-e", help="LinkedIn email (or use LINKEDIN_EMAIL env)")
    parser.add_argument("--password", "-p", help="LinkedIn password (or use LINKEDIN_PASSWORD env)")
    parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode")
    parser.add_argument("--no-headless", dest="headless", action="store_false", help="Show browser window")
    
    args = parser.parse_args()
    
    # Get credentials
    email = args.email or os.getenv("LINKEDIN_EMAIL")
    password = args.password or os.getenv("LINKEDIN_PASSWORD")
    
    if not email or not password:
        print("❌ Error: Please provide LinkedIn credentials via:")
        print("   - Command line: --email and --password")
        print("   - Environment variables: LINKEDIN_EMAIL and LINKEDIN_PASSWORD")
        print("   - .env file")
        return
    
    # Initialize scraper
    print("🚀 Starting LinkedIn Job Scraper...")
    scraper = LinkedInJobScraper(headless=args.headless)
    
    try:
        # Login
        print("🔐 Logging in...")
        if not scraper.login(email, password):
            print("❌ Login failed. Exiting.")
            return
        
        # Search for jobs
        print(f"🔍 Searching for '{args.keywords}' in '{args.location or 'Anywhere'}'...")
        jobs = scraper.search_jobs(
            keywords=args.keywords,
            location=args.location,
            limit=args.limit
        )
        
        print(f"\n✅ Scraped {len(jobs)} jobs successfully!")
        
        # Save results
        if args.format in ["json", "both"]:
            scraper.save_to_json(jobs, f"{args.output}.json")
        
        if args.format in ["csv", "both"]:
            scraper.save_to_csv(jobs, f"{args.output}.csv")
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
