# import streamlit as st
# import pandas as pd
# import geopandas as gpd
# import plotly.express as px
# import libpysal
# from esda.moran import Moran
# import numpy as np
# import plotly.graph_objects as go
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA

# # =====================================================================
# # PENGATURAN HALAMAN & TEMA WARNA
# # =====================================================================
# st.set_page_config(page_title="Kisah Ekonomi Nusantara", page_icon="🌾", layout="wide", initial_sidebar_state="collapsed")

# # Palet Warna (Mint / Sage Green / Earth Tones) + aksen hangat
# COLOR_MINT = '#d4edda'
# COLOR_SAGE = '#8fbc8f'
# COLOR_FOREST = '#2e8b57'
# COLOR_DARK = '#1a432b'
# COLOR_HIGHLIGHT = '#ff9f43'  # Warna kontras untuk Highlight/Pencilan
# COLOR_INK = '#12332b'
# COLOR_CORAL = '#e8590c'
# COLOR_AMBER = '#f2b33d'
# COLOR_SKY = '#3b8ad9'

# # OPSIONAL: isi dengan URL video .mp4 (mis. dari Pexels/Pixabay: kemiskinan, sawah, kota)
# # agar tampil sebagai video latar halus di bagian hero. Kosongkan jika tidak dipakai.
# HERO_VIDEO_URL = ""

# # =====================================================================
# # STYLE (CSS) & HELPER TAMPILAN
# # =====================================================================
# CSS = """
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
# @property --n { syntax: '<integer>'; initial-value: 0; inherits: false; }
# :root{
#   --ink:#12332b; --muted:#557268; --mint:#d4edda; --sage:#8fbc8f; --forest:#2e8b57; --deep:#1a432b;
#   --amber:#f2b33d; --coral:#e8590c; --sky:#3b8ad9;
# }
# html, body, .stApp, .stMarkdown, p, li, label, button, input, textarea{ font-family:'Plus Jakarta Sans', sans-serif; color:var(--ink); }
# h1,h2,h3,h4,h5{ font-family:'Bricolage Grotesque','Plus Jakarta Sans',sans-serif !important; color:var(--ink) !important; letter-spacing:-0.02em; }
# [data-testid="stMain"]{ scroll-behavior:smooth; }
# .stApp{ background:linear-gradient(180deg,#eef8f1 0%,#f7fbf4 45%,#fdf5e6 100%); }
# .stApp::before{
#   content:""; position:fixed; inset:-15%; z-index:0; pointer-events:none;
#   background:
#     radial-gradient(520px 380px at 10% 10%, rgba(143,188,143,.50), transparent 62%),
#     radial-gradient(480px 400px at 92% 16%, rgba(242,179,61,.30), transparent 62%),
#     radial-gradient(640px 460px at 82% 86%, rgba(59,138,217,.16), transparent 62%),
#     radial-gradient(480px 360px at 10% 88%, rgba(232,89,12,.12), transparent 62%);
#   animation:drift 26s ease-in-out infinite alternate;
# }
# @keyframes drift{ to{ transform:translate3d(3%,-2%,0) scale(1.08) rotate(2deg); } }
# [data-testid="stMainBlockContainer"], .block-container{ position:relative; z-index:1; max-width:1180px; padding-top:1.6rem; }
# header[data-testid="stHeader"]{ background:transparent; }
# footer{ visibility:hidden; }
# hr{ border:0 !important; height:2px !important; background:linear-gradient(90deg,transparent,rgba(46,139,87,.45),transparent) !important; margin:2.2rem 0 !important; }

# /* progress scroll */
# .progress{ position:fixed; top:0; left:0; right:0; height:4px; z-index:9999; transform-origin:0 50%; transform:scaleX(0);
#   background:linear-gradient(90deg,var(--forest),var(--amber),var(--coral)); }
# @supports (animation-timeline: scroll()){ .progress{ animation:prog linear both; animation-timeline:scroll(nearest); } }
# @keyframes prog{ to{ transform:scaleX(1); } }

# /* HERO */
# .hero{ position:relative; display:grid; grid-template-columns:1.1fr .9fr; gap:24px; align-items:center; padding:46px 42px 38px;
#   border-radius:32px; overflow:hidden; background:linear-gradient(135deg,rgba(255,255,255,.86),rgba(220,242,228,.72));
#   border:1px solid rgba(255,255,255,.95); box-shadow:0 30px 70px -30px rgba(23,64,50,.38); margin-bottom:1.6rem; }
# .hero-video{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:.26; z-index:0; }
# .hero > *:not(video){ position:relative; z-index:1; }
# .hero h1{ font-size:clamp(2.4rem,5vw,4.1rem); line-height:1.02; font-weight:800; margin:0 0 10px; padding:0; }
# .hero .sub{ font-size:1.15rem; color:var(--forest); font-weight:700; margin:0 0 14px; }
# .hero .lead{ color:var(--muted); font-size:1.02rem; line-height:1.65; max-width:52ch; margin:0 0 20px; }
# .hero-copy > *{ animation:rise .9s cubic-bezier(.2,.8,.2,1) both; }
# .hero-copy > *:nth-child(2){ animation-delay:.12s } .hero-copy > *:nth-child(3){ animation-delay:.24s }
# .hero-copy > *:nth-child(4){ animation-delay:.36s } .hero-copy > *:nth-child(5){ animation-delay:.48s }
# @keyframes rise{ from{ opacity:0; transform:translateY(22px); } to{ opacity:1; transform:none; } }
# .cta-row{ display:flex; gap:10px; flex-wrap:wrap; margin-bottom:22px; }
# .cta{ display:inline-block; padding:12px 22px; border-radius:999px; font-weight:700; text-decoration:none !important;
#   transition:transform .25s ease, box-shadow .25s ease; }
# .cta.main{ background:var(--forest); color:#fff !important; box-shadow:0 12px 24px -10px rgba(46,139,87,.8); }
# .cta.ghost{ background:rgba(255,255,255,.9); color:var(--deep) !important; border:1px solid rgba(46,139,87,.3); }
# .cta:hover{ transform:translateY(-3px); }
# .chips{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }
# .chip{ background:rgba(255,255,255,.85); border-radius:18px; padding:12px 14px; border:1px solid rgba(46,139,87,.12); }
# .chip b{ display:block; font-family:'Bricolage Grotesque',sans-serif; font-size:1.55rem; font-weight:800; color:var(--deep); }
# .chip span{ font-size:.78rem; color:var(--muted); }
# .cnt{ --n:0; counter-reset:n var(--n); animation:cnt 2.2s ease-out .6s both; }
# .cnt::before{ content:counter(n); }
# @keyframes cnt{ from{ --n:0; } to{ --n:var(--i); } }
# .scene{ width:100%; height:auto; }
# .scene .sway{ transform-box:fill-box; transform-origin:50% 100%; animation:sway 3.4s ease-in-out var(--d) infinite alternate; }
# @keyframes sway{ from{ transform:rotate(-5deg); } to{ transform:rotate(5deg); } }
# .scene .bar{ transform-box:fill-box; transform-origin:50% 100%; animation:grow 1.2s cubic-bezier(.2,.8,.2,1) var(--d) both; }
# @keyframes grow{ from{ transform:scaleY(0); } to{ transform:scaleY(1); } }
# .scene .trend{ stroke-dasharray:260; stroke-dashoffset:260; animation:draw 1.6s ease-out 1.3s forwards; }
# @keyframes draw{ to{ stroke-dashoffset:0; } }
# .scene .dot{ opacity:0; animation:pop .5s ease-out 2.8s forwards; }
# @keyframes pop{ to{ opacity:1; } }
# .scene .coin{ animation:float 4s ease-in-out var(--d) infinite alternate; }
# @keyframes float{ from{ transform:translateY(6px); } to{ transform:translateY(-10px); } }
# .scene .halo{ transform-box:fill-box; transform-origin:center; animation:pulse 4s ease-in-out infinite alternate; }
# @keyframes pulse{ to{ transform:scale(1.25); opacity:.08; } }
# @media (max-width:860px){ .hero{ grid-template-columns:1fr; padding:30px 22px; } .chips{ grid-template-columns:repeat(2,1fr); } }

# /* BADGE BAB */
# .badge{ display:inline-flex; align-items:center; gap:8px; padding:6px 14px; border-radius:999px; background:rgba(46,139,87,.12);
#   color:var(--forest); font-weight:700; font-size:.85rem; margin-bottom:4px; }
# .badge::before{ content:""; width:8px; height:8px; border-radius:50%; background:var(--forest); animation:blink 2s ease-in-out infinite; }
# @keyframes blink{ 50%{ opacity:.25; transform:scale(.7); } }

# /* CARDS */
# .card{ --c:var(--sky); position:relative; display:flex; gap:14px; align-items:flex-start; min-height:150px; height:100%;
#   background:rgba(255,255,255,.76); backdrop-filter:blur(14px); border:1px solid rgba(255,255,255,.95); border-radius:22px;
#   padding:20px 22px; box-shadow:0 12px 30px -14px rgba(23,64,50,.28); overflow:hidden;
#   transition:transform .35s cubic-bezier(.2,.8,.2,1), box-shadow .35s ease; }
# .card::after{ content:""; position:absolute; right:-40px; top:-40px; width:120px; height:120px; border-radius:50%;
#   background:var(--c); opacity:.12; transition:transform .5s ease, opacity .5s ease; }
# .card:hover{ transform:translateY(-6px); box-shadow:0 22px 40px -16px rgba(23,64,50,.4); }
# .card:hover::after{ transform:scale(1.8); opacity:.18; }
# .card.bad{ --c:var(--coral); } .card.good{ --c:var(--forest); } .card.info{ --c:var(--sky); } .card.warn{ --c:var(--amber); }
# .card-ico{ flex:0 0 auto; width:46px; height:46px; display:grid; place-items:center; font-size:1.4rem; border-radius:14px;
#   background:color-mix(in srgb, var(--c) 16%, white); transition:transform .4s ease; }
# .card:hover .card-ico{ transform:rotate(-8deg) scale(1.1); }
# .card-title{ font-family:'Bricolage Grotesque',sans-serif; font-weight:700; font-size:1.05rem; margin-bottom:2px; }
# .card p{ margin:6px 0 0; color:var(--muted); line-height:1.6; font-size:.95rem; }
# .card .big{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:1.9rem; color:var(--c); line-height:1.15; }
# .card ul{ margin:8px 0 0; padding-left:1.1rem; color:var(--muted); line-height:1.65; font-size:.95rem; }
# .card.wide{ min-height:0; }
# .mini{ text-align:center; display:block; min-height:0; padding:14px; }
# .mini .big{ font-size:1.7rem; } .mini .card-title{ font-size:.9rem; color:var(--muted); font-weight:600; }

# /* HEADER GRAFIK */
# .chart-head{ margin:.9rem 0 .5rem; padding-left:12px; border-left:4px solid var(--forest); }
# .chart-head b{ font-family:'Bricolage Grotesque',sans-serif; font-size:1.1rem; color:var(--ink); }
# .chart-head span{ display:block; color:var(--muted); font-size:.9rem; line-height:1.5; margin-top:2px; }

