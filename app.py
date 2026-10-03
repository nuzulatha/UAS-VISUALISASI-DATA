import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import libpysal
from esda.moran import Moran

# =====================================================================
# PENGATURAN HALAMAN (WEB STORY MODE)
# =====================================================================
st.set_page_config(
    page_title="Kisah Ekonomi Nusantara", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# =====================================================================
# FUNGSI PEMUATAN & PEMBERSIHAN DATA 
# =====================================================================
@st.cache_data 
def load_data():
    # --- 1. Data Hierarki Pengeluaran ---
    data = [
        ['Total', 'Makanan', 'Padi-padian', 94641, 89278],
        ['Total', 'Makanan', 'Rokok', 94476, 91708],
        ['Total', 'Bukan Makanan', 'Perumahan', 391751, 398657]
    ]
    df_pengeluaran = pd.DataFrame(data, columns=['Level_1', 'Level_2', 'Level_3', 'Maret_2024', 'Maret_2025'])
    df_pengeluaran['Pertumbuhan (%)'] = ((df_pengeluaran['Maret_2025'] - df_pengeluaran['Maret_2024']) / df_pengeluaran['Maret_2024']) * 100

    # --- 2. Data Geospasial & Ekonomi ---
    gdf_batas = gpd.read_file('data/kab_kota.geojson')
    df_miskin = pd.read_excel('data/Persentase_Penduduk_Miskin_dengan_Kode.xlsx')
    df_pdrb = pd.read_excel('data/PDRB_ADHB_KODE.xlsx')
    
    df_miskin.columns = [str(col).replace('.0', '').strip() for col in df_miskin.columns]
    df_pdrb.columns = [str(col).replace('.0', '').strip() for col in df_pdrb.columns]

    tahun_list = ['2021', '2022', '2023', '2024', '2025']
    
    df_miskin_melt = df_miskin.melt(id_vars=['Kode_Wilayah', 'Kab/Kota'], value_vars=tahun_list, var_name='Tahun', value_name='Pct_Miskin')
    df_pdrb_melt = df_pdrb.melt(id_vars=['Kode_Wilayah'], value_vars=tahun_list, var_name='Tahun', value_name='PDRB')

    # Fungsi Pembersih Angka
    def bersihkan_angka(val):
        if pd.isna(val):
            return None
        val_str = str(val).strip().replace(',', '.')
        try:
            return float(val_str)
        except ValueError:
            return None

    df_miskin_melt['Pct_Miskin'] = df_miskin_melt['Pct_Miskin'].apply(bersihkan_angka)
    df_pdrb_melt['PDRB'] = df_pdrb_melt['PDRB'].apply(bersihkan_angka)

    # --- 3. Proses Sapu Bersih Kode Wilayah ---
    def bersihkan_kode(x):
        x = str(x).strip()
        if x.endswith('.0'): 
            x = x[:-2]
        x = x.replace('.', '')
        return x

    gdf_batas['code'] = gdf_batas['code'].apply(bersihkan_kode)
    df_miskin_melt['Kode_Wilayah'] = df_miskin_melt['Kode_Wilayah'].apply(bersihkan_kode)
    df_pdrb_melt['Kode_Wilayah'] = df_pdrb_melt['Kode_Wilayah'].apply(bersihkan_kode)

    df_ekonomi = df_miskin_melt.merge(df_pdrb_melt, on=['Kode_Wilayah', 'Tahun'], how='left')
    gdf = gdf_batas.merge(df_ekonomi, left_on='code', right_on='Kode_Wilayah', how='left')

    # 🔍 DIAGNOSTIK KEGAGALAN JOIN (Cek di Terminal Codespaces)
    data_kosong_cek = gdf[gdf['Pct_Miskin'].isna()]['code'].unique()
    print(f"⚠️ PERINGATAN: Ada {len(data_kosong_cek)} kode wilayah di peta yang gagal ter-join dengan Excel pada tahun tertentu!")
    print("Contoh kode wilayah yang gagal:", data_kosong_cek[:10])

    gdf['centroid_x'] = gdf.geometry.centroid.x
    gdf['centroid_y'] = gdf.geometry.centroid.y
    gdf['Pct_Miskin'] = pd.to_numeric(gdf['Pct_Miskin'], errors='coerce')
    gdf['PDRB'] = pd.to_numeric(gdf['PDRB'], errors='coerce')

    return df_pengeluaran, gdf

df_pengeluaran, gdf = load_data()


# =====================================================================
# ALUR CERITA (SCROLLYTELLING)
# =====================================================================

st.markdown("<h1 style='text-align: center; font-size: 3.5em; margin-bottom: 0px;'>Bumi, Manusia, dan Rupiah</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray; font-weight: normal;'>Jejak Kesejahteraan Indonesia (2021 - 2025)</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.write("""
Setiap jengkal tanah di Nusantara menyimpan ceritanya sendiri. Ada wilayah yang roda ekonominya berputar kencang, namun ada pula yang masih berjuang melepaskan diri dari jerat kemiskinan. 
""")

st.write("""
Setiap jengkal tanah di Nusantara menyimpan ceritanya sendiri. Ada wilayah yang roda ekonominya berputar kencang, namun ada pula yang masih berjuang melepaskan diri dari jerat kemiskinan. 
""")
st.divider()

# --- BAB 1: Peta ---
# Membagi layar menjadi 2 kolom: kiri (lebar) untuk teks, kanan (kecil) untuk filter tahun
col_teks, col_tahun = st.columns([4, 1])

with col_teks:
    st.markdown("### Wajah Kesejahteraan dari Udara")
    st.write("Area yang tersapu warna **merah** menunjukkan tingginya persentase kemiskinan. Sementara itu, **pendaran cahaya hijau** adalah denyut nadi PDRB (dalam Triliun Rupiah) yang terkonsentrasi di wilayah tersebut.")

with col_tahun:
    # Menggunakan Dropdown (Selectbox) agar ringkas dan menempel dengan peta
    selected_year = st.selectbox(
        "⏳ Pilih Tahun:", 
        options=[2021, 2022, 2023, 2024, 2025], 
        index=4 # Default otomatis ke urutan terakhir (2025)
    )

# FILTER DATA BERDASARKAN TAHUN YANG DIPILIH
gdf_year = gdf[gdf['Tahun'] == str(selected_year)].copy()

# HIGHLIGHT CARD (Otomatis berubah sesuai tahun)
daerah_miskin_max = gdf_year.loc[gdf_year['Pct_Miskin'].idxmax()]
daerah_pdrb_max = gdf_year.loc[gdf_year['PDRB'].idxmax()]

col1, col2, col3 = st.columns(3)
with col1:
    st.error(f"🚨 **Tertinggi Miskin ({selected_year})**\n\n{daerah_miskin_max['Kab/Kota']} ({daerah_miskin_max['Pct_Miskin']}%)")
with col2:
    st.success(f"💎 **Pusat Kemakmuran ({selected_year})**\n\n{daerah_pdrb_max['Kab/Kota']} ({daerah_pdrb_max['PDRB']} Triliun)")
with col3:
    st.info("💡 **Jelajahi Sendiri**\n\nScroll untuk mendekat (*zoom*), atau arahkan kursor ke wilayah manapun.")

# 1. Tangani data yang kosong (NaN) agar tidak bolong transparan
gdf_year['Pct_Miskin_Clean'] = gdf_year['Pct_Miskin'].fillna(-1) # Beri penanda khusus -1 untuk data kosong

# 2. Render Peta Utama
# 1. Buat Layer Dasar Abu-Abu untuk menutup seluruh area agar tidak ada yang bolong/transparan
fig_base = px.choropleth_map(
    gdf_year, geojson=gdf_year.geometry, locations=gdf_year.index,
    color_discrete_sequence=['#d3d3d3'], # Warna abu-abu netral untuk wilayah tanpa data
    map_style="white-bg", zoom=4, center={"lat": -0.789, "lon": 113.921}
)

fig_base.update_layout(
    map_layers=[{"below": 'traces', "sourcetype": "raster", "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]}],
    margin={"r":0,"t":0,"l":0,"b":0} 
)

# 2. Buat Peta Utama Kemiskinan (Hanya memetakan data yang ada nilainya, abaikan yang NaN)
fig_map = px.choropleth_map(
    gdf_year.dropna(subset=['Pct_Miskin']), 
    geojson=gdf_year.geometry, 
    locations=gdf_year.dropna(subset=['Pct_Miskin']).index,
    color='Pct_Miskin', 
    color_continuous_scale="YlOrRd",
    map_style="white-bg", zoom=4, center={"lat": -0.789, "lon": 113.921},
    opacity=0.9, 
    hover_name='Kab/Kota',
    hover_data={'Pct_Miskin': ':.2f', 'PDRB': ':.2f'}, 
    labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Triliun)'}
)

# 3. Buat Layer Bubble PDRB (Hijau)
gdf_bubble = gdf_year.dropna(subset=['PDRB', 'centroid_x', 'centroid_y'])
fig_bubble = px.scatter_map( 
    gdf_bubble, lat='centroid_y', lon='centroid_x', size='PDRB',
    hover_name='Kab/Kota', hover_data={'PDRB': ':.2f', 'Pct_Miskin': ':.2f', 'centroid_y': False, 'centroid_x': False}, 
    labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Triliun)'},
    size_max=45, zoom=4
)
fig_bubble.update_traces(marker=dict(color='#00FF00', opacity=0.4))

# 4. Gabungkan semuanya ke kanvas utama (fig_base): Abu-abu di bawah -> Merah Kemiskinan di tengah -> Bubble Hijau di atas
for trace in fig_map.data:
    fig_base.add_trace(trace)

for trace in fig_bubble.data:
    fig_base.add_trace(trace)

# 5. Tampilkan ke Web Streamlit
st.plotly_chart(fig_base, use_container_width=True)

st.success(f"📌 **Catatan {selected_year}:** Peta di atas mengungkap bahwa pendaran hijau kemakmuran seringkali hanya terpusat pada titik tertentu, meninggalkan wilayah sekitarnya dalam balutan warna merah pekat.")
st.divider()

# --- BAB 2: Moran's I ---
st.markdown(f"### Mengendus Kantong Kemiskinan di {selected_year}")
st.write("Apakah kemiskinan menular secara geografis? Melalui analisis keruangan (*Moran's I*), kita melihat apakah wilayah miskin cenderung bergerombol dengan tetangganya.")

try:
    # gdf_moran = gdf_year.dropna(subset=['Pct_Miskin', 'geometry']).copy()
    # w = libpysal.weights.Queen.from_dataframe(gdf_moran)
    # w.transform = 'r' 

    # Ganti metode Queen dengan KNN agar pulau-pulau terluar tetap memiliki tetangga terdekat
    from libpysal.weights import KNN
    
    gdf_moran = gdf_year.dropna(subset=['Pct_Miskin', 'geometry']).copy()
    
    # Menggunakan K=5 (artinya setiap wilayah akan mencari 5 tetangga terdekat secara geografis)
    w = KNN.from_dataframe(gdf_moran, k=5)
    w.transform = 'r'

    gdf_moran['Spatial_Lag'] = libpysal.weights.lag_spatial(w, gdf_moran['Pct_Miskin'])
    gdf_moran['Z_Miskin'] = (gdf_moran['Pct_Miskin'] - gdf_moran['Pct_Miskin'].mean()) / gdf_moran['Pct_Miskin'].std()
    gdf_moran['Z_Lag'] = (gdf_moran['Spatial_Lag'] - gdf_moran['Spatial_Lag'].mean()) / gdf_moran['Spatial_Lag'].std()

    moran_global = Moran(gdf_moran['Pct_Miskin'], w)
    
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        st.metric(label=f"Indeks Global Moran's I ({selected_year})", value=f"{moran_global.I:.3f}")
        st.info("Karena nilainya positif, daerah-daerah miskin di Indonesia memang terbukti mengelompok secara berdekatan pada tahun ini.")

    with col_m2:
        fig_scatter = px.scatter(
            gdf_moran, x='Z_Miskin', y='Z_Lag', hover_name='Kab/Kota',
            hover_data={'Pct_Miskin': ':.2f', 'Z_Miskin': False, 'Z_Lag': False},
            labels={'Z_Miskin': 'Kemiskinan Daerah', 'Z_Lag': 'Kemiskinan Tetangga'},
            color_discrete_sequence=['#1E90FF'] 
        )
        fig_scatter.add_vline(x=0, line_width=2, line_dash="dash", line_color="black")
        fig_scatter.add_hline(y=0, line_width=2, line_dash="dash", line_color="black")
        fig_scatter.add_annotation(x=2.5, y=2.5, text="High-High (Hotspot)", showarrow=False, font=dict(color="#FF4500", size=14))
        fig_scatter.add_annotation(x=-1.5, y=-1.5, text="Low-Low (Coldspot)", showarrow=False, font=dict(color="#228B22", size=14))
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.warning("📌 **Fokus Analisis:** Perhatikan titik-titik di kuadran **Kanan Atas (Hotspot)**. Ini adalah wilayah prioritas yang terjebak di tengah kepungan wilayah miskin lainnya.")

except Exception as e:
    st.error(f"Kalkulasi spasial terhenti: {e}")

st.divider()

# --- BAB 3: Treemap ---
st.markdown("### Konklusi: Ke Mana Uang Kita Bermuara?")
st.write("Terlepas dari fluktuasi ekonomi dari 2021 hingga saat ini, prioritas bertahan hidup masyarakat bermuara pada struktur pengeluaran. Proporsi kotak di bawah ini menunjukkan lonjakan dan pergeseran prioritas konsumsi terbaru.")

fig_tree = px.treemap(
    df_pengeluaran, 
    path=['Level_1', 'Level_2', 'Level_3'], 
    values='Maret_2025', 
    color='Pertumbuhan (%)', 
    color_continuous_scale='RdYlGn'
)
st.plotly_chart(fig_tree, use_container_width=True)

st.info("📌 **Catatan:** Gradasi warna hijau menyoroti lonjakan pertumbuhan prioritas konsumsi, sementara warna merah menandakan penyusutan alokasi anggaran rumah tangga.")

st.markdown("<br><br><center><p style='color: gray;'><i>Sebuah eksplorasi data visual. Dibuat untuk Tugas Akhir Visualisasi Data.</i></p></center>", unsafe_allow_html=True)

# import streamlit as st
# import pandas as pd
# import geopandas as gpd
# import plotly.express as px
# import libpysal
# from esda.moran import Moran

# # =====================================================================
# # PENGATURAN HALAMAN (WEB STORY MODE)
# # =====================================================================
# # Menyembunyikan sidebar agar fokus pada cerita (scrollytelling)
# st.set_page_config(
#     page_title="Kisah Ekonomi Nusantara", 
#     layout="wide", 
#     initial_sidebar_state="collapsed"
# )

# # =====================================================================
# # FUNGSI PEMUATAN & PEMBERSIHAN DATA (TIDAK TERLIHAT OLEH USER)
# # =====================================================================
# @st.cache_data 
# def load_data():
#     # --- 1. Data Hierarki Pengeluaran ---
#     data = [
#         ['Total', 'Makanan', 'Padi-padian', 94641, 89278],
#         ['Total', 'Makanan', 'Rokok', 94476, 91708],
#         ['Total', 'Bukan Makanan', 'Perumahan', 391751, 398657]
#     ]
#     df_pengeluaran = pd.DataFrame(data, columns=['Level_1', 'Level_2', 'Level_3', 'Maret_2024', 'Maret_2025'])
#     df_pengeluaran['Pertumbuhan (%)'] = ((df_pengeluaran['Maret_2025'] - df_pengeluaran['Maret_2024']) / df_pengeluaran['Maret_2024']) * 100

#     # --- 2. Data Geospasial & Ekonomi ---
#     gdf_batas = gpd.read_file('data/kab_kota.geojson')
#     df_miskin = pd.read_excel('data/Persentase_Penduduk_Miskin_dengan_Kode.xlsx')
#     df_pdrb = pd.read_excel('data/PDRB_ADHB_KODE.xlsx')
    
#     df_miskin.columns = [str(col).replace('.0', '').strip() for col in df_miskin.columns]
#     df_pdrb.columns = [str(col).replace('.0', '').strip() for col in df_pdrb.columns]

#     df_miskin_25 = df_miskin[['Kode_Wilayah', 'Kab/Kota', '2025']].rename(columns={'2025': 'Pct_Miskin'})
#     df_pdrb_25 = df_pdrb[['Kode_Wilayah', '2025']].rename(columns={'2025': 'PDRB'})

#     # --- 3. Proses Penggabungan (Merge) Data ---
#     gdf_batas['code'] = gdf_batas['code'].astype(str).str.strip()
#     df_miskin_25['Kode_Wilayah'] = df_miskin_25['Kode_Wilayah'].astype(str).str.strip()
#     df_pdrb_25['Kode_Wilayah'] = df_pdrb_25['Kode_Wilayah'].astype(str).str.strip()

#     def rapikan_kode(x):
#         try:
#             return f"{float(x):.2f}"
#         except ValueError:
#             return str(x)

#     gdf_batas['code'] = gdf_batas['code'].apply(rapikan_kode)
#     df_miskin_25['Kode_Wilayah'] = df_miskin_25['Kode_Wilayah'].apply(rapikan_kode)
#     df_pdrb_25['Kode_Wilayah'] = df_pdrb_25['Kode_Wilayah'].apply(rapikan_kode)

#     gdf = gdf_batas.merge(df_miskin_25, left_on='code', right_on='Kode_Wilayah', how='left')
#     gdf = gdf.merge(df_pdrb_25, left_on='code', right_on='Kode_Wilayah', how='left')

#     gdf['centroid_x'] = gdf.geometry.centroid.x
#     gdf['centroid_y'] = gdf.geometry.centroid.y
#     gdf['Pct_Miskin'] = pd.to_numeric(gdf['Pct_Miskin'], errors='coerce')
#     gdf['PDRB'] = pd.to_numeric(gdf['PDRB'], errors='coerce')

#     return df_pengeluaran, gdf

# df_pengeluaran, gdf = load_data()


# # =====================================================================
# # ALUR CERITA (SCROLLYTELLING)
# # =====================================================================

# # Judul Bergaya Artikel Interaktif
# st.markdown("<h1 style='text-align: center; font-size: 3.5em; margin-bottom: 0px;'>Bumi, Manusia, dan Rupiah</h1>", unsafe_allow_html=True)
# st.markdown("<h3 style='text-align: center; color: gray; font-weight: normal;'>Sebuah Perjalanan Melintasi Data Ekonomi Indonesia 2025</h3>", unsafe_allow_html=True)
# st.markdown("<br>", unsafe_allow_html=True)

# st.write("""
# Setiap jengkal tanah di Nusantara menyimpan ceritanya sendiri. Ada wilayah yang roda ekonominya berputar kencang, namun ada pula yang masih berjuang melepaskan diri dari jerat kemiskinan. 

# Mari kita gulir ke bawah untuk menelusuri jejak-jejak kesejahteraan dari udara, menemukan kantong-kantong ekonomi, dan memahami ke mana sebenarnya uang masyarakat bermuara.
# """)
# st.divider()

# # --- BAB 1: Peta ---
# st.markdown("### Wajah Kesejahteraan dari Udara")
# st.write("Lihatlah hamparan kepulauan ini. Area yang tersapu warna **merah** menunjukkan tingginya tingkat kemiskinan. Sebaliknya, perhatikan **pendaran cahaya hijau** yang muncul—itu adalah denyut nadi triliunan rupiah (PDRB) yang terkonsentrasi di wilayah tersebut.")

# daerah_miskin_max = gdf.loc[gdf['Pct_Miskin'].idxmax()]
# daerah_pdrb_max = gdf.loc[gdf['PDRB'].idxmax()]

# # Highlight Metrik yang menyatu dengan narasi
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.error(f"🚨 **Titik Paling Rentan**\n\n{daerah_miskin_max['Kab/Kota']} mencatat angka kemiskinan hingga {daerah_miskin_max['Pct_Miskin']}%.")
# with col2:
#     st.success(f"💎 **Pusat Kemakmuran**\n\n{daerah_pdrb_max['Kab/Kota']} memimpin dengan putaran ekonomi {daerah_pdrb_max['PDRB']} Triliun.")
# with col3:
#     st.info("💡 **Jelajahi Sendiri**\n\nScroll untuk mendekat (*zoom*), atau sentuh/arahkan kursor ke wilayah manapun untuk detailnya.")

# # Render Peta
# fig_map = px.choropleth_map(
#     gdf, geojson=gdf.geometry, locations=gdf.index,
#     color='Pct_Miskin', color_continuous_scale="YlOrRd",
#     map_style="white-bg", zoom=4, center={"lat": -0.789, "lon": 113.921},
#     opacity=0.9, hover_name='Kab/Kota',
#     hover_data={'Pct_Miskin': ':.2f', 'PDRB': ':.2f'}, 
#     labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Triliun)', 'index': 'Kode ID'}
# )

# fig_map.update_layout(
#     map_layers=[{"below": 'traces', "sourcetype": "raster", "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]}],
#     margin={"r":0,"t":0,"l":0,"b":0} 
# )
 
# gdf_bubble = gdf.dropna(subset=['PDRB', 'centroid_x', 'centroid_y'])
# fig_bubble = px.scatter_map( 
#     gdf_bubble, lat='centroid_y', lon='centroid_x', size='PDRB',
#     hover_name='Kab/Kota', hover_data={'PDRB': ':.2f', 'Pct_Miskin': ':.2f', 'centroid_y': False, 'centroid_x': False}, 
#     labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Triliun)'},
#     size_max=45, zoom=4
# )

# fig_bubble.update_traces(marker=dict(color='#00FF00', opacity=0.4))

# for trace in fig_bubble.data:
#     fig_map.add_trace(trace)

# st.plotly_chart(fig_map, use_container_width=True)

# st.success("📌 **Catatan Perjalanan:** Peta di atas mengungkap sebuah realitas pahit. Pendaran hijau kemakmuran seringkali hanya terpusat pada titik-titik tertentu, meninggalkan wilayah sekitarnya dalam balutan warna merah pekat.")
# st.divider()

# # --- BAB 2: Moran's I ---
# st.markdown("### Mengendus Kantong Kemiskinan")
# st.write("Apakah kemiskinan itu menular secara geografis? Melalui analisis keruangan (*Moran's I*), kita bisa melihat apakah wilayah miskin cenderung bergerombol dengan tetangganya yang juga miskin, membentuk apa yang disebut sebagai 'kantong kemiskinan'.")

# try:
#     gdf_moran = gdf.dropna(subset=['Pct_Miskin', 'geometry']).copy()
#     w = libpysal.weights.Queen.from_dataframe(gdf_moran)
#     w.transform = 'r' 

#     gdf_moran['Spatial_Lag'] = libpysal.weights.lag_spatial(w, gdf_moran['Pct_Miskin'])
#     gdf_moran['Z_Miskin'] = (gdf_moran['Pct_Miskin'] - gdf_moran['Pct_Miskin'].mean()) / gdf_moran['Pct_Miskin'].std()
#     gdf_moran['Z_Lag'] = (gdf_moran['Spatial_Lag'] - gdf_moran['Spatial_Lag'].mean()) / gdf_moran['Spatial_Lag'].std()

#     moran_global = Moran(gdf_moran['Pct_Miskin'], w)
    
#     col_m1, col_m2 = st.columns([1, 2])
#     with col_m1:
#         st.metric(label="Indeks Global Moran's I", value=f"{moran_global.I:.3f}")
#         st.info("Karena nilainya positif (di atas 0), data memastikan bahwa daerah-daerah miskin di Indonesia memang cenderung mengelompok secara berdekatan.")

#     with col_m2:
#         fig_scatter = px.scatter(
#             gdf_moran, x='Z_Miskin', y='Z_Lag', hover_name='Kab/Kota',
#             hover_data={'Pct_Miskin': ':.2f', 'Z_Miskin': False, 'Z_Lag': False},
#             labels={'Z_Miskin': 'Kemiskinan Daerah', 'Z_Lag': 'Kemiskinan Tetangga'},
#             color_discrete_sequence=['#1E90FF'] 
#         )
#         fig_scatter.add_vline(x=0, line_width=2, line_dash="dash", line_color="black")
#         fig_scatter.add_hline(y=0, line_width=2, line_dash="dash", line_color="black")
#         fig_scatter.add_annotation(x=2.5, y=2.5, text="High-High (Hotspot)", showarrow=False, font=dict(color="#FF4500", size=14))
#         fig_scatter.add_annotation(x=-1.5, y=-1.5, text="Low-Low (Coldspot)", showarrow=False, font=dict(color="#228B22", size=14))
        
#         st.plotly_chart(fig_scatter, use_container_width=True)
    
#     st.warning("📌 **Catatan Perjalanan:** Fokuskan perhatian pada titik-titik di kuadran **Kanan Atas (Hotspot)**. Ini adalah 'lampu merah' bagi pembuat kebijakan: wilayah miskin yang terjebak di tengah kepungan wilayah miskin lainnya.")

# except Exception as e:
#     st.error(f"Kalkulasi spasial terhenti: {e}")

# st.divider()

# # --- BAB 3: Treemap ---
# st.markdown("### Ke Mana Uang Kita Bermuara?")
# st.write("Setelah menelusuri lokasinya, tibalah kita pada pertanyaan terakhir: di wilayah-wilayah tersebut, untuk apa sebenarnya masyarakat menghabiskan uangnya? Proporsi kotak di bawah ini menceritakan prioritas hidup mereka saat ini.")

# fig_tree = px.treemap(
#     df_pengeluaran, 
#     path=['Level_1', 'Level_2', 'Level_3'], 
#     values='Maret_2025', 
#     color='Pertumbuhan (%)', 
#     color_continuous_scale='RdYlGn'
# )
# st.plotly_chart(fig_tree, use_container_width=True)

# st.info("📌 **Catatan Perjalanan:** Gradasi warna hijau ke merah menyoroti pergeseran gaya hidup—kategori mana yang semakin ditinggalkan, dan mana yang kini menjadi prioritas utama rumah tangga.")

# st.markdown("<br><br><center><p style='color: gray;'><i>Sebuah eksplorasi data visual. Dibuat untuk Tugas Akhir Visualisasi Data.</i></p></center>", unsafe_allow_html=True)