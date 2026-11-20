"""
facade.py
Design Pattern: FACADE

StressExpertSystemFacade adalah satu-satunya pintu masuk yang dipakai UI (app.py).
Di baliknya ada subsistem yang disembunyikan dari UI:
  - knowledge_base.py     -> gejala, hasil, aturan, kasus uji
  - inference_engine.py   -> mesin inferensi Forward Chaining

UI tidak perlu tahu cara aturan dicocokkan atau bagaimana data disimpan.
"""

from dataclasses import dataclass, field

import knowledge_base as kb
from inference_engine import ForwardChainingEngine


@dataclass
class AnalysisReport:
    """Laporan hasil analisis yang siap ditampilkan oleh UI."""
    facts: list
    derived_facts: list
    fired_rule_ids: list
    rule_trace: list                      # status tiap aturan (untuk tab Mesin Inferensi)
    log: list
    found: bool                           # False bila tidak ada aturan yang cocok
    code: str = None                      # S01 / S02 / S03
    name: str = None
    summary: str = None
    advice: list = field(default_factory=list)
    color: str = "#1B2A4A"
    message: str = None                   # pesan bila tidak ada aturan cocok


class StressExpertSystemFacade:
    NO_RULE_MESSAGE = "Data gejala belum mencukupi untuk menarik kesimpulan aturan."

    def __init__(self):
        self._engine = ForwardChainingEngine(kb.ATURAN, kb.HASIL)

    # ------------------------------------------------------------------ gejala
    def symptom_groups(self):
        """{kategori: [(kode, teks gejala), ...]} untuk membangun kuesioner."""
        return {
            kategori: [(k, kb.GEJALA[k]) for k in kodes]
            for kategori, kodes in kb.KATEGORI_GEJALA.items()
        }

    def symptom_codes(self):
        return list(kb.GEJALA)

    def symptom_text(self, code):
        return kb.GEJALA[code]

    # ---------------------------------------------------------------- analisis
    def analyze(self, selected_codes):
        """Jalankan seluruh proses: fakta -> forward chaining -> laporan."""
        facts = set(selected_codes) & set(kb.GEJALA)
        res = self._engine.infer(facts)

        trace = []
        for rule in kb.ATURAN:
            matched = rule["id"] in res.fired_rule_ids
            trace.append(
                {
                    "id": rule["id"],
                    "premis": sorted(rule["premis"]),
                    "missing": sorted(rule["premis"] - facts),
                    "matched": matched,
                    "hasil": rule["hasil"],
                    "hasil_nama": kb.HASIL[rule["hasil"]]["nama"],
                }
            )

        base = dict(
            facts=sorted(facts),
            derived_facts=sorted(res.working_memory - facts),
            fired_rule_ids=res.fired_rule_ids,
            rule_trace=trace,
            log=res.log,
        )
        if res.conclusion is None:
            return AnalysisReport(found=False, message=self.NO_RULE_MESSAGE, **base)

        info = kb.HASIL[res.conclusion]
        return AnalysisReport(
            found=True,
            code=res.conclusion,
            name=info["nama"],
            summary=info["ringkasan"],
            advice=list(info["saran"]),
            color=info["warna"],
            **base,
        )

    # ------------------------------------------------------- basis pengetahuan
    def symptom_table(self):
        kat = {k: nama for nama, kodes in kb.KATEGORI_GEJALA.items() for k in kodes}
        return [
            {"kode": k, "kategori": kat[k], "gejala": t, "sumber": kb.SUMBER_GEJALA[k]}
            for k, t in kb.GEJALA.items()
        ]

    def rule_table(self):
        return [
            {
                "id": r["id"],
                "premis": sorted(r["premis"]),
                "hasil": r["hasil"],
                "hasil_nama": kb.HASIL[r["hasil"]]["nama"],
            }
            for r in kb.ATURAN
        ]

    def reference_notes(self):
        return [
            "DASS-21 (Lovibond & Lovibond, 1995), sub-skala Stres: dasar untuk gejala fisik, emosional, dan perilaku.",
            "PSS-10 (Cohen, Kamarck & Mermelstein, 1983): dasar untuk indikator tidak mampu mengendalikan hal penting dan merasa kewalahan.",
            "Pengetahuan berasal dari kajian literatur instrumen tervalidasi, bukan wawancara langsung.",
            "Kombinasi aturan R01-R12 adalah rancangan prototipe akademik dan belum divalidasi secara klinis.",
        ]

    # ------------------------------------------------------------- kasus uji
    def test_cases(self):
        return kb.KASUS_UJI

    def test_case(self, code):
        return next(k for k in kb.KASUS_UJI if k["kode"] == code)

    def run_test_case(self, code):
        return self.analyze(self.test_case(code)["gejala"])

    def validate_all(self):
        rows = []
        for k in kb.KASUS_UJI:
            rep = self.analyze(k["gejala"])
            rows.append(
                {
                    "kode": k["kode"],
                    "nama": k["nama"],
                    "fired": rep.fired_rule_ids,
                    "expected": k["ekspektasi"],
                    "actual": rep.code,
                    "ok": rep.code == k["ekspektasi"],
                }
            )
        return rows