# /* WIDGET STREAMLIT */
# [data-testid="stPlotlyChart"]{ background:rgba(255,255,255,.72); border-radius:24px; padding:10px; border:1px solid rgba(255,255,255,.95);
#   box-shadow:0 14px 34px -16px rgba(23,64,50,.3); overflow:hidden; transition:box-shadow .3s ease; }
# [data-testid="stPlotlyChart"]:hover{ box-shadow:0 22px 44px -16px rgba(23,64,50,.42); }
# [data-testid="stMetric"]{ background:rgba(255,255,255,.78); border-radius:20px; padding:14px 18px; border:1px solid rgba(255,255,255,.95);
#   box-shadow:0 10px 26px -14px rgba(23,64,50,.28); transition:transform .3s ease; }
# [data-testid="stMetric"]:hover{ transform:translateY(-4px); }
# div[data-baseweb="select"] > div{ border-radius:14px !important; background:rgba(255,255,255,.9) !important; border-color:rgba(46,139,87,.3) !important; }
# div[role="radiogroup"]{ gap:8px !important; flex-wrap:wrap; }
# label[data-baseweb="radio"]{ background:rgba(255,255,255,.85); border:1px solid rgba(46,139,87,.28); padding:6px 16px; border-radius:999px;
#   margin:0 !important; transition:all .25s ease; cursor:pointer; }
# label[data-baseweb="radio"] > div:first-child{ display:none; }
# label[data-baseweb="radio"]:hover{ transform:translateY(-2px); border-color:var(--forest); }
# label[data-baseweb="radio"]:has(input:checked){ background:var(--forest); border-color:var(--forest); box-shadow:0 8px 18px -8px rgba(46,139,87,.8); }
# label[data-baseweb="radio"]:has(input:checked) *{ color:#fff !important; }
# button[data-baseweb="tab"]{ font-weight:700; border-radius:12px 12px 0 0; transition:background .25s ease; }
# button[data-baseweb="tab"]:hover{ background:rgba(46,139,87,.1); }
# [data-baseweb="tab-highlight"]{ background-color:var(--forest) !important; height:3px !important; border-radius:3px; }
# [data-testid="stExpander"]{ border-radius:18px; background:rgba(255,255,255,.7); }
# @media (prefers-reduced-motion:reduce){
#   *, *::before, *::after{ animation:none !important; transition:none !important; }
#   .cnt{ --n:var(--i); } .scene .trend{ stroke-dashoffset:0; } .scene .dot{ opacity:1; }
# }
# </style>
# """


# def html(s):
#     """Render HTML tanpa baris kosong/indentasi agar tidak dibaca sebagai blok kode markdown."""
#     st.markdown("\n".join(l.strip() for l in s.splitlines() if l.strip()), unsafe_allow_html=True)


# def card(kind, icon, title, body, big=None):
#     big_html = f'<div class="big">{big}</div>' if big else ""
#     html(f'<div class="card {kind}"><div class="card-ico">{icon}</div><div><div class="card-title">{title}</div>{big_html}<p>{body}</p></div></div>')


# def mini_card(kind, title, value):
#     html(f'<div class="card mini {kind}"><div class="big">{value}</div><div class="card-title">{title}</div></div>')


# def bab(label):
#     html(f'<div class="badge">{label}</div>')


# def chart_header(judul, sub=""):
#     sub_html = f"<span>{sub}</span>" if sub else ""
#     html(f'<div class="chart-head"><b>{judul}</b>{sub_html}</div>')


# def fmt_id(v, d=2):
#     """Format angka gaya Indonesia: titik ribuan, koma desimal."""
#     return f"{v:,.{d}f}".replace(',', 'X').replace('.', ',').replace('X', '.')


# def anim_num(v, dec=False):
#     if dec:
#         a, b = f"{v:.1f}".split('.')
#         return f'<span class="cnt" style="--i:{a}"></span>,<span class="cnt" style="--i:{b}"></span>'
#     return f'<span class="cnt" style="--i:{int(v)}"></span>'


# def tema(fig):
#     """Selaraskan tampilan grafik Plotly dengan tema halaman (tanpa mengubah data)."""
#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         font=dict(family="Plus Jakarta Sans, sans-serif", color=COLOR_INK),
#         hoverlabel=dict(bgcolor="white", font_size=13, font_family="Plus Jakarta Sans, sans-serif"),
#     )
#     return fig


# # =====================================================================
# # FUNGSI PEMUATAN & PEMBERSIHAN DATA (TIDAK DIUBAH)
# # =====================================================================
# @st.cache_data 
# def load_data():
#     # --- 1. Data Hierarki Pengeluaran ---
#     df_pengeluaran = pd.read_excel('data/Rata-Rata Pengeluaran Ruta Per Komoditi Maret 2024-2025.xlsx')
    
#     # Menghitung persentase pertumbuhan dari 2024 ke 2025 untuk gradasi warna
#     df_pengeluaran['Pertumbuhan (%)'] = ((df_pengeluaran['Maret_2025'] - df_pengeluaran['Maret_2024']) / df_pengeluaran['Maret_2024']) * 100

#     # --- 2. Data Geospasial & Ekonomi ---
#     gdf_batas = gpd.read_file('data/kab_kota.geojson')
#     df_miskin = pd.read_excel('data/Persentase_Penduduk_Miskin_dengan_Kode.xlsx')
#     df_pdrb = pd.read_excel('data/PDRB_ADHB_KODE.xlsx')
    
#     df_miskin.columns = [str(col).replace('.0', '').strip() for col in df_miskin.columns]
#     df_pdrb.columns = [str(col).replace('.0', '').strip() for col in df_pdrb.columns]

#     tahun_list = ['2021', '2022', '2023', '2024', '2025']
    
#     df_miskin_melt = df_miskin.melt(id_vars=['Kode_Wilayah', 'Kab/Kota'], value_vars=tahun_list, var_name='Tahun', value_name='Pct_Miskin')
#     df_pdrb_melt = df_pdrb.melt(id_vars=['Kode_Wilayah'], value_vars=tahun_list, var_name='Tahun', value_name='PDRB')

#     # Fungsi Pembersih Angka
#     def bersihkan_angka(val):
#         if pd.isna(val):
#             return None
#         val_str = str(val).strip().replace(',', '.')
#         try:
#             return float(val_str)
#         except ValueError:
#             return None

#     df_miskin_melt['Pct_Miskin'] = df_miskin_melt['Pct_Miskin'].apply(bersihkan_angka)
#     df_pdrb_melt['PDRB'] = df_pdrb_melt['PDRB'].apply(bersihkan_angka)

#     # --- Proses Sapu Bersih Kode Wilayah ---
#     def bersihkan_kode(x):
#         x = str(x).strip()
#         if x.endswith('.0'): 
#             x = x[:-2]
#         x = x.replace('.', '')
#         return x

#     gdf_batas['code'] = gdf_batas['code'].apply(bersihkan_kode)
#     df_miskin_melt['Kode_Wilayah'] = df_miskin_melt['Kode_Wilayah'].apply(bersihkan_kode)
#     df_pdrb_melt['Kode_Wilayah'] = df_pdrb_melt['Kode_Wilayah'].apply(bersihkan_kode)

#     df_ekonomi = df_miskin_melt.merge(df_pdrb_melt, on=['Kode_Wilayah', 'Tahun'], how='left')
#     gdf = gdf_batas.merge(df_ekonomi, left_on='code', right_on='Kode_Wilayah', how='left')

#     # 🔍 DIAGNOSTIK KEGAGALAN JOIN (Cek di Terminal Codespaces)
#     data_kosong_cek = gdf[gdf['Pct_Miskin'].isna()]['code'].unique()
#     print(f"⚠️ PERINGATAN: Ada {len(data_kosong_cek)} kode wilayah di peta yang gagal ter-join dengan Excel pada tahun tertentu!")
#     print("Contoh kode wilayah yang gagal:", data_kosong_cek[:10])

#     gdf['centroid_x'] = gdf.geometry.centroid.x
#     gdf['centroid_y'] = gdf.geometry.centroid.y
#     gdf['Pct_Miskin'] = pd.to_numeric(gdf['Pct_Miskin'], errors='coerce')
#     gdf['PDRB'] = pd.to_numeric(gdf['PDRB'], errors='coerce')

#     # -- 3. Data Multivariat --
#     df_multi = pd.read_excel('data/Dataset_Multivariat_2025_Bersih.xlsx')

#     # Daftar kolom yang berisi angka dengan format koma berdasarkan Excel Anda
#     kolom_numerik_multi = [
#         'Persentase_Miskin', 'IPM', 'Akses_Sanitasi', 'Akses_Air_Minum', 
#         'Rata_Lama_Sekolah', 'Pengeluaran_Per_Kapita', 'TPT', 'UHH'
#     ]

#     # Sapu bersih koma menjadi titik dan ubah menjadi float (angka desimal)
#     for col in kolom_numerik_multi:
#         if col in df_multi.columns: # Memastikan kolom benar-benar ada
#             df_multi[col] = df_multi[col].apply(bersihkan_angka)

#     return df_pengeluaran, gdf, df_multi

# df_pengeluaran, gdf, df_multi = load_data()


# # =====================================================================
# # ALUR CERITA (SCROLLYTELLING)
# # =====================================================================
# html(CSS)
# html('<div class="progress"></div>')

# # ---------------------------- HERO ----------------------------------
# n_kab = gdf['Kab/Kota'].nunique()
# n_prov = len(df_multi)
# miskin_terbaru = gdf[gdf['Tahun'] == '2025']['Pct_Miskin'].mean()
# video_tag = (f'<video class="hero-video" src="{HERO_VIDEO_URL}" autoplay muted loop playsinline></video>'
#              if HERO_VIDEO_URL else "")

