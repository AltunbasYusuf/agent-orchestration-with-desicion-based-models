"""
SetFit ile Türkçe Kurumsal Ajan Yönlendirici (CUDA / RTX 3050)
Hedef: Sub-20ms gecikme ve %100'e yakın doğruluk.
"""

import time
import torch
from datasets import Dataset
from setfit import SetFitModel, Trainer, TrainingArguments

# ---------------------------------------------------------
# 1. 25 Örnekli Çekirdek Kurumsal Veri Seti
# ---------------------------------------------------------
LABELS = [
    "is_akisi_agent",
    "confluence_agent",
    "tfs_git_code_search_agent",
    "grafana_agent",
    "markdown_converter_agent",
]

train_data = {
    "text": [
        # is_akisi_agent
        "Kredi kartı başvuru akışı nasıl çalışır?",
        "Müşteri onay süreç adımlarını listele",
        "Şube kredi onay iş akışı şeması nedir?",
        "Mobil onboarding sürecindeki işlem adımları",
        "Hesap açılış iş akışı ve müşteri doğrulama basamakları",
        # confluence_agent
        "Yeni başlayanlar için rehber sayfasını confluencetan getir",
        "Yeni başlayan stajyer için hangi erişimleri talep etmem lazım?",
        "Jira'da nasıl subtask açarım?",
        "VPN kurulum kılavuzu wiki linki nerede?",
        "Şirket el kitabındaki izin ve tatil politikasını aç",
        # tfs_git_code_search_agent
        "tfsten mcp-atlassian kodunu analiz et ve anlat",
        "mcp semantic searchte search toolu hangi kod dosyasında?",
        "MCP-Atlassian projesindeki tüm kodları analiz et ve özetle.",
        "Backend repo içindeki auth middleware dosyasını bul",
        "Git deposunda bu fonksiyon nerede tanımlanmış?",
        # grafana_agent
        "backendin metriklerini grafanadan çek ve yorumla",
        "Backendin p95 grafiğini çek ve yorumla.",
        "Pod CPU ve bellek tüketim alarmı metrikleri",
        "Son 1 saatin hata oranları grafana dashboardu",
        "Sunucu gecikme ve latency grafiklerini ekrana getir",
        # markdown_converter_agent
        "PDF dosyasını markdowna çevir",
        "Word DOCX sözleşmeyi md formatına dönüştür",
        "Taranmış belgeyi markdown tablosu yap",
        "PDF formatındaki kılavuzu md yap",
        "Şu doküman dosyasını markdown haline getir",
    ],
    "label": [
        0, 0, 0, 0, 0,  # is_akisi
        1, 1, 1, 1, 1,  # confluence
        2, 2, 2, 2, 2,  # tfs
        3, 3, 3, 3, 3,  # grafana
        4, 4, 4, 4, 4,  # markdown
    ],
}

dataset = Dataset.from_dict(train_data)

# ---------------------------------------------------------
# 2. Hızlı ve Çok Dilli Temel Model
# ---------------------------------------------------------
print("[1/3] Temel model yükleniyor...")
device = "cuda" if torch.cuda.is_available() else "cpu"

model = SetFitModel.from_pretrained(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    labels=LABELS,
)
model.to(device)

# ---------------------------------------------------------
# 3. RTX 3050 Üzerinde Hızlı Eğitim (~20-30 saniye)
# ---------------------------------------------------------
print(f"[2/3] Model '{device}' üzerinde eğitiliyor...")
args = TrainingArguments(
    batch_size=8,
    num_epochs=2,
    num_iterations=20,
    show_progress_bar=True,
)

trainer = Trainer(
    model=model,
    train_dataset=dataset,
    args=args,
)

trainer.train()

# Eğitilen modeli yerel klasöre kaydet
model.save_pretrained("./fine_tuned_agent_router")
print("[BAŞARILI] Model eğitildi ve './fine_tuned_agent_router' dizinine kaydedildi.\n")

# ---------------------------------------------------------
# 4. Doğruluk ve Gecikme Testi
# ---------------------------------------------------------
print("[3/3] Test seti koşturuluyor...\n")

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

# GPU Isınma (Warmup)
if device == "cuda":
    torch.cuda.synchronize()
model.predict(["ping"])

for p in DEMO_PROMPTS:
    if device == "cuda":
        torch.cuda.synchronize()
    start = time.perf_counter()

    pred = model.predict([p])[0]
    probs = model.predict_proba([p])[0]

    if device == "cuda":
        torch.cuda.synchronize()
    latency_ms = (time.perf_counter() - start) * 1000

    best_prob = torch.max(probs).item() if isinstance(probs, torch.Tensor) else max(probs)
    print(f"Prompt  : {p}")
    print(f"Agent   : {pred} (güven: {best_prob:.2f}) | {latency_ms:.2f} ms")
    print("-" * 60)