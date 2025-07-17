import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import logging

def scrape_warranty(serial_number):
    """Scrape Lenovo warranty details with error handling"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # --- Page Navigation ---
            page.goto("https://pcsupport.lenovo.com/in/en/warranty-lookup#/", timeout=15000)
            
            # --- Form Submission ---
            page.fill("#input-sn", serial_number)
            page.click("#btn-sn")
            
            # --- Wait for Results ---
            selector = ".warrantyDetails, .error-message, #no-warranty"
            page.wait_for_selector(selector, timeout=10000)
            
            # --- Parse Results ---
            soup = BeautifulSoup(page.content(), "html.parser")
            
            if soup.select_one(".error-message, #no-warranty"):
                error_text = soup.select_one(".error-message, #no-warranty").get_text(strip=True)
                return {"error": f"Lenovo Error: {error_text}", "serial_number": serial_number}
            
            # --- Extract Data ---
            return {
                "serial_number": serial_number,
                "product_name": soup.select_one(".product-name").get_text(strip=True),
                "warranty_status": soup.select_one(".warranty-status").get_text(strip=True),
                "expiry_date": soup.select_one(".expiry-date").get_text(strip=True),
                "scraped_at": pd.Timestamp.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Scraping failed for {serial_number}: {str(e)}")
            return {"error": f"System Error: {str(e)}", "serial_number": serial_number}
        
        finally:
            context.close()
            browser.close()