# Warranty Scraper

This project fetches Lenovo product warranty information using a serial number.

## 🔧 How it works

It uses [Playwright](https://playwright.dev/) to open Lenovo's warranty lookup page, submit a serial number, wait for the redirect, and scrape the product & warranty info.

## ✅ Requirements

- Python 3.7+
- Playwright
- BeautifulSoup4

## 📦 Setup Instructions

```bash
git clone https://github.com/yourusername/warranty_scraper.git
cd warranty_scraper
pip install -r requirements.txt
playwright install
