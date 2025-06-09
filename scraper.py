import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- User-supplied market list ---
market_list = """
KARWAR	KOLAR	KOLLEGAL	KOPPA	KOPPAL	KORATAGERE	KOTTUR	KUDCHI	KUMTA	KUNDAPUR	KUNDGOL	KUNIGAL
KUSTAGI	LAXMESHWAR	LINGASARGUR	MADDUR	MADHUGIRI	MADIKERI	MAHALINGAPURA	MALAVALLI	MALUR	MANDYA
MANGALURU	MANVI	MASKI	MUDIGERE	MULBAGAL	MUNDAGOD	MUNDARGI	MYSURU	NAGAMANGALA	NANDAGAD	NANJANGUD
NARGUND	NIPPANI	PANDAVAPURA	PAVAGADA	PERIYAPATNA	PUTTUR	RAICHUR	RAMANAGARA	RAMDURGA	RAMPURA
RANIBENNUR	RONA	SAGAR	SAKLESHPUR	SANDUR	SANKESHWAR	SANTHESARGUR	SAVADATTI	SAVANUR	SEDAM	SHAHAPUR
SHIGGAON	SHIKARIPUR	SHIVAMOGGA	SHORAPUR	SIDDAPURA	SINDAGI	SINDHANUR	SIRA	SIRAGUPPA	SIRSI
SOMWARPET	SORABHA	SRINGERI	SRINIVASPUR	SRIRANGAPATNA	SULYA	T.NARSIPUR	TALIKOTE	TARIKERE
TIPTUR	TIRTHAHALLI	TUMAKURU	TURUVEKERE	UDIPI	VIJAYAPURA	VV TOWERS	YADGIR	YELBURGA	YELLAPURA
""".replace("\n", "\t").split("\t")
market_list = [m.strip() for m in market_list if m.strip()]

# --- User-supplied commodity list ---
commodity_list = """
Cattle	Goats	Sheep	Cotton(Ginned and Un-ginned)	All Flowers	Bajra	Jau	Jowar	Kambu	Maize	Navane
Paddy	Ragi	Rice	Save	Wheat	Antwala	Bamboo	Canes	Hippe Seeds	Honge Seeds	Neem Seeds	Soap Nuts
Tamarind	Tamarind Seeds	Apple	Banana	Borehannu	Citrus Fruits	Chakkothaihannu	Guava	Grapes
Jack Fruit	Jamun	Lemon	Kharbuja	Mango	Mosumbi	Marasebu	Pine apple	Pappaya	Pamogranate
Sapota	Siddota	Orange	Watermelon	Groundnut (Shelled and Unshelled)	Castor Seeds	Cotton seeds
Linseed	Mustard	Niger seeds	Safflower	Seasamum	Sunflower seeds	Soyabean	Cashewnut	Chillies(Dry)
Coconut	Copra	Corriander	Garlic	Ginger	Methi	Pepper	Turmeric	Alsande(Cowpea)(Whole & Split)
Avare(Whole & Split)	Bengalgram(Whole & Split)	Blackgram (Whole & Split)	Bullar (Whole & Split)
Greengram (Whole & Split)	Horse Gram	Lakh (Whole & Split)	Matki (Whole & Split)	Masoor (whole & Split)
Peas	Tur (Whole & Split)	Moath (Whole & Split)	All Vegetables [except Gherkin(including leafy)]
Goourds	Green Chillies	Onion	Potato	Suvarnagadde	Sweet Potato	Tomato	Beete(Rose)	Firewood
Teak	White Cedar	Silver Oak	Eucalyptus	Betal leaves	Jaggery	Dry grapes
""".replace("\n", "\t").split("\t")
commodity_list = [c.strip() for c in commodity_list if c.strip()]

# --- Month list ---
months_full = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
               'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
months_options = ['All'] + months_full

# --- UI ---
st.title("Krishi Maratha Vahini Data Scraper")

selected_months = st.multiselect("Select Month(s):", options=months_options, default='All')
if 'All' in selected_months:
    selected_months = months_full

col1, col2 = st.columns(2)
with col1:
    from_year = st.number_input("From Year:", min_value=2000, max_value=2100, value=2022)
with col2:
    to_year = st.number_input("To Year:", min_value=2000, max_value=2100, value=2024)

if from_year > to_year:
    st.error("❌ 'From Year' must be less than or equal to 'To Year'")
    st.stop()

years = [str(y) for y in range(from_year, to_year + 1)]

selected_commodity = st.selectbox("Select Commodity:", options=commodity_list)
selected_markets = st.multiselect("Select Market(s):", options=market_list, default=market_list[:5])

# --- Dummy scraping logic (to be replaced with real scraping) ---
def scrape_data(months, years, commodity, markets):
    # Simulate scraping: create a dummy DataFrame
    rows = []
    for year in years:
        for month in months:
            for market in markets:
                rows.append({
                    "Year": year,
                    "Month": month,
                    "Market": market,
                    "Commodity": commodity,
                    "Price": round(1000 + hash(f"{market}-{commodity}-{month}-{year}") % 500, 2)
                })
    return pd.DataFrame(rows)

# --- Scrape and show results ---
if st.button("Scrape Data"):
    with st.spinner("Scraping..."):
        df = scrape_data(selected_months, years, selected_commodity, selected_markets)
        if not df.empty:
            st.success(f"✅ Scraped {len(df)} records.")
            st.dataframe(df.head(50))
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", data=csv, file_name="kmvahini_data.csv", mime="text/csv")
        else:
            st.warning("⚠️ No data found.")
