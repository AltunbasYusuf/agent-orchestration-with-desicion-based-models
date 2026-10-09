"""
Laya Multilingual Router - Few-Shot Örnek Destekli Test
"""

import time
import laya

print("[1/2] Laya multilingual modeli yükleniyor...")
agent = laya.load("convaiinnovations/laya", subfolder="multilingual")

# JSON Schema formatında tanımlar ve örnek sorular
SCHEMA = {
    "type": "object",
    "properties": {
        "agent": {
            "type": "string",
            "description": "Kullanıcının isteğini yerine getirmeye en uygun ajanı seçin.",
            "enum": [
                "is_akisi_agent",
                "confluence_agent",
                "tfs_git_code_search_agent",
                "grafana_agent",
                "markdown_converter_agent",
            ],
            "criteria": {
                "is_akisi_agent": (
                    "BPMN iş akışları, mobil müşteri onay adımları ve başvuru süreçleri. "
                    "Örnek sorular: Kredi kartı başvuru akışı nasıl çalışır?, Müşteri onay adımları nelerdir?, "
                    "Hesap açılış süreci nasıl ilerler?"
                ),
                "confluence_agent": (
                    "Confluence dokümantasyonu, wiki sayfaları, şirket oryantasyon rehberleri, İK süreçleri, "
                    "yetki ve erişim talepleri, Jira kullanım kılavuzları ve subtask açma. "
                    "Örnek sorular: Yeni başlayan stajyer için hangi erişimleri talep etmem lazım?, "
                    "Jira'da nasıl subtask açarım?, Başlangıç rehber sayfasını confluencetan getir, VPN nasıl kurulur?"
                ),
                "tfs_git_code_search_agent": (
                    "TFS, Git depoları, Azure DevOps, kaynak kod dosyaları arama, repo analizi ve fonksiyon tanımları. "
                    "Örnek sorular: tfsten mcp-atlassian kodunu analiz et, search toolu hangi kod dosyasında?, "
                    "MCP projesindeki kodları özetle."
                ),
                "grafana_agent": (
                    "Grafana panelleri, sunucu metrikleri, performans grafikleri, p95 latency ve sistem izleme. "
                    "Örnek sorular: Backendin p95 grafiğini çek ve yorumla, backend metriklerini grafanadan getir, "
                    "CPU bellek tüketim grafiğini göster."
                ),
                "markdown_converter_agent": (
                    "PDF ve DOCX gibi belge dosyalarını Markdown formatına dönüştürme. "
                    "Örnek sorular: PDF dosyasını markdowna çevir, Word belgesini md formatına dönüştür."
                ),
            },
        }
    },
    "required": ["agent"],
}

TEST_PROMPTS = [
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

print("[2/2] Testler koşturuluyor...\n")
print("-" * 65)

for prompt in TEST_PROMPTS:
    start_time = time.perf_counter()
    result = agent.decide(prompt, SCHEMA)
    latency_ms = (time.perf_counter() - start_time) * 1000

    decision = result.get("agent", {})
    if isinstance(decision, dict):
        selected = decision.get("selection", "Bilinmiyor")
        confidence = decision.get("confidence", 0.0)
    else:
        selected = str(decision)
        confidence = 1.0

    print(f"Prompt  : {prompt}")
    print(f"Agent   : {selected} (güven: {confidence:.2f}) | {latency_ms:.2f} ms")
    print("-" * 65)