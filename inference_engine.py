"""
inference_engine.py
Subsistem: Mesin Inferensi Forward Chaining murni (tanpa Certainty Factor).

Modul ini tidak dipanggil langsung oleh UI. Akses melalui facade.py.
"""

from dataclasses import dataclass, field


@dataclass
class InferenceResult:
    facts: set                                  # fakta gejala awal (Working Memory)
    working_memory: set                         # fakta gejala + fakta turunan (S01-S03)
    fired_rule_ids: list = field(default_factory=list)
    conclusion: str = None                      # kode hasil tertinggi, None bila tidak ada
    log: list = field(default_factory=list)


class ForwardChainingEngine:
    def __init__(self, rules, results):
        self._rules = rules
        self._results = results

    def infer(self, facts):
        """
        Data-driven: tiap iterasi, aturan yang belum terpicu diuji dengan
        premis.issubset(working_memory). Aturan cocok -> terpicu dan kesimpulannya
        ditambahkan ke working memory. Berhenti saat tidak ada aturan baru.
        """
        wm = set(facts)
        fired = []
        log = []
        iterasi = 0
        changed = True

        while changed:
            changed = False
            iterasi += 1
            new_fired = []
            for rule in self._rules:
                if rule["id"] in fired:
                    continue
                if rule["premis"].issubset(wm):
                    fired.append(rule["id"])
                    new_fired.append(rule["id"])
                    wm.add(rule["hasil"])
                    changed = True
            if new_fired:
                log.append(f"Iterasi {iterasi}: terpicu {', '.join(new_fired)}")
            else:
                log.append(f"Iterasi {iterasi}: tidak ada aturan baru, berhenti")

        conclusion = None
        fired_rules = [r for r in self._rules if r["id"] in fired]
        if fired_rules:
            conclusion = max(
                (r["hasil"] for r in fired_rules),
                key=lambda s: self._results[s]["tingkat"],
            )

        return InferenceResult(
            facts=set(facts),
            working_memory=wm,
            fired_rule_ids=fired,
            conclusion=conclusion,
            log=log,
        )
