# In[1]:

import streamlit as st
import folium
import json
import random
from IPython.display import IFrame
from streamlit_folium import st_folium

# ====================
# 1. Load File GeoJSON
# ====================
pertanian_path = "rencana pertanian.json"
batas_path = "batas kecamatan.json"
output_path = "peta_rencana_pertanian_dengan_legenda.html"

with open(pertanian_path, "r", encoding="utf-8") as f:
    pertanian_data = json.load(f)

with open(batas_path, "r", encoding="utf-8") as f:
    batas_data = json.load(f)

# ==============================
# 2. Ambil Kategori dan Warna
# ==============================
kategori_field = "KETERANGAN"
kategori_vals = list(set(f["properties"].get(kategori_field, "Lainnya") for f in pertanian_data["features"]))
kategori_colors = {val: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for val in kategori_vals}

# =====================
# 3. Inisialisasi Peta
# =====================
m = folium.Map(location=[-6.85, 109.65], zoom_start=11, tiles="OpenStreetMap")

# ================================
# 4. Tambahkan Layer Pertanian
# ================================
pertanian_layer = folium.FeatureGroup(name="Rencana Pertanian")
folium.GeoJson(
    pertanian_data,
    style_function=lambda feature: {
        "fillColor": kategori_colors.get(feature["properties"].get(kategori_field, "Lainnya"), "#000000"),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.6,
    },
    tooltip=folium.GeoJsonTooltip(fields=[kategori_field])
).add_to(pertanian_layer)
pertanian_layer.add_to(m)

# ================================
# 5. Tambahkan Layer Batas Kecamatan
# ================================
batas_layer = folium.FeatureGroup(name="Batas Kecamatan")
folium.GeoJson(
    batas_data,
    style_function=lambda feature: {
        "color": "blue",
        "weight": 2,
        "fillOpacity": 0
    },
    tooltip=folium.GeoJsonTooltip(fields=["KEC"])
).add_to(batas_layer)
batas_layer.add_to(m)

# ================================
# 6. Tambahkan Legenda Pertanian
# ================================
legend_html = """
<div style="position: fixed;
     bottom: 30px; left: 30px; width: 300px; height: auto;
     z-index:9999; background-color:white; border:2px solid grey;
     padding: 10px; font-size:14px;">
     <b>Legenda Rencana Pertanian</b><br>
"""
for val, color in kategori_colors.items():
    legend_html += f'<i style="background:{color};width:18px;height:18px;float:left;margin-right:8px;"></i>{val}<br>'
legend_html += "</div>"

m.get_root().html.add_child(folium.Element(legend_html))

# ================================
# 7. Simpan dan Tampilkan
# ================================
folium.LayerControl(collapsed=False).add_to(m)
m.save(output_path)
IFrame(output_path, width='100%', height=600)



# In[2]:

import streamlit as st
import folium
import json
import random
from IPython.display import IFrame
from streamlit_folium import st_folium

# ====================
# 1. Load File GeoJSON
# ====================
perkebunan_path = "peruntukan perkebunan.json"
batas_path = "batas kecamatan.json"
output_path = "peta_peruntukan_perkebunan.html"

with open(perkebunan_path, "r", encoding="utf-8") as f:
    perkebunan_data = json.load(f)

with open(batas_path, "r", encoding="utf-8") as f:
    batas_data = json.load(f)

# ==============================
# 2. Ambil Kategori dan Warna
# ==============================
kategori_field = "KETERANGAN"
kategori_vals = list(set(f["properties"].get(kategori_field, "Lainnya") for f in perkebunan_data["features"]))
kategori_colors = {val: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for val in kategori_vals}

# =====================
# 3. Inisialisasi Peta
# =====================
m = folium.Map(location=[-6.87, 109.65], zoom_start=11, tiles="OpenStreetMap")

# ================================
# 4. Tambahkan Layer Perkebunan
# ================================
perkebunan_layer = folium.FeatureGroup(name="Peruntukan Perkebunan")
folium.GeoJson(
    perkebunan_data,
    style_function=lambda feature: {
        "fillColor": kategori_colors.get(feature["properties"].get(kategori_field, "Lainnya"), "#000000"),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.6,
    },
    tooltip=folium.GeoJsonTooltip(fields=[kategori_field])
).add_to(perkebunan_layer)
perkebunan_layer.add_to(m)

