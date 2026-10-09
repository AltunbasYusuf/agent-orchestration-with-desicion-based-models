# Agent Router Karşılaştırmalı Test Raporu

**Tarih:** 9 Ekim 2026  
**Kapsam:** Von, Laya, JEV ve SetFit tabanlı beş ajanlı yönlendirme yaklaşımları  
**Ajanlar:** `is_akisi_agent`, `confluence_agent`, `tfs_git_code_search_agent`, `grafana_agent`, `markdown_converter_agent`  
**Hedef:** Türkçe isteklerde doğru yönlendirme, out-of-domain (OOD) davranışı ve sub-20 ms gecikme

## 1. Yönetici özeti

Bu testler aynı veri kümesi, aynı donanım ve aynı çıkarım protokolüyle yapılmadığı için sonuçlar doğrudan üretim karşılaştırması olarak değil, yön gösteren bir benchmark olarak okunmalıdır. Buna rağmen mevcut çıktılardan şu sonuçlar desteklenmektedir:

- **SetFit**, görülmemiş Türkçe cümlelerden oluşan kontrollü testte en iyi dengeyi verdi: **9/10 doğru yönlendirme** ve **22.11 ms ortalama gecikme**.
- **Laya**, Türkçe anlamayı iyi sürdürse de **83.15 ms ortalama gecikmeyle** sub-20 ms hedefinden uzakta kaldı. 10 testin 2'sinde yanlış ajan seçti.
- **JEV**, tipik in-domain isteklerde karışık sonuç verdi (**7/10 doğru**); OOD istekleri reddetmek yerine bir ajana yönlendirdi. Bir testte **509,982.76 ms** aykırı gecikme görüldü.
- **Von**, İngilizce testte in-domain istekleri doğru yönlendirdi; ancak OOD sorularını da ajanlara verdi. Türkçe/çok dilli yapılandırmada kalite ve gecikme daha zayıf görünüyor.

**Öneri:** İlk üretim adayı olarak SetFit seçilebilir; ancak doğrudan güven skoruna dayanılmamalıdır. Modelin önüne açık bir **OOD/fallback katmanı**, kalibre edilmiş eşik, düşük marjda netleştirme ve gözlemlenebilirlik eklenmelidir.

## 2. Ölçüm özeti

| Model | Test yapılandırması | Test sayısı | Doğruluk* | Ortalama gecikme | Gözlenen aralık / aykırı değer | OOD davranışı |
|---|---|---:|---:|---:|---|---|
| **SetFit** | Eğitime dahil olmayan 10 Türkçe prompt, yerel fine-tuned model | 10 | **9/10 (%90)** | **22.11 ms** | 18.33–28.98 ms | Ayrı OOD testi yok; düşük skor tek başına reddetme mekanizması değil |
| **Laya** | Multilingual model + schema/few-shot tanımları, 10 Türkçe prompt | 10 | **8/10 (%80)** | **83.15 ms** | 73.18–92.17 ms | Ayrı OOD testi yok |
| **JEV** | `jev-1.13.0`, uzaktaki API, 12 Türkçe prompt | 12 | **7/10 in-domain (%70)** | — | Normal istekler 79.82–83.69 ms; bir istek 509,982.76 ms | OOD soruları fallback olmadan ajanlara dağıtıldı |
| **Von** | İngilizce Von modeli, 12 prompt | 12 | **10/10 in-domain (%100)** | ≈40.41 ms | 31.79–41.52 ms | 2/2 OOD isteği reddedilmedi |

> \* Doğruluk, promptların beklenen ajanları raporlanarak elle belirlenen etiketlere göre hesaplandı. OOD sorularında “doğru” davranış bir iş ajanı değil, `out_of_scope`/fallback döndürmektir. Bu nedenle in-domain ve OOD sonuçları ayrı raporlanmıştır. SetFit ve Laya sonuçlarında ilk 10'lu test seti kullanılmıştır; JEV ve Von için OOD soruları ayrıca değerlendirilmiştir.

## 3. Model bazında bulgular

### 3.1. SetFit

Kaynak: [setfit_agent_router_results.md](setfit-test/setfit_agent_router_results.md), [test_inference.py](setfit-test/test_inference.py), [setfit_train.py](setfit-test/setfit_train.py)