# html(f"""
# <section class="hero">
# {video_tag}
# <div class="hero-copy">
# <h1>Bumi, Manusia, dan Rupiah</h1>
# <div class="sub">Jejak Kesejahteraan Indonesia (2021 - 2025)</div>
# <p class="lead">Setiap jengkal tanah di Nusantara menyimpan ceritanya sendiri. Ada wilayah yang roda ekonominya berputar kencang, namun ada pula yang masih berjuang melepaskan diri dari jerat kemiskinan.</p>
# <div class="cta-row"><a class="cta main" href="#bab-1">Mulai dari peta</a><a class="cta ghost" href="#bab-4">Lompat ke profil provinsi</a></div>
# <div class="chips">
# <div class="chip"><b>{anim_num(n_kab)}</b><span>Kabupaten/Kota</span></div>
# <div class="chip"><b>{anim_num(n_prov)}</b><span>Provinsi dibedah</span></div>
# <div class="chip"><b>{anim_num(5)}</b><span>Tahun data (2021-2025)</span></div>
# <div class="chip"><b>{anim_num(miskin_terbaru, dec=True)}%</b><span>Rata-rata kemiskinan 2025</span></div>
# </div>
# </div>
# <div class="hero-art">
# <svg viewBox="0 0 520 380" class="scene" role="img" aria-label="Ilustrasi permukiman, padi, dan gedung pertumbuhan ekonomi">
# <defs>
# <linearGradient id="gbar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3fb37f"/><stop offset="1" stop-color="#2e8b57"/></linearGradient>
# <radialGradient id="gsun"><stop offset="0" stop-color="#ffd978"/><stop offset="1" stop-color="#f2b33d"/></radialGradient>
# <g id="wheat"><line x1="0" y1="0" x2="0" y2="-64" stroke="#b58b2a" stroke-width="3" stroke-linecap="round"/>
# <ellipse cx="0" cy="-70" rx="5" ry="10" fill="#f2b33d"/>
# <ellipse cx="-7" cy="-60" rx="4" ry="8" fill="#f2b33d" transform="rotate(-25 -7 -60)"/>
# <ellipse cx="7" cy="-60" rx="4" ry="8" fill="#f2b33d" transform="rotate(25 7 -60)"/>
# <ellipse cx="-7" cy="-48" rx="4" ry="8" fill="#e6a42c" transform="rotate(-25 -7 -48)"/>
# <ellipse cx="7" cy="-48" rx="4" ry="8" fill="#e6a42c" transform="rotate(25 7 -48)"/></g>
# </defs>
# <circle class="halo" cx="92" cy="78" r="52" fill="#f2b33d" opacity=".2"/>
# <circle cx="92" cy="78" r="34" fill="url(#gsun)"/>
# <path d="M0 292 Q130 246 262 286 T520 268 V380 H0Z" fill="#cfe8d5"/>
# <path d="M0 326 Q150 292 300 322 T520 306 V380 H0Z" fill="#9ccb9c"/>
# <path d="M0 352 Q170 330 330 350 T520 340 V380 H0Z" fill="#6fae7c"/>
# <rect x="34" y="266" width="52" height="36" fill="#f3d2ab"/><polygon points="28,268 60,240 92,268" fill="#c8794a"/><rect x="52" y="282" width="14" height="20" fill="#8a5a3b"/>
# <rect x="98" y="278" width="40" height="26" fill="#e8d6bb"/><polygon points="93,280 118,258 143,280" fill="#a8683f"/><rect x="111" y="289" width="10" height="15" fill="#7a4e33"/>
# <use href="#wheat" x="180" y="318" class="sway" style="--d:.2s"/>
# <use href="#wheat" x="202" y="322" class="sway" style="--d:.7s"/>
# <use href="#wheat" x="224" y="316" class="sway" style="--d:1.1s"/>
# <use href="#wheat" x="246" y="321" class="sway" style="--d:.5s"/>
# <rect class="bar" x="300" y="258" width="28" height="54" rx="5" fill="url(#gbar)" style="--d:.2s"/>
# <rect class="bar" x="336" y="230" width="28" height="82" rx="5" fill="url(#gbar)" style="--d:.4s"/>
# <rect class="bar" x="372" y="202" width="28" height="110" rx="5" fill="url(#gbar)" style="--d:.6s"/>
# <rect class="bar" x="408" y="172" width="28" height="140" rx="5" fill="url(#gbar)" style="--d:.8s"/>
# <rect class="bar" x="444" y="136" width="28" height="176" rx="5" fill="url(#gbar)" style="--d:1s"/>
# <polyline class="trend" points="314,246 350,218 386,190 422,156 458,112" fill="none" stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
# <circle class="dot" cx="458" cy="112" r="7" fill="#e8590c"/>
# <g class="coin" style="--d:0s"><circle cx="268" cy="168" r="15" fill="#f2b33d"/><circle cx="268" cy="168" r="11" fill="none" stroke="#fff" stroke-opacity=".7"/><text x="268" y="173" text-anchor="middle" font-size="11" font-weight="800" fill="#7a4e00">Rp</text></g>
# <g class="coin" style="--d:.9s"><circle cx="226" cy="118" r="13" fill="#f2b33d"/><circle cx="226" cy="118" r="9" fill="none" stroke="#fff" stroke-opacity=".7"/><text x="226" y="122" text-anchor="middle" font-size="10" font-weight="800" fill="#7a4e00">Rp</text></g>
# <g class="coin" style="--d:1.7s"><circle cx="170" cy="190" r="11" fill="#f2b33d"/><text x="170" y="194" text-anchor="middle" font-size="8" font-weight="800" fill="#7a4e00">Rp</text></g>
# <text x="62" y="366" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kemiskinan</text>
# <text x="214" y="366" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Pangan</text>
# <text x="386" y="366" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">PDRB</text>
# </svg>
# </div>
# </section>
# """)

# # --- BAB 1: Peta ---
# html('<div id="bab-1"></div>')
# bab("Bab 1")
# st.markdown("### Wajah Kesejahteraan dari Udara")
# st.write("Area yang tersapu warna **merah** menunjukkan tingginya persentase kemiskinan. Sementara itu, **pendaran cahaya hijau** adalah denyut nadi PDRB (dalam Triliun Rupiah) yang terkonsentrasi di wilayah tersebut.")

# # Wadah kartu: diisi setelah tahun dipilih, supaya kontrol berada tepat di atas peta
# area_kartu = st.container()

# chart_header("Peta Kemiskinan dan PDRB Kabupaten/Kota",
#              "Warna wilayah = persentase penduduk miskin (kuning ke merah). Lingkaran hijau = besar PDRB. Ubah tahun dan gaya peta di bawah ini.")

# # Kontrol peta (tepat di atas peta)
# ctl0, ctl1, ctl2 = st.columns([1, 1.2, 1.2])
# with ctl0:
#     selected_year = st.selectbox(
#         "⏳ Pilih Tahun:", 
#         options=[2021, 2022, 2023, 2024, 2025], 
#         index=4 # Default otomatis ke urutan terakhir (2025)
#     )
# with ctl1:
#     gaya_peta = st.radio("🗺️ Gaya peta", ["Satelit", "Terang"], horizontal=True)
# with ctl2:
#     tampil_pdrb = st.toggle("✨ Tampilkan pendaran PDRB", value=True)

# # FILTER DATA BERDASARKAN TAHUN YANG DIPILIH
# gdf_year = gdf[gdf['Tahun'] == str(selected_year)].copy()

# # HIGHLIGHT CARD (Otomatis berubah sesuai tahun)
# daerah_miskin_max = gdf_year.loc[gdf_year['Pct_Miskin'].idxmax()]
# daerah_pdrb_max = gdf_year.loc[gdf_year['PDRB'].idxmax()]

# def agregat(th):
#     d = gdf[gdf['Tahun'] == str(th)]
#     return d['Pct_Miskin'].mean(), d['PDRB'].sum()

# m_now, p_now = agregat(selected_year)
# ada_prev = selected_year > 2021
# m_prev, p_prev = agregat(selected_year - 1) if ada_prev else (None, None)
# n_atas = int((gdf_year['Pct_Miskin'] > m_now).sum())

# with area_kartu:
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         card("bad", "🚨", f"Tertinggi Miskin ({selected_year})", f"{daerah_miskin_max['Kab/Kota']}", big=f"{fmt_id(daerah_miskin_max['Pct_Miskin'])}%")
#     with col2:
#         card("good", "💎", f"Pusat Kemakmuran ({selected_year})", f"{daerah_pdrb_max['Kab/Kota']}", big=f"{fmt_id(daerah_pdrb_max['PDRB'])} Triliun")
#     with col3:
#         card("info", "💡", "Jelajahi Sendiri", "Scroll untuk mendekat (<i>zoom</i>), atau arahkan kursor ke wilayah manapun.")
#     st.markdown("<br>", unsafe_allow_html=True)
#     k1, k2, k3 = st.columns(3)
#     k1.metric("Rata-rata kemiskinan", f"{fmt_id(m_now)}%",
#               delta=(f"{m_now - m_prev:+.2f} poin vs {selected_year - 1}".replace('.', ',') if ada_prev else None), delta_color="inverse")
#     k2.metric("Total PDRB (Triliun Rp)", fmt_id(p_now, 0),
#               delta=(f"{(p_now - p_prev) / p_prev * 100:+.1f}% vs {selected_year - 1}".replace('.', ',') if ada_prev and p_prev else None))
#     k3.metric("Daerah di atas rata-rata miskin", f"{n_atas} daerah")

# # 1. Tangani data yang kosong (NaN) agar tidak bolong transparan
# gdf_year['Pct_Miskin_Clean'] = gdf_year['Pct_Miskin'].fillna(-1) # Beri penanda khusus -1 untuk data kosong

# # 2. Render Peta Utama
# fig_map = px.choropleth_map(
#     gdf_year, 
#     geojson=gdf_year.geometry, 
#     locations=gdf_year.index,
#     color='Pct_Miskin_Clean', 
#     color_continuous_scale="YlOrRd",
#     range_color=[0, gdf['Pct_Miskin'].max()],
#     map_style="white-bg", 
#     zoom=4, 
#     center={"lat": -0.789, "lon": 113.921},
#     opacity=0.9, 
#     hover_name='Kab/Kota',
#     hover_data={'Pct_Miskin': ':.2f', 'PDRB': ':.2f', 'Pct_Miskin_Clean': False}, 
#     labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Triliun)'}
# )

# sumber_tile = ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
#                if gaya_peta == "Satelit" else "https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png")
# fig_map.update_layout(
#     map_layers=[{"below": 'traces', "sourcetype": "raster", "source": [sumber_tile]}],
#     margin={"r":0,"t":0,"l":0,"b":0} 
# )
 
# gdf_bubble = gdf_year.dropna(subset=['PDRB', 'centroid_x', 'centroid_y'])
# fig_bubble = px.scatter_map( 
#     gdf_bubble, lat='centroid_y', lon='centroid_x', size='PDRB',
#     hover_name='Kab/Kota', hover_data={'PDRB': ':.2f', 'Pct_Miskin': ':.2f', 'centroid_y': False, 'centroid_x': False}, 
#     labels={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Triliun)'},
#     size_max=45, zoom=4
# )

# fig_bubble.update_traces(marker=dict(color='#00FF00' if gaya_peta == "Satelit" else COLOR_FOREST, opacity=0.4))

# if tampil_pdrb:
#     for trace in fig_bubble.data:
#         fig_map.add_trace(trace)

# st.plotly_chart(tema(fig_map), use_container_width=True)

# card("good", "📌", f"Catatan {selected_year}", "Peta di atas mengungkap bahwa pendaran hijau kemakmuran seringkali hanya terpusat pada titik tertentu, meninggalkan wilayah sekitarnya dalam balutan warna merah pekat.")

# # Eksplorasi lanjutan: peringkat, tren, tabel
# st.markdown("<br>", unsafe_allow_html=True)
# st.markdown("#### 🧭 Eksplorasi Lanjutan")
# tab_rank, tab_tren, tab_tabel = st.tabs(["🏆 Peringkat Daerah", "📈 Tren & Bandingkan", "🗂️ Tabel Data"])

# with tab_rank:
#     top_n = st.radio("Tampilkan daerah teratas", [5, 10], format_func=lambda n: f"Top {n}", horizontal=True, key="top_daerah")
#     cr1, cr2 = st.columns(2)
#     with cr1:
#         chart_header(f"Top {top_n} Kemiskinan Tertinggi ({selected_year})", "Daerah dengan persentase penduduk miskin terbesar.")
#         d_top_m = gdf_year.nlargest(top_n, 'Pct_Miskin')
#         fig_r1 = px.bar(d_top_m, x='Pct_Miskin', y='Kab/Kota', orientation='h',
#                         color_discrete_sequence=[COLOR_CORAL], labels={'Pct_Miskin': 'Kemiskinan (%)', 'Kab/Kota': ''})
#         fig_r1.update_yaxes(autorange='reversed')
#         fig_r1.update_layout(margin=dict(l=10, r=10, t=10, b=10))
#         st.plotly_chart(tema(fig_r1), use_container_width=True)
#     with cr2:
#         chart_header(f"Top {top_n} PDRB Tertinggi ({selected_year})", "Daerah dengan nilai tambah ekonomi terbesar (Triliun Rupiah).")
#         d_top_p = gdf_year.nlargest(top_n, 'PDRB')
#         fig_r2 = px.bar(d_top_p, x='PDRB', y='Kab/Kota', orientation='h',
#                         color_discrete_sequence=[COLOR_FOREST], labels={'PDRB': 'PDRB (Triliun)', 'Kab/Kota': ''})
#         fig_r2.update_yaxes(autorange='reversed')
#         fig_r2.update_layout(margin=dict(l=10, r=10, t=10, b=10))
#         st.plotly_chart(tema(fig_r2), use_container_width=True)

