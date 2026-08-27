# Proveniência dos dados — Fase 1

Registro de proveniência das bases usadas na Fase 1, exigido pela regra inviolável 5
do `CLAUDE.md`/`AGENTS.md`. Preencher uma linha por base (numérica, textual, visual)
antes de considerar a fase pronta — nenhum dado entra no repositório sem esta tabela
preenchida.

| Base | Tipo | Fonte | URL | DOI | Licença | Data de acesso | Nº de registros | Citação formal |
|---|---|---|---|---|---|---|---|---|
| UCI Heart Disease (base Cleveland) | numérico | UCI Machine Learning Repository | https://archive.ics.uci.edu/dataset/45/heart+disease | 10.24432/C52P4X | CC BY 4.0 | 2026-08-27 | 303 | Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1989). *Heart Disease* [Dataset]. UCI Machine Learning Repository. |
| Trajetórias da Saúde Cardiovascular... (texto 1) | textual | SciELO — Arquivos Brasileiros de Cardiologia | https://www.scielo.br/j/abc/a/ZQMYdZFc7nYvKzVC6mXFKMt/?lang=pt | 10.5935/abc.20140065 | CC BY-NC 3.0 | 2026-08-27 | 1 (1.608 palavras) | Pellanda, L. C. (2014). Trajetórias da Saúde Cardiovascular: Epidemiologia do Curso da Vida no Brasil [editorial]. Arquivos Brasileiros de Cardiologia, 102(5), 418–419. |
| Hipertensão (pressão alta) (texto 2) | textual | Ministério da Saúde — Saúde de A a Z | https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/h/hipertensao | — | CC BY-ND 3.0 (SemDerivações) | 2026-08-27 | 1 (858 palavras) | Ministério da Saúde. *Hipertensão (pressão alta)*. Saúde de A a Z. Data de publicação não localizada na página — TODO(humano) se necessário para a rubrica. |
| ECG Images dataset of Cardiac Patients (v2) | visual | Mendeley Data | https://data.mendeley.com/datasets/gwbz3fsgp8/2 | 10.17632/gwbz3fsgp8.2 | CC BY 4.0 (confirmada na página; artigo descritor tem licença separada, CC BY-NC-ND) | 2026-08-27 | 120 selecionadas (de 928 arquivos / 491 imagens únicas por MD5) | Khan, A. H., & Hussain, M. (2021). *ECG Images dataset of Cardiac Patients* (Version 2) [Data set]. Mendeley Data. |
| | | | | | | | | |

Campos:

- **Base**: nome curto da base (ex.: "UCI Heart Disease").
- **Tipo**: numérico / textual / visual.
- **Fonte**: instituição ou repositório de origem.
- **URL**: link público verificado — nunca inventado (regra inviolável 1).
- **DOI**: quando existir.
- **Licença**: licença de uso/redistribuição encontrada na página da base.
- **Data de acesso**: data em que o dado foi baixado/verificado neste projeto.
- **Nº de registros**: contagem real (linhas do CSV, imagens do conjunto, arquivos de texto).
- **Citação formal**: referência no formato acadêmico padrão.
