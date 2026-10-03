import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import libpysal
from esda.moran import Moran
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# =====================================================================
# PENGATURAN HALAMAN & TEMA WARNA
# =====================================================================
st.set_page_config(page_title="Kisah Ekonomi Nusantara", layout="wide", initial_sidebar_state="collapsed")

# Palet Warna berdasarkan Referensi Frame 3 (1).pdf (Mint / Sage Green / Earth Tones)
COLOR_MINT = '#d4edda'
COLOR_SAGE = '#8fbc8f'
COLOR_FOREST = '#2e8b57'
COLOR_DARK = '#1a432b'
COLOR_HIGHLIGHT = '#ff9f43' # Warna kontras untuk Highlight/Pencilan

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
    df_pengeluaran = pd.read_excel('data/Rata-Rata Pengeluaran Ruta Per Komoditi Maret 2024-2025.xlsx')
    
    # Menghitung persentase pertumbuhan dari 2024 ke 2025 untuk gradasi warna
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

    # --- Proses Sapu Bersih Kode Wilayah ---
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

    # -- 3. Data Multivariat --
    df_multi = pd.read_excel('data/Dataset_Multivariat_2025_Bersih.xlsx')

    # Daftar kolom yang berisi angka dengan format koma berdasarkan Excel Anda
    kolom_numerik_multi = [
        'Persentase_Miskin', 'IPM', 'Akses_Sanitasi', 'Akses_Air_Minum', 
        'Rata_Lama_Sekolah', 'Pengeluaran_Per_Kapita', 'TPT', 'UHH'
    ]

    # Sapu bersih koma menjadi titik dan ubah menjadi float (angka desimal)
    for col in kolom_numerik_multi:
        if col in df_multi.columns: # Memastikan kolom benar-benar ada
            df_multi[col] = df_multi[col].apply(bersihkan_angka)

    return df_pengeluaran, gdf, df_multi

df_pengeluaran, gdf, df_multi = load_data()


# =====================================================================
# ALUR CERITA (SCROLLYTELLING)
# =====================================================================

st.markdown("<h1 style='text-align: center; font-size: 3.5em; margin-bottom: 0px;'>Bumi, Manusia, dan Rupiah</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray; font-weight: normal;'>Jejak Kesejahteraan Indonesia (2021 - 2025)</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

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
fig_map = px.choropleth_map(
    gdf_year, 
    geojson=gdf_year.geometry, 
    locations=gdf_year.index,
    color='Pct_Miskin_Clean', 
    color_continuous_scale="YlOrRd",
    # Jika nilainya -1 (kosong), warnai dengan abu-abu terang agar tidak bolong
    # (Catatan: Plotly continuous scale bisa diatur, atau kita pisah dengan layer warna solid di bawah)
    range_color=[0, gdf['Pct_Miskin'].max()],
    map_style="white-bg", 
    zoom=4, 
    center={"lat": -0.789, "lon": 113.921},
    opacity=0.9, 
    hover_name='Kab/Kota',
    hover_data={'Pct_Miskin': ':.2f', 'PDRB': ':.2f', 'Pct_Miskin_Clean': False}, 
    labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Triliun)'}
)

