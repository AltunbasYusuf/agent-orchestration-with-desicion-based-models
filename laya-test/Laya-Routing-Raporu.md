# Laya LLM Routing Deney Raporu

**Tarih:** 4 Ekim 2026  
**Proje klasörü:** `C:\Users\90536\Desktop\laya-test`  
**Ana dosya:** [`llm-routing.py`](./llm-routing.py)

## 1. Amaç

Bu çalışmanın amacı, gelen bir kullanıcı isteğini analiz ederek isteğin ihtiyaç
duyduğu model yetenek seviyesini belirlemek ve isteği aşağıdaki model
seçeneklerinden birine yönlendirecek bir prototip oluşturmaktır:

| Capability tier | Gerçek model eşlemesi | Kullanım alanı |
|---|---|---|
| `local_fast` | `qwen_3_8` | Basit, kısa ve düşük riskli istekler |
| `general` | `claude_sonnet_5_5` | Özetleme, bağlamdan cevaplama ve rutin kod işleri |
| `advanced` | `gpt_6_luna` | Zor hata ayıklama, log analizi ve mimari |
| `critical` | `gpt_6_1_sol` | Kritik, belirsiz, yüksek riskli veya geniş kapsamlı işler |

## 2. Kullanılan ortam

- Python: `3.11.9`
- Laya: `0.3.24`
- Sanal ortam: `.venv`
- Laya checkpoint'i: `convaiinnovations/laya`
- Kullanılan checkpoint alt klasörü: `multilingual`

Laya başarıyla import edildi ve checkpoint ilk çalıştırmada indirildi.

## 3. İlk yaklaşım

İlk versiyonda Laya'ya doğrudan gerçek model adları kategori olarak verildi:

```python
qwen_3_8
claude_sonnet_5_5
gpt_6_luna
gpt_6_1_sol
```

Bu yaklaşımın problemi, bu isimlerin Laya için gerçek yetenek sınıfları
olmamasıdır. Bunlar yalnızca uygulamaya ait model etiketleridir. Laya'nın
önceden eğitilmiş router modeli bu adları bizim beklediğimiz anlamda bilmez.

## 4. Yapılan düzeltme

Routing kategorileri gerçek model isimlerinden ayrıldı:

```python
MODEL_IDS = {
    "local_fast": "qwen_3_8",
    "general": "claude_sonnet_5_5",
    "advanced": "gpt_6_luna",
    "critical": "gpt_6_1_sol",
}
```

Laya önce yetenek seviyesini seçiyor, uygulama daha sonra bu seviyeyi gerçek
model kimliğine çeviriyor.

Bu ayrımın avantajı:

1. Laya, sağlayıcı/model adlarını ezberlemek yerine isteğin zorluğunu analiz eder.
2. Gerçek model değişiklikleri routing mantığını değiştirmeden yapılabilir.
3. Aynı capability tier farklı bir model sağlayıcısına bağlanabilir.
4. Fallback davranışı açıkça `critical` seviyesine bağlanır.

## 5. Routing mantığı

`route()` fonksiyonu şu akışı kullanır:

1. Kullanıcı isteğini Laya'ya gönderir.
2. Laya bir capability tier ve confidence döndürür.
3. Confidence threshold değerinden düşükse `critical` fallback'i kullanılır.
4. Seçilen tier gerçek model kimliğine çevrilir.

Özet akış:

```text
Kullanıcı isteği
        |
        v
Laya: capability tier + confidence
        |
        v
Threshold kontrolü
        |
        +-- yeterli güven --> seçilen tier
        |
        +-- düşük güven ----> critical fallback
        |
        v
Gerçek model kimliği
```

Varsayılan threshold:

```text
0.5
```

## 6. Dataset

### Türkçe dataset

Toplam **51 örnek**:

- 14 `local_fast`
- 14 `general`
- 12 `advanced`
- 11 `critical`

Örnek kapsamı:

- Basit tanımlar, çeviriler ve kısa kod soruları
- Doküman özetleme ve e-posta düzenleme
- Kubernetes, PostgreSQL, deadlock ve dağıtık sistem analizi
- Bankacılık, sağlık verisi, zero trust ve felaket kurtarma

### İngilizce dataset

Toplam **24 örnek**:

- 6 `local_fast`
- 6 `general`
- 6 `advanced`
- 6 `critical`

İngilizce örnekler, Türkçe dataset ile aynı capability seviyelerini daha
kontrollü ve dengeli biçimde test etmek amacıyla eklendi.

## 7. Benchmark sonuçları

### İngilizce benchmark

Komut:

```powershell
cd C:\Users\90536\Desktop\laya-test
.\.venv\Scripts\python.exe .\llm-routing.py
```

Sonuç:

| Threshold | Doğruluk | Fallback sayısı |
|---:|---:|---:|
| `0.3` | `8/24` | 14 |
| `0.5` | `8/24` | 17 |
| `0.7` | `5/24` | 21 |

