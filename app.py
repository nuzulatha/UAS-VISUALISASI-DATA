#!pip install streamlit
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Mengatur konfigurasi dasar halaman web
st.set_page_config(page_title="Dashboard UAS Visualisasi", layout="wide")
st.title("Dashboard Profil Sosial-Ekonomi Indonesia")
st.write("Eksplorasi data kemiskinan, multivariat, dan struktur pengeluaran.")

# 2. Membuat Tab Menu agar 3 tugas UAS Anda rapi dalam satu web
tab1, tab2, tab3 = st.tabs(["Peta Geospasial", "Reduksi Dimensi (PCA)", "Hierarki Pengeluaran"])

# 3. Memasukkan visualisasi ke Tab 3
with tab3:
    st.header("Struktur Pengeluaran Rumah Tangga")
    
    # Menyiapkan data sederhana
    data = [
        ['Total', 'Makanan', 'Padi-padian', 94641, 89278],
        ['Total', 'Makanan', 'Rokok', 94476, 91708],
        ['Total', 'Bukan Makanan', 'Perumahan', 391751, 398657]
    ]
    df = pd.DataFrame(data, columns=['Level_1', 'Level_2', 'Level_3', 'Maret_2024', 'Maret_2025'])
    df['Pertumbuhan (%)'] = ((df['Maret_2025'] - df['Maret_2024']) / df['Maret_2024']) * 100

    # Membuat grafik Treemap dengan Plotly
    fig = px.treemap(df, path=['Level_1', 'Level_2', 'Level_3'], values='Maret_2025', color='Pertumbuhan (%)', color_continuous_scale='RdYlGn')
    
    # 4. PERINTAH AJAIB STREAMLIT: Memunculkan grafik ke web
    st.plotly_chart(fig, use_container_width=True)
