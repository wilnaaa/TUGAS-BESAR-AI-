"""
knowledge_base.py
Basis Pengetahuan Sistem Pakar Identifikasi Dini Tingkat Stres Mahasiswa.

Sumber pengetahuan: diadaptasi dari indikator instrumen psikologi tervalidasi
DASS-21 (sub-skala Stres) dan PSS-10 (Perceived Stress Scale), bukan dari
wawancara langsung dengan pakar.
"""

# ---------------------------------------------------------------------------
# 1. GEJALA (G01 - G12) dalam 4 kategori
# ---------------------------------------------------------------------------
KATEGORI_GEJALA = {
    "Gejala Fisik": ["G01", "G02", "G03"],
    "Gejala Emosional": ["G04", "G05", "G06"],
    "Gejala Perilaku": ["G07", "G08", "G09"],
    "Gejala Akademik": ["G10", "G11", "G12"],
}

GEJALA = {
    "G01": "Sulit tidur atau gangguan pola tidur akibat memikirkan tugas/ujian",
    "G02": "Sering mengalami sakit kepala, tegang otot leher/bahu, atau nyeri lambung",
    "G03": "Mudah merasa lelah secara fisik meskipun aktivitas tidak berat",
    "G04": "Merasa cemas, gelisah, atau panik berlebihan menjelang deadline/ujian",
    "G05": "Mudah marah, tersinggung, atau mengalami perubahan suasana hati (mood swing)",
    "G06": "Merasa tidak mampu mengendalikan hal-hal penting dalam perkuliahan (indikator PSS-10)",
    "G07": "Menunda-nunda pengerjaan tugas (procrastination) karena merasa terbebani",
    "G08": "Menarik diri dari pergaulan, teman kampus, atau organisasi",
    "G09": "Perubahan pola makan drastis (hilang nafsu makan atau makan berlebih)",
    "G10": "Sulit berkonsentrasi saat dosen menjelaskan atau saat belajar mandiri",
    "G11": "Merasa kewalahan dengan tumpukan tugas, praktikum, dan jadwal kuliah",
    "G12": "Kehilangan motivasi belajar dan menurunnya minat menyelesaikan studi",
}

# Referensi instrumen yang menjadi dasar adaptasi tiap gejala
SUMBER_GEJALA = {
    "G01": "DASS-21 (Stres)",
    "G02": "DASS-21 (Stres)",
    "G03": "DASS-21 (Stres)",
    "G04": "DASS-21 (Stres)",
    "G05": "DASS-21 (Stres)",
    "G06": "PSS-10",
    "G07": "Adaptasi PSS-10",
    "G08": "Adaptasi DASS-21",
    "G09": "Adaptasi DASS-21",
    "G10": "Adaptasi PSS-10",
    "G11": "PSS-10",
    "G12": "Adaptasi PSS-10",
}

# ---------------------------------------------------------------------------
# 2. HASIL / KESIMPULAN (S01 - S03)
# ---------------------------------------------------------------------------
HASIL = {
    "S01": {
        "nama": "Stres Rendah",
        "tingkat": 1,
        "warna": "#3E7C59",
        "ringkasan": (
            "Terdapat beberapa indikator stres ringan. Kondisi ini masih wajar "
            "dalam dinamika perkuliahan dan dapat dikelola secara mandiri."
        ),
        "saran": [
            "Susun jadwal belajar mingguan dan tetapkan tenggat internal sebelum deadline asli.",
            "Pecah tugas besar menjadi bagian kecil agar terasa lebih ringan.",
            "Jaga ritme istirahat: tidur 7-8 jam dan beri jeda singkat saat belajar.",
            "Sisihkan waktu untuk aktivitas santai atau olahraga ringan secara rutin.",
        ],
    },
    "S02": {
        "nama": "Stres Sedang",
        "tingkat": 2,
        "warna": "#B7791F",
        "ringkasan": (
            "Terdapat kombinasi indikator yang menunjukkan tekanan akademik "
            "sedang. Perlu perhatian agar tidak berkembang menjadi stres tinggi."
        ),
        "saran": [
            "Latih teknik relaksasi: pernapasan 4-7-8, peregangan, atau meditasi singkat 5-10 menit.",
            "Terapkan skala prioritas tugas (misalnya matriks penting-mendesak).",
            "Ceritakan beban Anda kepada teman, keluarga, atau kelompok belajar (peer support).",
            "Batasi begadang dan kurangi kafein berlebih.",
        ],
    },
    "S03": {
        "nama": "Stres Tinggi",
        "tingkat": 3,
        "warna": "#A63D40",
        "ringkasan": (
            "Terdapat banyak indikator yang saling menguatkan pada aspek fisik, "
            "emosional, perilaku, dan akademik. Disarankan segera mencari dukungan."
        ),
        "saran": [
            "Kurangi beban sementara: diskusikan perpanjangan tenggat atau penyesuaian beban studi dengan dosen/dosen wali.",
            "Hubungi layanan konseling kampus untuk pendampingan lebih lanjut.",
            "Pertimbangkan berkonsultasi dengan psikolog atau tenaga kesehatan profesional.",
            "Jangan menghadapi sendirian: libatkan orang terdekat yang dipercaya.",
        ],
    },
}