### Türkçe benchmark

Komut:

```powershell
.\.venv\Scripts\python.exe .\llm-routing.py --language tr
```

Sonuç:

| Threshold | Doğruluk | Fallback sayısı |
|---:|---:|---:|
| `0.3` | `15/51` | 27 |
| `0.5` | `14/51` | 35 |
| `0.7` | `12/51` | 42 |

Bu iki datasetin örnek sayıları eşit olmadığı için doğruluk oranları doğrudan
tek başına karşılaştırılmamalıdır.

## 8. İnteraktif test

Kendi isteklerini test etmek için:

```powershell
.\.venv\Scripts\python.exe .\llm-routing.py --interactive
```

Belirli bir threshold ile:

```powershell
.\.venv\Scripts\python.exe .\llm-routing.py --interactive --threshold 0.7
```

Örnek istekler:

```text
What is JSON?
Summarize these meeting notes.
Analyze this Kubernetes crash loop.
Design a secure multi-region banking platform.
```

Çıkmak için:

```text
q
```

## 9. Fine-tuning durumu

Datasetin benchmark içinde kullanılması Laya'nın ağırlıklarını değiştirmez.
Mevcut kod:

- Laya'yı yeniden eğitmiyor.
- Datasetten kalıcı olarak öğrenmiyor.
- Sadece beklenen etiket ile Laya'nın tahminini karşılaştırıyor.

Kurulu `laya==0.3.24` paketinde doğrudan model ağırlığı fine-tuning API'si
bulunamadı. Paket daha çok inference, routing, evaluation ve confidence
calibration işlevleri sağlıyor.

Mevcut calibration desteği confidence skorlarını düzeltebilir; ancak bu işlem
model ağırlıklarını değiştiren gerçek fine-tuning değildir.

## 10. Sonuçların değerlendirilmesi

Sistem teknik olarak çalışıyor:

- Laya import ediliyor.
- Checkpoint yükleniyor.
- Türkçe ve İngilizce istekler işleniyor.
- Capability tier seçiliyor.
- Threshold ve fallback uygulanıyor.
- Benchmark sonuçları ölçülüyor.

Buna karşılık mevcut hazır checkpoint'in bu özel dört seviyeli routing görevi
için doğruluğu düşüktür. En iyi ölçülen sonuçlar:

- İngilizce: `8/24`
- Türkçe: `15/51`

Bu sonuçlar, yalnızca datasetin küçük olmasından değil, hazır Laya
checkpoint'inin bizim özel routing tanımlarımıza tam uyumlu olmamasından da
etkileniyor olabilir.

## 11. Mevcut sınırlamalar

1. Sistem şu anda gerçek Qwen, Claude veya GPT endpoint'lerine istek göndermiyor.
   Yalnızca hangi modelin seçileceğini döndürüyor.
2. Model adları örnek uygulama kimlikleridir; gerçek API sağlayıcı yapılandırması
   henüz eklenmemiştir.
3. 24 ve 51 örnek, üretim routing sistemi için yeterli değildir.
4. Datasetin beklenen etiketleri insan tarafından atanmıştır; etiket tutarlılığı
   ayrıca gözden geçirilmelidir.
5. Tek bir sabit threshold bütün model kategorileri için ideal olmayabilir.
6. İngilizce ve Türkçe datasetlerin boyutları eşit değildir.

## 12. Önerilen sonraki adımlar

### Kısa vadede

1. İngilizce ve Türkçe datasetleri eşitlemek.
2. Her tier için en az 50-100 örnek hazırlamak.
3. Eğitim/validasyon/test ayrımı yapmak.
4. Laya'nın ham confidence ve olasılık çıktılarını daha ayrıntılı kaydetmek.
5. Capability tier bazında precision, recall ve confusion matrix hesaplamak.

### Orta vadede

1. Laya confidence calibration özelliğini test etmek.
2. Basit bir supervised classifier ile Laya'yı karşılaştırmak.
3. Gerçek model adapter katmanı eklemek:

```python
MODEL_HANDLERS = {
    "qwen_3_8": call_qwen,
    "claude_sonnet_5_5": call_claude,
    "gpt_6_luna": call_gpt_luna,
    "gpt_6_1_sol": call_gpt_sol,
}
```

4. Gerçek kullanıcı isteklerinden anonimleştirilmiş test verisi toplamak.
5. Kritik istekler için yalnızca confidence değil, kural tabanlı güvenlik
   override'ları da eklemek.

## 13. Genel karar

Mevcut çalışma, Laya'nın bir LLM cevaplayıcısı değil, **önceden eğitilmiş bir
typed decision/router modeli** olarak nasıl kullanılacağını göstermektedir.

Prototip ve ölçüm altyapısı çalışır durumdadır. Ancak üretim kullanımından önce
dataset kalitesi, model seçimi, calibration ve gerçek model API adapter'ları
üzerinde ek çalışma gereklidir.
