import streamlit as st
import leafmap.foliumap as leafmap
import os
import json  # untuk parsing geojson string ke dict

# Sidebar
markdown = """
Rencana Pertanian Perkebunan Di Kabupaten Pekalongan  
"""
st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Judul halaman
st.title("RENCANA PERTANIAN")
st.info("Peta menggunakan basemap: OpenStreetMap")

# Buat objek peta
m = leafmap.Map(
    locate_control=True,
    latlon_control=True,
    draw_export=True,
    minimap_control=True
)

# Tambahkan basemap OpenStreetMap
m.add_basemap("OpenStreetMap")

# Tambahkan GeoJSON rencana pertanian dengan style warna
geojson_path = "Data_Login/rencana pertanian.json"
if os.path.exists(geojson_path):
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_str = f.read()
    
    # Parsing string geojson jadi dict
    geojson_obj = json.loads(geojson_str)

    # Definisikan fungsi style berdasarkan 'keterangan'
    def style_function(feature):
        keterangan = feature['properties'].get('KETERANGAN', '').lower()
        if "pertanian lahan basah" in keterangan:
            fillColor = '#228B22'  # Hijau
        elif "pertanian lahan kering" in keterangan:
            fillColor = '#FFD700'  # Kuning
        else:
            fillColor = '#808080'  # Abu-abu default
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
            'color': 'blue',      # Warna garis batas kecamatan
            'weight': 2,          # Ketebalan garis
            'fillOpacity': 0      # Tidak fill area
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
<div style="display: flex; align-items: center; margin-bottom: 4px;">
    <div style="background-color: #228B22; width: 20px; height: 20px; margin-right: 8px; border: 1px solid black;"></div>
    Pertanian Lahan Basah
</div>
<div style="display: flex; align-items: center;">
    <div style="background-color: #FFD700; width: 20px; height: 20px; margin-right: 8px; border: 1px solid black;"></div>
    Pertanian Lahan Kering
</div>
<div style="display: flex; align-items: center; margin-top: 8px;">
    <div style="border: 2px solid blue; width: 20px; height: 20px; margin-right: 8px;"></div>
    Batas Kecamatan
</div>
"""
st.markdown(legend_html, unsafe_allow_html=True)