# ================================
# 5. Tambahkan Layer Batas Kecamatan
# ================================
batas_layer = folium.FeatureGroup(name="Batas Kecamatan")
folium.GeoJson(
    batas_data,
    style_function=lambda feature: {
        "color": "blue",
        "weight": 2,
        "fillOpacity": 0
    },
    tooltip=folium.GeoJsonTooltip(fields=["KEC"])
).add_to(batas_layer)
batas_layer.add_to(m)

# ================================
# 6. Tambahkan Legenda Perkebunan
# ================================
legend_html = """
<div style="position: fixed;
     bottom: 30px; left: 30px; width: 280px; height: auto;
     z-index:9999; background-color:white; border:2px solid grey;
     padding: 10px; font-size:14px;">
     <b>Legenda Peruntukan Perkebunan</b><br>
"""
for val, color in kategori_colors.items():
    legend_html += f'<i style="background:{color};width:18px;height:18px;float:left;margin-right:8px;"></i>{val}<br>'
legend_html += "</div>"

m.get_root().html.add_child(folium.Element(legend_html))

# ================================
# 7. Simpan dan Tampilkan
# ================================
folium.LayerControl(collapsed=False).add_to(m)
m.save(output_path)
IFrame(output_path, width='100%', height=600)



# In[3]:

import streamlit as st
import folium
import json
import random
from IPython.display import IFrame
from streamlit_folium import st_folium

# ====================
# 1. Load File GeoJSON
# ====================
agropolitan_path = "kaw agropolytan.json"
batas_path = "batas kecamatan.json"
output_path = "peta_agropolitan_dengan_legenda.html"

with open(agropolitan_path, "r", encoding="utf-8") as f:
    agropolitan_data = json.load(f)

with open(batas_path, "r", encoding="utf-8") as f:
    batas_data = json.load(f)

# ==============================
# 2. Ambil Kategori dan Warna
# ==============================
kategori_field = "KAW_AGROPL"
kategori_vals = list(set(f["properties"].get(kategori_field, "Lainnya") for f in agropolitan_data["features"]))
kategori_colors = {val: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for val in kategori_vals}

# =====================
# 3. Inisialisasi Peta
# =====================
m = folium.Map(location=[-6.95, 109.7], zoom_start=11, tiles="OpenStreetMap")

# ================================
# 4. Tambahkan Layer Agropolitan
# ================================
agropolitan_layer = folium.FeatureGroup(name="Kawasan Agropolitan")
folium.GeoJson(
    agropolitan_data,
    style_function=lambda feature: {
        "fillColor": kategori_colors.get(feature["properties"].get(kategori_field, "Lainnya"), "#000000"),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.6,
    },
    tooltip=folium.GeoJsonTooltip(fields=[kategori_field])
).add_to(agropolitan_layer)
agropolitan_layer.add_to(m)

# ================================
# 5. Tambahkan Layer Batas Kecamatan
# ================================
batas_layer = folium.FeatureGroup(name="Batas Kecamatan")
folium.GeoJson(
    batas_data,
    style_function=lambda feature: {
        "color": "blue",
        "weight": 2,
        "fillOpacity": 0
    },
    tooltip=folium.GeoJsonTooltip(fields=["KEC"])
).add_to(batas_layer)
batas_layer.add_to(m)

# ================================
# 6. Tambahkan Legenda Agropolitan
# ================================
legend_html = """
<div style="position: fixed;
     bottom: 30px; left: 30px; width: 280px; height: auto;
     z-index:9999; background-color:white; border:2px solid grey;
     padding: 10px; font-size:14px;">
     <b>Legenda Kawasan Agropolitan</b><br>
"""
for val, color in kategori_colors.items():
    legend_html += f'<i style="background:{color};width:18px;height:18px;float:left;margin-right:8px;"></i>{val}<br>'
legend_html += "</div>"

