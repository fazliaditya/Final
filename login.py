import streamlit as st
from db_handler import authenticate_user, create_users_table, register_user
import time

create_users_table()

def login_page():
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
                display: none;
            }
            .block-container {
                padding-left: 2rem;
                padding-right: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, _, col2 = st.columns([10, 1, 10])
    
    with col1:
        st.image("Logo-Olivia-X-2025.png")
    
    with col2:
        st.title("Login / Sign Up")
        email = st.text_input("E-mail")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password (for Sign Up)", type="password")

        col_login, col_signup = st.columns(2)

        with col_login:
            if st.button("Login"):
                time.sleep(1)
                if not (email and password):
                    st.error("Please provide email and password")
                elif authenticate_user(email, password):
                    st.session_state['authenticated'] = True
                    st.session_state['page'] = 'home'
                    st.rerun()
                else:
                    st.error("Invalid login credentials")

        with col_signup:
            if st.button("Sign Up"):
                if not (email and password and confirm_password):
                    st.error("Please fill all fields for registration")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    if register_user(email, password):
                        st.success("Registration successful. You can now log in.")
                    else:
                        st.error("Email already registered")

def home_page():
    st.set_page_config(layout="wide")
    st.sidebar.title("Keterangan")
    st.sidebar.info("WebGIS ini menampilkan peta interaktif yang mencakup rencana lahan pertanian dan perkebunan, kawasan agropolitan, serta kawasan strategis agropolitan, berdasarkan data RTRW dari BAPPEDA dan Dinas Pekerjaan Umum, guna mendukung perencanaan wilayah agraris yang terarah dan berkelanjutan")
    st.sidebar.image("Logo Pertanian.png")
    st.title("Halaman login WebGIS ini merupakan pintu masuk menuju sistem informasi geografis yang dirancang untuk menampilkan rencana pengembangan wilayah pertanian dan perkebunan. Sistem ini dibangun dengan dasar data spasial dan perencanaan yang bersumber dari dokumen RTRW (Rencana Tata Ruang Wilayah) milik Bappeda serta informasi teknis dari Dinas Pekerjaan Umum")
    st.success("Berhasil login")

    if st.button("Logout"):
        st.session_state.clear()
        st.session_state['page'] = 'login'
        st.rerun()

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'home':
        home_page()

if __name__ == "__main__":
    main()
