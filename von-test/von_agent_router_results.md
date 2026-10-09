Prompt  : Kredi kartı başvuru akışı nasıl çalışır?
Agent   : confluence_agent (confidence 0.41)
Latency : 509982.76 ms
Probs   : confluence_agent=0.53, grafana_agent=0.21, tfs_git_code_search_agent=0.14, is_akisi_agent=0.08, markdown_converter_agent=0.04

Prompt  : Yeni başlayanlar için rehber sayfasını confluencetan getir
Agent   : confluence_agent (confidence 0.33)
Latency : 80.11 ms
Probs   : confluence_agent=0.47, grafana_agent=0.24, tfs_git_code_search_agent=0.14, is_akisi_agent=0.08, markdown_converter_agent=0.07

Prompt  : tfsten mcp-atlassian kodunu analiz et ve anlat
Agent   : grafana_agent (confidence 0.14)
Latency : 80.61 ms
Probs   : grafana_agent=0.31, tfs_git_code_search_agent=0.30, confluence_agent=0.29, is_akisi_agent=0.09, markdown_converter_agent=0.00

Prompt  : backendin metriklerini grafanadan çek ve yorumla
Agent   : grafana_agent (confidence 0.45)
Latency : 81.29 ms
Probs   : grafana_agent=0.56, confluence_agent=0.30, tfs_git_code_search_agent=0.08, is_akisi_agent=0.04, markdown_converter_agent=0.03

Prompt  : PDF dosyasını markdowna çevir
Agent   : markdown_converter_agent (confidence 0.51)
Latency : 83.69 ms
Probs   : markdown_converter_agent=0.61, confluence_agent=0.11, grafana_agent=0.11, tfs_git_code_search_agent=0.10, is_akisi_agent=0.07

Prompt  : mcp semantic searchte search toolu hangi kod dosyasında?
Agent   : tfs_git_code_search_agent (confidence 0.41)
Latency : 79.82 ms
Probs   : tfs_git_code_search_agent=0.52, grafana_agent=0.27, confluence_agent=0.09, is_akisi_agent=0.06, markdown_converter_agent=0.05

Prompt  : MCP-Atlassian projesindeki tüm kodları analiz et ve özetle.
Agent   : tfs_git_code_search_agent (confidence 0.23)
Latency : 81.13 ms
Probs   : tfs_git_code_search_agent=0.39, grafana_agent=0.36, is_akisi_agent=0.11, confluence_agent=0.09, markdown_converter_agent=0.05

Prompt  : Backendin p95 grafiğini çek ve yorumla.
Agent   : grafana_agent (confidence 0.45)
Latency : 82.32 ms
Probs   : grafana_agent=0.56, tfs_git_code_search_agent=0.16, confluence_agent=0.11, markdown_converter_agent=0.09, is_akisi_agent=0.09

Prompt  : Türkiye'nin başkenti neresi?
Agent   : confluence_agent (confidence 0.57)
Latency : 81.45 ms
Probs   : confluence_agent=0.66, grafana_agent=0.26, tfs_git_code_search_agent=0.05, is_akisi_agent=0.02, markdown_converter_agent=0.01

Prompt  : Bugün hava nasıl?
Agent   : confluence_agent (confidence 0.97)
Latency : 83.32 ms
Probs   : confluence_agent=0.98, grafana_agent=0.02, tfs_git_code_search_agent=0.00, is_akisi_agent=0.00, markdown_converter_agent=0.00

Prompt  : Yeni başlayan stajyer için hangi erişimleri talep etmem lazım?
Agent   : grafana_agent (confidence 0.30)
Latency : 82.03 ms
Probs   : grafana_agent=0.44, confluence_agent=0.24, tfs_git_code_search_agent=0.13, is_akisi_agent=0.10, markdown_converter_agent=0.08

Prompt  : Jira'da nasıl subtask açarım?
Agent   : confluence_agent (confidence 0.56)
Latency : 81.59 ms
Probs   : confluence_agent=0.65, grafana_agent=0.19, tfs_git_code_search_agent=0.13, is_akisi_agent=0.03, markdown_converter_agent=0.01


Prompt  : How does the credit card application workflow work?
Agent   : workflow_agent (confidence: 0.92) | 40.00 ms
Top 3   : workflow_agent=0.94, confluence_agent=0.04, grafana_agent=0.01
------------------------------------------------------------
Prompt  : Get the onboarding guide page from confluence for new starters
Agent   : confluence_agent (confidence: 0.95) | 41.00 ms
Top 3   : confluence_agent=0.96, code_search_agent=0.01, markdown_converter_agent=0.01
------------------------------------------------------------
Prompt  : Analyze and explain the mcp-atlassian code from TFS
Agent   : code_search_agent (confidence: 0.71) | 41.01 ms
Top 3   : code_search_agent=0.76, confluence_agent=0.08, grafana_agent=0.06
------------------------------------------------------------
Prompt  : Fetch and interpret backend metrics from Grafana
Agent   : grafana_agent (confidence: 0.63) | 40.97 ms
Top 3   : grafana_agent=0.70, code_search_agent=0.15, markdown_converter_agent=0.08
------------------------------------------------------------
Prompt  : Convert this PDF file into markdown
Agent   : markdown_converter_agent (confidence: 0.99) | 31.79 ms
Top 3   : markdown_converter_agent=1.00, code_search_agent=0.00, workflow_agent=0.00
------------------------------------------------------------
Prompt  : Which code file contains the search tool in mcp semantic search?
Agent   : code_search_agent (confidence: 0.73) | 41.44 ms
Top 3   : code_search_agent=0.78, confluence_agent=0.17, markdown_converter_agent=0.04
------------------------------------------------------------
Prompt  : Analyze and summarize all the codebase in the MCP-Atlassian project.
Agent   : code_search_agent (confidence: 0.53) | 41.93 ms
Top 3   : code_search_agent=0.62, confluence_agent=0.13, grafana_agent=0.12
------------------------------------------------------------
Prompt  : Fetch the backend p95 graph and interpret it.
Agent   : grafana_agent (confidence: 0.62) | 41.02 ms
Top 3   : grafana_agent=0.70, code_search_agent=0.11, confluence_agent=0.10
------------------------------------------------------------
Prompt  : What is the capital of Turkey?
Agent   : confluence_agent (confidence: 1.00) | 40.20 ms
Top 3   : confluence_agent=1.00, code_search_agent=0.00, workflow_agent=0.00
------------------------------------------------------------
Prompt  : What is the weather like today?
Agent   : confluence_agent (confidence: 0.88) | 31.85 ms
Top 3   : confluence_agent=0.91, code_search_agent=0.03, workflow_agent=0.03
------------------------------------------------------------
Prompt  : What permissions should I request for the newly joined intern?
Agent   : confluence_agent (confidence: 0.97) | 40.93 ms
Top 3   : confluence_agent=0.97, code_search_agent=0.01, workflow_agent=0.01
------------------------------------------------------------
Prompt  : How do I create a subtask in Jira?
Agent   : confluence_agent (confidence: 0.96) | 41.52 ms
Top 3   : confluence_agent=0.97, code_search_agent=0.01, workflow_agent=0.01
------------------------------------------------------------
