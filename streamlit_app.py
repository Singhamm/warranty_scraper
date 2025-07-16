import streamlit as st
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Scraper function (same as main.py)
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

# Streamlit UI
st.title("🔧 Lenovo Warranty Scraper")

# Option 1: Manual input
serial_input = st.text_input("Enter Lenovo Product Serial Code")

if st.button("Check Warranty"):
    if serial_input:
        with st.spinner("Fetching warranty info..."):
            result = fetch_lenovo_warranty(serial_input)
            st.success("Done!")
            st.json(result)
    else:
        st.warning("Please enter a serial number.")

# Option 2: Excel Upload
st.markdown("---")
st.subheader("📤 Upload Excel/CSV with Serial Numbers")

uploaded_file = st.file_uploader("Upload file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if "Serial Number" not in df.columns:
        st.error("Excel/CSV must have a column named 'Serial Number'")
    else:
        serials = df["Serial Number"].dropna().unique().tolist()

        with st.spinner("Fetching warranty data..."):
            results = [fetch_lenovo_warranty(serial) for serial in serials]
            result_df = pd.DataFrame(results)

        st.success("✅ All Done!")
        st.dataframe(result_df)

        # Download button
        st.download_button("📥 Download Results as CSV", result_df.to_csv(index=False), file_name="warranty_results.csv", mime="text/csv")
