"""
app.py
Antarmuka Streamlit. Seluruh logika diakses lewat StressExpertSystemFacade
(lihat facade.py). File ini tidak mengimpor knowledge_base maupun inference_engine.

Jalankan:  streamlit run app.py
"""

import html

import streamlit as st

from facade import StressExpertSystemFacade

st.set_page_config(
    page_title="Stres Mahasiswa",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_resource
def get_facade():
    return StressExpertSystemFacade()


sistem = get_facade()

NAVY, NAVY_HOVER, TEXT = "#1B2A4A", "#2C4270", "#10192B"
CREAM, CREAM_SOFT, BORDER = "#FDFBF7", "#F2ECE1", "#D8CFC0"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
html, body, .stApp, .stMarkdown, button, input {{ font-family: 'Plus Jakarta Sans', sans-serif !important; }}
.stApp {{ background: {CREAM}; color: {TEXT}; }}
.block-container {{ max-width: 1100px; padding-top: 2rem; }}
header[data-testid="stHeader"] {{ background: transparent; }}
section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {{ display: none; }}
h1, h2, h3, h4, p, label, li, span {{ color: {TEXT}; }}

.judul {{ font-size: 1.7rem; font-weight: 700; color: {NAVY}; margin-bottom: 2px; }}
.sub {{ color: #5B6275; margin-bottom: 18px; }}

.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BORDER}; }}
.stTabs [data-baseweb="tab"] {{ padding: 8px 16px; }}
.stTabs [data-baseweb="tab"] p {{ font-weight: 600; }}
.stTabs [aria-selected="true"] p {{ color: {NAVY}; }}
.stTabs [data-baseweb="tab-highlight"] {{ background-color: {NAVY}; }}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {CREAM_SOFT}; border: 1px solid {BORDER} !important; border-radius: 12px;
}}
.kat {{ font-weight: 700; color: {NAVY}; margin-bottom: 6px; }}

.stButton > button {{
    background: {NAVY}; color: {CREAM}; border: none; border-radius: 8px;
    font-weight: 600; padding: 0.5rem 1.2rem;
}}
.stButton > button p {{ color: {CREAM} !important; }}
.stButton > button:hover {{ background: {NAVY_HOVER}; color: {CREAM}; }}

