import streamlit as st
import kmvahini.scraper as scraper

# Title
st.title("Krishi Maratha Vahini Data Scraper")

# --- 1. Get lists of commodities and markets from the scraper package ---
try:
    commodity_list = scraper.get_commodity_list()
    market_list = scraper.get_market_list()
except Exception as e:
    st.error("Error fetching commodity or market list. Please check kmvahini.scraper.")
    st.stop()

# --- 2. Month selection ---
months_full = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
               'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
months_options = ['All'] + months_full
selected_months = st.multiselect("Select Month(s):", options=months_options, default='All')
if 'All' in selected_months:
    selected_months = months_full

# --- 3. Year range input ---
st.markdown("### Select Year Range")
col1, col2 = st.columns(2)
with col1:
    from_year = st.number_input("From Year:", min_value=2000, max_value=2100, value=2020)
with col2:
    to_year = st.number_input("To Year:", min_value=2000, max_value=2100, value=2024)

if from_year > to_year:
    st.error("❌ 'From Year' must be less than or equal to 'To Year'")
    st.stop()

years = [str(y) for y in range(from_year, to_year + 1)]

# --- 4. Commodity selection ---
selected_commodity = st.selectbox("Select Commodity:", commodity_list)

# --- 5. Market selection ---
selected_markets = st.multiselect("Select Market(s):", options=market_list, default=market_list)

# --- 6. Scrape button ---
if st.button("Scrape Data"):
    with st.spinner("🔍 Scraping data from Krishi Maratha Vahini..."):
        try:
            df = scraper.scrape_website(selected_months, years, [selected_commodity], selected_markets)
            if not df.empty:
                st.success("✅ Data scraped successfully!")
                st.dataframe(df.head(50))
                st.download_button("📥 Download Full CSV", data=df.to_csv(index=False), file_name="scraped_data.csv", mime="text/csv")
            else:
                st.warning("⚠️ No data found for the selected filters.")
        except Exception as e:
            st.error(f"❌ An error occurred while scraping: {e}")
