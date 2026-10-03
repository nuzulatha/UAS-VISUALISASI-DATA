# %% Blok 1: Import Library & Setup Halaman
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Mengatur konfigurasi dasar halaman web
st.set_page_config(page_title="Dashboard UAS Visualisasi", layout="wide")
st.title("📊 Dashboard Profil Sosial-Ekonomi Indonesia")
st.write("Eksplorasi data kemiskinan, multivariat, dan struktur pengeluaran.")

# %% Blok 2: Load dan Preprocessing Data (Bisa di-Run untuk cek error data)
@st.cache_data # Mencegah data diload berulang kali saat web berjalan
def load_data():
    # --- Data Hierarki (Tab 3) ---
    data = [
        ['Total', 'Makanan', 'Padi-padian', 94641, 89278],
        ['Total', 'Makanan', 'Rokok', 94476, 91708],
        ['Total', 'Bukan Makanan', 'Perumahan', 391751, 398657]
    ]
    df_pengeluaran = pd.DataFrame(data, columns=['Level_1', 'Level_2', 'Level_3', 'Maret_2024', 'Maret_2025'])
    df_pengeluaran['Pertumbuhan (%)'] = ((df_pengeluaran['Maret_2025'] - df_pengeluaran['Maret_2024']) / df_pengeluaran['Maret_2024']) * 100

    # --- Data Geospasial (Tab 1) ---
    gdf_batas = gpd.read_file('data/kab_kota.geojson')
    df_miskin = pd.read_excel('data/Persentase_Penduduk_Miskin_dengan_Kode.xlsx')
    df_pdrb = pd.read_excel('data/PDRB_ADHB_KODE.xlsx')
    gdf_batas = gpd.read_file('data/kab_kota.geojson')

    print("Kolom Peta GeoJSON:", gdf_batas.columns.tolist()) # TAMBAHKAN INI
    
    df_miskin.columns = [str(col).replace('.0', '').strip() for col in df_miskin.columns]
    df_pdrb.columns = [str(col).replace('.0', '').strip() for col in df_pdrb.columns]

    # Cek outputnya (pasti semuanya sudah pakai tanda kutip dan rapi!)
    print("Kolom Miskin :", df_miskin.columns.tolist())
    print("Kolom PDRB :", df_pdrb.columns.tolist())

    # Filter tahun 2025 dan sesuaikan nama kolom
    df_miskin_25 = df_miskin[['Kode_Wilayah', 'Kab/Kota', '2025']].rename(columns={'2025': 'Pct_Miskin'})
    df_pdrb_25 = df_pdrb[['Kode_Wilayah', '2025']].rename(columns={'2025': 'PDRB'})

    # Ganti 'KODE_KAB' di bawah ini dengan nama kolom asli yang Anda temukan dari Langkah 1
    kolom_kode_peta = 'code' 
    
    # --- PROSES MERGE DATA ---
    
    # 1. Pastikan ketiga kunci wilayah menjadi string (teks)
    gdf_batas['code'] = gdf_batas['code'].astype(str)
    df_miskin_25['Kode_Wilayah'] = df_miskin_25['Kode_Wilayah'].astype(str)
    df_pdrb_25['Kode_Wilayah'] = df_pdrb_25['Kode_Wilayah'].astype(str)

    # 2. "Sapu Bersih" Jebakan Desimal (Memaksa '11.1' kembali menjadi '11.10')
    def rapikan_kode(x):
        try:
            return f"{float(x):.2f}"
        except ValueError:
            return str(x)

    gdf_batas['code'] = gdf_batas['code'].apply(rapikan_kode)
    df_miskin_25['Kode_Wilayah'] = df_miskin_25['Kode_Wilayah'].apply(rapikan_kode)
    df_pdrb_25['Kode_Wilayah'] = df_pdrb_25['Kode_Wilayah'].apply(rapikan_kode)

    # 3. Eksekusi merge (Sekarang dijamin aman!)
    gdf = gdf_batas.merge(df_miskin_25, left_on='code', right_on='Kode_Wilayah', how='left')
    gdf = gdf.merge(df_pdrb_25, left_on='code', right_on='Kode_Wilayah', how='left')

    # Titik pusat untuk lingkaran PDRB
    # Ekstrak koordinat X dan Y menjadi angka biasa agar aman dibaca Folium
    gdf['centroid_x'] = gdf.geometry.centroid.x
    gdf['centroid_y'] = gdf.geometry.centroid.y

    return df_pengeluaran, gdf

