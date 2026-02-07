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
    parser.add_argument("--manual-login", "-m", action="store_true", help="Login manually (for 2FA)")
    parser.add_argument("--cookies", "-c", default="linkedin_cookies.pkl", help="Cookies file path")
    parser.add_argument("--no-cookies", action="store_true", help="Don't use cookies")
    
    args = parser.parse_args()
    
    # Initialize scraper
    print("🚀 Starting LinkedIn Job Scraper...")
    scraper = LinkedInJobScraper(headless=args.headless, cookies_file=args.cookies)
    
    try:
        # Login
        print("🔐 Logging in...")
        
        if args.manual_login:
            # Manual login mode (for first time or 2FA)
            if not scraper.login_with_manual():
                print("❌ Manual login failed. Exiting.")
                return
        else:
            # Auto login with cookies support
            # Try cookies first if available
            if not args.no_cookies and os.path.exists(args.cookies):
                print("🍪 Found existing cookies, trying to login...")
                if scraper.is_logged_in():
                    print("✅ Logged in with cookies!")
                else:
                    # Cookies expired, need credentials
                    email = args.email or os.getenv("LINKEDIN_EMAIL")
                    password = args.password or os.getenv("LINKEDIN_PASSWORD")
                    
                    if not email or not password:
                        print("⚠️  Cookies expired and no credentials provided.")
                        print("   Options:")
                        print("   1. Run with --manual-login to login with 2FA")
                        print("   2. Provide --email and --password")
                        print("   3. Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env")
                        return
                    
                    if not scraper.login(email, password):
                        print("❌ Login failed. Try --manual-login for 2FA.")
                        return
            else:
                # No cookies, need credentials
                email = args.email or os.getenv("LINKEDIN_EMAIL")
                password = args.password or os.getenv("LINKEDIN_PASSWORD")
                
                if not email or not password:
                    print("❌ Error: Please provide LinkedIn credentials via:")
                    print("   - Command line: --email and --password")
                    print("   - Environment variables: LINKEDIN_EMAIL and LINKEDIN_PASSWORD")
                    print("   - .env file")
                    print("   Or use --manual-login for first-time login with 2FA")
                    return
                
                if not scraper.login(email, password):
                    print("❌ Login failed. Try --manual-login for 2FA.")
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
