"""
Dry-run LLM router: shows which LLM a request WOULD be routed to.
Only Jev (TypeSafe System One) is called, for classification. No target model is called.

Setup:
    pip install requests python-dotenv
    .env:
        JEV_API_KEY=...
        JEV_BASE_URL=https://api.typesafe.ai   # optional, this is the default
Run:
    python router_dryrun.py                 # interactive
    python router_dryrun.py "your prompt"   # single prompt
    python router_dryrun.py --demo          # run built-in sample prompts
"""
import os
import sys
import time

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_URL = os.environ.get("JEV_BASE_URL", "https://api.typesafe.ai").rstrip("/")
API_KEY = os.environ.get("JEV_API_KEY")
if not API_KEY:
    raise RuntimeError("JEV_API_KEY is not set. Copy .env.example to .env and configure it.")
JEV_MODEL = "jev-latest"

# model -> when it should be picked (edit these descriptions to tune routing)
CRITERIA = {
    "qwen-3.8": "Greetings, small talk, short factual questions, trivial requests that need no depth",
    "gpt-6-luna": "Summarization, translation, rewriting, data extraction, formatting, other quick text transformations",
    "claude-sonnet-5-5": "Everyday coding: writing functions, debugging, explaining or refactoring code; creative writing",
    "gpt-6.1-sol": "Hard math, logic puzzles, proofs, and multi-step analytical reasoning",
    "claude-opus-5-5": "Complex software engineering: system or agent architecture, large multi-file design, long multi-step planning",
}

QUESTION = {
    "type": "choice",
    "instructions": "Choose the LLM best suited to handle the user's request.",
    "criteria": CRITERIA,
}


RETRY_STATUS = {429, 502, 503, 504, 529}
MAX_RETRIES = 5


def route(prompt: str) -> dict:
    for attempt in range(MAX_RETRIES + 1):
        r = requests.post(
            f"{BASE_URL}/v1/systemone",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": JEV_MODEL, "state": prompt, "questions": {"llm": QUESTION}},
            timeout=30,
        )
        if r.ok:
            return r.json()["answers"]["llm"]
        if r.status_code in RETRY_STATUS and attempt < MAX_RETRIES:
            wait = 2 ** attempt  # 1, 2, 4, 8, 16 seconds
            print(f"[retry] {r.status_code}, waiting {wait}s...", file=sys.stderr)
            time.sleep(wait)
            continue
        raise RuntimeError(f"{r.status_code}: {r.text}")


def show(prompt: str) -> None:
    ans = route(prompt)
    print(f"\nPrompt : {prompt}")
    print(f"Routed : {ans['choice']}  (confidence {ans['confidence']:.2f})")
    ranked = sorted(ans["probabilities"].items(), key=lambda kv: kv[1], reverse=True)
    print("Probs  : " + ", ".join(f"{k}={v:.2f}" for k, v in ranked))


DEMO_PROMPTS = [
    "selam nasılsın",
    "Türkiye'nin başkenti neresi?",
    "Bu makaleyi 3 cümlede özetle: ...",
    "Translate this paragraph to German: ...",
    "Python'da bu fonksiyondaki IndexError'ı düzelt: def f(a): return a[len(a)]",
    "Prove that the square root of 2 is irrational.",
    "Bir train'in hızı 60 km/s, diğeri 90 km/s... ne zaman karşılaşırlar?",
    "Design a multi-agent orchestration architecture with a root router and per-department agents.",
    "Write a short story about a lighthouse keeper.",
]

# Bank software company scenarios (expected route in the comment)
BANK_DEMO_PROMPTS = [
    "Merhaba, bugün hangi toplantılarım var?",                                              # qwen
    "IBAN formatı kaç karakterdir?",                                                        # qwen
    "Bu müşteri şikayet e-postasını 3 maddede özetle: ...",                                 # luna
    "Aşağıdaki kredi başvuru metninden ad, TCKN maskesi, gelir ve talep edilen tutarı JSON olarak çıkar: ...",  # luna
    "Release note'u müşteri temsilcilerinin anlayacağı sade bir dile çevir: ...",           # luna
    "Spring Boot servisimde havale endpoint'i bazen NullPointerException veriyor, stack trace: ...",  # sonnet
    "Bu SQL sorgusu hesap hareketleri tablosunda çok yavaş, index önerir misin? SELECT * FROM transactions WHERE ...",  # sonnet
    "Bu Java metodu için JUnit test senaryoları yaz: public BigDecimal calculateInterest(...)",  # sonnet
    "Mobil bankacılık uygulaması için yeni özellik duyuru metni yaz, samimi ama kurumsal olsun.",  # sonnet
    "Aylık %3,5 faizle 24 ay vadeli 250.000 TL kredinin eşit taksitli ödeme planını adım adım hesapla.",  # sol
    "Basel III'e göre bu portföyün risk ağırlıklı varlık hesabını adım adım yap: ...",      # sol
    "Fraud skorlama modelimizde precision-recall dengesini bozmadan false positive oranını nasıl düşürürüz? Matematiksel olarak analiz et.",  # sol
    "Çekirdek bankacılık sistemini monolitten mikroservislere geçirmek için migration mimarisi tasarla; veri tutarlılığı, rollback ve sıfır kesinti gereksinimleri var.",  # opus
    "Departman bazlı agent'lardan oluşan, root orchestrator'lı bir iç operasyon asistanı mimarisi tasarla; KVKK ve audit log gereksinimlerini de kapsasın.",  # opus
    "Event-driven ödeme sistemi için saga pattern ile dağıtık transaction akışını, hata senaryoları ve idempotency dahil uçtan uca planla.",  # opus
]

if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--demo"]:
        for p in DEMO_PROMPTS:
            show(p)
    elif args == ["--bank"]:
        for p in BANK_DEMO_PROMPTS:
            show(p)
    elif args:
        show(" ".join(args))
    else:
        while True:
            try:
                q = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if q:
                show(q)