# ---------------------------------------------------------------------------
# 3. BASIS ATURAN (R01 - R12): IF premis THEN kesimpulan
#    premis disimpan sebagai frozenset agar cocok dengan premis.issubset(fakta)
# ---------------------------------------------------------------------------
ATURAN = [
    # --- Stres Rendah (S01)
    {"id": "R01", "premis": frozenset({"G03", "G10"}), "hasil": "S01"},
    {"id": "R02", "premis": frozenset({"G01", "G07"}), "hasil": "S01"},
    {"id": "R03", "premis": frozenset({"G03", "G09"}), "hasil": "S01"},
    # --- Stres Sedang (S02)
    {"id": "R04", "premis": frozenset({"G01", "G04", "G07"}), "hasil": "S02"},
    {"id": "R05", "premis": frozenset({"G02", "G05", "G10"}), "hasil": "S02"},
    {"id": "R06", "premis": frozenset({"G04", "G07", "G11"}), "hasil": "S02"},
    {"id": "R07", "premis": frozenset({"G03", "G05", "G08", "G10"}), "hasil": "S02"},
    # --- Stres Tinggi (S03)
    {"id": "R08", "premis": frozenset({"G01", "G04", "G06", "G11"}), "hasil": "S03"},
    {"id": "R09", "premis": frozenset({"G04", "G06", "G11", "G12"}), "hasil": "S03"},
    {"id": "R10", "premis": frozenset({"G01", "G02", "G05", "G08", "G12"}), "hasil": "S03"},
    {"id": "R11", "premis": frozenset({"G06", "G08", "G10", "G11", "G12"}), "hasil": "S03"},
    {"id": "R12", "premis": frozenset({"G01", "G04", "G05", "G11", "G12"}), "hasil": "S03"},
]

# ---------------------------------------------------------------------------
# 4. KASUS UJI (Test Cases) untuk simulasi validasi
# ---------------------------------------------------------------------------
KASUS_UJI = [
    {
        "kode": "T1",
        "nama": "Kasus Mahasiswa Akhir",
        "deskripsi": (
            "Mahasiswa tingkat akhir yang sedang mengerjakan skripsi: sulit tidur, "
            "cemas menjelang sidang, merasa tidak mampu mengendalikan progres, "
            "kewalahan, dan kehilangan motivasi."
        ),
        "gejala": ["G01", "G02", "G04", "G06", "G07", "G10", "G11", "G12"],
        "ekspektasi": "S03",
    },
    {
        "kode": "T2",
        "nama": "Kasus Maba Adaptasi",
        "deskripsi": (
            "Mahasiswa baru yang masih beradaptasi: cemas, menunda tugas, mulai "
            "menarik diri, dan merasa kewalahan dengan jadwal kuliah."
        ),
        "gejala": ["G04", "G07", "G08", "G11"],
        "ekspektasi": "S02",
    },
    {
        "kode": "T3",
        "nama": "Kasus Normal",
        "deskripsi": (
            "Mahasiswa dengan dinamika kuliah biasa: sesekali lelah dan agak "
            "sulit berkonsentrasi."
        ),
        "gejala": ["G03", "G10"],
        "ekspektasi": "S01",
    },
    {
        "kode": "T4",
        "nama": "Kasus Data Tidak Cukup",
        "deskripsi": (
            "Hanya satu gejala terpilih (mudah marah) sehingga tidak ada aturan "
            "yang terpenuhi."
        ),
        "gejala": ["G05"],
        "ekspektasi": None,
    },
]
