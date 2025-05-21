import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
Rencana Pertanian Perkebunan Di Kabupaten Pekalongan 

"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("Peta Gabungan Rencana Pertanian, Perkebunan, Agropolitan, dan Kawasan Strategis")


