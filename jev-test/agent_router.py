"""
Agent router (dry-run): shows which of 5 agents a request would be routed to.
Only Jev (TypeSafe System One) is called, for classification. No agent is executed.

Setup:
    pip install requests python-dotenv
    .env:
        JEV_API_KEY=...
        JEV_BASE_URL=https://api.typesafe.ai   # optional, this is the default
Run:
    python agent_router.py                 # interactive
    python agent_router.py "your prompt"   # single prompt
    python agent_router.py --demo          # run built-in sample prompts
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
JEV_MODEL = "jev-1.13.0"

# agent -> when it should be picked (edit these descriptions to tune routing)
AGENTS = {
    "is_akisi_agent": "Mobil iş akışlarını uçtan uca, kanıta dayalı raporlayan iş akışı analiz asistanı. Mobil iş akışları, süreçler, kullanıcı deneyimi, iş analizi ve raporlama konularında sorulara yanıt verir.",
    "confluence_agent": "Confluence wiki ve dokümantasyon asistanı. Confluence sayfaları, makaleler, rehberler, dokümanlar ve wiki içerikleri hakkında sorulara yanıt verir.",
    "tfs_git_code_search_agent": "Azure DevOps'taki kod depolarnda mcp-code-search ile arama yapabilen kod asistanı.Kod arama konularında sorulara yanıt verir.",
    "grafana_agent": "Grafana verilerini doğal dil ile sorgulamak, dashboard ve metriklere hızlı erişmek için MCP tabanlı gözlemleme aracı. Grafana, metrikler, dashboardlar ve gözlemleme konularında sorulara yanıt verir.",
    "markdown_converter_agent": "PDF,Word veya diğer belge formatlarındaki dosyalarınızı Markdown formatına dönüştürür.Belge dönüştürme sorularına yanıt verir.",
}

QUESTION = {
    "type": "choice",
    "instructions": "Choose the agent best suited to handle the user's request.",
    "criteria": AGENTS,
}

RETRY_STATUS = {429, 502, 503, 504, 529}
MAX_RETRIES = 5


def route(prompt: str) -> dict:
    for attempt in range(MAX_RETRIES + 1):
        r = requests.post(
            f"{BASE_URL}/v1/systemone",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": JEV_MODEL, "state": prompt, "questions": {"agent": QUESTION}},
            timeout=30,
        )
        if r.ok:
            return r.json()["answers"]["agent"]
        if r.status_code in RETRY_STATUS and attempt < MAX_RETRIES:
            wait = 2 ** attempt
            print(f"[retry] {r.status_code}, waiting {wait}s...", file=sys.stderr)
            time.sleep(wait)
            continue
        raise RuntimeError(f"{r.status_code}: {r.text}")


def show(prompt: str) -> None:
    ans = route(prompt)
    print(f"\nPrompt : {prompt}")
    print(f"Agent  : {ans['choice']}  (confidence {ans['confidence']:.2f})")
    ranked = sorted(ans["probabilities"].items(), key=lambda kv: kv[1], reverse=True)
    print("Probs  : " + ", ".join(f"{k}={v:.2f}" for k, v in ranked))


# expected agent in the comment
DEMO_PROMPTS = [
    "Kredi kartı başvuru akışı nasıl çalışır?",         
    "Yeni başlayanlar için rehber sayfasını confluencetan getir",           
    "tfsten mcp-atlassian kodunu analiz et ve anlat",  
    "backendin metriklerini grafanadan çek ve yorumla",                              
    "PDF dosyasını markdowna çevir",  
    "mcp semantic searchte search toolu hangi kod dosyasında?",  
    "MCP-Atlassian projesindeki tüm kodları analiz et ve özetle.",            
    "Backendin p95 grafiğini çek ve yorumla.",         
    "Türkiye'nin başkenti neresi?",                                
    "Bugün hava nasıl?",                               
    "Yeni başlayan stajyer için hangi erişimleri talep etmem lazım?",                       
    "Jira'da nasıl subtask açarım?", 
]

if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--demo"]:
        for p in DEMO_PROMPTS:
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