# %% Blok 1: Import Library & Setup Halaman
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

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
    gdf_batas['code'] = gdf_batas['code'].astype(str).str.strip()
    df_miskin_25['Kode_Wilayah'] = df_miskin_25['Kode_Wilayah'].astype(str).str.strip()
    df_pdrb_25['Kode_Wilayah'] = df_pdrb_25['Kode_Wilayah'].astype(str).str.strip()

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
# ... (Blok 1 dan Blok 2 load data tetap sama seperti sebelumnya) ...

# --- MULAILAH BERCERITA (WEB STORY MODE) ---

st.markdown("""
# 🌍 Kisah Ekonomi Indonesia (2025)
Selamat datang di eksplorasi interaktif ekonomi Nusantara. Mari kita gulir ke bawah untuk melihat bagaimana kesejahteraan dan pengeluaran masyarakat kita tersebar dari Sabang sampai Merauke.
""")
st.divider() # Garis pemisah estetik

# --- BAGIAN 1: PETA BUMI SATELIT (PLOTLY TERBARU) ---
st.header("1. Wajah Kesejahteraan dari Udara")
st.write("Warna merah menunjukkan kemiskinan yang lebih tinggi, sementara besarnya lingkaran cyan mewakili kekuatan ekonomi (PDRB).")

# 🌟 FITUR BARU: ANOTASI OTOMATIS (Mencari Tertinggi & Terendah)
gdf['Pct_Miskin'] = pd.to_numeric(gdf['Pct_Miskin'], errors='coerce')
gdf['PDRB'] = pd.to_numeric(gdf['PDRB'], errors='coerce')

daerah_miskin_max = gdf.loc[gdf['Pct_Miskin'].idxmax()]
daerah_pdrb_max = gdf.loc[gdf['PDRB'].idxmax()]

# Tampilkan sebagai kartu metrik estetik di atas peta
col1, col2, col3 = st.columns(3)
with col1:
    st.error(f"🚨 Kemiskinan Tertinggi:\n**{daerah_miskin_max['Kab/Kota']}** ({daerah_miskin_max['Pct_Miskin']}%)")
with col2:
    st.success(f"💎 PDRB Tertinggi:\n**{daerah_pdrb_max['Kab/Kota']}** ({daerah_pdrb_max['PDRB']} Miliar)")
with col3:
    st.info("💡 Interaksi Peta:\nScroll untuk Zoom, arahkan kursor (hover) ke pulau/titik untuk detail.")

st.divider()

# 🚀 PEMBUATAN PETA PLOTLY (SUPER MULUS & ESTETIK)

# Layer 1: Peta Area (Choropleth)
fig_map = px.choropleth_map(
    gdf,
    geojson=gdf.geometry,
    locations=gdf.index,
    color='Pct_Miskin',
    color_continuous_scale="YlOrRd",
    map_style="white-bg", 
    zoom=4,
    center={"lat": -0.789, "lon": 113.921},
    opacity=0.9, # <-- NAIK JADI 0.9: Warna akan jauh lebih tajam dan tidak "mendem"
    hover_name='Kab/Kota',
    # Menampilkan kedua data di kotak hover dengan format 2 desimal
    hover_data={'Pct_Miskin': ':.2f', 'PDRB': ':.2f'}, 
    # Merapikan nama variabel yang muncul di hover
    labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Miliar)', 'index': 'Kode ID'}
)

# Layer Satelit Asli Esri
fig_map.update_layout(
    map_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]
        }
    ],
    margin={"r":0,"t":0,"l":0,"b":0} 
)
 
# Layer 2: Bubble PDRB 
gdf_bubble = gdf.dropna(subset=['PDRB', 'centroid_x', 'centroid_y'])
fig_bubble = px.scatter_map( 
    gdf_bubble,
    lat='centroid_y',
    lon='centroid_x',
    size='PDRB',
    hover_name='Kab/Kota',
    hover_data={'PDRB': ':.2f', 'Pct_Miskin': ':.2f', 'centroid_y': False, 'centroid_x': False}, 
    labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Miliar)'},
    size_max=45, 
    zoom=4
)

# 🌟 TRIK EFEK GLOWING (Merah Pudar)
fig_bubble.update_traces(
    marker=dict(
        color='#00FF00',     # Warna merah menyala
        opacity=0.4          # Semi-transparan agar terlihat membaur (TIDAK ADA KOMA DI SINI)
        # HAPUS BARIS 'line=dict(width=0)' KARENA TIDAK DIDUKUNG OLEH SCATTER_MAP
    )
)

# Gabungkan Layer Bubble ke atas Layer Peta
for trace in fig_bubble.data:
    fig_map.add_trace(trace)

# Tampilkan Peta ke Web Streamlit
st.plotly_chart(fig_map, use_container_width=True)