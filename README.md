# Sistem Pakar Identifikasi Dini Tingkat Stres Mahasiswa
Rule-Based Expert System, Forward Chaining murni (tanpa Certainty Factor). Streamlit.

## Struktur
stres_pakar/
├── app.py              # UI Streamlit (hanya memanggil facade)
├── facade.py           # Pola Facade: satu pintu akses untuk UI
├── inference_engine.py # Mesin inferensi Forward Chaining
├── knowledge_base.py   # Gejala G01-G12, hasil S01-S03, aturan R01-R12, kasus uji
├── requirements.txt
└── .streamlit/config.toml   # tema Biru Navy & Cream

## Menjalankan
    python -m venv venv
    source venv/bin/activate        # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    streamlit run app.py
Buka http://localhost:8501
