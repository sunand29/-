# cosmic_ray_explorer_noaa.py

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="NOAA Cosmic Ray Explorer", layout="wide")

st.title("☄️ NOAA Cosmic Ray Explorer")
st.markdown("""
Real-time **proton flux vs. energy** from NOAA GOES satellites.  
Source: [NOAA SWPC](https://www.swpc.noaa.gov/products/goes-proton-flux)
""")

# ✅ NOAA API
noaa_url = "https://services.swpc.noaa.gov/json/goes/primary/differential-proton-flux-1-day.json"

st.info("Fetching latest proton flux data from NOAA...")

try:
    response = requests.get(noaa_url)
    raw_data = response.json()

    df = pd.DataFrame(raw_data)
    df['time_tag'] = pd.to_datetime(df['time_tag'])

    # Get the latest flux for each energy channel
    latest_flux = df.groupby('energy').tail(1)
    latest_flux = latest_flux.sort_values('energy')

    # Clean columns
    latest_flux = latest_flux[['energy', 'flux', 'satellite', 'time_tag']]

    # Plot using matplotlib
    fig, ax = plt.subplots()
    for sat in latest_flux['satellite'].unique():
        sat_data = latest_flux[latest_flux['satellite'] == sat]
        ax.plot(sat_data['energy'], sat_data['flux'], marker='o', linestyle='-', label=f"GOES-{sat}")

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("Energy [MeV]")
    ax.set_ylabel("Proton Flux [particles/cm²·s·sr·MeV]")
    ax.set_title("Latest Proton Flux from NOAA GOES")
    ax.grid(True, which='both', linestyle='--', alpha=0.4)
    ax.legend()

    st.pyplot(fig)
    st.dataframe(latest_flux)

    st.download_button("⬇️ Download CSV", latest_flux.to_csv(index=False), file_name="noaa_goes_proton_flux.csv")

except Exception as e:
    st.error(f"❌ Failed to fetch NOAA data: {e}")
