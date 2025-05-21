import streamlit as st
from leafmap.foliumap import Map
import os
import json
import folium

# Sidebar
markdown = """
Rencana Pertanian Perkebunan Di Kabupaten Pekalongan
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Judul halaman
st.title("Rencana Kawasan Strategis")
st.info("Peta menggunakan basemap: OpenStreetMap")


# Tata letak peta
col1 = st.columns([1])[0]  # Hanya satu kolom tanpa selectbox

with col1:
    # Buat objek peta
    m = Map(
        locate_control=True,
        latlon_control=True,
        draw_export=True,
        minimap_control=True
    )

    # Tambahkan basemap default
    m.add_basemap("OpenTopoMap")

    # Path ke geojson titik
    geojson_path = "Data_Login/renc kaw strategis ek agropolytan.json"
    if os.path.exists(geojson_path):
        with open(geojson_path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        # Kamus agropolitan
        agropolitan_kepanjangan = {
            "KTU": "Kawasan Terpadu Utama",
            "KSP": "Kawasan Strategis Produksi",
            "KSE A": "Kawasan Strategis Ekonomi Agropolitan A",
            "KSE B": "Kawasan Strategis Ekonomi Agropolitan B",
            "KSE C": "Kawasan Strategis Ekonomi Agropolitan C",
            "KSE D": "Kawasan Strategis Ekonomi Agropolitan D",
            "Lainnya": "Lainnya"
        }

        for feature in geojson_data['features']:
            geometry = feature.get("geometry", {})
            properties = feature.get("properties", {})
            agropolyta_code = properties.get("AGROPOLYTA", "").strip().upper()
            coords = geometry.get("coordinates", [])

            # Ambil nama panjang berdasarkan kode AGROPOLYTA
            keterangan_lengkap = agropolitan_kepanjangan.get(agropolyta_code, "Lainnya")

            # Tentukan warna berdasarkan nama panjang
            if "produksi" in keterangan_lengkap.lower():
                color = "purple"
            elif "terpadu utama" in keterangan_lengkap.lower():
                color = "green"
            elif "ekonomi" in keterangan_lengkap.lower():
                color = "#FFD700"
            else:
                color = "gray"

            # Tambahkan bulatan (CircleMarker)
            if geometry.get("type") == "Point" and len(coords) == 2:
                lon, lat = coords
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=6,
                    color='black',
                    weight=1,
                    fill=True,
                    fill_color=color,
                    fill_opacity=1,
                    popup=keterangan_lengkap
                ).add_to(m)

    else:
        st.error(f"File '{geojson_path}' tidak ditemukan.")

    # Tambahkan batas kecamatan
    batas_kecamatan_path = "Data_Login/batas kecamatan.json"
    if os.path.exists(batas_kecamatan_path):
        with open(batas_kecamatan_path, "r", encoding="utf-8") as f:
            batas_kecamatan_geojson = json.load(f)

        def batas_style(feature):
            return {
                'color': 'blue',
                'weight': 2,
                'fillOpacity': 0
            }

        m.add_geojson(
            batas_kecamatan_geojson,
            layer_name="Batas Kecamatan",
            style_function=batas_style,
            show=True
        )
    else:
        st.warning(f"File '{batas_kecamatan_path}' tidak ditemukan.")

    # Tampilkan peta
    m.to_streamlit(height=700)

# Legenda warna
legend_html = """
<b>Legenda Warna</b><br>
<div style="display: flex; align-items: center; margin-top: 8px;">
    <div style="background-color: purple; width: 20px; height: 20px; border: 1px solid black; margin-right: 8px;"></div>
    Kawasan Strategis Produksi
</div>
<div style="display: flex; align-items: center; margin-top: 8px;">
    <div style="background-color: green; width: 20px; height: 20px; border: 1px solid black; margin-right: 8px;"></div>
    Kawasan Terpadu Utama
</div>
<div style="display: flex; align-items: center; margin-top: 8px;">
    <div style="border: 2px solid blue; width: 20px; height: 20px; margin-right: 8px;"></div>
    Batas Kecamatan
</div>
"""
st.markdown(legend_html, unsafe_allow_html=True)