- Test seti eğitim cümlelerinde bulunmayan 10 Türkçe prompttan oluşuyor; bu, aynı cümlelerin tekrarından daha anlamlı bir genelleme ölçümü sağlıyor.
- 10 testin 9'unda beklenen ajan seçildi.
- Tek hata, **“Jira üzerinde backlog görevlerini nasıl filtrelerim?”** cümlesinin `grafana_agent` seçilmesi. Bu hata, modelin Jira/backlog semantiğini gözlemleme alanına yakın gördüğünü gösteriyor.
- Gecikme **18.33–28.98 ms**, ortalama **22.11 ms**. Bu nedenle sonuç **sub-20 ms hedefini ortalama olarak karşılamıyor**, ancak hedefe en yakın yaklaşım.
- Güven skorları daha ayrışmış görünse de bunların olasılık kalibrasyonu ölçülmedi. `%93` güven, otomatik olarak `%93 doğruluk anlamına gelmez`.
- Kodda warm-up ve CUDA senkronizasyonu bulunuyor; bu, ölçümü daha tutarlı hale getiriyor. Buna karşılık yalnızca 10 örnek ve tek proses koşusu üretim performansı için yeterli değildir.

### 3.2. Laya

Kaynak: [laya_agent_router_results.md](laya-test/laya_agent_router_results.md), [Laya-Routing-Raporu.md](laya-test/Laya-Routing-Raporu.md)

- Net anahtar/alan ifadelerinde yüksek güven üretiyor.
- Ortalama gecikme **83.15 ms**; ölçülen tüm istekler 73–92 ms aralığında. Sub-20 ms hedefi karşılanmıyor.
- **“Yeni başlayan stajyer için hangi erişimleri talep etmem lazım?”** için `is_akisi_agent`, **“Jira'da nasıl subtask açarım?”** için `grafana_agent` seçildi. Tanım şemasında bu konuların `confluence_agent` altında açıkça örneklendirilmiş olması, tanım/few-shot bilgisinin tek başına yeterli olmadığını gösteriyor.
- Çıktıların neredeyse tamamında güven `%100` olduğundan güven skorları karar eşiği için kalibre edilmiş kabul edilmemeli.
- Router kodunda OOD eşiği veya fallback akışı yok; düşük marjlı kararlar için uygulama katmanında ek koruma gerekiyor.

### 3.3. JEV

Kaynak: [jev_agent_router_results.md](jev-test/jev_agent_router_results.md), [agent_router.py](jev-test/agent_router.py)

- 12 promptluk sette 10'u in-domain, 2'si OOD olarak değerlendirildi. In-domain sonuç **7/10**.
- Doğru örnekler: Confluence rehberi, Grafana metrikleri, PDF→Markdown, kod arama ve p95 grafiği.
- Hatalı in-domain örnekler:
  - Kredi kartı başvuru akışı → `confluence_agent` yerine `is_akisi_agent` beklenirdi.
  - TFS'ten kod analizi → `grafana_agent` yerine `tfs_git_code_search_agent` beklenirdi.
  - Stajyer erişimleri → `grafana_agent` yerine `confluence_agent` beklenirdi.
- **“Türkiye'nin başkenti neresi?”** ve **“Bugün hava nasıl?”** soruları sırasıyla `confluence_agent` ve `grafana_agent` olarak seçildi. Bu, modelin OOD farkındalığının olmadığını gösteriyor.
- Bir istekte **509,982.76 ms** gecikme kaydedilmiş. Bu değer, kalan 11 isteğin yaklaşık 80 ms civarındaki davranışından tamamen ayrışıyor; ortalama hesaplanırken normal performansı temsil eden bir değer gibi kullanılmamalı. Aykırı değerin ağ, API yeniden denemesi veya servis tarafı kaynaklı olup olmadığı ayrıca loglarla doğrulanmalı.
- Router kodunda `MAX_RETRIES = 5`, 30 saniyelik HTTP timeout ve yeniden deneme bulunuyor. Bu mekanizma dayanıklılığı artırırken tail latency'yi büyütebilir; üretimde toplam deadline/circuit breaker eklenmeli.

### 3.4. Von

