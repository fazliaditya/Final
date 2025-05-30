import streamlit as st
import leafmap.foliumap as leafmap
import os
import json  # perlu untuk parsing geojson string ke dict

# Sidebar
markdown = """
Peta ini menampilkan kawasan agropolitan, yaitu wilayah pedesaan yang dikembangkan secara terencana sebagai pusat pertumbuhan berbasis pertanian dan agribisnis
Data dan delineasi kawasan ini merujuk pada dokumen
RTRW yang disusun oleh BAPPEDA
"""
st.sidebar.title("Keterangan")
st.sidebar.info(markdown)
logo = "Logo Pertanian.png"
st.sidebar.image(logo)

# Judul halaman
st.title("Peta Kawasan Agropolitan")
st.info("Peta menggunakan basemap: OpenStreetMap")


# Layout untuk peta (tanpa selectbox basemap)
m = leafmap.Map(
    locate_control=True,
    latlon_control=True,
    draw_export=True,
    minimap_control=True
)

# Gunakan OpenStreetMap sebagai basemap default
m.add_basemap("OpenStreetMap")

# Tambahkan GeoJSON rencana pertanian dengan style warna
geojson_path = "Data_Login/kaw agropolytan.json"
if os.path.exists(geojson_path):
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_str = f.read()
    
    # Parsing string geojson jadi dict
    geojson_obj = json.loads(geojson_str)

    # Definisikan fungsi style berdasarkan 'keterangan'
    def style_function(feature):
        keterangan = feature['properties'].get('KAW_AGROPL', '').lower()
        if "sentral produksi" in keterangan:
            fillColor = 'purple'
        elif "kota tani" in keterangan:
            fillColor = '#FFD700'
        elif "kota tani utama" in keterangan:
            fillColor = "green"
        else:
            fillColor = '#808080'
        return {
            'fillColor': fillColor,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        }

    m.add_geojson(
        geojson_obj,
        layer_name="Rencana Pertanian",
        style_function=style_function
    )
else:
    st.error(f"File '{geojson_path}' tidak ditemukan.")

# Tambahkan batas kecamatan dari GeoJSON
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

# Zoom otomatis ke area geojson jika ada
try:
    m.fit_bounds(m.get_bounds())
except Exception:
    pass

# Tampilkan peta
m.to_streamlit(height=700)

# Tambahkan legenda warna di bawah peta
legend_html = """
<b>Legenda Warna</b><br>
<div style="display: flex; align-items: center;">
    <div style="background-color: purple; width: 20px; height: 20px; margin-right: 8px; border: 1px solid black;"></div>
    Kebun
</div>
<div style="display: flex; align-items: center; margin-top: 8px;">
    <div style="border: 2px solid blue; width: 20px; height: 20px; margin-right: 8px;"></div>
    Batas Kecamatan
</div>
"""
st.markdown(legend_html, unsafe_allow_html=True)
