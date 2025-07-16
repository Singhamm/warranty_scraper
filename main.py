from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_lenovo_warranty(serial_number):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Go to warranty lookup page
        page.goto("https://pcsupport.lenovo.com/in/en/warranty-lookup")

        # Step 2: Fill serial number and submit
        page.fill("#txtSerialNumber", serial_number)
        page.click("#btnSubmit")

        # Step 3: Wait for redirect and warranty section
        page.wait_for_url("**/warranty", timeout=15000)
        page.wait_for_selector(".warrantyDetails", timeout=10000)

        # Step 4: Parse final page with BeautifulSoup
        soup = BeautifulSoup(page.content(), "html.parser")
        product = soup.find("h1").get_text(strip=True)

        warranty_rows = soup.find_all("div", class_="row warrantyDetailsRow")
        output = f"🔧 {serial_number} — {product}\n🛡️ WARRANTY DETAILS:\n"

        for row in warranty_rows:
            label = row.find("div", class_="col-sm-4 col-xs-5").get_text(strip=True)
            value = row.find("div", class_="col-sm-8 col-xs-7").get_text(strip=True)
            output += f"{label}: {value}\n"

        browser.close()
        return output.strip()

# 🟢 Dynamic input from user
if __name__ == "__main__":
    serial = input("Enter Lenovo Product Serial Code: ").strip()
    print(fetch_lenovo_warranty(serial))
