import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="Cosmic Ray Data Explorer", layout="wide")
st.title("☄️ Cosmic Ray Data Explorer")
st.markdown("Explore cosmic ray spectra from real space missions (Voyager, AMS-02, etc.) using CRDB data.")

# Define sources and particles (you can expand this)
sources = ['Voyager', 'AMS02', 'PAMELA']
particles = ['Proton', 'Helium', 'Electron']

# Sidebar selection
source = st.sidebar.selectbox("Select Cosmic Ray Source", sources)
particle = st.sidebar.selectbox("Select Particle Type", particles)

# Fetch data from CRDB
def fetch_crdb_data(source, particle):
    base_url = "https://tools.ssdc.asi.it/CRDB/get_data.php"
    params = {
        'exp': source,
        'nuc': particle,
        'flux': '1',
        'format': 'json'
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        try:
            data_json = response.json()
            df = pd.DataFrame(data_json['data'], columns=['Ekn', 'Ekn_err', 'Flux', 'Flux_err'])
            return df
        except Exception as e:
            st.error("Error parsing CRDB data: " + str(e))
            return None
    else:
        st.error("Failed to fetch data from CRDB.")
        return None

# Load and display plot
data = fetch_crdb_data(source, particle)

if data is not None and not data.empty:
    st.subheader(f"{particle} Flux from {source}")
    fig, ax = plt.subplots()
    ax.errorbar(data['Ekn'], data['Flux'], yerr=data['Flux_err'], fmt='o', ecolor='red', capsize=2)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("Kinetic Energy per Nucleon [GeV/n]")
    ax.set_ylabel("Flux [particles / m² sr s GeV/n]")
    ax.set_title(f"{particle} Spectrum from {source}")
    ax.grid(True, which="both", ls="--")
    st.pyplot(fig)
else:
    st.warning("No data available or failed to fetch.")
