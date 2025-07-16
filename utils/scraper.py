from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_lenovo_warranty(serial_number):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://pcsupport.lenovo.com/in/en/warranty-lookup")
            page.fill("#txtSerialNumber", serial_number)
            page.click("#btnSubmit")

            page.wait_for_url("**/warranty", timeout=15000)
            page.wait_for_selector(".warrantyDetails", timeout=10000)

            soup = BeautifulSoup(page.content(), "html.parser")
            product = soup.find("h1").get_text(strip=True)

            warranty_rows = soup.find_all("div", class_="row warrantyDetailsRow")
            warranty_info = {}
            for row in warranty_rows:
                label = row.find("div", class_="col-sm-4 col-xs-5").get_text(strip=True)
                value = row.find("div", class_="col-sm-8 col-xs-7").get_text(strip=True)
                warranty_info[label] = value

            browser.close()

            return {
                "Serial Number": serial_number,
                "Model": product,
                **warranty_info
            }

    except Exception as e:
        return {
            "Serial Number": serial_number,
            "Model": "Error",
            "Error": str(e)
        }
