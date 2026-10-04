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
st.set_page_config(page_title="Kisah Ekonomi Nusantara", page_icon="🌾", layout="wide", initial_sidebar_state="collapsed")

# Palet Warna (Mint / Sage Green / Earth Tones) + aksen hangat
COLOR_MINT = '#d4edda'
COLOR_SAGE = '#8fbc8f'
COLOR_FOREST = '#2e8b57'
COLOR_DARK = '#1a432b'
COLOR_HIGHLIGHT = '#ff9f43'  # Warna kontras untuk Highlight/Pencilan
COLOR_INK = '#12332b'
COLOR_CORAL = '#e8590c'
COLOR_AMBER = '#f2b33d'
COLOR_SKY = '#3b8ad9'

# OPSIONAL: isi dengan URL video .mp4 (mis. dari Pexels/Pixabay: kemiskinan, sawah, kota)
# agar tampil sebagai video latar halus di bagian hero. Kosongkan jika tidak dipakai.
HERO_VIDEO_URL = ""

# =====================================================================
# STYLE (CSS) & HELPER TAMPILAN
# =====================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
@property --n { syntax: '<integer>'; initial-value: 0; inherits: false; }
:root{
  --ink:#12332b; --muted:#557268; --mint:#d4edda; --sage:#8fbc8f; --forest:#2e8b57; --deep:#1a432b;
  --amber:#f2b33d; --coral:#e8590c; --sky:#3b8ad9;
}
html, body, .stApp, .stMarkdown, p, li, label, button, input, textarea{ font-family:'Plus Jakarta Sans', sans-serif; color:var(--ink); }
h1,h2,h3,h4,h5{ font-family:'Bricolage Grotesque','Plus Jakarta Sans',sans-serif !important; color:var(--ink) !important; letter-spacing:-0.02em; }
[data-testid="stMain"]{ scroll-behavior:smooth; }
.stApp{ background:linear-gradient(180deg,#eef8f1 0%,#f7fbf4 45%,#fdf5e6 100%); }
.stApp::before{
  content:""; position:fixed; inset:-15%; z-index:0; pointer-events:none;
  background:
    radial-gradient(520px 380px at 10% 10%, rgba(143,188,143,.50), transparent 62%),
    radial-gradient(480px 400px at 92% 16%, rgba(242,179,61,.30), transparent 62%),
    radial-gradient(640px 460px at 82% 86%, rgba(59,138,217,.16), transparent 62%),
    radial-gradient(480px 360px at 10% 88%, rgba(232,89,12,.12), transparent 62%);
  animation:drift 26s ease-in-out infinite alternate;
}
@keyframes drift{ to{ transform:translate3d(3%,-2%,0) scale(1.08) rotate(2deg); } }
[data-testid="stMainBlockContainer"], .block-container{ position:relative; z-index:1; max-width:1180px; padding-top:1.6rem; }
header[data-testid="stHeader"]{ background:transparent; }
footer{ visibility:hidden; }
hr{ border:0 !important; height:2px !important; background:linear-gradient(90deg,transparent,rgba(46,139,87,.45),transparent) !important; margin:2.2rem 0 !important; }

/* progress scroll */
.progress{ position:fixed; top:0; left:0; right:0; height:4px; z-index:9999; transform-origin:0 50%; transform:scaleX(0);
  background:linear-gradient(90deg,var(--forest),var(--amber),var(--coral)); }
@supports (animation-timeline: scroll()){ .progress{ animation:prog linear both; animation-timeline:scroll(nearest); } }
@keyframes prog{ to{ transform:scaleX(1); } }

/* HERO */
.hero{ position:relative; display:grid; grid-template-columns:1.1fr .9fr; gap:24px; align-items:center; padding:46px 42px 38px;
  border-radius:32px; overflow:hidden; background:linear-gradient(135deg,rgba(255,255,255,.86),rgba(220,242,228,.72));
  border:1px solid rgba(255,255,255,.95); box-shadow:0 30px 70px -30px rgba(23,64,50,.38); margin-bottom:1.6rem; }
.hero-video{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:.26; z-index:0; }
.hero > *:not(video){ position:relative; z-index:1; }
.hero h1{ font-size:clamp(2.4rem,5vw,4.1rem); line-height:1.02; font-weight:800; margin:0 0 10px; padding:0; }
.hero .sub{ font-size:1.15rem; color:var(--forest); font-weight:700; margin:0 0 14px; }
.hero .lead{ color:var(--muted); font-size:1.02rem; line-height:1.65; max-width:52ch; margin:0 0 20px; }
.hero-copy > *{ animation:rise .9s cubic-bezier(.2,.8,.2,1) both; }
.hero-copy > *:nth-child(2){ animation-delay:.12s } .hero-copy > *:nth-child(3){ animation-delay:.24s }
.hero-copy > *:nth-child(4){ animation-delay:.36s } .hero-copy > *:nth-child(5){ animation-delay:.48s }
@keyframes rise{ from{ opacity:0; transform:translateY(22px); } to{ opacity:1; transform:none; } }
.cta-row{ display:flex; gap:10px; flex-wrap:wrap; margin-bottom:22px; }
.cta{ display:inline-block; padding:12px 22px; border-radius:999px; font-weight:700; text-decoration:none !important;
  transition:transform .25s ease, box-shadow .25s ease; }
.cta.main{ background:var(--forest); color:#fff !important; box-shadow:0 12px 24px -10px rgba(46,139,87,.8); }
.cta.ghost{ background:rgba(255,255,255,.9); color:var(--deep) !important; border:1px solid rgba(46,139,87,.3); }
.cta:hover{ transform:translateY(-3px); }
.chips{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }
.chip{ background:rgba(255,255,255,.85); border-radius:18px; padding:12px 14px; border:1px solid rgba(46,139,87,.12); }
.chip b{ display:block; font-family:'Bricolage Grotesque',sans-serif; font-size:1.55rem; font-weight:800; color:var(--deep); }
.chip > span{ font-size:.9rem; color:var(--muted); }
.cnt{ --n:0; counter-reset:n var(--n); animation:cnt 2.2s ease-out .6s both; }
.cnt::before{ content:counter(n); }
@keyframes cnt{ from{ --n:0; } to{ --n:var(--i); } }
.scene{ width:100%; height:auto; }
.scene .sway{ transform-box:fill-box; transform-origin:50% 100%; animation:sway 3.4s ease-in-out var(--d) infinite alternate; }
@keyframes sway{ from{ transform:rotate(-5deg); } to{ transform:rotate(5deg); } }
.scene .bar{ transform-box:fill-box; transform-origin:50% 100%; animation:grow 1.2s cubic-bezier(.2,.8,.2,1) var(--d) both; }
@keyframes grow{ from{ transform:scaleY(0); } to{ transform:scaleY(1); } }
.scene .trend{ stroke-dasharray:260; stroke-dashoffset:260; animation:draw 1.6s ease-out 1.3s forwards; }
@keyframes draw{ to{ stroke-dashoffset:0; } }
.scene .dot{ opacity:0; animation:pop .5s ease-out 2.8s forwards; }
@keyframes pop{ to{ opacity:1; } }
.scene .coin{ animation:float 4s ease-in-out var(--d) infinite alternate; }
@keyframes float{ from{ transform:translateY(6px); } to{ transform:translateY(-10px); } }
.scene .halo{ transform-box:fill-box; transform-origin:center; animation:pulse 4s ease-in-out infinite alternate; }
@keyframes pulse{ to{ transform:scale(1.25); opacity:.08; } }
@media (max-width:860px){ .hero{ grid-template-columns:1fr; padding:30px 22px; } .chips{ grid-template-columns:repeat(2,1fr); } }

/* BADGE BAB */
.badge{ display:inline-flex; align-items:center; gap:8px; padding:6px 14px; border-radius:999px; background:rgba(46,139,87,.12);
  color:var(--forest); font-weight:700; font-size:.85rem; margin-bottom:4px; }
.badge::before{ content:""; width:8px; height:8px; border-radius:50%; background:var(--forest); animation:blink 2s ease-in-out infinite; }
@keyframes blink{ 50%{ opacity:.25; transform:scale(.7); } }

/* CARDS */
.card{ --c:var(--sky); position:relative; display:flex; gap:14px; align-items:flex-start; min-height:160px; height:100%;
  background:rgba(255,255,255,.76); backdrop-filter:blur(14px); border:1px solid rgba(255,255,255,.95); border-radius:22px;
  padding:20px 22px; box-shadow:0 12px 30px -14px rgba(23,64,50,.28); overflow:hidden;
  transition:transform .35s cubic-bezier(.2,.8,.2,1), box-shadow .35s ease; }
.card::after{ content:""; position:absolute; right:-40px; top:-40px; width:120px; height:120px; border-radius:50%;
  background:var(--c); opacity:.12; transition:transform .5s ease, opacity .5s ease; }
.card:hover{ transform:translateY(-6px); box-shadow:0 22px 40px -16px rgba(23,64,50,.4); }
.card:hover::after{ transform:scale(1.8); opacity:.18; }
.card.bad{ --c:var(--coral); } .card.good{ --c:var(--forest); } .card.info{ --c:var(--sky); } .card.warn{ --c:var(--amber); }
.card-ico{ flex:0 0 auto; width:46px; height:46px; display:grid; place-items:center; font-size:1.4rem; border-radius:14px;
  background:color-mix(in srgb, var(--c) 16%, white); transition:transform .4s ease; }
.card:hover .card-ico{ transform:rotate(-8deg) scale(1.1); }
.card-title{ font-family:'Bricolage Grotesque',sans-serif; font-weight:700; font-size:1.05rem; margin-bottom:2px; }
.card p{ margin:6px 0 0; color:var(--muted); line-height:1.6; font-size:.95rem; }
.card .big{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:1.9rem; color:var(--c); line-height:1.15; }
.card ul{ margin:8px 0 0; padding-left:1.1rem; color:var(--muted); line-height:1.65; font-size:.95rem; }
.card.wide{ min-height:0; }
.mini{ text-align:center; display:block; min-height:0; padding:14px; }
.mini .big{ font-size:1.7rem; } .mini .card-title{ font-size:.9rem; color:var(--muted); font-weight:600; }

/* HEADER GRAFIK */
.chart-head{ margin:.9rem 0 .5rem; padding-left:12px; border-left:4px solid var(--forest); }
.chart-head b{ font-family:'Bricolage Grotesque',sans-serif; font-size:1.1rem; color:var(--ink); }
.chart-head span{ display:block; color:var(--muted); font-size:.9rem; line-height:1.5; margin-top:2px; }

/* STORY / PIKTOGRAM */
.story{ display:grid; grid-template-columns:minmax(0,.9fr) 3px minmax(0,1.3fr); gap:30px; align-items:center; min-height:58vh; padding:2.2rem 0; }
.story .rail{ align-self:stretch; background:linear-gradient(180deg,transparent,var(--deep),transparent); border-radius:3px; }
.story-card{ background:rgba(255,255,255,.88); border:1.5px solid var(--deep); border-radius:28px; padding:26px 28px; box-shadow:0 18px 40px -20px rgba(23,64,50,.35); }
.story-card h4{ margin:.5rem 0 .5rem; font-size:1.4rem; }
.story-card p{ color:var(--muted); line-height:1.7; margin:0; }
.vis-title{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:1.7rem; color:var(--deep); text-align:center; margin-bottom:12px; }
.vis-panel{ background:rgba(255,255,255,.85); border-radius:24px; padding:22px 24px; box-shadow:0 14px 34px -16px rgba(23,64,50,.3); }
.vis-note{ margin-top:10px; text-align:center; color:var(--coral); font-weight:600; font-size:.9rem; }
.pic-bad{ --pc:var(--coral); } .pic-good{ --pc:var(--forest); } .pic-gold{ --pc:var(--amber); }
.cell{ position:relative; display:inline-block; flex:none; width:var(--w,24px); transition:transform .25s ease; }
.cell:hover{ transform:translateY(-5px) scale(1.18); }
.cell svg{ display:block; width:100%; height:auto; fill:currentColor; }
.cell.on{ color:var(--pc); } .cell.off, .cell.part{ color:#d3e6d9; }
.cell .over{ position:absolute; inset:0; color:var(--pc); clip-path:inset(0 calc(100% - var(--f)) 0 0); }
.grid100{ display:grid; grid-template-columns:repeat(10,1fr); gap:8px; max-width:420px; margin:0 auto; }
.grid100 .cell{ width:100%; }
.prow{ display:grid; grid-template-columns:minmax(90px,150px) 1fr auto; gap:12px; align-items:center; padding:8px 0; border-bottom:1px dashed rgba(46,139,87,.22); }
.prow:last-child{ border-bottom:0; }
.plabel{ font-weight:600; font-size:.92rem; }
.prow.hl .plabel{ font-weight:800; color:var(--deep); }
.prow.hl{ background:rgba(242,179,61,.14); border-radius:12px; padding-left:8px; }
.picons{ display:flex; flex-wrap:wrap; gap:4px; }
.pval{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800; color:var(--deep); white-space:nowrap; }
@supports (animation-timeline: view()){
  .story{ animation:stepin linear both; animation-timeline:view(); animation-range:entry 5% entry 50%; }
  .cell{ animation:popin linear backwards; animation-timeline:view(); animation-range:entry 0% entry 90%; }
}
@keyframes stepin{ from{ opacity:0; transform:translateY(60px); } to{ opacity:1; transform:none; } }
@keyframes popin{ from{ opacity:0; transform:scale(.3); } to{ opacity:1; transform:none; } }
@media (max-width:860px){ .story{ grid-template-columns:1fr; min-height:0; } .story .rail{ display:none; } .prow{ grid-template-columns:1fr; } }

/* WIDGET STREAMLIT */
[data-testid="stPlotlyChart"]{ background:rgba(255,255,255,.72); border-radius:24px; padding:0px; border:1px solid rgba(255,255,255,.95);
  box-shadow:0 14px 34px -16px rgba(23,64,50,.3); overflow:hidden; transition:box-shadow .3s ease; }
[data-testid="stPlotlyChart"]:hover{ box-shadow:0 22px 44px -16px rgba(23,64,50,.42); }
[data-testid="stMetric"]{ background:rgba(255,255,255,.78); border-radius:20px; padding:14px 18px; border:1px solid rgba(255,255,255,.95);
  box-shadow:0 10px 26px -14px rgba(23,64,50,.28); transition:transform .3s ease; }
[data-testid="stMetric"]:hover{ transform:translateY(-4px); }
div[data-baseweb="select"] > div{ border-radius:14px !important; background:rgba(255,255,255,.9) !important; border-color:rgba(46,139,87,.3) !important; }
div[role="radiogroup"]{ gap:8px !important; flex-wrap:wrap; }
label[data-baseweb="radio"]{ background:rgba(255,255,255,.85); border:1px solid rgba(46,139,87,.28); padding:6px 16px; border-radius:999px;
  margin:0 !important; transition:all .25s ease; cursor:pointer; }
label[data-baseweb="radio"] > div:first-child{ display:none; }
label[data-baseweb="radio"]:hover{ transform:translateY(-2px); border-color:var(--forest); }
label[data-baseweb="radio"]:has(input:checked){ background:var(--forest); border-color:var(--forest); box-shadow:0 8px 18px -8px rgba(46,139,87,.8); }
label[data-baseweb="radio"]:has(input:checked) *{ color:#fff !important; }
button[data-baseweb="tab"]{ font-weight:700; border-radius:12px 12px 0 0; transition:background .25s ease; }
button[data-baseweb="tab"]:hover{ background:rgba(46,139,87,.1); }
[data-baseweb="tab-highlight"]{ background-color:var(--forest) !important; height:3px !important; border-radius:3px; }
[data-testid="stExpander"]{ border-radius:18px; background:rgba(255,255,255,.7); }
@media (prefers-reduced-motion:reduce){
  *, *::before, *::after{ animation:none !important; transition:none !important; }
  .cnt{ --n:var(--i); } .scene .trend{ stroke-dashoffset:0; } .scene .dot{ opacity:1; }
}
</style>
"""


def html(s):
    """Render HTML tanpa baris kosong/indentasi agar tidak dibaca sebagai blok kode markdown."""
    st.markdown("\n".join(l.strip() for l in s.splitlines() if l.strip()), unsafe_allow_html=True)


def card(kind, icon, title, body, big=None):
    big_html = f'<div class="big">{big}</div>' if big else ""
    html(f'<div class="card {kind}"><div class="card-ico">{icon}</div><div><div class="card-title">{title}</div>{big_html}<p>{body}</p></div></div>')


def mini_card(kind, title, value):
    html(f'<div class="card mini {kind}"><div class="big">{value}</div><div class="card-title">{title}</div></div>')


def bab(label):
    html(f'<div class="badge">{label}</div>')


def chart_header(judul, sub=""):
    sub_html = f"<span>{sub}</span>" if sub else ""
    html(f'<div class="chart-head"><b>{judul}</b>{sub_html}</div>')


def fmt_id(v, d=2):
    """Format angka gaya Indonesia: titik ribuan, koma desimal."""
    return f"{v:,.{d}f}".replace(',', 'X').replace('.', ',').replace('X', '.')


PERSON = '<svg viewBox="0 0 20 28"><circle cx="10" cy="6" r="5"/><path d="M2 28V16a8 8 0 0 1 16 0v12z"/></svg>'
COIN = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11"/><circle cx="12" cy="12" r="8" fill="none" stroke="#fff" stroke-opacity=".7"/><text x="12" y="15.5" text-anchor="middle" font-size="9" font-weight="800" fill="#7a4e00">Rp</text></svg>'


def nice_unit(maxv, target=10):
    """Pilih satuan 'bulat' agar baris piktogram terpanjang sekitar 10 ikon."""
    raw = maxv / target
    for u in [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]:
        if u >= raw:
            return u
    return raw


def ikon(svg, f=1.0, ghost=False):
    """Satu ikon piktogram: penuh (f=1), sebagian (0<f<1), atau kosong/pudar (ghost)."""
    if f >= 0.999:
        return f'<span class="cell on">{svg}</span>'
    if f <= 0.001:
        return f'<span class="cell off">{svg}</span>' if ghost else ''
    return f'<span class="cell part" style="--f:{f * 100:.0f}%">{svg}<span class="over">{svg}</span></span>'


def pic_rows(items, svg, unit, fmt, hl=None):
    out = ""
    for label, val in items:
        n = max(val, 0) / unit
        full = int(n)
        icons = ikon(svg) * full + ikon(svg, n - full)
        cls = " hl" if hl is not None and str(label) == str(hl) else ""
        out += f'<div class="prow{cls}"><div class="plabel">{label}</div><div class="picons">{icons}</div><div class="pval">{fmt(val)}</div></div>'
    return out


def anim_num(v, dec=False):
    if dec:
        a, b = f"{v:.1f}".split('.')
        return f'<span class="cnt" style="--i:{a}"></span>,<span class="cnt" style="--i:{b}"></span>'
    return f'<span class="cnt" style="--i:{int(v)}"></span>'


def tema(fig):
    """Selaraskan tampilan grafik Plotly dengan tema halaman (tanpa mengubah data)."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=COLOR_INK),
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Plus Jakarta Sans, sans-serif"),
    )
    return fig

# =====================================================================
# FUNGSI PEMUATAN & PEMBERSIHAN DATA (TIDAK DIUBAH)
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
html(CSS)
html('<div class="progress"></div>')

# ---------------------------- HERO ----------------------------------
n_kab = gdf['Kab/Kota'].nunique()
n_prov = len(df_multi)
miskin_terbaru = gdf[gdf['Tahun'] == '2025']['Pct_Miskin'].mean()
ipm_terbaru = df_multi['IPM'].mean()
video_tag = (f'<video class="hero-video" src="{HERO_VIDEO_URL}" autoplay muted loop playsinline></video>'
             if HERO_VIDEO_URL else "")

html(f"""
<section class="hero">
{video_tag}
<div class="hero-copy">
<h1>Di Antara Angka dan Realita</h1>
<div class="sub">Jejak Kesejahteraan Indonesia (2021 - 2025)</div>
<p class="lead">Setiap jengkal tanah di Nusantara menyimpan ceritanya sendiri. Ada wilayah yang roda ekonominya berputar kencang, namun ada pula yang masih berjuang melepaskan diri dari jerat kemiskinan.</p>
<div class="cta-row"><a class="cta main" href="#bab-1">Mulai dari peta</a><a class="cta ghost" href="#bab-4">Langsung ke profil provinsi</a></div>
<div class="chips">
<div class="chip"><b>{anim_num(514)}</b><span>Kabupaten & Kota</span></div>
<div class="chip"><b>{anim_num(n_prov)}</b><span>Provinsi dibedah</span></div>
<div class="chip"><b>{anim_num(ipm_terbaru, dec=True)}</b><span>Rata-rata IPM 2025</span></div>
<div class="chip"><b>{anim_num(miskin_terbaru, dec=True)}%</b><span>Penduduk Miskin 2025</span></div>
</div>
</div>
<div class="hero-art">
<svg viewBox="0 0 520 380" class="scene" role="img" aria-label="Ilustrasi permukiman, padi, dan gedung pertumbuhan ekonomi">
<defs>
<linearGradient id="gbar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3fb37f"/><stop offset="1" stop-color="#2e8b57"/></linearGradient>
<radialGradient id="gsun"><stop offset="0" stop-color="#ffd978"/><stop offset="1" stop-color="#f2b33d"/></radialGradient>
<g id="wheat"><line x1="0" y1="0" x2="0" y2="-64" stroke="#b58b2a" stroke-width="3" stroke-linecap="round"/>
<ellipse cx="0" cy="-70" rx="5" ry="10" fill="#f2b33d"/>
<ellipse cx="-7" cy="-60" rx="4" ry="8" fill="#f2b33d" transform="rotate(-25 -7 -60)"/>
<ellipse cx="7" cy="-60" rx="4" ry="8" fill="#f2b33d" transform="rotate(25 7 -60)"/>
<ellipse cx="-7" cy="-48" rx="4" ry="8" fill="#e6a42c" transform="rotate(-25 -7 -48)"/>
<ellipse cx="7" cy="-48" rx="4" ry="8" fill="#e6a42c" transform="rotate(25 7 -48)"/></g>
</defs>
<circle class="halo" cx="92" cy="78" r="52" fill="#f2b33d" opacity=".2"/>
<circle cx="92" cy="78" r="34" fill="url(#gsun)"/>
<path d="M0 292 Q130 246 262 286 T520 268 V380 H0Z" fill="#cfe8d5"/>
<path d="M0 326 Q150 292 300 322 T520 306 V380 H0Z" fill="#9ccb9c"/>
<path d="M0 352 Q170 330 330 350 T520 340 V380 H0Z" fill="#6fae7c"/>
<rect x="34" y="266" width="52" height="36" fill="#f3d2ab"/><polygon points="28,268 60,240 92,268" fill="#c8794a"/><rect x="52" y="282" width="14" height="20" fill="#8a5a3b"/>
<rect x="98" y="278" width="40" height="26" fill="#e8d6bb"/><polygon points="93,280 118,258 143,280" fill="#a8683f"/><rect x="111" y="289" width="10" height="15" fill="#7a4e33"/>
<use href="#wheat" x="180" y="318" class="sway" style="--d:.2s"/>
<use href="#wheat" x="202" y="322" class="sway" style="--d:.7s"/>
<use href="#wheat" x="224" y="316" class="sway" style="--d:1.1s"/>
<use href="#wheat" x="246" y="321" class="sway" style="--d:.5s"/>
<rect class="bar" x="300" y="258" width="28" height="54" rx="5" fill="url(#gbar)" style="--d:.2s"/>
<rect class="bar" x="336" y="230" width="28" height="82" rx="5" fill="url(#gbar)" style="--d:.4s"/>
<rect class="bar" x="372" y="202" width="28" height="110" rx="5" fill="url(#gbar)" style="--d:.6s"/>
<rect class="bar" x="408" y="172" width="28" height="140" rx="5" fill="url(#gbar)" style="--d:.8s"/>
<rect class="bar" x="444" y="136" width="28" height="176" rx="5" fill="url(#gbar)" style="--d:1s"/>
<polyline class="trend" points="314,246 350,218 386,190 422,156 458,112" fill="none" stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<circle class="dot" cx="458" cy="112" r="7" fill="#e8590c"/>
<g class="coin" style="--d:0s"><circle cx="268" cy="168" r="15" fill="#f2b33d"/><circle cx="268" cy="168" r="11" fill="none" stroke="#fff" stroke-opacity=".7"/><text x="268" y="173" text-anchor="middle" font-size="11" font-weight="800" fill="#7a4e00">Rp</text></g>
<g class="coin" style="--d:.9s"><circle cx="226" cy="118" r="13" fill="#f2b33d"/><circle cx="226" cy="118" r="9" fill="none" stroke="#fff" stroke-opacity=".7"/><text x="226" y="122" text-anchor="middle" font-size="9" font-weight="800" fill="#7a4e00">Rp</text></g>
<g class="coin" style="--d:1.7s"><circle cx="170" cy="190" r="11" fill="#f2b33d"/><text x="170" y="194" text-anchor="middle" font-size="8" font-weight="800" fill="#7a4e00">Rp</text></g>
<text x="62" y="366" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kemiskinan</text>
<text x="214" y="366" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Pangan</text>
<text x="386" y="366" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">PDRB</text>
</svg>
</div>
</section>
""")

# --- BAB 1: Peta ---
html('<div id="bab-1"></div>')
bab("Bab 1")
st.markdown("### Potret Ekonomi Wilayah Indonesia")
st.write("Peta ini membandingkan dua sisi realita ekonomi daerah. Warna yang semakin **merah** menandakan tingginya persentase penduduk miskin. Di sisi lain, besarnya **lingkaran hijau** menunjukkan tingginya nilai ekonomi (PDRB) yang berputar di wilayah tersebut.")

# Wadah kartu: diisi setelah tahun dipilih, supaya kontrol berada tepat di atas peta
area_kartu = st.container()

# Judul peta diperbesar font-nya menggunakan tag <span>
chart_header("<span style='font-size: 1.6rem; margin-top: 20px;'>Peta Kemiskinan dan PDRB Kabupaten/Kota</span>",
            "Pilih tahun untuk melihat perbandingan data kemiskinan dan PDRB di seluruh Indonesia.")

# Injeksi CSS Khusus untuk Efek Peta Full Frame & Dropdown Mengapung
st.markdown("""
    <style>
    /* Mempercantik bentuk Selectbox (Dropdown) agar tidak kaku */
    div[data-baseweb="select"] > div {
        border-radius: 99px !important;
        background: rgba(255,255,255,0.92) !important;
        border: 2px solid rgba(46,139,87,0.3) !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        font-weight: 700;
        cursor: pointer;
    }
    /* Memposisikan Selectbox agar mengapung rapi di sudut kiri atas peta */
    div[data-testid="stSelectbox"] {
        position: relative;
        z-index: 10;
        width: 130px; 
        margin-left: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Dropdown Tahun: Label disembunyikan (collapsed) agar hemat tempat
selected_year = st.selectbox(
    "Pilih Tahun", 
    options=[2021, 2022, 2023, 2024, 2025], 
    index=4,
    label_visibility="collapsed"
)

# FILTER DATA BERDASARKAN TAHUN YANG DIPILIH
gdf_year = gdf[gdf['Tahun'] == str(selected_year)].copy()

# HIGHLIGHT CARD (Otomatis berubah sesuai tahun)
daerah_miskin_max = gdf_year.loc[gdf_year['Pct_Miskin'].idxmax()]
daerah_pdrb_max = gdf_year.loc[gdf_year['PDRB'].idxmax()]

def agregat(th):
    d = gdf[gdf['Tahun'] == str(th)]
    return d['Pct_Miskin'].mean(), d['PDRB'].sum()

m_now, p_now = agregat(selected_year)
ada_prev = selected_year > 2021
m_prev, p_prev = agregat(selected_year - 1) if ada_prev else (None, None)
n_atas = int((gdf_year['Pct_Miskin'] > m_now).sum())

with area_kartu:
    col1, col2, col3 = st.columns(3)
    with col1:
        card("bad", "🚨", f"Kab/Kota Kemiskinan Tertinggi ({selected_year})", f"{daerah_miskin_max['Kab/Kota']}", big=f"{fmt_id(daerah_miskin_max['Pct_Miskin'])}%")
    with col2:
        card("good", "💎", f"Kab/Kota PDRB  Tertinggi ({selected_year})", f"{daerah_pdrb_max['Kab/Kota']}", big=f"{fmt_id(daerah_pdrb_max['PDRB'])} Triliun")
    with col3:
        # Kartu ketiga diganti dengan jumlah daerah di atas rata-rata
        card("warn", "⚠️", f"Wilayah Rentan ({selected_year})", f"Daerah dengan kemiskinan di atas rerata nasional ({fmt_id(m_now)}%).", big=f"{n_atas} Daerah")

# Teks Tip Peta yang berkedip elegan
st.markdown('''
    <style>@keyframes pulse-hint { 0% { opacity: 0.2; } 100% { opacity: 0.8; } }</style>
    <div style="text-align: center; margin: 20px 0 5px; font-size: 0.85rem; color: var(--muted); animation: pulse-hint 1.5s infinite alternate ease-in-out;">
        💡 <i>Tip: Gunakan scroll untuk zoom-in/out peta, atau arahkan kursor ke wilayah mana pun untuk detailnya.</i>
    </div>
''', unsafe_allow_html=True)

# 1. Tangani data yang kosong (NaN)
gdf_year['Pct_Miskin_Clean'] = gdf_year['Pct_Miskin'].fillna(-1) 

# 2. Render Peta Utama
fig_map = px.choropleth_map(
    gdf_year, 
    geojson=gdf_year.geometry, 
    locations=gdf_year.index,
    color='Pct_Miskin_Clean', 
    color_continuous_scale="YlOrRd",
    range_color=[0, gdf['Pct_Miskin'].max()],
    map_style="white-bg", 
    zoom=4, 
    center={"lat": -0.789, "lon": 113.921},
    opacity=0.9, 
    hover_name='Kab/Kota',
    hover_data={'Pct_Miskin': ':.2f', 'PDRB': ':.2f', 'Pct_Miskin_Clean': False}, 
    labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Triliun)'}
)

# 3. Pengaturan Layout Peta
sumber_tile = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"

fig_map.update_layout(
    map_layers=[{"below": 'traces', "sourcetype": "raster", "source": [sumber_tile]}],
    margin={"r":0, "t":0, "l":0, "b":0},
    # Menarik Legenda (Colorbar) ke dalam pojok kanan bawah peta
    coloraxis_colorbar=dict(
        title="Kemiskinan(%)",
        orientation="v",
        yanchor="bottom", y=0.03,
        xanchor="right", x=0.98,
        thickness=8, 
        len=0.45,
        bgcolor="rgba(255,255,255,0.85)", 
        bordercolor="rgba(46,139,87,0.3)",
        borderwidth=1,
        title_side="top"
    )
)

# 4. Tambahkan Pendaran Hijau untuk PDRB
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

# 5. TAMPILKAN PETA KE STREAMLIT (Ini yang tadi terlewat!)
st.plotly_chart(tema(fig_map), use_container_width=True)

card("good", "📌", f"Catatan {selected_year}", "Wilayah yang kosong (tidak berwarna) pada peta menunjukkan bahwa data untuk kabupaten/kota tersebut tidak tersedia atau tidak tercatat pada tahun observasi.")
st.markdown("<br>", unsafe_allow_html=True)

# Eksplorasi lanjutan: cerita bergulir (scrollytelling)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 🧭 Eksplorasi Lanjutan")
st.write("Gulir pelan ke bawah. Setiap fase memunculkan satu cerita baru yang menyoroti realitas ekonomi Nusantara.")

# Hapus pilihan st.radio, patenkan ke Top 5
top_n = 5

tahun_semua = [2021, 2022, 2023, 2024, 2025]
agr = {t: agregat(t) for t in tahun_semua}

# ==========================================
# HELPER BARU: Scrollytelling (Perataan Vertikal di Tengah)
# ==========================================
def fase_st(no, judul, isi, vis_judul, vis_content, catatan=""):
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    html_card = f'<div class="story-card" style="margin: 0;"><div class="badge">Fase {no}</div><h4>{judul}</h4><p>{isi}</p></div>'
    html_rail = '<div style="height: 100%; min-height: 180px; width: 3px; background: linear-gradient(180deg, transparent, var(--deep), transparent); margin: 0 auto;"></div>'
    html_vis_title = f'<div class="vis-title" style="margin-bottom: 12px; font-weight: 800; font-size: 1.2rem; color: var(--deep); text-align:center;">{vis_judul}</div>'
    html_note = f'<div class="vis-note" style="text-align: center; color: var(--coral); font-weight: 600; font-size: 0.85rem; margin-top: 10px;">{catatan}</div>' if catatan else ""

    # Tambahkan vertical_alignment="center" agar text card dan grafik sejajar di tengah
    c_text, c_rail, c_vis = st.columns([1.1, 0.1, 1.2], gap="large", vertical_alignment="center")
    
    with c_text:
        st.markdown(html_card, unsafe_allow_html=True)
    with c_rail:
        st.markdown(html_rail, unsafe_allow_html=True)
    with c_vis:
        st.markdown(html_vis_title, unsafe_allow_html=True)
        if isinstance(vis_content, str):
            st.markdown(f'<div class="vis-panel">{vis_content}</div>', unsafe_allow_html=True)
        else:
            st.plotly_chart(tema(vis_content), use_container_width=True)
        st.markdown(html_note, unsafe_allow_html=True)


# ==========================================
# FASE 1: Potret Nasional (PIE CHART PLOTLY)
# ==========================================
fig_pie = px.pie(
    names=['Hidup Miskin', 'Di Atas Garis Kemiskinan'],
    values=[m_now, 100 - m_now],
    hole=0.5, 
    color_discrete_sequence=[COLOR_CORAL, '#d3e6d9']
)
# Menambahkan textposition='outside' agar label tidak saling tumpuk
fig_pie.update_traces(textinfo='percent+label', textfont_size=13, textposition='outside')
# Lebarkan sedikit margin kiri-kanan agar label luar tidak terpotong, tinggi 260
fig_pie.update_layout(margin=dict(t=10, b=10, l=40, r=40), showlegend=False, height=260)

fase_st(1, f"Potret Penduduk {selected_year}",
     f"Pada {selected_year}, rata-rata persentase penduduk di seluruh kabupaten/kota yang hidup di bawah garis kemiskinan adalah <b>{fmt_id(m_now)}%</b>. Mayoritas lainnya berhasil mempertahankan diri di atas garis tersebut, namun porsi ini belum tentu merata di tiap daerah.",
     f"Proporsi Nasional {selected_year}", fig_pie,
     "Persentase Rata-rata Nasional Kabupaten/Kota.")


# ==========================================
# FASE 2: Daerah Paling Miskin (PIKTOGRAM 1 BARIS)
# ==========================================
def pic_rows_per_10(items, svg, fmt):
    out = ""
    for label, val in items:
        n = val / 10
        full = int(n)
        icons = ikon(svg) * full + ikon(svg, n - full)
        sisa = max(0, 10 - full - 1)
        icons += ikon(svg, 0, ghost=True) * sisa
        
        # flex-wrap: nowrap untuk menolak turun baris, --w: 16px untuk mengecilkan icon
        out += f'<div class="prow" style="padding: 6px 0; grid-template-columns: minmax(80px, 1fr) auto 45px;"><div class="plabel" style="font-size: 0.85rem;">{label}</div><div class="picons" style="flex-wrap: nowrap; gap:3px; --w:16px;">{icons}</div><div class="pval" style="text-align:right; font-size: 0.9rem;">{fmt(val)}</div></div>'
    return out

d2 = gdf_year.dropna(subset=['Kab/Kota', 'Pct_Miskin']).nlargest(top_n, 'Pct_Miskin')
top2 = d2.iloc[0]

html_pic_10 = f'<div class="pic-bad" style="max-width: 100%; overflow-x: auto;">{pic_rows_per_10([(r["Kab/Kota"], r["Pct_Miskin"]) for _, r in d2.iterrows()], PERSON, lambda v: f"{fmt_id(v)}%")}</div>'

fase_st(2, f"{top_n} Daerah yang Paling Berat",
     f"Seandainya kita kumpulkan 10 orang dari <b>{top2['Kab/Kota']}</b>, lebih dari <b>{fmt_id(top2['Pct_Miskin'] / 10, 1)}</b> di antaranya sedang berjuang hidup di bawah garis kemiskinan. Rata-rata {top_n} daerah teratas ini mencapai <b>{fmt_id(d2['Pct_Miskin'].mean())}%</b>.",
     f"Kemiskinan Tertinggi {selected_year}",
     html_pic_10,
     "1 ikon = 1 dari 10 orang. Ikon pudar = di atas garis kemiskinan.")


# ==========================================
# FASE 3: Tren PDRB (LINE CHART PLOTLY)
# ==========================================
df_pdrb_tren = pd.DataFrame([{'Tahun': str(t), 'Total PDRB (Triliun)': agr[t][1]} for t in tahun_semua])

fig_line = px.line(df_pdrb_tren, x='Tahun', y='Total PDRB (Triliun)', markers=True)
# Ubah line_shape jadi 'spline' (melengkung), tambahkan fill tozeroy (area tipis)
fig_line.update_traces(
    line_color=COLOR_AMBER, 
    line_width=3, 
    line_shape='spline',
    fill='tozeroy', 
    fillcolor='rgba(242, 179, 61, 0.1)', 
    marker=dict(size=10, color=COLOR_FOREST)
)
# Tinggi diperkecil jadi 260
fig_line.update_layout(margin=dict(t=20, b=10, l=10, r=20), xaxis_title="", yaxis_title="Triliun Rupiah", hovermode="x unified", height=260)
# Matikan garis grid vertikal (showgrid=False)
fig_line.update_xaxes(type='category', showgrid=False)

p0, p1 = agr[2021][1], agr[2025][1]
g = (p1 - p0) / p0 * 100 if p0 else 0

fase_st(3, "Denyut Ekonomi, Lima Tahun",
     f"Total perputaran uang (PDRB) seluruh kabupaten/kota di Indonesia {'tumbuh' if g >= 0 else 'menyusut'} <b>{fmt_id(abs(g), 1)}%</b> sejak 2021. Dari Rp {fmt_id(p0, 0)} Triliun menjadi Rp {fmt_id(p1, 0)} Triliun pada 2025. Pertanyaan tersisa: apakah pertumbuhan ini dinikmati merata?",
     "Tren Akumulasi PDRB Nasional", fig_line,
     "Nilai Total PDRB Kabupaten/Kota dari tahun ke tahun.")

st.divider()

# --- BAB 2: Moran's I ---
bab("Bab 2")
st.markdown(f"### Mendeteksi Pola Kemiskinan di Tahun {selected_year}")
st.write("Melalui analisis keruangan (*Moran's I*), kita akan melihat apakah wilayah miskin cenderung bergerombol dengan tetangganya.")

try:
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

    # Tipe wilayah (bahasa awam) dari posisi kuadran
    N_KANTONG = "Pusat Kemiskinan"
    N_MAPAN = "Pusat Kesejahteraan"
    N_PULAU = "Tertinggal dari Sekitarnya"
    N_BINTANG = "Lebih Baik dari Sekitarnya"
    m_hh = (gdf_moran['Z_Miskin'] > 0) & (gdf_moran['Z_Lag'] > 0)
    m_ll = (gdf_moran['Z_Miskin'] < 0) & (gdf_moran['Z_Lag'] < 0)
    m_hl = (gdf_moran['Z_Miskin'] > 0) & (gdf_moran['Z_Lag'] < 0)
    m_lh = (gdf_moran['Z_Miskin'] < 0) & (gdf_moran['Z_Lag'] > 0)
    gdf_moran['Tipe Wilayah'] = np.select([m_hh, m_ll, m_hl, m_lh], [N_KANTONG, N_MAPAN, N_PULAU, N_BINTANG], default="Mendekati rata-rata")
    
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        st.metric(label=f"Indeks Global Moran's I ({selected_year})", value=f"{moran_global.I:.3f}")
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

        # Kartu informasi diganti dengan narasi analitis yang lebih profesional
        if moran_global.I > 0:
            card("info", "🗺️", "Pola Sebaran Spasial", f"Nilai positif menunjukkan bahwa daerah dengan tingkat kemiskinan tinggi di Indonesia cenderung mengelompok atau berdekatan secara geografis.")
        else:
            card("info", "🗺️", "Pola Sebaran Spasial", f"Nilai mendekati nol menunjukkan bahwa sebaran wilayah miskin cenderung acak dan tidak membentuk klaster spasial khusus.")

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        card("warn", "🧭", "Skala angkanya", "Jika Moran's I makin mendekati +1, maka akan bergerombol. Dekat 0 berarti acak.")

    with col_m2:
        chart_header("Apakah Kemiskinan Menular secara Geografis?")
        #              "Makin ke kanan, daerah itu makin miskin dari rata-rata. Makin ke atas, tetangga-tetangganya makin miskin.")
        fig_scatter = px.scatter(
            gdf_moran, x='Z_Miskin', y='Z_Lag', hover_name='Kab/Kota', color='Tipe Wilayah',
            hover_data={'Pct_Miskin': ':.2f', 'Z_Miskin': False, 'Z_Lag': False, 'Tipe Wilayah': False},
            labels={'Z_Miskin': 'Kemiskinan daerah (kanan = lebih miskin)', 'Z_Lag': 'Kemiskinan tetangga (atas = lebih miskin)'},
            color_discrete_map={N_KANTONG: COLOR_CORAL, N_MAPAN: COLOR_FOREST, N_PULAU: COLOR_AMBER, N_BINTANG: COLOR_SKY, "Mendekati rata-rata": "#b0b8b4"}
        )
        fig_scatter.update_traces(marker=dict(size=8, opacity=0.7))
        fig_scatter.add_vline(x=0, line_width=2, line_dash="dash", line_color="black")
        fig_scatter.add_hline(y=0, line_width=2, line_dash="dash", line_color="black")
        for tx, px_, py_, xa, ya, wr in [(N_KANTONG, .98, .98, 'right', 'top', COLOR_CORAL), (N_BINTANG, .02, .98, 'left', 'top', COLOR_SKY),
                                         (N_MAPAN, .02, .02, 'left', 'bottom', COLOR_FOREST), (N_PULAU, .98, .02, 'right', 'bottom', '#b9821a')]:
            fig_scatter.add_annotation(xref='paper', yref='paper', x=px_, y=py_, xanchor=xa, yanchor=ya, text=f"<b>{tx}</b>", showarrow=False, font=dict(color=wr, size=13))
        fig_scatter.update_layout(legend=dict(orientation='h', y=-0.22, title=None), margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(tema(fig_scatter), use_container_width=True)

    # Empat tipe wilayah, dijelaskan dengan bahasa cerita
    st.markdown("#### Empat Tipe Wilayah dalam Analisis")
    st.write("Dengan membandingkan tingkat kemiskinan sebuah daerah dengan wilayah tetangganya, kita mendapati empat kategori:")
    q1, q2, q3, q4 = st.columns(4)
    with q1: card("bad", "🔥", N_KANTONG, "Daerah miskin yang dikelilingi oleh wilayah yang juga miskin. <i>(High-High)</i>", big=f"{int(m_hh.sum())} daerah")
    with q2: card("good", "🌿", N_MAPAN, "Daerah sejahtera yang dikelilingi oleh wilayah yang kondisinya serupa. <i>(Low-Low)</i>", big=f"{int(m_ll.sum())} daerah")
    with q3: card("warn", "📍", N_PULAU, "Daerah miskin yang secara anomali berada di tengah kawasan relatif sejahtera. <i>(High-Low)</i>", big=f"{int(m_hl.sum())} daerah")
    with q4: card("info", "⭐", N_BINTANG, "Daerah yang kondisinya baik meskipun dikelilingi oleh kawasan miskin. <i>(Low-High)</i>", big=f"{int(m_lh.sum())} daerah")
    
    # Mengambil data daerah dengan tingkat kemiskinan tertinggi di kuadran Pusat Kemakmuran/Pusat Kemiskinan (High-High)
    df_hot = pd.DataFrame(gdf_moran.loc[m_hh, ['Kab/Kota', 'Pct_Miskin']]).sort_values('Pct_Miskin', ascending=False)
    contoh = df_hot.head(3)['Kab/Kota'].tolist()
    
    # Menyusun narasi yang lebih natural, manusiawi, dan menyoroti wilayah parah
    cerita_natural = (
        f"Dari total <b>514 kabupaten/kota</b> yang diamati pada {selected_year}, terdapat <b>{int(m_hh.sum())} daerah</b> "
        f"yang masuk dalam kategori pusat kemiskinan. Wilayah-wilayah ini tidak hanya berstatus miskin, tetapi juga dikelilingi "
        f"oleh tetangga dengan tantangan serupa, menciptakan rantai ketertinggalan yang membutuhkan intervensi serius—terutama "
        f"di titik terparah seperti <b>{', '.join(contoh)}</b>. "
        f"Sebaliknya, <b>{int(m_ll.sum())} daerah</b> menikmati zona kesejahteraan bersama wilayah sekitar, sementara sisanya "
        f"berada di posisi transisi baik sebagai anomali positif maupun wilayah tertinggal sendirian."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    # Digabung menjadi 1 kartu dengan gaya "good" atau "info" yang bersih
    card("good", "📊", f"Ringkasan Analisis Spasial ({selected_year})", cerita_natural)

except Exception as e:
    st.error(f"Kalkulasi spasial terhenti: {e}")

st.divider()

# --- BAB 3: Hierarki Pengeluaran (Memenuhi Syarat UAS Multirepresentasi) ---
bab("Bab 3")
st.markdown("### Konklusi: Ke Mana Uang Kita Mengalir?")
st.write("Terlepas dari fluktuasi ekonomi hingga saat ini, prioritas bertahan hidup masyarakat bergantung pada sektor pengeluaran. Klik pada area mana pun untuk melakukan *drill-down/zoom*, atau arahkan kursor Anda untuk melihat rincian spesifik.")
st.write("Visualisasi ini memetakan alokasi anggaran rumah tangga. Semakin pekat warna **biru**, semakin tinggi tingkat pertumbuhan anggaran komoditas tersebut dibanding tahun sebelumnya.")

# Skala warna: merah (terendah) ke kuning (tertinggi)
SKALA_PERTUMBUHAN = [[0, '#e0f2fe'], [0.5, "#68b6d8"], [1, '#0369a1']]

# Total & fakta ringkas untuk narasi
total_pengeluaran = df_pengeluaran['Maret_2025'].sum()
total_format = f"{total_pengeluaran:,.0f}".replace(',', '.') 
l1 = df_pengeluaran.groupby('Level_1')['Maret_2025'].sum().sort_values(ascending=False)

# 1. Ambil data Level 1 dan buang baris yang mengandung kata "Total"
df_l1 = df_pengeluaran.dropna(subset=['Level_1'])
df_l1_bersih = df_l1[~df_l1['Level_1'].str.contains('Total', case=False, na=False)]

# 2. Cari komoditas terbesar dari data yang sudah bersih
top_l1 = df_l1_bersih.loc[df_l1_bersih['Maret_2025'].idxmax()]
nama_l1 = top_l1['Level_1']

# 3. Hitung porsinya terhadap total keseluruhan (pastikan total_semua mengambil angka total yang benar)
total_semua = df_pengeluaran['Maret_2025'].max() # atau total yang sudah Anda definisikan
porsi_l1 = (top_l1['Maret_2025'] / total_semua) * 100

df_g = df_pengeluaran.replace([np.inf, -np.inf], np.nan).dropna(subset=['Pertumbuhan (%)']).copy()
df_g['Komoditas'] = df_g['Level_3'].fillna(df_g['Level_2']).fillna(df_g['Level_1'])
naik_1 = df_g.nlargest(1, 'Pertumbuhan (%)').iloc[0]
turun_1 = df_g.nsmallest(1, 'Pertumbuhan (%)').iloc[0]

# Representasi 1: Treemap
chart_header("Treemap Struktur Pengeluaran", "Luas Kotak - Besar Pengeluaran Rumah Tangga Maret 2025 & " \
"Warna - Pertumbuhan Dibanding Maret 2024.")
fig_tree = px.treemap(
    df_pengeluaran, 
    path=['Level_1', 'Level_2', 'Level_3'], 
    values='Maret_2025',                    
    color='Pertumbuhan (%)',                
    color_continuous_scale=SKALA_PERTUMBUHAN
)
fig_tree.update_traces(
    textinfo='label+percent parent',
    hovertemplate='<b>%{label}</b><br>Pengeluaran 2025: %{value:,.0f}<br>Pertumbuhan: %{color:.2f}%<extra></extra>'
)
# 🌟 KUNCI FORMAT INDONESIA: Ubah pemisah desimal jadi koma, pemisah ribuan jadi titik
fig_tree.update_layout(separators=",.", margin=dict(l=10, r=10, t=10, b=10))
c_t1, c_t2 = st.columns([2.4, 1])
with c_t1:
    st.plotly_chart(tema(fig_tree), use_container_width=True)
with c_t2:
    card("info", "📦", "Pusat Pengeluaran Terbesar", f"Struktur anggaran rumah tangga didominasi oleh kelompok <b>Bukan Makanan</b>, di mana pos <b>{nama_l1}</b> sendiri menyedot porsi paling besar yaitu <b>{fmt_id(porsi_l1, 1)}%</b> dari total pengeluaran.")
    st.markdown("<br>", unsafe_allow_html=True)
    card("warn", "📈", "Pertumbuhan Anggaran", f"Dibandingkan tahun 2024, komoditas <b>{naik_1['Komoditas']}</b> mengalami lonjakan anggaran paling tinggi dengan pertumbuhan mencapai <b>{fmt_id(naik_1['Pertumbuhan (%)'], 1)}%</b>.")

st.divider() # Garis pemisah antar grafik

# Representasi 2: Sunburst
# --- Representasi 2: Sunburst ---
chart_header("Sunburst Struktur Pengeluaran", "Cincin dalam = kelompok besar & cincin luar = rincian komoditas. <i>Klik sebuah irisan untuk memperbesar.</i>")

fig_sun = px.sunburst(
    df_pengeluaran,
    path=['Level_1', 'Level_2', 'Level_3'],    
    values='Maret_2025',                    
    color='Pertumbuhan (%)',                
    color_continuous_scale=SKALA_PERTUMBUHAN
)

fig_sun.update_traces(
    textinfo='none',    
    hovertemplate='<b>Kategori: %{label}</b><br>Pengeluaran 2025: %{value:,.0f}<br>Pertumbuhan dari 2024: %{color:.2f}%<extra></extra>',
    insidetextorientation='radial'
)

# ✨ TAMBAHKAN SHAPE LINGKARAN PUTIH PADAT DI TENGAH
# Karena width dan height seimbang (400x400), lingkaran ini dijamin bulat sempurna (tidak oval)
fig_sun.update_layout(
    separators=",.", 
    margin=dict(l=10, r=10, t=10, b=10),
    height=400,
    width=400, # Mengunci lebar agar aspek rasio 1:1 (bulat sempurna)
    shapes=[
        dict(
            type="circle",
            xref="paper", yref="paper",
            x0=0.34, y0=0.34, x1=0.66, y1=0.66, # Ukuran lubang tengah sunburst
            fillcolor="white",
            line=dict(color="white", width=2),
            layer="above" # Diletakkan di bawah teks total tapi di atas grafik
        )
    ]
)

# Menaruh teks Total tepat di tengah lingkaran putih
fig_sun.add_annotation(
    text=f"<b>TOTAL</b><br>Rp {total_format}",
    x=0.5, y=0.5,
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=12, color="#12332b"),
    align="center"
)

# Ambil data komoditas terluar (Level_3) tertinggi untuk ditaruh di kartu
df_l3 = df_pengeluaran.dropna(subset=['Level_3'])
top_komoditas = df_l3.loc[df_l3['Maret_2025'].idxmax()]
nama_komoditas_tertinggi = top_komoditas['Level_3']
nilai_komoditas_tertinggi = fmt_id(top_komoditas['Maret_2025'])

c_s1, c_s2 = st.columns([2.2, 1], vertical_alignment="center")

with c_s1:
    st.plotly_chart(tema(fig_sun), use_container_width=True)

with c_s2:
    card("info", "🎯", "Komoditas Terbesar", f"Dari cincin terluar rincian komoditas, pos <b>{nama_komoditas_tertinggi}</b> menjadi penyedot anggaran paling mendominasi dengan nilai mencapai <b>Rp {nilai_komoditas_tertinggi}</b>.")


st.divider()

# ---------------------------------------------------------------------
# BAB 4: PROFIL MULTIDIMENSI (Syarat UAS Visualisasi Data Multivariat)
# ---------------------------------------------------------------------
# --- BAB 4: Profil Multidimensi ---
html('<div id="bab-4"></div>')
bab("Bab 4")
st.markdown("### Menyelami Profil Kesejahteraan Antar Provinsi")
st.write("Kesejahteraan tidak hanya diukur dari aspek materi. Mari kita lihat perbandingan berbagai dimensi kehidupan di 38 Provinsi Indonesia.")

# CSS untuk memperlebar kotak dropdown agar tidak terpotong (kelelep)
st.markdown("""
    <style>
    /* Mengatur jarak (margin) agar dropdown tidak terlalu renggang */
    div[data-testid="stSelectbox"] {
        margin-top: -10px;
        margin-bottom: 15px;
        width: 260px !important;
    }
    
    /* Mengubah background kotak selectbox dari abu-abu menjadi putih bersih & border elegan */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid rgba(46, 139, 87, 0.25) !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    </style>
""", unsafe_allow_html=True)

# Filter Provinsi (Label "Sorot (Highlight)" dihapus agar lebih bersih)
provinsi_terpilih = st.selectbox(
    "Pilih Provinsi untuk disorot:",
    options=df_multi['Provinsi'].tolist(),
    index=0 # Sesuaikan index default jika ada
)
# 1. PARALLEL COORDINATES (Brushing Technique)
# --- Bagian Parallel Coordinates ---
st.markdown("#### Jejaring Indikator Antar Dimensi")
st.write("Menampilkan sebaran nilai seluruh indikator secara simultan untuk membandingkan karakteristik tiap provinsi.")

# Buat salinan data dan pastikan provinsi yang dipilih mendapat perhatian khusus di visual
df_para = df_multi.copy()
# Berikan penanda warna atau urutan agar garis provinsi terpilih berada di lapisan teratas (paling jelas)

fig_para = px.parallel_coordinates(
    df_para,
    color=df_para['Provinsi'].apply(lambda x: 1 if x == provinsi_terpilih else 0),
    color_continuous_scale=[(0, 'rgba(46,139,87,0.18)'), (1, '#e11d48')], # Garis biasa transparan, yang dipilih merah/kontras
    dimensions=['Persentase_Miskin', 'IPM', 'Akses_Sanitasi','Akses_Air_Minum', 'Rata_Lama_Sekolah', 'Pengeluaran_Per_Kapita', 'TPT', 'UHH'] # Sesuaikan nama kolom Anda
)

fig_para.update_layout(
    height=500, # Menambah tinggi agar sumbu vertikal lebih leluasa dan tidak terpotong atas-bawah
    margin=dict(l=40, r=40, t=50, b=40),
    coloraxis_showscale=False
)

st.plotly_chart(tema(fig_para), use_container_width=True)

# Membagi layar untuk PCA dan Radar Chart
col_pca, col_radar = st.columns(2)
kolom_numerik = df_multi.select_dtypes(include=[np.number]).columns.tolist()

# 2. PCA SCATTERPLOT (Dimensionality Reduction)
with col_pca:
    st.markdown("#### Peta Pengelompokan Wilayah (PCA)")
    
    # Proses PCA (Reduksi 8 variabel menjadi 2 komponen utama)
    scaler = StandardScaler()
    # Menggunakan kolom_numerik sesuai definisi Anda
    data_scaled = scaler.fit_transform(df_multi[kolom_numerik])
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data_scaled)
    
    df_pca = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])
    df_pca['Provinsi'] = df_multi['Provinsi']
    df_pca['Status'] = np.where(df_multi['Provinsi'] == provinsi_terpilih, 'Disorot', 'Lainnya')

    # Pencilan = 3 provinsi paling jauh dari pusat peta
    df_pca['Jarak'] = np.sqrt(df_pca['PC1'] ** 2 + df_pca['PC2'] ** 2)
    nama_pencilan = df_pca.nlargest(3, 'Jarak')['Provinsi'].tolist()

    chart_header(f"Varian yang dijelaskan: {pca.explained_variance_ratio_.sum()*100:.1f}%",
                 f"Makin dekat dua titik, makin mirip profilnya. <i> Label hanya untuk provinsi terpilih dan 3 yang paling terpencil.</i>")
    fig_pca = px.scatter(
        df_pca, x='PC1', y='PC2', color='Status', hover_name='Provinsi', hover_data={'Status': False, 'Jarak': False, 'PC1': ':.2f', 'PC2': ':.2f'},
        color_discrete_map={'Disorot': COLOR_HIGHLIGHT, 'Lainnya': COLOR_SAGE}
    )
    fig_pca.update_traces(marker=dict(size=10, opacity=0.8))
    fig_pca.update_traces(marker=dict(size=18, opacity=1, line=dict(width=2, color='white')), selector=dict(name='Disorot'))
    for _, r in df_pca[df_pca['Provinsi'].isin(nama_pencilan + [provinsi_terpilih])].iterrows():
        sel = r['Provinsi'] == provinsi_terpilih
        fig_pca.add_annotation(x=r['PC1'], y=r['PC2'], text=f"<b>{r['Provinsi']}</b>" if sel else r['Provinsi'],
                               showarrow=True, arrowhead=0, arrowcolor=COLOR_CORAL if sel else '#7a8a83', ax=38, ay=-38,
                               font=dict(size=13 if sel else 11, color=COLOR_CORAL if sel else COLOR_INK),
                               bgcolor="rgba(255,255,255,.9)", borderpad=3)
    fig_pca.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(tema(fig_pca), use_container_width=True)

# 3. RADAR CHART (Profil Individu)
with col_radar:
    st.markdown(f"#### Profil Radar Indikator: **{provinsi_terpilih}**")
    
    # Standarisasi skala 0-100 untuk radar chart agar bentuknya seimbang menggunakan kolom_numerik
    df_radar_norm = (df_multi[kolom_numerik] - df_multi[kolom_numerik].min()) / (df_multi[kolom_numerik].max() - df_multi[kolom_numerik].min()) * 100
    nilai_provinsi = df_radar_norm[df_multi['Provinsi'] == provinsi_terpilih].values[0]
    nilai_nasional = df_radar_norm.mean().values

    chart_header("Profil dibanding rata-rata nasional", "Makin menjauh dari pusat, makin tinggi nilai indikatornya (skala 0-100). <i>Klik label di legenda (kanan) untuk memilih garis.</i>")
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=nilai_nasional, theta=kolom_numerik, fill='toself', name='Rata-rata Nasional', marker_color=COLOR_SAGE, opacity=0.5))
    fig_radar.add_trace(go.Scatterpolar(r=nilai_provinsi, theta=kolom_numerik, fill='toself', name=provinsi_terpilih, marker_color=COLOR_DARK))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        height=450,
        margin=dict(l=60, r=60, t=40, b=40) 
    )
    st.plotly_chart(tema(fig_radar), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### Interpretasi Analisis Multidimensi")

# Membagi menjadi 3 kolom untuk 3 kartu interpretasi
c_int1, c_int2, c_int3 = st.columns(3)

with c_int1:
    card("info", "🧩", "Kelompok Mayoritas", "Titik-titik yang menumpuk di tengah menunjukkan tingkat kesejahteraan mayoritas wilayah cenderung serupa dan mendekati rata-rata nasional.")
with c_int2:
    card("good", "🚀", "Anomali Positif", "<b>DKI Jakarta</b> terpisah jauh sebagai pencilan positif karena mendominasi indikator ekonomi, infrastruktur, dan IPM dibanding wilayah lain.")
with c_int3:
    card("bad", "🚨", "Prioritas Daerah", "<b>Papua Pegunungan & Tengah</b> terlempar sebagai pencilan ekstrem akibat ketertinggalan ekonomi hampir seluruh layanan dasar.")

st.markdown("<br>", unsafe_allow_html=True)

# Sekilas provinsi terpilih dibanding rata-rata nasional
st.markdown(f"#### Sekilas: **{provinsi_terpilih}** vs Rata-rata Nasional")
idx_prov = df_multi.index[df_multi['Provinsi'] == provinsi_terpilih][0]
kolom_sekilas = [c for c in ['IPM', 'Persentase_Miskin', 'TPT', 'UHH'] if c in kolom_numerik]
kolom_negatif = {'Persentase_Miskin', 'TPT'}  # makin kecil makin baik
cols_sk = st.columns(len(kolom_sekilas)) if kolom_sekilas else []
for cs, kc in zip(cols_sk, kolom_sekilas):
    nilai = df_multi.loc[idx_prov, kc]
    rata = df_multi[kc].mean()
    cs.metric(kc.replace('_', ' '), f"{nilai:.2f}".replace('.', ','),
              delta=f"{nilai - rata:+.2f} vs nasional".replace('.', ','),
              delta_color="inverse" if kc in kolom_negatif else "normal")

# D. Peringkat antarprovinsi (Hanya Top 5, provinsi terpilih selalu ikut ditampilkan)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### Pemeringkatan Antar Provinsi Berdasarkan Indikator")
cp1, cp2 = st.columns([2, 1.4])
with cp1:
    indikator_pilih = st.selectbox("Pilih indikator:", kolom_numerik, format_func=lambda c: c.replace('_', ' '))
with cp2:
    urutan = st.radio("Urutan", ["Tertinggi", "Terendah"], horizontal=True)

# Patenkan langsung ke angka 5
top_p = 5 

df_rank = df_multi[['Provinsi', indikator_pilih]].dropna().sort_values(indikator_pilih, ascending=(urutan == "Terendah")).reset_index(drop=True)
df_rank['Peringkat'] = df_rank.index + 1
df_show = df_rank.head(top_p)
if provinsi_terpilih not in df_show['Provinsi'].values:
    df_show = pd.concat([df_show, df_rank[df_rank['Provinsi'] == provinsi_terpilih]])
df_show = df_show.copy()
df_show['Label'] = df_show['Peringkat'].astype(str) + ". " + df_show['Provinsi']
df_show['Status'] = np.where(df_show['Provinsi'] == provinsi_terpilih, 'Disorot', 'Lainnya')
chart_header(f"Provinsi Teratas: {indikator_pilih.replace('_', ' ')}",
             f"Menampilkan 5 provinsi teratas. Jika {provinsi_terpilih} tidak masuk, ia ditambahkan di bawah lengkap dengan peringkatnya.")
fig_rank = px.bar(df_show, x=indikator_pilih, y='Label', orientation='h', color='Status',
                  color_discrete_map={'Disorot': COLOR_HIGHLIGHT, 'Lainnya': COLOR_SAGE},
                  labels={indikator_pilih: indikator_pilih.replace('_', ' '), 'Label': ''}, height=90 + 38 * len(df_show))
fig_rank.update_yaxes(autorange='reversed')
fig_rank.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(tema(fig_rank), use_container_width=True)

# 4. KOTAK METADATA & METODOLOGI (Sebagai penutup dashboard)
st.markdown("<br>", unsafe_allow_html=True)
html("""
<div class="card info wide"><div class="card-ico">📚</div><div>
<div class="card-title">Catatan Metodologi & Sumber Data</div>
<ul style="margin-bottom: 0;">
<li><b>Sumber Data:</b> Data indikator sosial-ekonomi (Kemiskinan, PDRB, Pengeluaran, dan Indikator Kesejahteraan) pada level 514 Kabupaten/Kota dan 38 Provinsi di Indonesia.</li>
<li><b>Analisis Spasial:</b> Indeks <i>Moran's I</i> digunakan untuk mengukur tingkat autokorelasi spasial, mengidentifikasi seberapa kuat kondisi suatu wilayah dipengaruhi oleh tetangga geografisnya.</li>
<li><b>Reduksi Dimensi (PCA):</b> <i>Principal Component Analysis</i> diaplikasikan untuk menyederhanakan 8 variabel kesejahteraan yang kompleks menjadi 2 komponen utama yang lebih mudah divisualisasikan, tanpa kehilangan banyak informasi (varians).</li>
</ul></div></div>
""")

st.markdown("<br><br><center><p style='color: gray;'><i>Sebuah eksplorasi data visual. Dibuat untuk Tugas Akhir Visualisasi Data.</i></p></center>", unsafe_allow_html=True)