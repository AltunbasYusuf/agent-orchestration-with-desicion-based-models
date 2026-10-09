# Decision-Based AI Models

Beş kurumsal ajana yönlendirme yapan farklı router yaklaşımlarının karşılaştırması:

- Von
- Laya
- JEV
- SetFit

Benchmark sonuçları için [results.md](results.md) dosyasına bakabilirsiniz.

## Güvenlik

API anahtarları ve yerel yapılandırma dosyaları repoya eklenmemelidir. JEV testi için:

```powershell
Copy-Item jev-test\.env.example jev-test\.env
```

Ardından `jev-test\.env` dosyasındaki `JEV_API_KEY` değerini yerel anahtarınızla doldurun. `.env` dosyaları `.gitignore` tarafından dışlanır.

> Daha önce herhangi bir API anahtarı paylaşılmış veya yanlışlıkla commit edilmişse anahtarı sağlayıcı panelinden iptal edip yenisini üretin. Git geçmişinden silmek, sızmış anahtarı geçersiz kılmaz.

## Proje yapısı

| Dizin | İçerik |
|---|---|
| `jev-test` | JEV API tabanlı agent ve LLM router testleri |
| `laya-test` | Laya multilingual router testi |
| `setfit-test` | SetFit fine-tuning ve görülmemiş Türkçe prompt testi |
| `von-test` | Von ve SentenceTransformer tabanlı router testleri |

Yerel `.venv`, model çıktıları ve training checkpoint'leri GitHub'a eklenmez. Bunlar yeniden üretilebilir yerel artefaktlardır.