Kaynak: [von_agent_router_results.md](von-test/von_agent_router_results.md), [agent_router.py](von-test/agent_router.py), [multilingual_router.py](von-test/multilingual_router.py)

- İngilizce testte 10 in-domain senaryonun tamamı doğru yönlendirilmiş; Türkçe/çok dilli sonuçlar aynı kaliteyi göstermiyor.
- İngilizce ölçümlerde gecikme **31.79–41.52 ms** aralığında. Bu, sub-20 ms hedefinin üzerinde.
- **“What is the capital of Turkey?”** ve **“What is the weather like today?”** soruları OOD olmasına rağmen `confluence_agent` olarak yönlendirildi. Ajan router'daki `CONFIDENCE_THRESHOLD = 0.25` yalnızca düşük güvenli sonuçları reddediyor; bu OOD örneklerinde güven yüksek kaldığı için eşik tek başına yeterli değil.
- `agent_router.py` ile `multilingual_router.py` aynı değerlendirme değildir: ilki Von'un İngilizce ajan tanımları ve eşik mantığını, ikincisi SentenceTransformer tabanlı Türkçe açıklama benzerliğini kullanır. Bu iki yapılandırmanın sonuçları raporda ayrı tutulmalıdır.
- Çok dilli SentenceTransformer router'ında olasılıklar, benzerlik skorlarının `softmax(score * 10)` ile dönüştürülmesiyle üretiliyor. Bu değerler istatistiksel olarak kalibre edilmiş güven olasılıkları değildir.

## 4. Üretim için önerilen karar akışı

1. **Başlangıç modeli:** SetFit'i düşük gecikmeli aday olarak kullanın; model dosyasını sabitleyin ve CPU/GPU sonuçlarını ayrı benchmarklayın.
2. **OOD katmanı:** Model skorundan bağımsız olarak izin verilen alanları kontrol edin. Alan dışı isteklerde `out_of_scope` veya genel asistana yönlendirme yapın.
3. **İki eşikli karar:**
   ```python
   if confidence < 0.60 or (top1_confidence - top2_confidence) < 0.10:
       return "clarification_or_fallback"
   return predicted_agent
   ```
   Bu değerler başlangıç önerisidir; üretime alınmadan doğrulama setinde kalibre edilmelidir.
4. **Benzer alanları ayırın:** Jira/backlog ile Grafana/metrics gibi karışan çiftler için zor-negatif örnekler ekleyin.
5. **Kalibrasyon:** Ayrı bir validation setinde accuracy, macro-F1, confusion matrix, coverage-risk ve Expected Calibration Error (ECE) ölçün.
6. **Gecikme ölçümü:** En az 100–1,000 istek, warm-up sonrası p50/p95/p99, cold start ve eşzamanlı isteklerle raporlanmalı. Ortalama tek başına yeterli değildir.
7. **Dayanıklılık:** JEV gibi uzaktaki servislerde toplam deadline, sınırlı retry, exponential backoff + jitter, circuit breaker ve açık hata/fallback durumu eklenmeli.
8. **Güvenlik ve veri:** Prompt, API anahtarı veya kurum içi içerik loglara yazılmamalı; testlerde model sağlayıcısına veri gönderimi ve saklama politikası ayrıca doğrulanmalı.

## 5. Sonuç

Mevcut küçük örneklem içinde **SetFit en dengeli adaydır**, fakat 22.11 ms ortalama ile sub-20 ms hedefi henüz karşılanmış değildir. **Laya ve Von** in-domain örneklerde bazı güçlü sonuçlar verse de gecikme veya OOD eksikleri nedeniyle doğrudan üretime hazır görünmüyor. **JEV** için özellikle uzak API kaynaklı aykırı gecikme ve OOD reddinin olmaması kritik risklerdir.

Üretim kararı verilmeden önce ortak bir benchmark hazırlanmalı: aynı Türkçe test seti, aynı beklenen etiketler, ayrı OOD seti, tekrarlı gecikme ölçümü ve modelden bağımsız doğruluk/kalibrasyon metrikleri. Bu rapordaki sonuçlar bu ortak benchmarkın yerine değil, onu hazırlamak için başlangıç kanıtı olarak kullanılmalıdır.