fig_map.update_layout(
    map_layers=[{"below": 'traces', "sourcetype": "raster", "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]}],
    margin={"r":0,"t":0,"l":0,"b":0} 
)
 
gdf_bubble = gdf_year.dropna(subset=['PDRB', 'centroid_x', 'centroid_y'])
fig_bubble = px.scatter_map( 
    gdf_bubble, lat='centroid_y', lon='centroid_x', size='PDRB',
    hover_name='Kab/Kota', hover_data={'PDRB': ':.2f', 'Pct_Miskin': ':.2f', 'centroid_y': False, 'centroid_x': False}, 
    labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Triliun)'},
    size_max=45, zoom=4
)

fig_bubble.update_traces(marker=dict(color='#00FF00', opacity=0.4))

for trace in fig_bubble.data:
    fig_map.add_trace(trace)

st.plotly_chart(fig_map, use_container_width=True)

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

# --- BAB 3: Hierarki Pengeluaran (Memenuhi Syarat UAS Multirepresentasi) ---
st.markdown("### Konklusi: Ke Mana Uang Kita Bermuara?")
st.write("Terlepas dari fluktuasi ekonomi dari 2021 hingga saat ini, prioritas bertahan hidup masyarakat bermuara pada struktur pengeluaran. Klik pada area mana pun untuk melakukan *drill-down/zoom*, atau arahkan kursor Anda untuk melihat rincian spesifik.")

# Representasi 1: Treemap
fig_tree = px.treemap(
    df_pengeluaran, 
    path=['Level_1', 'Level_2', 'Level_3'], 
    values='Maret_2025',                    
    color='Pertumbuhan (%)',                
    color_continuous_scale='RdYlGn',
    color_continuous_midpoint=0, 
    title="Peta Struktur Pengeluaran (Treemap)"
)
fig_tree.update_traces(
    textinfo='label+percent parent',
    # Tambahkan format ,.0f pada value agar angka diformat dengan pemisah ribuan
    hovertemplate='<b>%{label}</b><br>Pengeluaran 2025: %{value:,.0f}<br>Pertumbuhan: %{color:.2f}%<extra></extra>'
)
# 🌟 KUNCI FORMAT INDONESIA: Ubah pemisah desimal jadi koma, pemisah ribuan jadi titik
fig_tree.update_layout(separators=",.")
st.plotly_chart(fig_tree, use_container_width=True)

st.divider() # Garis pemisah antar grafik

# Representasi 2: Sunburst
fig_sun = px.sunburst(
    df_pengeluaran,
    path=['Level_1', 'Level_2', 'Level_3'], 
    values='Maret_2025',                    
    color='Pertumbuhan (%)',                
    color_continuous_scale='RdYlGn',
    color_continuous_midpoint=0, 
    title="Cincin Struktur Pengeluaran (Sunburst)"
)
fig_sun.update_traces(
    textinfo='none', 
    # Tambahkan format ,.0f pada value
    hovertemplate='<b>Kategori: %{label}</b><br>Pengeluaran 2025: %{value:,.0f}<br>Pertumbuhan dari 2024: %{color:.2f}%<extra></extra>'
)
# 🌟 KUNCI FORMAT INDONESIA: Ubah pemisah desimal jadi koma, pemisah ribuan jadi titik
fig_sun.update_layout(separators=",.")

# Menghitung total dan menaruhnya di lingkaran tengah (Sudah pakai format Indonesia)
total_pengeluaran = df_pengeluaran['Maret_2025'].sum()
total_format = f"{total_pengeluaran:,.0f}".replace(',', '.') 

fig_sun.add_annotation(
    text=f"<b>TOTAL</b><br>Rp {total_format}",
    x=0.5, y=0.5, 
    showarrow=False,
    font=dict(size=15, color="black"),
    align="center"
)

st.plotly_chart(fig_sun, use_container_width=True)

# --- KARTU INTERPRETASI (CARDS) ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 💡 Membaca Arah Konsumsi Masyarakat")
st.write("Dua variabel yang kita ukur (Total Pengeluaran & Pertumbuhan) menceritakan realitas ekonomi rumah tangga saat ini:")

col_c1, col_c2, col_c3 = st.columns(3)

with col_c1:
    st.info("📦 **Tulang Punggung (Ukuran Area)**\n\nKotak atau irisan yang paling luas mewakili penyedot anggaran terbesar. Ini adalah pengeluaran primer yang tidak bisa dihindari oleh masyarakat.")

with col_c2:
    st.success("📈 **Prioritas Baru (Warna Hijau)**\n\nArea dengan warna hijau pekat menandakan komoditas yang anggarannya meroket di tahun 2025. Ini bisa berarti pergeseran gaya hidup atau dampak inflasi di sektor tersebut.")

with col_c3:
    st.error("📉 **Ikat Pinggang (Warna Merah)**\n\nArea berwarna merah menyoroti pengeluaran yang paling banyak dipangkas (minus). Saat ekonomi sulit, pos-pos berwarna merah inilah yang pertama kali dikorbankan.")

st.markdown("<br><br><center><p style='color: gray;'><i>Sebuah eksplorasi data visual. Dibuat untuk Tugas Akhir Visualisasi Data.</i></p></center>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# BAB 4: PROFIL MULTIDIMENSI (Syarat UAS Visualisasi Data Multivariat)
# ---------------------------------------------------------------------
st.markdown("### 4. Membedah Profil Kesejahteraan Multidimensi (34 Provinsi)")
st.write("Kesejahteraan tidak hanya diukur dari uang. Mari kita lihat 8 dimensi kehidupan dari 34 Provinsi di Indonesia.")

# FITUR LINKING: Dropdown untuk menyorot (Highlight) Provinsi tertentu di semua grafik
provinsi_terpilih = st.selectbox("🎯 Sorot (Highlight) Provinsi:", options=df_multi['Provinsi'].tolist(), index=10)

# 1. PARALLEL COORDINATES (Brushing Technique)
st.markdown("#### A. Jejaring Indikator (Parallel Coordinates)")
st.write("💡 *Tip Interaksi (Brushing):* Klik dan seret (drag) kursor Anda pada garis sumbu vertikal di bawah ini untuk memfilter (brushing) rentang nilai tertentu.")

kolom_numerik = df_multi.select_dtypes(include=[np.number]).columns.tolist()
# Membuat kolom penanda warna (1 untuk provinsi terpilih, 0 untuk lainnya)
df_multi['Color_Flag'] = np.where(df_multi['Provinsi'] == provinsi_terpilih, 1, 0)

fig_par = px.parallel_coordinates(
    df_multi, dimensions=kolom_numerik, color='Color_Flag',
    color_continuous_scale=[[0, COLOR_SAGE], [1, COLOR_DARK]],
    labels={col: col.replace('_', ' ') for col in kolom_numerik}
)
fig_par.update_layout(coloraxis_showscale=False, margin=dict(l=50, r=50, t=30, b=30))
st.plotly_chart(fig_par, use_container_width=True)

# Membagi layar untuk PCA dan Radar Chart
col_pca, col_radar = st.columns(2)

# 2. PCA SCATTERPLOT (Dimensionality Reduction)
with col_pca:
    st.markdown("#### B. Peta Pengelompokan (PCA)")
    
    # Proses PCA (Reduksi 8 variabel menjadi 2 komponen utama)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(df_multi[kolom_numerik])
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data_scaled)
    
    df_pca = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])
    df_pca['Provinsi'] = df_multi['Provinsi']
    df_pca['Status'] = np.where(df_multi['Provinsi'] == provinsi_terpilih, 'Disorot', 'Lainnya')
    
    fig_pca = px.scatter(
        df_pca, x='PC1', y='PC2', text='Provinsi', color='Status',
        color_discrete_map={'Disorot': COLOR_HIGHLIGHT, 'Lainnya': COLOR_SAGE},
        title=f"Varian yang dijelaskan: {pca.explained_variance_ratio_.sum()*100:.1f}%"
    )
    fig_pca.update_traces(textposition='top center')
    fig_pca.update_layout(showlegend=False)
    st.plotly_chart(fig_pca, use_container_width=True)