# Eksekusi fungsi load data
df_pengeluaran, gdf = load_data()
print("Blok 2 Selesai: Data berhasil dimuat!")

# %% Blok 3: Membuat Tab Menu
tab1, tab2, tab3 = st.tabs(["Peta Geospasial", "Reduksi Dimensi (PCA)", "Hierarki Pengeluaran"])

# %% Blok 4: Eksekusi Tab 3 (Hierarki Pengeluaran)
with tab3:
    st.header("Struktur Pengeluaran Rumah Tangga")
    
    # Membuat grafik Treemap dengan Plotly
    fig = px.treemap(
        df_pengeluaran, 
        path=['Level_1', 'Level_2', 'Level_3'], 
        values='Maret_2025', 
        color='Pertumbuhan (%)', 
        color_continuous_scale='RdYlGn'
    )
    
    # Memunculkan grafik ke web
    st.plotly_chart(fig, use_container_width=True)
    print("Blok 4 Selesai: Grafik Treemap siap!")

# %% Blok 5: Eksekusi Tab 1 (Peta Geospasial)
with tab1:
    st.header("Peta Kesejahteraan dan Ekonomi (2025)")
    
    # Inisialisasi Peta Dasar Folium
    m = folium.Map(location=[-0.789, 113.921], zoom_start=5, tiles='CartoDB positron')

    # Layer 1: Choropleth (Persentase Kemiskinan)
    choropleth = folium.Choropleth(
        geo_data=gdf,
        name='Persentase Kemiskinan (%)',
        data=gdf,
        columns=['code', 'Pct_Miskin'],
        key_on='feature.properties.code', # Pastikan properti di geojson Anda juga bernama persis seperti ini
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Persentase Penduduk Miskin 2025 (%)'
    ).add_to(m)

    # Tooltip Interaktif untuk Choropleth menggunakan kolom Kab/Kota
    tooltip = folium.GeoJsonTooltip(
        fields=['Kab/Kota', 'Pct_Miskin'],
        aliases=['Kabupaten/Kota:', 'Kemiskinan (%):'],
        localize=True
    )
    choropleth.geojson.add_child(tooltip)

    # Layer 2: Proportional Symbol (PDRB ADHB)
    pdrb_layer = folium.FeatureGroup(name="PDRB ADHB (Simbol Ukuran)")
    for idx, row in gdf.iterrows():
        if pd.notnull(row['PDRB']):
            radius_size = row['PDRB'] / 10000 
            
            folium.CircleMarker(
                location=[row['centroid_y'], row['centroid_x']],
                radius=radius_size,
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.5,
                tooltip=f"{row['Kab/Kota']} - PDRB: {row['PDRB']} Miliar"
            ).add_to(pdrb_layer)

    pdrb_layer.add_to(m)

    # Kontrol Layer
    folium.LayerControl(position='topright').add_to(m)

    # Memunculkan di Web Streamlit
    st_folium(m, width=1000, height=600)
    print("Blok 5 Selesai: Peta Folium siap!")

# #!pip install streamlit
# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # 1. Mengatur konfigurasi dasar halaman web
# st.set_page_config(page_title="Dashboard UAS Visualisasi", layout="wide")
# st.title("Dashboard Profil Sosial-Ekonomi Indonesia")
# st.write("Eksplorasi data kemiskinan, multivariat, dan struktur pengeluaran.")

# # 2. Membuat Tab Menu agar 3 tugas UAS Anda rapi dalam satu web
# tab1, tab2, tab3 = st.tabs(["Peta Geospasial", "Reduksi Dimensi (PCA)", "Hierarki Pengeluaran"])

# # 3. Memasukkan visualisasi ke Tab 3
# with tab3:
#     st.header("Struktur Pengeluaran Rumah Tangga")
    
#     # Menyiapkan data sederhana
#     data = [
#         ['Total', 'Makanan', 'Padi-padian', 94641, 89278],
#         ['Total', 'Makanan', 'Rokok', 94476, 91708],
#         ['Total', 'Bukan Makanan', 'Perumahan', 391751, 398657]
#     ]
#     df = pd.DataFrame(data, columns=['Level_1', 'Level_2', 'Level_3', 'Maret_2024', 'Maret_2025'])
#     df['Pertumbuhan (%)'] = ((df['Maret_2025'] - df['Maret_2024']) / df['Maret_2024']) * 100