# with tab_tren:
#     df_tren_all = pd.DataFrame(gdf.drop(columns=['geometry']))
#     daftar_daerah = sorted(df_tren_all['Kab/Kota'].dropna().unique().tolist())
#     default_daerah = list(dict.fromkeys([daerah_miskin_max['Kab/Kota'], daerah_pdrb_max['Kab/Kota']]))
#     cari_daerah = st.multiselect("Pilih daerah untuk dibandingkan:", daftar_daerah, default=default_daerah, max_selections=5)
#     metrik_tren = st.radio("Indikator", ["Kemiskinan (%)", "PDRB (Triliun)"], horizontal=True)
#     kol_tren = 'Pct_Miskin' if metrik_tren.startswith("Kemiskinan") else 'PDRB'
#     chart_header(f"Tren {metrik_tren} 2021-2025", "Bandingkan perjalanan beberapa daerah dari tahun ke tahun.")
#     if cari_daerah:
#         df_t = df_tren_all[df_tren_all['Kab/Kota'].isin(cari_daerah)].sort_values('Tahun')
#         fig_t = px.line(df_t, x='Tahun', y=kol_tren, color='Kab/Kota', markers=True,
#                         color_discrete_sequence=[COLOR_FOREST, COLOR_CORAL, COLOR_SKY, COLOR_AMBER, '#8e5ea2'],
#                         labels={kol_tren: metrik_tren})
#         fig_t.update_traces(line=dict(width=3), marker=dict(size=9))
#         fig_t.update_layout(margin=dict(l=10, r=10, t=10, b=10))
#         st.plotly_chart(tema(fig_t), use_container_width=True)
#     else:
#         st.info("Pilih minimal satu daerah untuk melihat trennya.")

# with tab_tabel:
#     df_tabel = pd.DataFrame(gdf_year[['Kab/Kota', 'Pct_Miskin', 'PDRB']]).dropna(subset=['Kab/Kota'])
#     df_tabel = df_tabel.rename(columns={'Pct_Miskin': 'Kemiskinan (%)', 'PDRB': 'PDRB (Triliun)'}).sort_values('Kemiskinan (%)', ascending=False)
#     st.dataframe(df_tabel, use_container_width=True, hide_index=True, height=360)

# st.divider()

# # --- BAB 2: Moran's I ---
# bab("Bab 2")
# st.markdown(f"### Mengendus Kantong Kemiskinan di {selected_year}")
# st.write("Apakah kemiskinan menular secara geografis? Melalui analisis keruangan (*Moran's I*), kita melihat apakah wilayah miskin cenderung bergerombol dengan tetangganya.")

# try:
#     # Ganti metode Queen dengan KNN agar pulau-pulau terluar tetap memiliki tetangga terdekat
#     from libpysal.weights import KNN
    
#     gdf_moran = gdf_year.dropna(subset=['Pct_Miskin', 'geometry']).copy()
    
#     # Menggunakan K=5 (artinya setiap wilayah akan mencari 5 tetangga terdekat secara geografis)
#     w = KNN.from_dataframe(gdf_moran, k=5)
#     w.transform = 'r'

#     gdf_moran['Spatial_Lag'] = libpysal.weights.lag_spatial(w, gdf_moran['Pct_Miskin'])
#     gdf_moran['Z_Miskin'] = (gdf_moran['Pct_Miskin'] - gdf_moran['Pct_Miskin'].mean()) / gdf_moran['Pct_Miskin'].std()
#     gdf_moran['Z_Lag'] = (gdf_moran['Spatial_Lag'] - gdf_moran['Spatial_Lag'].mean()) / gdf_moran['Spatial_Lag'].std()

#     moran_global = Moran(gdf_moran['Pct_Miskin'], w)

#     # Tipe wilayah (bahasa awam) dari posisi kuadran
#     N_KANTONG, N_MAPAN, N_PULAU, N_BINTANG = "Kantong Kemiskinan", "Kawasan Mapan", "Pulau yang Tertinggal", "Bintang di Tengah Kesulitan"
#     m_hh = (gdf_moran['Z_Miskin'] > 0) & (gdf_moran['Z_Lag'] > 0)
#     m_ll = (gdf_moran['Z_Miskin'] < 0) & (gdf_moran['Z_Lag'] < 0)
#     m_hl = (gdf_moran['Z_Miskin'] > 0) & (gdf_moran['Z_Lag'] < 0)
#     m_lh = (gdf_moran['Z_Miskin'] < 0) & (gdf_moran['Z_Lag'] > 0)
#     gdf_moran['Tipe Wilayah'] = np.select([m_hh, m_ll, m_hl, m_lh], [N_KANTONG, N_MAPAN, N_PULAU, N_BINTANG], default="Mendekati rata-rata")
    
#     col_m1, col_m2 = st.columns([1, 2])
#     with col_m1:
#         st.metric(label=f"Indeks Global Moran's I ({selected_year})", value=f"{moran_global.I:.3f}")
#         if moran_global.I > 0:
#             card("info", "🧲", "Membaca hasilnya", "Karena nilainya positif, daerah-daerah miskin di Indonesia memang terbukti mengelompok secara berdekatan pada tahun ini.")
#         else:
#             card("info", "🧲", "Membaca hasilnya", "Nilainya nol atau negatif: pada tahun ini daerah miskin tidak terbukti bergerombol dengan tetangganya.")
#         card("warn", "🧭", "Skala angkanya", "Moran's I berkisar dari -1 sampai +1. Makin mendekati +1, makin kuat kemiskinan bergerombol. Dekat 0 berarti acak.")

#     with col_m2:
#         chart_header("Peta Tetangga: Apakah Kemiskinan Menular?",
#                      "Satu titik = satu kabupaten/kota. Makin ke kanan, daerah itu makin miskin dari rata-rata. Makin ke atas, tetangga-tetangganya makin miskin.")
#         fig_scatter = px.scatter(
#             gdf_moran, x='Z_Miskin', y='Z_Lag', hover_name='Kab/Kota', color='Tipe Wilayah',
#             hover_data={'Pct_Miskin': ':.2f', 'Z_Miskin': False, 'Z_Lag': False, 'Tipe Wilayah': False},
#             labels={'Z_Miskin': 'Kemiskinan daerah (kanan = lebih miskin)', 'Z_Lag': 'Kemiskinan tetangga (atas = lebih miskin)'},
#             color_discrete_map={N_KANTONG: COLOR_CORAL, N_MAPAN: COLOR_FOREST, N_PULAU: COLOR_AMBER, N_BINTANG: COLOR_SKY, "Mendekati rata-rata": "#b0b8b4"}
#         )
#         fig_scatter.update_traces(marker=dict(size=8, opacity=0.7))
#         fig_scatter.add_vline(x=0, line_width=2, line_dash="dash", line_color="black")
#         fig_scatter.add_hline(y=0, line_width=2, line_dash="dash", line_color="black")
#         for tx, px_, py_, xa, ya, wr in [(N_KANTONG, .98, .98, 'right', 'top', COLOR_CORAL), (N_BINTANG, .02, .98, 'left', 'top', COLOR_SKY),
#                                          (N_MAPAN, .02, .02, 'left', 'bottom', COLOR_FOREST), (N_PULAU, .98, .02, 'right', 'bottom', '#b9821a')]:
#             fig_scatter.add_annotation(xref='paper', yref='paper', x=px_, y=py_, xanchor=xa, yanchor=ya, text=f"<b>{tx}</b>", showarrow=False, font=dict(color=wr, size=13))
#         fig_scatter.update_layout(legend=dict(orientation='h', y=-0.22, title=None), margin=dict(l=10, r=10, t=10, b=10))
#         st.plotly_chart(tema(fig_scatter), use_container_width=True)

#     # Empat tipe wilayah, dijelaskan dengan bahasa cerita
#     st.markdown("#### Empat Tipe Wilayah dalam Cerita Ini")
#     st.write("Setiap daerah punya \"nasib\" yang dipengaruhi tetangganya. Dengan membandingkan kemiskinan sebuah daerah dengan kemiskinan sekitarnya, kita mendapat empat tipe:")
#     q1, q2, q3, q4 = st.columns(4)
#     with q1: card("bad", "🔥", N_KANTONG, "Miskin, dan tetangganya juga miskin. Kemiskinan di sini saling mengunci. <i>(High-High)</i>", big=f"{int(m_hh.sum())} daerah")
#     with q2: card("good", "🌿", N_MAPAN, "Kemiskinan rendah, tetangganya pun rendah. Kemakmuran menular ke sekitarnya. <i>(Low-Low)</i>", big=f"{int(m_ll.sum())} daerah")
#     with q3: card("warn", "🏝️", N_PULAU, "Miskin, padahal tetangganya relatif baik. Tertinggal sendirian di tengah kemajuan. <i>(High-Low)</i>", big=f"{int(m_hl.sum())} daerah")
#     with q4: card("info", "⭐", N_BINTANG, "Relatif baik, padahal tetangganya miskin. Layak dipelajari: apa yang membuatnya bertahan? <i>(Low-High)</i>", big=f"{int(m_lh.sum())} daerah")

#     df_hot = pd.DataFrame(gdf_moran.loc[m_hh, ['Kab/Kota', 'Pct_Miskin']]).sort_values('Pct_Miskin', ascending=False)
#     contoh = df_hot.head(3)['Kab/Kota'].tolist()
#     cerita = (f"Dari {len(gdf_moran)} kabupaten/kota pada {selected_year}, <b>{int(m_hh.sum())}</b> terkunci dalam kantong kemiskinan: miskin, dan dikelilingi tetangga yang miskin pula. "
#               f"Di sisi lain, <b>{int(m_ll.sum())}</b> daerah hidup berdampingan dengan tetangga yang sama-sama sejahtera. "
#               f"Hanya <b>{int(m_hl.sum())}</b> daerah yang tertinggal sendirian di tengah tetangga yang lebih baik, dan <b>{int(m_lh.sum())}</b> daerah yang mampu bertahan baik meski dikelilingi kemiskinan.")
#     if contoh:
#         cerita += f" Kantong yang paling dalam ada di {', '.join(contoh)}."
#     st.markdown("<br>", unsafe_allow_html=True)
#     card("good", "📖", f"Kisah {selected_year} dalam Satu Paragraf", cerita)

#     with st.expander("🔎 Lihat daftar wilayah Kantong Kemiskinan"):
#         st.dataframe(df_hot.rename(columns={'Pct_Miskin': 'Kemiskinan (%)'}), use_container_width=True, hide_index=True)
    
#     card("warn", "📌", "Fokus Analisis", "Perhatikan titik-titik di kuadran <b>Kanan Atas (Kantong Kemiskinan)</b>. Ini adalah wilayah prioritas yang terjebak di tengah kepungan wilayah miskin lainnya.")

# except Exception as e:
#     st.error(f"Kalkulasi spasial terhenti: {e}")

# st.divider()

# # --- BAB 3: Hierarki Pengeluaran (Memenuhi Syarat UAS Multirepresentasi) ---
# bab("Bab 3")
# st.markdown("### Konklusi: Ke Mana Uang Kita Bermuara?")
# st.write("Terlepas dari fluktuasi ekonomi dari 2021 hingga saat ini, prioritas bertahan hidup masyarakat bermuara pada struktur pengeluaran. Klik pada area mana pun untuk melakukan *drill-down/zoom*, atau arahkan kursor Anda untuk melihat rincian spesifik.")
# st.write("Dua variabel yang kita ukur (Total Pengeluaran & Pertumbuhan) menceritakan realitas ekonomi rumah tangga saat ini. Warna bergradasi dari **kuning** (pertumbuhan tertinggi) sampai **merah** (pertumbuhan terendah).")

# # Skala warna: merah (terendah) ke kuning (tertinggi)
# SKALA_PERTUMBUHAN = [[0, "#FFFFFF"], [0.5, "#71B8E7"], [1, "#0A5A8F"]]

