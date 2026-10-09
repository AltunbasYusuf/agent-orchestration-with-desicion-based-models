"""
SetFit Fine-Tuned Model Canlı Çıkarım ve Doğruluk Testi
- Kaydedilen yerel modeli yükler (yeniden eğitim yapmaz).
- Eğitim setinde bulunmayan yeni/farklı Türkçe promptlarla test eder.
- Milisaniye bazında CUDA gecikmesini (latency) ve güven skorunu ölçer.
- İnteraktif terminal modu içerir.
"""

import time
import torch
from setfit import SetFitModel

MODEL_PATH = "./fine_tuned_agent_router"

# 1. Donanım belirleme ve modeli yükleme
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[*] Model '{MODEL_PATH}' dizininden '{device}' aygıtına yükleniyor...")

model = SetFitModel.from_pretrained(MODEL_PATH)
model.to(device)
print("[+] Model hazır!\n")

# 2. Eğitim setinde HİÇ YER ALMAYAN yeni test promptları
UNSEEN_TEST_PROMPTS = [
    # is_akisi_agent testleri (farklı ifadeler)
    "Mevduat hesabı açma akışındaki adımlar neler?",
    "Müşteri kredi onayından sonra hangi ekrana yönlendiriliyor?",
    
    # confluence_agent testleri
    "Yeni işe başlayan çalışan izin politikasını nereden okuyabilir?",
    "Jira üzerinde backlog görevlerini nasıl filtrelerim?",
    
    # tfs_git_code_search_agent testleri
    "Git geçmişinde bu commiti kimin attığını ve fonksiyonu bul",
    "Azure DevOps reposundaki Dockerfile nerede tutuluyor?",
    
    # grafana_agent testleri
    "Canlı ortamdaki veritabanı sorgu sürelerinin grafiğini göster",
    "Sunucunun bellek doluluk oranını panellerden kontrol et",
    
    # markdown_converter_agent testleri
    "Elimdeki docx raporu markdown tablosuna çevirmem lazım",
    "Taranmış PDF faturayı md formatına dönüştür",
]


def predict_route(text: str) -> tuple[str, float, float]:
    """
    Verilen metin için ajanı, güven skorunu ve çıkarım süresini hesaplar.
    CUDA senkronizasyonu ile gerçek donanım gecikmesini ölçer.
    """
    if device == "cuda":
        torch.cuda.synchronize()
    start_time = time.perf_counter()

    # Tahmin ve olasılık dağılımı
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]

    if device == "cuda":
        torch.cuda.synchronize()
    latency_ms = (time.perf_counter() - start_time) * 1000

    # En yüksek sınıf olasılığını float olarak al
    confidence = (
        torch.max(probabilities).item()
        if isinstance(probabilities, torch.Tensor)
        else float(max(probabilities))
    )

    return prediction, confidence, latency_ms


# 3. GPU Isınma (Warmup) — İlk çıkarımdaki CUDA başlatma gecikmesini eler
if device == "cuda":
    torch.cuda.synchronize()
model.predict(["warmup"])

# 4. Otomasyon Test Döngüsü
print(f"{'PROMPT':<65} | {'AGENT':<25} | {'GÜVEN':<7} | {'SÜRE'}")
print("-" * 115)

for prompt in UNSEEN_TEST_PROMPTS:
    agent, conf, lat = predict_route(prompt)
    print(f"{prompt:<65} | {agent:<25} | %{conf * 100:<5.1f} | {lat:5.2f} ms")

print("-" * 115)

# 5. İnteraktif Kullanıcı Test Modu
print("\n[?] Kendi cümlelerini test edebilirsin (Çıkmak için 'q' yaz):")
while True:
    try:
        user_input = input("\nTest Cümlesi > ").strip()
        if not user_input or user_input.lower() == "q":
            print("Test sonlandırıldı.")
            break
        agent, conf, lat = predict_route(user_input)
        print(f"-> Ajan  : {agent}")
        print(f"-> Güven : %{conf * 100:.2f}")
        print(f"-> Süre  : {lat:.2f} ms")
    except (KeyboardInterrupt, EOFError):
        print("\nÇıkış yapıldı.")
        break