"""
Multilingual Agent Router (CUDA / RTX 3050 Ti)
Fine-tune gerektirmeden çok dilli (Türkçe & İngilizce) anlamsal yönlendirme.
Von ile aynı mantık: Deterministik, ultra düşük gecikme (<15ms).
"""

import sys
import time
import torch
from sentence_transformers import SentenceTransformer, util

# ---------------------------------------------------------
# 1. Ajan Tanımları (Türkçe)
# ---------------------------------------------------------
AGENTS = {
    "is_akisi_agent": (
        "Mobil iş akışlarını uçtan uca, kanıta dayalı raporlayan iş akışı analiz asistanı. Mobil iş akışları, süreçler, kullanıcı deneyimi, iş analizi ve raporlama konularında sorulara yanıt verir."
    ),
    "confluence_agent": (
        "Confluence wiki ve dokümantasyon asistanı. Confluence sayfaları, makaleler, rehberler, dokümanlar ve wiki içerikleri hakkında sorulara yanıt verir."
    ),
    "tfs_git_code_search_agent": (
        "Azure DevOps'taki kod depolarnda mcp-code-search ile arama yapabilen kod asistanı.Kod arama konularında sorulara yanıt verir."
    ),
    "grafana_agent": (
        "Grafana verilerini doğal dil ile sorgulamak, dashboard ve metriklere hızlı erişmek için MCP tabanlı gözlemleme aracı. Grafana, metrikler, dashboardlar ve gözlemleme konularında sorulara yanıt verir."
    ),
    "markdown_converter_agent": (
        "PDF,Word veya diğer belge formatlarındaki dosyalarınızı Markdown formatına dönüştürür.Belge dönüştürme sorularına yanıt verir."
    ),
}

CHOICE_KEYS = list(AGENTS.keys())
CHOICE_DESCRIPTIONS = list(AGENTS.values())

# ---------------------------------------------------------
# 2. Çok Dilli Model ve GPU Hazırlığı
# ---------------------------------------------------------
# 50+ dili ve özellikle Türkçeyi çok güçlü anlayan hafif (118M) model
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[BİLGİ] Model yükleniyor ({device})...")

model = SentenceTransformer(MODEL_NAME, device=device)

# PERFORMANS OPTİMİZASYONU:
# Ajan açıklamalarının embedding vektörlerini her istekte tekrar hesaplamıyoruz.
# GPU belleğinde önceden encode edip sabit tutuyoruz (Pre-computation).
with torch.no_grad():
    AGENT_EMBEDDINGS = model.encode(
        CHOICE_DESCRIPTIONS,
        convert_to_tensor=True,
        normalize_embeddings=True,
        device=device,
    )

print("[BAŞARILI] Ajan vektörleri GPU VRAM'e sabitlendi.\n")


# ---------------------------------------------------------
# 3. Yönlendirme (Sub-15ms CUDA İşlemi)
# ---------------------------------------------------------
def route(prompt: str) -> dict:
    if device == "cuda":
        torch.cuda.synchronize()

    start_time = time.perf_counter()

    with torch.no_grad():
        # 1. Kullanıcı promptunu encode et
        prompt_embedding = model.encode(
            prompt,
            convert_to_tensor=True,
            normalize_embeddings=True,
            device=device,
        )

        # 2. GPU üzerinde kosinüs benzerliği (Dot-Product Matris Çarpımı)
        scores = util.cos_sim(prompt_embedding, AGENT_EMBEDDINGS)[0]

        # 3. Softmax ile olasılık dağılımı üret
        probabilities = torch.softmax(scores * 10, dim=0)

        # 4. En yüksek skorlu ajanı seç
        best_idx = torch.argmax(scores).item()
        confidence = probabilities[best_idx].item()
        winner = CHOICE_KEYS[best_idx]

    if device == "cuda":
        torch.cuda.synchronize()

    latency_ms = (time.perf_counter() - start_time) * 1000

    prob_dict = {
        CHOICE_KEYS[i]: probabilities[i].item() for i in range(len(CHOICE_KEYS))
    }

    return {
        "choice": winner,
        "confidence": confidence,
        "probabilities": prob_dict,
        "latency_ms": latency_ms,
    }


def show(prompt: str) -> None:
    res = route(prompt)
    print(f"Prompt  : {prompt}")
    print(f"Agent   : {res['choice']} (güven: {res['confidence']:.2f}) | {res['latency_ms']:.2f} ms")

    ranked = sorted(res["probabilities"].items(), key=lambda kv: kv[1], reverse=True)[:3]
    print("İlk 3   : " + ", ".join(f"{k}={v:.2f}" for k, v in ranked))
    print("-" * 60)


# Orijinal Türkçe Test Setimiz
DEMO_PROMPTS = [
    "Kredi kartı başvuru akışı nasıl çalışır?",
    "Yeni başlayanlar için rehber sayfasını confluencetan getir",
    "tfsten mcp-atlassian kodunu analiz et ve anlat",
    "backendin metriklerini grafanadan çek ve yorumla",
    "PDF dosyasını markdowna çevir",
    "mcp semantic searchte search toolu hangi kod dosyasında?",
    "MCP-Atlassian projesindeki tüm kodları analiz et ve özetle.",
    "Backendin p95 grafiğini çek ve yorumla.",
    "Yeni başlayan stajyer için hangi erişimleri talep etmem lazım?",
    "Jira'da nasıl subtask açarım?",
]

if __name__ == "__main__":
    # Isınma (Warmup)
    route("ping")
    print("--- ÇOK DİLLİ TEST BAŞLATILIYOR (FİNE-TUNESUZ) ---\n")
    for p in DEMO_PROMPTS:
        show(p)