.hasil {{
    background: {CREAM_SOFT}; border: 1px solid {BORDER}; border-left: 8px solid var(--c);
    border-radius: 12px; padding: 18px 22px; margin-top: 8px;
}}
.hasil .kode {{ font-size: 0.78rem; font-weight: 700; color: var(--c); }}
.hasil .nama {{ font-size: 1.6rem; font-weight: 700; margin: 0 0 6px 0; }}
.hasil ul {{ margin: 6px 0 0 0; padding-left: 20px; }}
.catatan {{ font-size: 0.82rem; color: #5B6275; margin-top: 12px; }}
.kosong {{
    background: #FBF1DC; border: 1px solid #E5CE94; border-radius: 12px;
    padding: 14px 18px; margin-top: 8px;
}}
.chip {{
    display: inline-block; background: {NAVY}; color: {CREAM} !important;
    border-radius: 999px; padding: 3px 11px; font-size: 0.8rem; margin: 2px 4px 2px 0;
}}
.chip.turunan {{ background: transparent; color: {NAVY} !important; border: 1.5px solid {NAVY}; }}
table.tbl {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; background: {CREAM}; }}
table.tbl th {{ background: {NAVY}; color: {CREAM}; text-align: left; padding: 8px 12px; }}
table.tbl td {{ padding: 8px 12px; border-bottom: 1px solid {BORDER}; vertical-align: top; }}
table.tbl tr.on td {{ background: #E8F0E6; font-weight: 600; }}
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------ state
def _dipilih():
    return [k for k in sistem.symptom_codes() if st.session_state.get(f"cb_{k}")]


def cb_analisis():
    st.session_state["fakta"] = _dipilih()                         # Working Memory
    st.session_state["laporan"] = sistem.analyze(st.session_state["fakta"])


def cb_reset():
    for k in sistem.symptom_codes():
        st.session_state[f"cb_{k}"] = False
    for key in ("fakta", "laporan", "kasus_aktif"):
        st.session_state.pop(key, None)


def cb_kasus(kode):
    gejala = sistem.test_case(kode)["gejala"]
    for k in sistem.symptom_codes():
        st.session_state[f"cb_{k}"] = k in gejala
    cb_analisis()
    st.session_state["kasus_aktif"] = kode


for _k in sistem.symptom_codes():
    st.session_state.setdefault(f"cb_{_k}", False)


# ---------------------------------------------------------------- helper UI
def tabel(header, baris, aktif=None):
    th = "".join(f"<th>{h}</th>" for h in header)
    tr = ""
    for i, b in enumerate(baris):
        kls = ' class="on"' if aktif and aktif[i] else ""
        tr += f"<tr{kls}>" + "".join(f"<td>{c}</td>" for c in b) + "</tr>"
    st.markdown(f'<table class="tbl"><tr>{th}</tr>{tr}</table>', unsafe_allow_html=True)


def chips(items, kelas=""):
    if not items:
        return "-"
    return "".join(f'<span class="chip {kelas}">{html.escape(i)}</span>' for i in items)


def kartu_hasil(lap, lengkap=True):
    if not lap.found:
        st.markdown(
            f'<div class="kosong"><b>{lap.message}</b><br>'
            "Silakan lengkapi data atau periksa kembali gejala yang dipilih.</div>",
            unsafe_allow_html=True,
        )
        return
    isi = (
        f'<div class="hasil" style="--c:{lap.color}">'
        f'<div class="kode">{lap.code}</div><div class="nama">{lap.name}</div>'
        f"<div>{html.escape(lap.summary)}</div>"
    )
    if lengkap:
        saran = "".join(f"<li>{html.escape(s)}</li>" for s in lap.advice)
        isi += f"<p style='margin:12px 0 0 0'><b>Saran:</b></p><ul>{saran}</ul>"
    isi += f'<div class="catatan">Aturan terpicu: {", ".join(lap.fired_rule_ids)}</div>'
    if lengkap:
        isi += (
            '<div class="catatan">Hasil ini adalah skrining awal non-klinis, bukan diagnosis. '
            "Jika keluhan berlanjut, hubungi konselor kampus atau psikolog.</div>"
        )
    st.markdown(isi + "</div>", unsafe_allow_html=True)


# --------------------------------------------------------------------- judul
st.markdown('<div class="judul">Sistem Pakar Identifikasi Dini Tingkat Stres Mahasiswa</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Pilih gejala yang Anda alami, lalu tekan Analisis.</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Skrining Stres", "Mesin Inferensi", "Basis Pengetahuan", "Uji Validasi"])

# ------------------------------------------------------------------- TAB 1
with tab1:
    kolom = st.columns(4)
    for col, (kategori, gejala) in zip(kolom, sistem.symptom_groups().items()):
        with col.container(border=True):
            st.markdown(f'<div class="kat">{kategori}</div>', unsafe_allow_html=True)
            for kode, teks in gejala:
                st.checkbox(teks, key=f"cb_{kode}")

    b1, b2, _ = st.columns([1.3, 0.7, 4])
    b1.button("Analisis Tingkat Stres", on_click=cb_analisis, use_container_width=True)
    b2.button("Reset", on_click=cb_reset, use_container_width=True)

    lap = st.session_state.get("laporan")
    if lap:
        kartu_hasil(lap)

# ------------------------------------------------------------------- TAB 2
with tab2:
    lap = st.session_state.get("laporan")
    if not lap:
        st.info("Jalankan analisis di tab Skrining Stres terlebih dahulu.")
    else:
        st.markdown("**Fakta di Working Memory**")
        st.markdown(chips(lap.facts), unsafe_allow_html=True)
        st.markdown("**Fakta turunan hasil inferensi**")
        st.markdown(chips(lap.derived_facts, "turunan"), unsafe_allow_html=True)

        st.markdown("&nbsp;", unsafe_allow_html=True)
        st.markdown("**Pencocokan aturan** (aturan terpicu jika semua premis ada di fakta)")
        tabel(
            ["Aturan", "IF", "Status", "THEN"],
            [
                [
                    t["id"],
                    " AND ".join(t["premis"]),
                    "Terpicu" if t["matched"] else "Tidak (kurang " + ", ".join(t["missing"]) + ")",
                    t["hasil"],
                ]
                for t in lap.rule_trace
            ],
            aktif=[t["matched"] for t in lap.rule_trace],
        )
        st.markdown("&nbsp;", unsafe_allow_html=True)
        if lap.found:
            st.markdown(
                f"**Kesimpulan:** {lap.code} ({lap.name}), tingkat tertinggi dari aturan "
                f"{', '.join(lap.fired_rule_ids)}"
            )
        else:
            st.markdown(f"**Kesimpulan:** {lap.message}")

# ------------------------------------------------------------------- TAB 3
with tab3:
    st.markdown("**Daftar Gejala**")
    tabel(
        ["Kode", "Kategori", "Gejala"],
        [[g["kode"], g["kategori"], html.escape(g["gejala"])] for g in sistem.symptom_table()],
    )
    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown("**Tabel Keputusan (Aturan IF-THEN)**")
    tabel(
        ["Aturan", "IF", "THEN"],
        [[r["id"], " AND ".join(r["premis"]), f'{r["hasil"]} ({r["hasil_nama"]})'] for r in sistem.rule_table()],
    )
    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown("**Catatan Referensi**")
    for n in sistem.reference_notes():
        st.markdown(f"- {n}")

# ------------------------------------------------------------------- TAB 4
with tab4:
    st.markdown("Pilih skenario untuk mengisi kuesioner dan menjalankan analisis otomatis.")
    cases = sistem.test_cases()
    for col, k in zip(st.columns(len(cases)), cases):
        col.button(k["nama"], key=f"kasus_{k['kode']}", on_click=cb_kasus, args=(k["kode"],), use_container_width=True)

    aktif = st.session_state.get("kasus_aktif")
    if aktif:
        k = sistem.test_case(aktif)
        st.markdown(f"**{k['nama']}**: {k['deskripsi']}")
        st.markdown(chips(k["gejala"]), unsafe_allow_html=True)
        kartu_hasil(st.session_state["laporan"], lengkap=False)

    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown("**Rekap Validasi**")
    rows = sistem.validate_all()
    tabel(
        ["Kasus", "Aturan terpicu", "Ekspektasi", "Hasil sistem", "Status"],
        [
            [r["nama"], ", ".join(r["fired"]) or "-", r["expected"] or "Tidak ada", r["actual"] or "Tidak ada",
             "Sesuai" if r["ok"] else "Tidak sesuai"]
            for r in rows
        ],
    )