#     # Membuat grafik Treemap dengan Plotly
#     fig = px.treemap(df, path=['Level_1', 'Level_2', 'Level_3'], values='Maret_2025', color='Pertumbuhan (%)', color_continuous_scale='RdYlGn')
    
#     # 4. PERINTAH AJAIB STREAMLIT: Memunculkan grafik ke web
#     st.plotly_chart(fig, use_container_width=True)

# import streamlit as st
# import geopandas as gpd
# import pandas as pd
# import folium
# from streamlit_folium import st_folium

# st.title("Peta Kesejahteraan dan Ekonomi (2025)")

# # 1. Membaca Data dari Folder 'data'
# # (Asumsi data sudah dibersihkan dan memiliki kolom kunci yang sama, misal 'KODE_KAB')
# gdf_batas = gpd.read_file('data/kab_kota.geojson')
# df_miskin = pd.read_excel('data/Persentase_Penduduk_Miskin_dengan_Kode.xlsx')
# df_pdrb = pd.read_excel('data/PDRB_ADHB_KODE.xlsx')

# # Filter untuk mengambil tahun 2025 saja (sesuaikan nama kolom Anda)
# df_miskin_25 = df_miskin[['Kode Wilayah', 'Kab_Kota', '2025']].rename(columns={'2025': 'Pct_Miskin'})
# df_pdrb_25 = df_pdrb[['Kode Wilayah', '2025']].rename(columns={'2025': 'PDRB'})

# # 2. Menggabungkan (Merge) Data Atribut ke Geometri Spasial
# gdf = gdf_batas.merge(df_miskin_25, on='Kode Wilayah', how='left')
# gdf = gdf.merge(df_pdrb_25, on='Kode Wilayah', how='left')

# # Mendapatkan titik pusat (centroid) tiap kab/kota untuk meletakkan simbol lingkaran PDRB
# gdf['centroid'] = gdf.geometry.centroid

# # 3. Inisialisasi Peta Dasar Folium (Titik tengah Indonesia)
# m = folium.Map(location=[-0.789, 113.921], zoom_start=5, tiles='CartoDB positron')

# # 4. Layer 1: Choropleth (Persentase Kemiskinan)
# choropleth = folium.Choropleth(
#     geo_data=gdf,
#     name='Persentase Kemiskinan (%)',
#     data=gdf,
#     columns=['Kode Wilayah', 'Pct_Miskin'],
#     key_on='feature.properties.KODE_KAB',
#     fill_color='YlOrRd', # Justifikasi warna: kuning ke merah
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Persentase Penduduk Miskin 2025 (%)'
# ).add_to(m)

# # Menambahkan Tooltip Interaktif untuk Choropleth
# tooltip = folium.GeoJsonTooltip(
#     fields=['Kab_Kota', 'Pct_Miskin'],
#     aliases=['Kabupaten/Kota:', 'Kemiskinan (%):'],
#     localize=True
# )
# choropleth.geojson.add_child(tooltip)
# kode

# # 5. Layer 2: Proportional Symbol (PDRB ADHB)
# pdrb_layer = folium.FeatureGroup(name="PDRB ADHB (Simbol Ukuran)")
# for idx, row in gdf.iterrows():
#     if pd.notnull(row['PDRB']):
#         # Skala ukuran lingkaran disesuaikan (dibagi angka tertentu agar tidak menutupi peta)
#         radius_size = row['PDRB'] / 10000 
        
#         folium.CircleMarker(
#             location=[row['centroid'].y, row['centroid'].x],
#             radius=radius_size,
#             color='blue',
#             fill=True,
#             fill_color='blue',
#             fill_opacity=0.5,
#             tooltip=f"{row['Kab_Kota']} - PDRB: {row['PDRB']} Miliar"
#         ).add_to(pdrb_layer)

# pdrb_layer.add_to(m)

# # 6. Menambahkan Kontrol Layer (Bisa menyalakan/mematikan peta tertentu)
# folium.LayerControl(position='topright').add_to(m)

# # 7. Memunculkan di Web Streamlit (Zoom, Pan sudah aktif otomatis)
# st_folium(m, width=1000, height=600)