# # Total & fakta ringkas untuk narasi
# total_pengeluaran = df_pengeluaran['Maret_2025'].sum()
# total_format = f"{total_pengeluaran:,.0f}".replace(',', '.') 
# l1 = df_pengeluaran.groupby('Level_1')['Maret_2025'].sum().sort_values(ascending=False)
# nama_l1, porsi_l1 = l1.index[0], l1.iloc[0] / total_pengeluaran * 100
# df_g = df_pengeluaran.replace([np.inf, -np.inf], np.nan).dropna(subset=['Pertumbuhan (%)']).copy()
# df_g['Komoditas'] = df_g['Level_3'].fillna(df_g['Level_2']).fillna(df_g['Level_1'])
# naik_1 = df_g.nlargest(1, 'Pertumbuhan (%)').iloc[0]
# turun_1 = df_g.nsmallest(1, 'Pertumbuhan (%)').iloc[0]

# # Representasi 1: Treemap
# chart_header("Peta Struktur Pengeluaran (Treemap)", "Luas kotak = besar pengeluaran rumah tangga (Maret 2025). Warna = pertumbuhan dibanding 2024.")
# fig_tree = px.treemap(
#     df_pengeluaran, 
#     path=['Level_1', 'Level_2', 'Level_3'], 
#     values='Maret_2025',                    
#     color='Pertumbuhan (%)',                
#     color_continuous_scale=SKALA_PERTUMBUHAN
# )
# fig_tree.update_traces(
#     textinfo='label+percent parent',
#     hovertemplate='<b>%{label}</b><br>Pengeluaran 2025: %{value:,.0f}<br>Pertumbuhan: %{color:.2f}%<extra></extra>'
# )
# # 🌟 KUNCI FORMAT INDONESIA: Ubah pemisah desimal jadi koma, pemisah ribuan jadi titik
# fig_tree.update_layout(separators=",.", margin=dict(l=10, r=10, t=10, b=10))
# c_t1, c_t2 = st.columns([2.4, 1])
# with c_t1:
#     st.plotly_chart(tema(fig_tree), use_container_width=True)
# with c_t2:
#     card("info", "📦", "Tulang Punggung (Ukuran Area)", f"Kotak yang paling luas mewakili penyedot anggaran terbesar. Ini adalah pengeluaran primer yang tidak bisa dihindari. Pos terbesar: <b>{nama_l1}</b> ({fmt_id(porsi_l1, 1)}% dari total).")
#     st.markdown("<br>", unsafe_allow_html=True)
#     card("warn", "📈", "Prioritas Baru (Warna Kuning)", f"Area kuning menandakan komoditas yang anggarannya paling meroket di 2025. Bisa berarti pergeseran gaya hidup atau dampak inflasi. Yang tertinggi: <b>{naik_1['Komoditas']}</b> ({fmt_id(naik_1['Pertumbuhan (%)'], 1)}%).")

# st.divider() # Garis pemisah antar grafik

# # Representasi 2: Sunburst
# chart_header("Cincin Struktur Pengeluaran (Sunburst)", "Cincin dalam = kelompok besar, cincin luar = rincian komoditas. Klik sebuah irisan untuk memperbesar.")
# fig_sun = px.sunburst(
#     df_pengeluaran,
#     path=['Level_1', 'Level_2', 'Level_3'], 
#     values='Maret_2025',                    
#     color='Pertumbuhan (%)',                
#     color_continuous_scale=SKALA_PERTUMBUHAN
# )
# fig_sun.update_traces(
#     textinfo='none', 
#     hovertemplate='<b>Kategori: %{label}</b><br>Pengeluaran 2025: %{value:,.0f}<br>Pertumbuhan dari 2024: %{color:.2f}%<extra></extra>'
# )
# fig_sun.update_layout(separators=",.", margin=dict(l=10, r=10, t=10, b=10))
# # Total di lingkaran tengah (format Indonesia)
# fig_sun.add_annotation(
#     text=f"<b>TOTAL</b><br>Rp {total_format}",
#     x=0.5, y=0.5, 
#     showarrow=False,
#     font=dict(size=15, color="black"),
#     align="center"
# )
# c_s1, c_s2 = st.columns([2.4, 1])
# with c_s1:
#     st.plotly_chart(tema(fig_sun), use_container_width=True)
# with c_s2:
#     card("info", "🎯", "Membaca Cincin", "Mulai dari lingkaran tengah, lalu bergerak keluar: setiap cincin memecah pengeluaran menjadi pos yang lebih rinci. Makin lebar irisan, makin besar porsi anggarannya.")
#     st.markdown("<br>", unsafe_allow_html=True)
#     card("bad", "📉", "Ikat Pinggang (Warna Merah)", f"Irisan merah menyoroti pengeluaran yang paling banyak dipangkas. Saat ekonomi sulit, pos-pos inilah yang pertama dikorbankan. Yang terdalam: <b>{turun_1['Komoditas']}</b> ({fmt_id(turun_1['Pertumbuhan (%)'], 1)}%).")

# # Komoditas yang paling naik & paling turun (hanya Top 5/10)
# st.markdown("#### 📊 Siapa yang Naik, Siapa yang Turun?")
# n_g = st.radio("Tampilkan komoditas teratas", [5, 10], format_func=lambda n: f"Top {n}", horizontal=True, key="top_komoditas")
# cg1, cg2 = st.columns(2)
# with cg1:
#     chart_header(f"Top {n_g} Paling Meroket", "Pertumbuhan pengeluaran Maret 2024 ke Maret 2025.")
#     naik = df_g.nlargest(n_g, 'Pertumbuhan (%)')
#     f_naik = px.bar(naik, x='Pertumbuhan (%)', y='Komoditas', orientation='h', color_discrete_sequence=[COLOR_AMBER])
#     f_naik.update_yaxes(autorange='reversed', title='')
#     f_naik.update_layout(separators=",.", margin=dict(l=10, r=10, t=10, b=10))
#     st.plotly_chart(tema(f_naik), use_container_width=True)
# with cg2:
#     chart_header(f"Top {n_g} Paling Dipangkas", "Komoditas dengan pertumbuhan terendah (atau penurunan terdalam).")
#     turun = df_g.nsmallest(n_g, 'Pertumbuhan (%)')
#     f_turun = px.bar(turun, x='Pertumbuhan (%)', y='Komoditas', orientation='h', color_discrete_sequence=["#b4b70e"])
#     f_turun.update_yaxes(autorange='reversed', title='')
#     f_turun.update_layout(separators=",.", margin=dict(l=10, r=10, t=10, b=10))
#     st.plotly_chart(tema(f_turun), use_container_width=True)

# st.divider()

# # ---------------------------------------------------------------------
# # BAB 4: PROFIL MULTIDIMENSI (Syarat UAS Visualisasi Data Multivariat)
# # ---------------------------------------------------------------------
# html('<div id="bab-4"></div>')
# bab("Bab 4")
# st.markdown("### 4. Membedah Profil Kesejahteraan Multidimensi (34 Provinsi)")
# st.write("Kesejahteraan tidak hanya diukur dari uang. Mari kita lihat 8 dimensi kehidupan dari 34 Provinsi di Indonesia.")

# # FITUR LINKING: Dropdown untuk menyorot (Highlight) Provinsi tertentu di semua grafik
# provinsi_terpilih = st.selectbox("🎯 Sorot (Highlight) Provinsi:", options=df_multi['Provinsi'].tolist(), index=10)

# # 1. PARALLEL COORDINATES (Brushing Technique)
# st.markdown("#### A. Jejaring Indikator (Parallel Coordinates)")
# st.write("💡 *Tip Interaksi (Brushing):* Klik dan seret (drag) kursor Anda pada garis sumbu vertikal di bawah ini untuk memfilter (brushing) rentang nilai tertentu. Satu garis = satu provinsi; garis gelap adalah provinsi yang Anda sorot.")

# kolom_numerik = df_multi.select_dtypes(include=[np.number]).columns.tolist()
# # Membuat kolom penanda warna (1 untuk provinsi terpilih, 0 untuk lainnya)
# df_multi['Color_Flag'] = np.where(df_multi['Provinsi'] == provinsi_terpilih, 1, 0)

# fig_par = px.parallel_coordinates(
#     df_multi, dimensions=kolom_numerik, color='Color_Flag',
#     color_continuous_scale=[[0, COLOR_SAGE], [1, COLOR_DARK]],
#     labels={col: col.replace('_', ' ') for col in kolom_numerik}
# )
# fig_par.update_layout(coloraxis_showscale=False, margin=dict(l=50, r=50, t=30, b=30))
# st.plotly_chart(tema(fig_par), use_container_width=True)

# # Membagi layar untuk PCA dan Radar Chart
# col_pca, col_radar = st.columns(2)

# # 2. PCA SCATTERPLOT (Dimensionality Reduction)
# with col_pca:
#     st.markdown("#### B. Peta Pengelompokan (PCA)")
    
#     # Proses PCA (Reduksi 8 variabel menjadi 2 komponen utama)
#     scaler = StandardScaler()
#     data_scaled = scaler.fit_transform(df_multi[kolom_numerik])
#     pca = PCA(n_components=2)
#     pca_result = pca.fit_transform(data_scaled)
    
#     df_pca = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])
#     df_pca['Provinsi'] = df_multi['Provinsi']
#     df_pca['Status'] = np.where(df_multi['Provinsi'] == provinsi_terpilih, 'Disorot', 'Lainnya')

#     # Pencilan = 3 provinsi paling jauh dari pusat peta
#     df_pca['Jarak'] = np.sqrt(df_pca['PC1'] ** 2 + df_pca['PC2'] ** 2)
#     nama_pencilan = df_pca.nlargest(3, 'Jarak')['Provinsi'].tolist()

#     chart_header(f"Varian yang dijelaskan: {pca.explained_variance_ratio_.sum()*100:.1f}%",
#                  f"Makin dekat dua titik, makin mirip profilnya. Titik oranye = {provinsi_terpilih}. Label hanya untuk provinsi terpilih dan 3 yang paling terpencil.")
#     fig_pca = px.scatter(
#         df_pca, x='PC1', y='PC2', color='Status', hover_name='Provinsi', hover_data={'Status': False, 'Jarak': False, 'PC1': ':.2f', 'PC2': ':.2f'},
#         color_discrete_map={'Disorot': COLOR_HIGHLIGHT, 'Lainnya': COLOR_SAGE}
#     )
#     fig_pca.update_traces(marker=dict(size=10, opacity=0.8))
#     fig_pca.update_traces(marker=dict(size=18, opacity=1, line=dict(width=2, color='white')), selector=dict(name='Disorot'))
#     for _, r in df_pca[df_pca['Provinsi'].isin(nama_pencilan + [provinsi_terpilih])].iterrows():
#         sel = r['Provinsi'] == provinsi_terpilih
#         fig_pca.add_annotation(x=r['PC1'], y=r['PC2'], text=f"<b>{r['Provinsi']}</b>" if sel else r['Provinsi'],
#                                showarrow=True, arrowhead=0, arrowcolor=COLOR_CORAL if sel else '#7a8a83', ax=38, ay=-38,
#                                font=dict(size=13 if sel else 11, color=COLOR_CORAL if sel else COLOR_INK),
#                                bgcolor="rgba(255,255,255,.9)", borderpad=3)
#     fig_pca.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
#     st.plotly_chart(tema(fig_pca), use_container_width=True)

# # 3. RADAR CHART (Profil Individu)
# with col_radar:
#     st.markdown(f"#### C. Jaring Laba-laba: **{provinsi_terpilih}**")
    
#     # Standarisasi skala 0-100 untuk radar chart agar bentuknya seimbang
#     df_radar_norm = (df_multi[kolom_numerik] - df_multi[kolom_numerik].min()) / (df_multi[kolom_numerik].max() - df_multi[kolom_numerik].min()) * 100
#     nilai_provinsi = df_radar_norm[df_multi['Provinsi'] == provinsi_terpilih].values[0]
#     nilai_nasional = df_radar_norm.mean().values

