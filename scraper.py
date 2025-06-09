import streamlit as st
import pandas as pd

# Market list
market_list = """
KARWAR	KOLAR	KOLLEGAL	KOPPA	KOPPAL	KORATAGERE	KOTTUR	KUDCHI	KUMTA	KUNDAPUR	KUNDGOL	KUNIGAL
KUSTAGI	LAXMESHWAR	LINGASARGUR	MADDUR	MADHUGIRI	MADIKERI	MAHALINGAPURA	MALAVALLI	MALUR	MANDYA
MANGALURU	MANVI	MASKI	MUDIGERE	MULBAGAL	MUNDAGOD	MUNDARGI	MYSURU	NAGAMANGALA	NANDAGAD	NANJANGUD
NARGUND	NIPPANI	PANDAVAPURA	PAVAGADA	PERIYAPATNA	PUTTUR	RAICHUR	RAMANAGARA	RAMDURGA	RAMPURA
RANIBENNUR	RONA	SAGAR	SAKLESH... (truncated, full as per your list)
""".replace("\n", "\t").split("\t")
market_list = [m.strip() for m in market_list if m.strip()]

# Commodity list
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

st.title("Krishi Maratha Vahini - Date Wise Report")

# Date range input
date_range = st.date_input(
    "Select Date Range:",
    value=(pd.to_datetime("2023-01-01"), pd.to_datetime("2023-12-31")),
    min_value=pd.to_datetime("2000-01-01"),
    max_value=pd.to_datetime("2100-12-31")
)

if len(date_range) != 2:
    st.error("Please select both start and end dates.")
    st.stop()

start_date, end_date = date_range
if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

# Commodity select box
selected_commodity = st.selectbox("Select Commodity:", options=commodity_list)

# Market multiselect
selected_markets = st.multiselect("Select Markets:", options=market_list, default=market_list[:5])

# Dummy scraping function - replace with actual scraping logic
def scrape_data_datewise(start_date, end_date, commodity, markets):
    dates = pd.date_range(start=start_date, end=end_date)
    rows = []
    for date in dates:
        for market in markets:
            # Generate dummy price data (replace this)
            price = round(1000 + hash(f"{market}-{commodity}-{date}") % 500, 2)
            rows.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Market": market,
                "Commodity": commodity,
                "Price": price
            })
    return pd.DataFrame(rows)

# Scrape button
if st.button("Get Date Wise Report"):
    with st.spinner("Fetching data..."):
        df = scrape_data_datewise(start_date, end_date, selected_commodity, selected_markets)
        if df.empty:
            st.warning("No data found.")
        else:
            st.success(f"Fetched {len(df)} records.")
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "kmvahini_datewise_report.csv", "text/csv")