# 3. RADAR CHART (Profil Individu)
with col_radar:
    st.markdown(f"#### C. Jaring Laba-laba: **{provinsi_terpilih}**")
    
    # Standarisasi skala 0-100 untuk radar chart agar bentuknya seimbang
    df_radar_norm = (df_multi[kolom_numerik] - df_multi[kolom_numerik].min()) / (df_multi[kolom_numerik].max() - df_multi[kolom_numerik].min()) * 100
    nilai_provinsi = df_radar_norm[df_multi['Provinsi'] == provinsi_terpilih].values[0]
    nilai_nasional = df_radar_norm.mean().values
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=nilai_nasional, theta=kolom_numerik, fill='toself', name='Rata-rata Nasional', marker_color=COLOR_SAGE, opacity=0.5))
    fig_radar.add_trace(go.Scatterpolar(r=nilai_provinsi, theta=kolom_numerik, fill='toself', name=provinsi_terpilih, marker_color=COLOR_DARK))
    
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)), showlegend=True, margin=dict(l=30, r=30, t=30, b=30))
    st.plotly_chart(fig_radar, use_container_width=True)

# 4. KOTAK INTERPRETASI
st.info("""
**🔎 Interpretasi Analisis Multidimensi:**
*   **Pengelompokan (Klastering):** Pada grafik PCA (kiri), provinsi yang posisinya saling berdekatan menandakan mereka memiliki karakteristik sosial-ekonomi yang sangat mirip di ke-8 variabel tersebut.
*   **Pencilan (Outlier):** Provinsi yang posisinya terasing/menjauh dari kerumunan utama di grafik PCA adalah provinsi dengan anomali (misalnya DKI Jakarta yang biasanya memiliki IPM dan PDRB ekstrem tinggi, atau Papua dengan kemiskinan ekstrem tinggi).
*   **Profil Radar:** Bentuk jaring yang condong mendekati batas luar menandakan performa yang sangat baik di atas rata-rata nasional pada indikator tersebut.
""")