#     chart_header("Profil dibanding rata-rata nasional", "Makin menjauh dari pusat, makin tinggi nilai indikatornya (skala 0-100).")
#     fig_radar = go.Figure()
#     fig_radar.add_trace(go.Scatterpolar(r=nilai_nasional, theta=kolom_numerik, fill='toself', name='Rata-rata Nasional', marker_color=COLOR_SAGE, opacity=0.5))
#     fig_radar.add_trace(go.Scatterpolar(r=nilai_provinsi, theta=kolom_numerik, fill='toself', name=provinsi_terpilih, marker_color=COLOR_DARK))
    
#     fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)), showlegend=True, margin=dict(l=30, r=30, t=30, b=30))
#     st.plotly_chart(tema(fig_radar), use_container_width=True)

# # Sekilas provinsi terpilih dibanding rata-rata nasional
# st.markdown(f"#### Sekilas: **{provinsi_terpilih}** vs Rata-rata Nasional")
# idx_prov = df_multi.index[df_multi['Provinsi'] == provinsi_terpilih][0]
# kolom_sekilas = [c for c in ['IPM', 'Persentase_Miskin', 'TPT', 'UHH'] if c in kolom_numerik]
# kolom_negatif = {'Persentase_Miskin', 'TPT'}  # makin kecil makin baik
# cols_sk = st.columns(len(kolom_sekilas)) if kolom_sekilas else []
# for cs, kc in zip(cols_sk, kolom_sekilas):
#     nilai = df_multi.loc[idx_prov, kc]
#     rata = df_multi[kc].mean()
#     cs.metric(kc.replace('_', ' '), f"{nilai:.2f}".replace('.', ','),
#               delta=f"{nilai - rata:+.2f} vs nasional".replace('.', ','),
#               delta_color="inverse" if kc in kolom_negatif else "normal")

# # D. Peringkat antarprovinsi (Top 5/10, provinsi terpilih selalu ikut ditampilkan)
# st.markdown("#### D. Peringkat Antarprovinsi")
# cp1, cp2, cp3 = st.columns([2, 1.4, 1.2])
# with cp1:
#     indikator_pilih = st.selectbox("Pilih indikator:", kolom_numerik, format_func=lambda c: c.replace('_', ' '))
# with cp2:
#     urutan = st.radio("Urutan", ["Tertinggi dulu", "Terendah dulu"], horizontal=True)
# with cp3:
#     top_p = st.radio("Tampilkan", [5, 10], format_func=lambda n: f"Top {n}", horizontal=True, key="top_prov")
# df_rank = df_multi[['Provinsi', indikator_pilih]].dropna().sort_values(indikator_pilih, ascending=(urutan == "Terendah dulu")).reset_index(drop=True)
# df_rank['Peringkat'] = df_rank.index + 1
# df_show = df_rank.head(top_p)
# if provinsi_terpilih not in df_show['Provinsi'].values:
#     df_show = pd.concat([df_show, df_rank[df_rank['Provinsi'] == provinsi_terpilih]])
# df_show = df_show.copy()
# df_show['Label'] = df_show['Peringkat'].astype(str) + ". " + df_show['Provinsi']
# df_show['Status'] = np.where(df_show['Provinsi'] == provinsi_terpilih, 'Disorot', 'Lainnya')
# chart_header(f"Top {top_p} Provinsi: {indikator_pilih.replace('_', ' ')}",
#              f"Menampilkan {top_p} provinsi teratas. Jika {provinsi_terpilih} tidak masuk, ia ditambahkan di bawah lengkap dengan peringkatnya.")
# fig_rank = px.bar(df_show, x=indikator_pilih, y='Label', orientation='h', color='Status',
#                   color_discrete_map={'Disorot': COLOR_HIGHLIGHT, 'Lainnya': COLOR_SAGE},
#                   labels={indikator_pilih: indikator_pilih.replace('_', ' '), 'Label': ''}, height=90 + 38 * len(df_show))
# fig_rank.update_yaxes(autorange='reversed')
# fig_rank.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
# st.plotly_chart(tema(fig_rank), use_container_width=True)

# # 4. KOTAK INTERPRETASI
# html(f"""
# <div class="card info wide"><div class="card-ico">🔎</div><div>
# <div class="card-title">Interpretasi Analisis Multidimensi</div>
# <ul>
# <li><b>Pengelompokan (Klastering):</b> Pada grafik PCA (kiri), provinsi yang posisinya saling berdekatan menandakan mereka memiliki karakteristik sosial-ekonomi yang sangat mirip di ke-8 variabel tersebut.</li>
# <li><b>Pencilan (Outlier):</b> Provinsi yang posisinya terasing/menjauh dari kerumunan utama di grafik PCA adalah provinsi dengan anomali. Pada data ini yang paling terpencil adalah <b>{', '.join(nama_pencilan)}</b>.</li>
# <li><b>Profil Radar:</b> Bentuk jaring yang condong mendekati batas luar menandakan performa yang sangat baik di atas rata-rata nasional pada indikator tersebut.</li>
# </ul></div></div>
# """)

