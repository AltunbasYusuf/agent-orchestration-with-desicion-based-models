PROMPT                                                            | AGENT                     | GÜVEN   | SÜRE
-------------------------------------------------------------------------------------------------------------------
Mevduat hesabı açma akışındaki adımlar neler?                     | is_akisi_agent            | %56.4  | 25.20 ms
Müşteri kredi onayından sonra hangi ekrana yönlendiriliyor?       | is_akisi_agent            | %69.8  | 23.17 ms
Yeni işe başlayan çalışan izin politikasını nereden okuyabilir?   | confluence_agent          | %62.8  | 23.66 ms
Jira üzerinde backlog görevlerini nasıl filtrelerim?              | grafana_agent             | %39.9  | 21.02 ms
Git geçmişinde bu commiti kimin attığını ve fonksiyonu bul        | tfs_git_code_search_agent | %48.2  | 28.98 ms
Azure DevOps reposundaki Dockerfile nerede tutuluyor?             | tfs_git_code_search_agent | %47.9  | 18.33 ms
Canlı ortamdaki veritabanı sorgu sürelerinin grafiğini göster     | grafana_agent             | %88.2  | 20.81 ms
Sunucunun bellek doluluk oranını panellerden kontrol et           | grafana_agent             | %93.7  | 18.61 ms
Elimdeki docx raporu markdown tablosuna çevirmem lazım            | markdown_converter_agent  | %80.9  | 21.54 ms
Taranmış PDF faturayı md formatına dönüştür                       | markdown_converter_agent  | %96.5  | 19.75 ms
-------------------------------------------------------------------------------------------------------------------

Test Cümlesi > yeni başlayanlar için rehber sayfasını getir
-> Ajan  : confluence_agent
-> Güven : %95.49
-> Süre  : 42.21 ms

Test Cümlesi > mobil backend login akışını getir
-> Ajan  : confluence_agent
-> Güven : %46.42
-> Süre  : 44.74 ms

Test Cümlesi > backend p95 grafiğini getir
-> Ajan  : grafana_agent
-> Güven : %93.56
-> Süre  : 42.74 ms

Test Cümlesi > bunu markdowna çevir
-> Ajan  : markdown_converter_agent
-> Güven : %59.27
-> Süre  : 40.36 ms

Test Cümlesi > login fonksiyonu backendde nerede
-> Ajan  : tfs_git_code_search_agent
-> Güven : %46.95
-> Süre  : 40.69 ms