m.get_root().html.add_child(folium.Element(legend_html))

# ================================
# 7. Simpan dan Tampilkan
# ================================
folium.LayerControl(collapsed=False).add_to(m)
m.save(output_path)
IFrame(output_path, width='100%', height=600)


# In[6]:

import streamlit as st
import folium
import json
import random
from IPython.display import IFrame
from streamlit_folium import st_folium

# ====================
# 1. Load File GeoJSON
# ====================
agro_point_path = "renc kaw strategis ek agropolytan.json"
batas_path = "batas kecamatan.json"
output_path = "peta_strategis_ekonomi_agropolitan_kepanjangan.html"

with open(agro_point_path, "r", encoding="utf-8") as f:
    agro_point_data = json.load(f)

with open(batas_path, "r", encoding="utf-8") as f:
    batas_data = json.load(f)

# ======================================
# 2. Ambil Kategori dan Pemetaan Warna
# ======================================
kategori_field = "AGROPOLYTA"
kategori_vals = list(set(f["properties"].get(kategori_field, "Lainnya") for f in agro_point_data["features"]))
kategori_colors = {val: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for val in kategori_vals}

# ======================================
# 3. Pemetaan Kepanjangan Nama
# ======================================
agropolitan_kepanjangan = {
    "KTU": "Kawasan Terpadu Utama",
    "KSP": "Kawasan Strategis Produksi",
    "KSE A": "Kawasan Strategis Ekonomi Agropolitan A",
    "KSE B": "Kawasan Strategis Ekonomi Agropolitan B",
    "KSE C": "Kawasan Strategis Ekonomi Agropolitan C",
    "KSE D": "Kawasan Strategis Ekonomi Agropolitan D",
    "Lainnya": "Lainnya"
}

# =====================
# 4. Inisialisasi Peta
# =====================
m = folium.Map(location=[-7.05, 109.7], zoom_start=11, tiles="OpenStreetMap")

# ===================================================
# 5. Tambahkan Layer Titik Kawasan Strategis Agropolitan
# ===================================================
agro_point_layer = folium.FeatureGroup(name="Kawasan Strategis Ekonomi Agropolitan")
for feature in agro_point_data["features"]:
    coords = feature["geometry"]["coordinates"]
    kategori = feature["properties"].get(kategori_field, "Lainnya")
    warna = kategori_colors.get(kategori, "#000000")
    label = agropolitan_kepanjangan.get(kategori, kategori)
    
    folium.CircleMarker(
        location=[coords[1], coords[0]],
        radius=6,
        color=warna,
        fill=True,
        fill_color=warna,
        fill_opacity=0.8,
        tooltip=label
    ).add_to(agro_point_layer)
agro_point_layer.add_to(m)

# ================================
# 6. Tambahkan Layer Batas Kecamatan
# ================================
batas_layer = folium.FeatureGroup(name="Batas Kecamatan")
folium.GeoJson(
    batas_data,
    style_function=lambda feature: {
        "color": "blue",
        "weight": 2,
        "fillOpacity": 0
    },
    tooltip=folium.GeoJsonTooltip(fields=["KEC"])
).add_to(batas_layer)
batas_layer.add_to(m)

# ================================
# 7. Tambahkan Legenda (Kepanjangan)
# ================================
legend_html = """
<div style="position: fixed;
     bottom: 30px; left: 30px; width: 320px; height: auto;
     z-index:9999; background-color:white; border:2px solid grey;
     padding: 10px; font-size:14px;">
     <b>Legenda Kawasan Strategis Ekonomi Agropolitan</b><br>
"""
for val, color in kategori_colors.items():
    label = agropolitan_kepanjangan.get(val, val)
    legend_html += f'<i style="background:{color};width:18px;height:18px;float:left;margin-right:8px;"></i>{label}<br>'
legend_html += "</div>"

m.get_root().html.add_child(folium.Element(legend_html))

# ================================
# 8. Simpan dan Tampilkan
# ================================
folium.LayerControl(collapsed=False).add_to(m)
m.save(output_path)
IFrame(output_path, width='100%', height=600)
