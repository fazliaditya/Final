import streamlit as st
import folium
import json
import random
from streamlit_folium import st_folium


# ==================== LOAD GEOJSON ====================
def load_geojson(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==================== GENERATE COLOR ====================
def generate_colors(categories):
    random.seed(42)
    return {cat: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for cat in categories}


# ==================== BASE MAP OPTIONS ====================
def add_base_maps(m):
    folium.TileLayer(
        tiles="OpenStreetMap",
        name="OpenStreetMap"
    ).add_to(m)

    folium.TileLayer(
        tiles="Stamen Terrain",
        name="Terrain",
        attr="Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    ).add_to(m)

    folium.TileLayer(
        tiles="Stamen Toner",
        name="Toner",
        attr="Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    ).add_to(m)

    folium.TileLayer(
        tiles="CartoDB positron",
        name="Positron",
        attr="Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    ).add_to(m)

    folium.TileLayer(
        tiles="CartoDB dark_matter",
        name="Dark Matter",
        attr="Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    ).add_to(m)

    # Custom tile (dengan attribution wajib)
    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="© OpenStreetMap contributors",
        name="Custom OpenStreetMap"
    ).add_to(m)

    folium.LayerControl().add_to(m)


# ==================== TAMPILKAN PETA DENGAN GEOJSON ====================
def show_map(title, geojson_data, color_field):
    st.subheader(title)

    kategori = list(set(f["properties"].get(color_field, "Lainnya") for f in geojson_data["features"]))
    warna = generate_colors(kategori)

    m = folium.Map(location=[-6.9, 109.65], zoom_start=11)
    add_base_maps(m)

    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            "fillColor": warna.get(feature["properties"].get(color_field, "Lainnya"), "#000000"),
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.6,
        },
        tooltip=folium.GeoJsonTooltip(fields=[color_field])
    ).add_to(m)

    # Legenda
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 30px; left: 30px; width: 280px; max-height: 250px;
        overflow-y: auto; background-color: white;
        border:2px solid grey; padding: 10px; font-size:14px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    ">
        <b>Legenda {title}</b><br>
    """
    for val, color in warna.items():
        legend_html += f'<i style="background:{color};width:18px;height:18px;float:left;margin-right:8px;"></i>{val}<br>'
    legend_html += "</div>"
    m.get_root().html.add_child(folium.Element(legend_html))

    st_folium(m, width=700, height=600)


# ==================== TAMPILKAN TITIK AGROPOLITAN ====================
def show_agro_point():
    data = load_geojson("renc kaw strategis ek agropolytan.json")
    agropolitan_kepanjangan = {
        "KTU": "Kawasan Terpadu Utama",
        "KSP": "Kawasan Strategis Produksi",
        "KSE A": "Kawasan Strategis Ekonomi Agropolitan A",
        "KSE B": "Kawasan Strategis Ekonomi Agropolitan B",
        "KSE C": "Kawasan Strategis Ekonomi Agropolitan C",
        "KSE D": "Kawasan Strategis Ekonomi Agropolitan D",
        "Lainnya": "Lainnya"
    }

    kategori = list(set(f["properties"].get("AGROPOLYTA", "Lainnya") for f in data["features"]))
    warna = generate_colors(kategori)

    m = folium.Map(location=[-6.9, 109.65], zoom_start=11)
    add_base_maps(m)

    for feature in data["features"]:
        coords = feature["geometry"]["coordinates"]
        kategori = feature["properties"].get("AGROPOLYTA", "Lainnya")
        label = agropolitan_kepanjangan.get(kategori, kategori)
        color = warna.get(kategori, "#000000")

        folium.CircleMarker(
            location=[coords[1], coords[0]],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            tooltip=label
        ).add_to(m)

    # Legenda
    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px; left: 30px; width: 300px;
        background-color: white; padding: 10px;
        border: 2px solid grey; font-size:14px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    ">
        <b>Legenda Titik Kawasan Strategis</b><br>
    """
    for val, color in warna.items():
        label = agropolitan_kepanjangan.get(val, val)
        legend_html += f'<i style="background:{color};width:18px;height:18px;float:left;margin-right:8px;"></i>{label}<br>'
    legend_html += "</div>"
    m.get_root().html.add_child(folium.Element(legend_html))

    st_folium(m, width=700, height=600)


# ==================== MAIN STREAMLIT APP ====================
def main():
    st.set_page_config(layout="wide")
    st.title("Peta Rencana dan Kawasan Strategis")

    menu = st.sidebar.radio("Pilih Menu:", [
        "Rencana Pertanian",
        "Peruntukan Perkebunan",
        "Kawasan Agropolitan",
        "Rencana Kawasan Strategis Ekonomi Agropolitan"
    ])

    if menu == "Rencana Pertanian":
        data = load_geojson("rencana pertanian.json")
        show_map("Rencana Pertanian", data, "KETERANGAN")

    elif menu == "Peruntukan Perkebunan":
        data = load_geojson("peruntukan perkebunan.json")
        show_map("Peruntukan Perkebunan", data, "KETERANGAN")

    elif menu == "Kawasan Agropolitan":
        data = load_geojson("kaw agropolytan.json")
        show_map("Kawasan Agropolitan", data, "KAW_AGROPL")

    elif menu == "Rencana Kawasan Strategis Ekonomi Agropolitan":
        show_agro_point()


# ==================== RUN APP ====================
if __name__ == "__main__":
    main()
