import streamlit as st
import kmvahini.scraper as scraper
 
# Title
st.title("Krishi Maratha Vahini Data Scraper")

# --- Market List (from user) ---
market_list = """
KARWAR	KOLAR	KOLLEGAL	KOPPA
KOPPAL	KORATAGERE	KOTTUR	KUDCHI
KUMTA	KUNDAPUR	KUNDGOL	KUNIGAL
KUSTAGI	LAXMESHWAR	LINGASARGUR	MADDUR
MADHUGIRI	MADIKERI	MAHALINGAPURA	MALAVALLI
MALUR	MANDYA	MANGALURU	MANVI
MASKI	MUDIGERE	MULBAGAL	MUNDAGOD
MUNDARGI	MYSURU	NAGAMANGALA	NANDAGAD
NANJANGUD	NARGUND	NIPPANI	PANDAVAPURA
PAVAGADA	PERIYAPATNA	PUTTUR	RAICHUR
RAMANAGARA	RAMDURGA	RAMPURA	RANIBENNUR
RONA	SAGAR	SAKLESHPUR	SANDUR
SANKESHWAR	SANTHESARGUR	SAVADATTI	SAVANUR
SEDAM	SHAHAPUR	SHIGGAON	SHIKARIPUR
SHIVAMOGGA	SHORAPUR	SIDDAPURA	SINDAGI
SINDHANUR	SIRA	SIRAGUPPA	SIRSI
SOMWARPET	SORABHA	SRINGERI	SRINIVASPUR
SRIRANGAPATNA	SULYA	T.NARSIPUR	TALIKOTE
TARIKERE	TIPTUR	TIRTHAHALLI	TUMAKURU
TURUVEKERE	UDIPI	VIJAYAPURA	VV TOWERS
YADGIR	YELBURGA	YELLAPURA
"""
market_list = list(filter(None, market_list.replace('\n', '\t').split('\t')))

# --- Commodity List (from user) ---
commodity_list = """
Cattle
Goats
Sheep
Cotton(Ginned and Un-ginned)
All Flowers
Bajra
Jau
Jowar
Kambu
Maize
Navane
Paddy
Ragi
Rice
Save
Wheat
Antwala
Bamboo
Canes
Hippe Seeds
Honge Seeds
Neem Seeds
Soap Nuts
Tamarind
Tamarind Seeds
Apple
Banana
Borehannu
Citrus Fruits
Chakkothaihannu
Guava
Grapes
Jack Fruit
Jamun
Lemon
Kharbuja
Mango
Mosumbi
Marasebu
Pine apple
Pappaya
Pamogranate
Sapota
Siddota
Orange
Watermelon
Groundnut (Shelled and Unshelled)
Castor Seeds
Cotton seeds
Linseed
Mustard
Niger seeds
Safflower
Seasamum
Sunflower seeds
Soyabean
Cashewnut
Chillies(Dry)
Coconut
Copra
Corriander
Garlic
Ginger
Methi
Pepper
Turmeric
Alsande(Cowpea)(Whole & Split)
Avare(Whole & Split)
Bengalgram(Whole & Split)
Blackgram (Whole & Split)
Bullar (Whole & Split)
Greengram (Whole & Split)
Horse Gram
Lakh (Whole & Split)
Matki (Whole & Split)
Masoor (whole & Split)
Peas
Tur (Whole & Split)
Moath (Whole & Split)
All Vegetables [except Gherkin(including leafy)]
Goourds
Green Chillies
Onion
Potato
Suvarnagadde
Sweet Potato
Tomato
Beete(Rose)
Bilwala
Firewood
Ganjan
Hadga
Haldi
Hanimattal
Honne
Iyani
Jacktree
Jamba
Kalan
Kindal
Mango
Mathi
Nandi
Rampatre
Teak
White Cedar
Silver Oak
Eucalyptus
Betal leaves
Jaggery
Seegu
Dry grapes
"""
commodity_list = list(filter(None, commodity_list.strip().split('\n')))

# --- Month selection ---
months_full = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
               'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
months_options = ['All'] + months_full
selected_months = st.multiselect("Select Month(s):", options=months_options, default='All')
if 'All' in selected_months:
    selected_months = months_full

# --- Year range input ---
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

# --- Commodity selection ---
selected_commodity = st.selectbox("Select Commodity:", commodity_list)

# --- Market selection ---
selected_markets = st.multiselect("Select Market(s):", options=market_list, default=market_list)

# --- Scrape button ---
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