# st.markdown("<br><br><center><p style='color: gray;'><i>Sebuah eksplorasi data visual. Dibuat untuk Tugas Akhir Visualisasi Data.</i></p></center>", unsafe_allow_html=True)

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
.chip span{ font-size:.78rem; color:var(--muted); }
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
.card{ --c:var(--sky); position:relative; display:flex; gap:14px; align-items:flex-start; min-height:150px; height:100%;
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
[data-testid="stPlotlyChart"]{ background:rgba(255,255,255,.72); border-radius:24px; padding:10px; border:1px solid rgba(255,255,255,.95);
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
video_tag = (f'<video class="hero-video" src="{HERO_VIDEO_URL}" autoplay muted loop playsinline></video>'
             if HERO_VIDEO_URL else "")

html(f"""
<section class="hero">
{video_tag}
<div class="hero-copy">
<h1>Bumi, Manusia, dan Rupiah</h1>
<div class="sub">Jejak Kesejahteraan Indonesia (2021 - 2025)</div>
<p class="lead">Setiap jengkal tanah di Nusantara menyimpan ceritanya sendiri. Ada wilayah yang roda ekonominya berputar kencang, namun ada pula yang masih berjuang melepaskan diri dari jerat kemiskinan.</p>
<div class="cta-row"><a class="cta main" href="#bab-1">Mulai dari peta</a><a class="cta ghost" href="#bab-4">Lompat ke profil provinsi</a></div>
<div class="chips">
<div class="chip"><b>{anim_num(n_kab)}</b><span>Kabupaten/Kota</span></div>
<div class="chip"><b>{anim_num(n_prov)}</b><span>Provinsi dibedah</span></div>
<div class="chip"><b>{anim_num(5)}</b><span>Tahun data (2021-2025)</span></div>
<div class="chip"><b>{anim_num(miskin_terbaru, dec=True)}%</b><span>Rata-rata kemiskinan 2025</span></div>
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
st.markdown("### Wajah Kesejahteraan dari Udara")
st.write("Area yang tersapu warna **merah** menunjukkan tingginya persentase kemiskinan. Sementara itu, **pendaran cahaya hijau** adalah denyut nadi PDRB (dalam Triliun Rupiah) yang terkonsentrasi di wilayah tersebut.")

# Wadah kartu: diisi setelah tahun dipilih, supaya kontrol berada tepat di atas peta
area_kartu = st.container()

chart_header("Peta Kemiskinan dan PDRB Kabupaten/Kota",
             "Warna wilayah = persentase penduduk miskin (kuning ke merah). Lingkaran hijau = besar PDRB. Ubah tahun di bawah ini.")

# Kontrol peta (tepat di atas peta)
ctl0, _ctl_sisa = st.columns([1, 3])
with ctl0:
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
        card("bad", "🚨", f"Tertinggi Miskin ({selected_year})", f"{daerah_miskin_max['Kab/Kota']}", big=f"{fmt_id(daerah_miskin_max['Pct_Miskin'])}%")
    with col2:
        card("good", "💎", f"Pusat Kemakmuran ({selected_year})", f"{daerah_pdrb_max['Kab/Kota']}", big=f"{fmt_id(daerah_pdrb_max['PDRB'])} Triliun")
    with col3:
        card("info", "💡", "Jelajahi Sendiri", "Scroll untuk mendekat (<i>zoom</i>), atau arahkan kursor ke wilayah manapun.")
    st.markdown("<br>", unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    k1.metric("Rata-rata kemiskinan", f"{fmt_id(m_now)}%",
              delta=(f"{m_now - m_prev:+.2f} poin vs {selected_year - 1}".replace('.', ',') if ada_prev else None), delta_color="inverse")
    k2.metric("Total PDRB (Triliun Rp)", fmt_id(p_now, 0),
              delta=(f"{(p_now - p_prev) / p_prev * 100:+.1f}% vs {selected_year - 1}".replace('.', ',') if ada_prev and p_prev else None))
    k3.metric("Daerah di atas rata-rata miskin", f"{n_atas} daerah")

# 1. Tangani data yang kosong (NaN) agar tidak bolong transparan
gdf_year['Pct_Miskin_Clean'] = gdf_year['Pct_Miskin'].fillna(-1) # Beri penanda khusus -1 untuk data kosong

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

sumber_tile = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
fig_map.update_layout(
    map_layers=[{"below": 'traces', "sourcetype": "raster", "source": [sumber_tile]}],
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

fig_map.update_layout(coloraxis_colorbar=dict(title="Kemiskinan (%)"))
st.plotly_chart(tema(fig_map), use_container_width=True)

card("good", "📌", f"Catatan {selected_year}", "Peta di atas mengungkap bahwa pendaran hijau kemakmuran seringkali hanya terpusat pada titik tertentu, meninggalkan wilayah sekitarnya dalam balutan warna merah pekat.")

# Eksplorasi lanjutan: cerita bergulir (scrollytelling) berbentuk piktogram
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

# st.markdown("<br>", unsafe_allow_html=True)
# st.markdown("#### 🧭 Eksplorasi Lanjutan")
# st.write("Gulir pelan ke bawah. Setiap fase memunculkan satu cerita baru, digambarkan dengan piktogram.")
# top_n = st.radio("Jumlah daerah teratas pada Fase 2 dan 3", [5, 10], format_func=lambda n: f"Top {n}", horizontal=True, key="top_daerah")

# tahun_semua = [2021, 2022, 2023, 2024, 2025]
# agr = {t: agregat(t) for t in tahun_semua}


# def fase(no, judul, isi, vis_judul, vis_html, catatan=""):
#     cat = f'<div class="vis-note">{catatan}</div>' if catatan else ""
#     html(f'<section class="story"><div class="story-card"><div class="badge">Fase {no}</div><h4>{judul}</h4><p>{isi}</p></div>'
#          f'<div class="rail"></div><div class="story-vis"><div class="vis-title">{vis_judul}</div><div class="vis-panel">{vis_html}</div>{cat}</div></section>')


# def fmt_unit(u):
#     return fmt_id(u, 0 if float(u).is_integer() else 1)


# # Fase 1: 100 orang
# full1 = int(m_now)
# sel1 = ikon(PERSON, m_now - full1, ghost=True)
# sisa1 = max(0, 100 - full1 - 1)
# cells1 = "".join(ikon(PERSON) for _ in range(full1)) + sel1 + "".join(ikon(PERSON, 0, ghost=True) for _ in range(sisa1))
# fase(1, "Seandainya Satu Daerah Dihuni 100 Orang",
#      f"Pada {selected_year}, rata-rata kabupaten/kota memiliki <b>{fmt_id(m_now)}%</b> penduduk yang hidup di bawah garis kemiskinan. Bayangkan satu daerah yang dihuni 100 orang: sebanyak inilah yang berada di sana. Arahkan kursor ke ikon untuk melihatnya lebih dekat.",
#      f"Potret {selected_year}", f'<div class="grid100 pic-bad">{cells1}</div>',
#      "1 ikon = 1 dari 100 orang. Ikon merah = hidup di bawah garis kemiskinan.")

# # Fase 2: daerah paling miskin
# d2 = gdf_year.dropna(subset=['Kab/Kota', 'Pct_Miskin']).nlargest(top_n, 'Pct_Miskin')
# unit2 = nice_unit(d2['Pct_Miskin'].max())
# top2 = d2.iloc[0]
# fase(2, f"{top_n} Daerah yang Paling Berat",
#      f"Di <b>{top2['Kab/Kota']}</b>, sekitar <b>{fmt_id(top2['Pct_Miskin'] / 10, 1)}</b> dari setiap 10 penduduk hidup di bawah garis kemiskinan. Rata-rata {top_n} daerah teratas mencapai <b>{fmt_id(d2['Pct_Miskin'].mean())}%</b>, sementara rata-rata seluruh daerah {fmt_id(m_now)}%.",
#      f"Kemiskinan Tertinggi {selected_year}",
#      f'<div class="pic-bad">{pic_rows([(r["Kab/Kota"], r["Pct_Miskin"]) for _, r in d2.iterrows()], PERSON, unit2, lambda v: f"{fmt_id(v)}%")}</div>',
#      f"1 ikon = {fmt_unit(unit2)} poin persen penduduk miskin.")

# # Fase 3: PDRB tertinggi
# d3 = gdf_year.dropna(subset=['Kab/Kota', 'PDRB']).nlargest(top_n, 'PDRB')
# unit3 = nice_unit(d3['PDRB'].max())
# top3 = d3.iloc[0]
# share3 = d3['PDRB'].sum() / p_now * 100 if p_now else 0
# fase(3, "Di Mana Rupiah Berputar",
#      f"<b>{top3['Kab/Kota']}</b> memimpin dengan PDRB <b>{fmt_id(top3['PDRB'])} Triliun</b>. {top_n} daerah teratas menyumbang <b>{fmt_id(share3, 1)}%</b> dari total PDRB seluruh kabupaten/kota pada {selected_year}.",
#      f"PDRB Tertinggi {selected_year}",
#      f'<div class="pic-gold">{pic_rows([(r["Kab/Kota"], r["PDRB"]) for _, r in d3.iterrows()], COIN, unit3, lambda v: f"{fmt_id(v, 1)} T")}</div>',
#      f"1 koin = {fmt_unit(unit3)} Triliun Rupiah.")

# # Fase 4: tren kemiskinan nasional
# m0, m1 = agr[2021][0], agr[2025][0]
# dm = m1 - m0
# fase(4, "Lima Tahun Perjalanan",
#      f"Dari 2021 ke 2025, rata-rata kemiskinan kabupaten/kota {'turun' if dm < 0 else 'naik'} <b>{fmt_id(abs(dm))} poin</b>, dari {fmt_id(m0)}% menjadi {fmt_id(m1)}%. Baris yang disorot adalah tahun yang sedang Anda pilih.",
#      "Tren Kemiskinan per Tahun",
#      f'<div class="pic-bad">{pic_rows([(str(t), agr[t][0]) for t in tahun_semua], PERSON, 1.0, lambda v: f"{fmt_id(v)}%", hl=selected_year)}</div>',
#      "1 ikon = 1 poin persen penduduk miskin.")

# # Fase 5: tren PDRB nasional
# p0, p1 = agr[2021][1], agr[2025][1]
# g = (p1 - p0) / p0 * 100 if p0 else 0
# unit5 = nice_unit(max(agr[t][1] for t in tahun_semua))
# fase(5, "Denyut Ekonomi, Lima Tahun",
#      f"Total PDRB seluruh kabupaten/kota {'tumbuh' if g >= 0 else 'menyusut'} <b>{fmt_id(abs(g), 1)}%</b>, dari Rp {fmt_id(p0, 0)} Triliun (2021) menjadi Rp {fmt_id(p1, 0)} Triliun (2025). Pertanyaannya: apakah pertumbuhan itu sudah dinikmati merata?",
#      "Tren PDRB per Tahun",
#      f'<div class="pic-gold">{pic_rows([(str(t), agr[t][1]) for t in tahun_semua], COIN, unit5, lambda v: f"{fmt_id(v, 0)} T", hl=selected_year)}</div>',
#      f"1 koin = {fmt_unit(unit5)} Triliun Rupiah.")

st.divider()

# --- BAB 2: Moran's I ---
bab("Bab 2")
st.markdown(f"### Mengendus Kantong Kemiskinan di {selected_year}")
st.write("Apakah kemiskinan menular secara geografis? Melalui analisis keruangan (*Moran's I*), kita melihat apakah wilayah miskin cenderung bergerombol dengan tetangganya.")

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
    N_KANTONG, N_MAPAN, N_PULAU, N_BINTANG = "Kantong Kemiskinan", "Kawasan Mapan", "Pulau yang Tertinggal", "Bintang di Tengah Kesulitan"
    m_hh = (gdf_moran['Z_Miskin'] > 0) & (gdf_moran['Z_Lag'] > 0)
    m_ll = (gdf_moran['Z_Miskin'] < 0) & (gdf_moran['Z_Lag'] < 0)
    m_hl = (gdf_moran['Z_Miskin'] > 0) & (gdf_moran['Z_Lag'] < 0)
    m_lh = (gdf_moran['Z_Miskin'] < 0) & (gdf_moran['Z_Lag'] > 0)
    gdf_moran['Tipe Wilayah'] = np.select([m_hh, m_ll, m_hl, m_lh], [N_KANTONG, N_MAPAN, N_PULAU, N_BINTANG], default="Mendekati rata-rata")
    
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        st.metric(label=f"Indeks Global Moran's I ({selected_year})", value=f"{moran_global.I:.3f}")
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        if moran_global.I > 0:
            card("info", "🧲", "Membaca hasilnya", "Karena nilainya positif, daerah-daerah miskin di Indonesia memang terbukti mengelompok secara berdekatan pada tahun ini.")
        else:
            card("info", "🧲", "Membaca hasilnya", "Nilainya nol atau negatif: pada tahun ini daerah miskin tidak terbukti bergerombol dengan tetangganya.")
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        card("warn", "🧭", "Skala angkanya", "Moran's I berkisar dari -1 sampai +1. Makin mendekati +1, makin kuat kemiskinan bergerombol. Dekat 0 berarti acak.")

    with col_m2:
        chart_header("Peta Tetangga: Apakah Kemiskinan Menular?",
                     "Satu titik = satu kabupaten/kota. Makin ke kanan, daerah itu makin miskin dari rata-rata. Makin ke atas, tetangga-tetangganya makin miskin.")
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
    st.markdown("#### Empat Tipe Wilayah dalam Cerita Ini")
    st.write("Setiap daerah punya \"nasib\" yang dipengaruhi tetangganya. Dengan membandingkan kemiskinan sebuah daerah dengan kemiskinan sekitarnya, kita mendapat empat tipe:")
    q1, q2, q3, q4 = st.columns(4)
    with q1: card("bad", "🔥", N_KANTONG, "Miskin, dan tetangganya juga miskin. Kemiskinan di sini saling mengunci. <i>(High-High)</i>", big=f"{int(m_hh.sum())} daerah")
    with q2: card("good", "🌿", N_MAPAN, "Kemiskinan rendah, tetangganya pun rendah. Kemakmuran menular ke sekitarnya. <i>(Low-Low)</i>", big=f"{int(m_ll.sum())} daerah")
    with q3: card("warn", "🏝️", N_PULAU, "Miskin, padahal tetangganya relatif baik. Tertinggal sendirian di tengah kemajuan. <i>(High-Low)</i>", big=f"{int(m_hl.sum())} daerah")
    with q4: card("info", "⭐", N_BINTANG, "Relatif baik, padahal tetangganya miskin. Layak dipelajari: apa yang membuatnya bertahan? <i>(Low-High)</i>", big=f"{int(m_lh.sum())} daerah")

    df_hot = pd.DataFrame(gdf_moran.loc[m_hh, ['Kab/Kota', 'Pct_Miskin']]).sort_values('Pct_Miskin', ascending=False)
    contoh = df_hot.head(3)['Kab/Kota'].tolist()
    cerita = (f"Dari {len(gdf_moran)} kabupaten/kota pada {selected_year}, <b>{int(m_hh.sum())}</b> terkunci dalam kantong kemiskinan: miskin, dan dikelilingi tetangga yang miskin pula. "
              f"Di sisi lain, <b>{int(m_ll.sum())}</b> daerah hidup berdampingan dengan tetangga yang sama-sama sejahtera. "
              f"Hanya <b>{int(m_hl.sum())}</b> daerah yang tertinggal sendirian di tengah tetangga yang lebih baik, dan <b>{int(m_lh.sum())}</b> daerah yang mampu bertahan baik meski dikelilingi kemiskinan.")
    if contoh:
        cerita += f" Kantong yang paling dalam ada di {', '.join(contoh)}."
    st.markdown("<br>", unsafe_allow_html=True)
    card("good", "📖", f"Kisah {selected_year} dalam Satu Paragraf", cerita)
    st.markdown("<br>", unsafe_allow_html=True)

    # with st.expander("🔎 Lihat daftar wilayah Kantong Kemiskinan"):
    #     st.dataframe(df_hot.rename(columns={'Pct_Miskin': 'Kemiskinan (%)'}), use_container_width=True, hide_index=True)
    
    card("warn", "📌", "Fokus Analisis", "Perhatikan titik-titik di kuadran <b>Kanan Atas (Kantong Kemiskinan)</b>. Ini adalah wilayah prioritas yang terjebak di tengah kepungan wilayah miskin lainnya.")

except Exception as e:
    st.error(f"Kalkulasi spasial terhenti: {e}")

st.divider()

# --- BAB 3: Hierarki Pengeluaran (Memenuhi Syarat UAS Multirepresentasi) ---
bab("Bab 3")
st.markdown("### Konklusi: Ke Mana Uang Kita Bermuara?")
st.write("Terlepas dari fluktuasi ekonomi dari 2021 hingga saat ini, prioritas bertahan hidup masyarakat bermuara pada struktur pengeluaran. Klik pada area mana pun untuk melakukan *drill-down/zoom*, atau arahkan kursor Anda untuk melihat rincian spesifik.")
st.write("Dua variabel yang kita ukur (Total Pengeluaran & Pertumbuhan) menceritakan realitas ekonomi rumah tangga saat ini. Warna bergradasi dari **kuning** (pertumbuhan tertinggi) sampai **merah** (pertumbuhan terendah).")

# Skala warna: merah (terendah) ke kuning (tertinggi)
SKALA_PERTUMBUHAN = [[0, '#b7160e'], [0.5, '#f2761a'], [1, '#ffd93d']]

# Total & fakta ringkas untuk narasi
total_pengeluaran = df_pengeluaran['Maret_2025'].sum()
total_format = f"{total_pengeluaran:,.0f}".replace(',', '.') 
l1 = df_pengeluaran.groupby('Level_1')['Maret_2025'].sum().sort_values(ascending=False)
nama_l1, porsi_l1 = l1.index[0], l1.iloc[0] / total_pengeluaran * 100
df_g = df_pengeluaran.replace([np.inf, -np.inf], np.nan).dropna(subset=['Pertumbuhan (%)']).copy()
df_g['Komoditas'] = df_g['Level_3'].fillna(df_g['Level_2']).fillna(df_g['Level_1'])
naik_1 = df_g.nlargest(1, 'Pertumbuhan (%)').iloc[0]
turun_1 = df_g.nsmallest(1, 'Pertumbuhan (%)').iloc[0]

# Representasi 1: Treemap
chart_header("Peta Struktur Pengeluaran (Treemap)", "Luas kotak = besar pengeluaran rumah tangga (Maret 2025). Warna = pertumbuhan dibanding 2024.")
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
    card("info", "📦", "Tulang Punggung (Ukuran Area)", f"Kotak yang paling luas mewakili penyedot anggaran terbesar. Ini adalah pengeluaran primer yang tidak bisa dihindari. Pos terbesar: <b>{nama_l1}</b> ({fmt_id(porsi_l1, 1)}% dari total).")
    st.markdown("<br>", unsafe_allow_html=True)
    card("warn", "📈", "Prioritas Baru (Warna Kuning)", f"Area kuning menandakan komoditas yang anggarannya paling meroket di 2025. Bisa berarti pergeseran gaya hidup atau dampak inflasi. Yang tertinggi: <b>{naik_1['Komoditas']}</b> ({fmt_id(naik_1['Pertumbuhan (%)'], 1)}%).")

st.divider() # Garis pemisah antar grafik

# Representasi 2: Sunburst
chart_header("Cincin Struktur Pengeluaran (Sunburst)", "Cincin dalam = kelompok besar, cincin luar = rincian komoditas. Klik sebuah irisan untuk memperbesar.")
fig_sun = px.sunburst(
    df_pengeluaran,
    path=['Level_1', 'Level_2', 'Level_3'], 
    values='Maret_2025',                    
    color='Pertumbuhan (%)',                
    color_continuous_scale=SKALA_PERTUMBUHAN
)
fig_sun.update_traces(
    textinfo='none', 
    hovertemplate='<b>Kategori: %{label}</b><br>Pengeluaran 2025: %{value:,.0f}<br>Pertumbuhan dari 2024: %{color:.2f}%<extra></extra>'
)
fig_sun.update_layout(separators=",.", margin=dict(l=10, r=10, t=10, b=10))
# Total di lingkaran tengah (format Indonesia)
fig_sun.add_annotation(
    text=f"<b>TOTAL</b><br>Rp {total_format}",
    x=0.5, y=0.5, 
    showarrow=False,
    font=dict(size=15, color="black"),
    align="center"
)
c_s1, c_s2 = st.columns([2.4, 1])
with c_s1:
    st.plotly_chart(tema(fig_sun), use_container_width=True)
with c_s2:
    card("info", "🎯", "Membaca Cincin", "Mulai dari lingkaran tengah, lalu bergerak keluar: setiap cincin memecah pengeluaran menjadi pos yang lebih rinci. Makin lebar irisan, makin besar porsi anggarannya.")
    st.markdown("<br>", unsafe_allow_html=True)
    card("bad", "📉", "Ikat Pinggang (Warna Merah)", f"Irisan merah menyoroti pengeluaran yang paling banyak dipangkas. Saat ekonomi sulit, pos-pos inilah yang pertama dikorbankan. Yang terdalam: <b>{turun_1['Komoditas']}</b> ({fmt_id(turun_1['Pertumbuhan (%)'], 1)}%).")

# Komoditas yang paling naik & paling turun (hanya Top 5/10)
st.markdown("#### 📊 Siapa yang Naik, Siapa yang Turun?")
n_g = st.radio("Tampilkan komoditas teratas", [5, 10], format_func=lambda n: f"Top {n}", horizontal=True, key="top_komoditas")
cg1, cg2 = st.columns(2)
with cg1:
    chart_header(f"Top {n_g} Paling Meroket", "Pertumbuhan pengeluaran Maret 2024 ke Maret 2025.")
    naik = df_g.nlargest(n_g, 'Pertumbuhan (%)')
    f_naik = px.bar(naik, x='Pertumbuhan (%)', y='Komoditas', orientation='h', color_discrete_sequence=[COLOR_AMBER])
    f_naik.update_yaxes(autorange='reversed', title='')
    f_naik.update_layout(separators=",.", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(tema(f_naik), use_container_width=True)
with cg2:
    chart_header(f"Top {n_g} Paling Dipangkas", "Komoditas dengan pertumbuhan terendah (atau penurunan terdalam).")
    turun = df_g.nsmallest(n_g, 'Pertumbuhan (%)')
    f_turun = px.bar(turun, x='Pertumbuhan (%)', y='Komoditas', orientation='h', color_discrete_sequence=['#b7160e'])
    f_turun.update_yaxes(autorange='reversed', title='')
    f_turun.update_layout(separators=",.", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(tema(f_turun), use_container_width=True)

st.divider()

# ---------------------------------------------------------------------
# BAB 4: PROFIL MULTIDIMENSI (Syarat UAS Visualisasi Data Multivariat)
# ---------------------------------------------------------------------
html('<div id="bab-4"></div>')
bab("Bab 4")
st.markdown("### 4. Membedah Profil Kesejahteraan Multidimensi (34 Provinsi)")
st.write("Kesejahteraan tidak hanya diukur dari uang. Mari kita lihat 8 dimensi kehidupan dari 34 Provinsi di Indonesia.")

# FITUR LINKING: Dropdown untuk menyorot (Highlight) Provinsi tertentu di semua grafik
provinsi_terpilih = st.selectbox("🎯 Sorot (Highlight) Provinsi:", options=df_multi['Provinsi'].tolist(), index=10)

# 1. PARALLEL COORDINATES (Brushing Technique)
st.markdown("#### A. Jejaring Indikator (Parallel Coordinates)")
st.write("💡 *Tip Interaksi (Brushing):* Klik dan seret (drag) kursor Anda pada garis sumbu vertikal di bawah ini untuk memfilter (brushing) rentang nilai tertentu. Satu garis = satu provinsi; garis gelap adalah provinsi yang Anda sorot.")

kolom_numerik = df_multi.select_dtypes(include=[np.number]).columns.tolist()
# Membuat kolom penanda warna (1 untuk provinsi terpilih, 0 untuk lainnya)
df_multi['Color_Flag'] = np.where(df_multi['Provinsi'] == provinsi_terpilih, 1, 0)

fig_par = px.parallel_coordinates(
    df_multi, dimensions=kolom_numerik, color='Color_Flag',
    color_continuous_scale=[[0, COLOR_SAGE], [1, COLOR_DARK]],
    labels={col: col.replace('_', ' ') for col in kolom_numerik}
)
fig_par.update_layout(coloraxis_showscale=False, margin=dict(l=50, r=50, t=30, b=30))
st.plotly_chart(tema(fig_par), use_container_width=True)

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

    # Pencilan = 3 provinsi paling jauh dari pusat peta
    df_pca['Jarak'] = np.sqrt(df_pca['PC1'] ** 2 + df_pca['PC2'] ** 2)
    nama_pencilan = df_pca.nlargest(3, 'Jarak')['Provinsi'].tolist()

    chart_header(f"Varian yang dijelaskan: {pca.explained_variance_ratio_.sum()*100:.1f}%",
                 f"Makin dekat dua titik, makin mirip profilnya. Titik oranye = {provinsi_terpilih}. Label hanya untuk provinsi terpilih dan 3 yang paling terpencil.")
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
    st.markdown(f"#### C. Jaring Laba-laba: **{provinsi_terpilih}**")
    
    # Standarisasi skala 0-100 untuk radar chart agar bentuknya seimbang
    df_radar_norm = (df_multi[kolom_numerik] - df_multi[kolom_numerik].min()) / (df_multi[kolom_numerik].max() - df_multi[kolom_numerik].min()) * 100
    nilai_provinsi = df_radar_norm[df_multi['Provinsi'] == provinsi_terpilih].values[0]
    nilai_nasional = df_radar_norm.mean().values

    chart_header("Profil dibanding rata-rata nasional", "Makin menjauh dari pusat, makin tinggi nilai indikatornya (skala 0-100).")
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=nilai_nasional, theta=kolom_numerik, fill='toself', name='Rata-rata Nasional', marker_color=COLOR_SAGE, opacity=0.5))
    fig_radar.add_trace(go.Scatterpolar(r=nilai_provinsi, theta=kolom_numerik, fill='toself', name=provinsi_terpilih, marker_color=COLOR_DARK))
    
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)), showlegend=True, margin=dict(l=30, r=30, t=30, b=30))
    st.plotly_chart(tema(fig_radar), use_container_width=True)

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

# D. Peringkat antarprovinsi (Top 5/10, provinsi terpilih selalu ikut ditampilkan)
# D. Peringkat antarprovinsi (Hanya Top 5, provinsi terpilih selalu ikut ditampilkan)
st.markdown("#### D. Peringkat Antarprovinsi")
cp1, cp2 = st.columns([2, 1.4])
with cp1:
    indikator_pilih = st.selectbox("Pilih indikator:", kolom_numerik, format_func=lambda c: c.replace('_', ' '))
with cp2:
    urutan = st.radio("Urutan", ["Tertinggi dulu", "Terendah dulu"], horizontal=True)

# Patenkan langsung ke angka 5
top_p = 5 

df_rank = df_multi[['Provinsi', indikator_pilih]].dropna().sort_values(indikator_pilih, ascending=(urutan == "Terendah dulu")).reset_index(drop=True)
df_rank['Peringkat'] = df_rank.index + 1
df_show = df_rank.head(top_p)
if provinsi_terpilih not in df_show['Provinsi'].values:
    df_show = pd.concat([df_show, df_rank[df_rank['Provinsi'] == provinsi_terpilih]])
df_show = df_show.copy()
df_show['Label'] = df_show['Peringkat'].astype(str) + ". " + df_show['Provinsi']
df_show['Status'] = np.where(df_show['Provinsi'] == provinsi_terpilih, 'Disorot', 'Lainnya')
chart_header(f"Top {top_p} Provinsi: {indikator_pilih.replace('_', ' ')}",
             f"Menampilkan {top_p} provinsi teratas. Jika {provinsi_terpilih} tidak masuk, ia ditambahkan di bawah lengkap dengan peringkatnya.")
fig_rank = px.bar(df_show, x=indikator_pilih, y='Label', orientation='h', color='Status',
                  color_discrete_map={'Disorot': COLOR_HIGHLIGHT, 'Lainnya': COLOR_SAGE},
                  labels={indikator_pilih: indikator_pilih.replace('_', ' '), 'Label': ''}, height=90 + 38 * len(df_show))
fig_rank.update_yaxes(autorange='reversed')
fig_rank.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(tema(fig_rank), use_container_width=True)

# 4. KOTAK INTERPRETASI
html(f"""
<div class="card info wide"><div class="card-ico">🔎</div><div>
<div class="card-title">Interpretasi Analisis Multidimensi</div>
<ul>
<li><b>Pengelompokan (Klastering):</b> Pada grafik PCA (kiri), provinsi yang posisinya saling berdekatan menandakan mereka memiliki karakteristik sosial-ekonomi yang sangat mirip di ke-8 variabel tersebut.</li>
<li><b>Pencilan (Outlier):</b> Provinsi yang posisinya terasing/menjauh dari kerumunan utama di grafik PCA adalah provinsi dengan anomali. Pada data ini yang paling terpencil adalah <b>{', '.join(nama_pencilan)}</b>.</li>
<li><b>Profil Radar:</b> Bentuk jaring yang condong mendekati batas luar menandakan performa yang sangat baik di atas rata-rata nasional pada indikator tersebut.</li>
</ul></div></div>
""")

st.markdown("<br><br><center><p style='color: gray;'><i>Sebuah eksplorasi data visual. Dibuat untuk Tugas Akhir Visualisasi Data.</i></p></center>", unsafe_allow_html=True)