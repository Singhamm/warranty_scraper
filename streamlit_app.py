import streamlit as st
from utils.scraper import scrape_warranty
from utils.file_processor import process_uploaded_file
import pandas as pd
import time

# --- App Config ---
st.set_page_config(
    page_title="Lenovo Warranty Scraper",
    page_icon="🖥️",
    layout="wide"
)

# --- Sidebar ---
with st.sidebar:
    st.image("assets/lenovo-logo.png", width=150)
    st.markdown("""
    **How to Use:**
    1. Enter a serial number OR
    2. Upload CSV/Excel with `Serial Number` column
    """)
    st.divider()
    st.caption("Made with ❤️ using Streamlit + Playwright")

# --- Main UI ---
tab1, tab2 = st.tabs(["🔍 Single Check", "📁 Batch Processing"])

with tab1:
    col1, col2 = st.columns([3, 1])
    serial = col1.text_input("Enter Lenovo Serial Number:", placeholder="PF3A2XYZ")
    
    if col2.button("Check Warranty", type="primary"):
        if serial:
            with st.spinner("Fetching warranty details..."):
                result = scrape_warranty(serial.strip())
                
                if "error" in result:
                    st.error(f"❌ {result['error']}")
                else:
                    st.success("✅ Warranty details found!")
                    st.json(result)
                    
                    # Display as nice cards
                    cols = st.columns(3)
                    cols[0].metric("Product", result.get("product_name", "N/A"))
                    cols[1].metric("Status", result.get("warranty_status", "N/A"))
                    cols[2].metric("Expiry", result.get("expiry_date", "N/A"))
        else:
            st.warning("Please enter a serial number")

with tab2:
    uploaded_file = st.file_uploader("Choose CSV/Excel", type=["csv", "xlsx"])
    if uploaded_file:
        df = process_uploaded_file(uploaded_file)
        st.dataframe(df.head(3), use_container_width=True)
        
        if st.button("Process All Serial Numbers", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            results = []
            
            for i, row in df.iterrows():
                result = scrape_warranty(str(row["Serial Number"])).strip()
                results.append(result)
                
                # Update UI
                progress_bar.progress((i + 1) / len(df))
                status_text.text(f"Processing {i+1}/{len(df)}: {row['Serial Number']}")
                time.sleep(1)  # Rate limiting
            
            # Show results
            results_df = pd.DataFrame(results)
            st.success(f"✅ Processed {len(results_df)} records")
            st.dataframe(results_df, use_container_width=True)
            
            # Download
            st.download_button(
                label="📥 Download Results (CSV)",
                data=results_df.to_csv(index=False),
                file_name="warranty_results.csv",
                mime="text/csv"
            )