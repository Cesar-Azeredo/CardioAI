# Proveniência dos textos — Fase 2 (fontes do mapa de conhecimento)

Gerado por `scripts/fase-02/00_coleta_fontes_mapa.py`. Nada foi completado de
memória: metadado que a página não expõe está registrado como ausente.

O mapa de conhecimento cobre **três doenças** (decisão 1 da Fase 2, seção
5bis do `CLAUDE.md`/`AGENTS.md`):

| Doença | Fonte primária | Fonte complementar |
|---|---|---|
| Hipertensão | Texto 2 da Fase 1 — `assets/textos/texto_02_hipertensao-pressao-alta-ministerio-saude.txt` (ficha em `assets/textos/PROVENIENCIA.md`) | — |
| Infarto | Texto 3 (gov.br) | — |
| AVC | Texto 4 (gov.br) | — |

**Fontes complementares da BVS inacessíveis (HTTP 503 em todo o domínio,
verificado por script e navegador em 2026-09-23), retiradas do escopo.** Eram
as páginas `https://bvsms.saude.gov.br/ataque-cardiaco-infarto/` e
`https://bvsms.saude.gov.br/avc-acidente-vascular-cerebral/`; o servidor
respondeu com a página de bloqueio do WAF ("The requested URL was rejected")
para qualquer URL do domínio, inclusive a home. Nenhum conteúdo delas foi
lido, e portanto nenhuma linha do mapa se apoia nelas. A cobertura de infarto
e AVC vem inteira das páginas do gov.br (Saúde de A a Z), que são a fonte
primária.

**Restrição de licença (CC BY-ND 3.0 nas páginas do gov.br)**: estes textos
podem ser **analisados** (extrair termos de sintoma para o mapa, contar,
indexar), mas não reescritos, resumidos ou traduzidos livremente. O mapa de
conhecimento cita o trecho literal de onde cada sintoma saiu; as frases de
paciente da Fase 2 são redação própria do grupo, não paráfrase destes textos.

## Texto 3 — Infarto

- **Arquivo**: `texto_03_infarto-ministerio-saude.txt`
- **Doença coberta no mapa**: infarto
- **Título**: Infarto
- **Autor**: Ministério da Saúde (conteúdo institucional, sem autoria individual assinada)
- **Fonte**: Ministério da Saúde — Saúde de A a Z
- **URL**: https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto
- **Licença**: Todo o conteúdo deste site está publicado sob a licença Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada. (https://creativecommons.org/licenses/by-nd/3.0/deed.pt_BR)
- **Data de publicação/última atualização**: a página-fonte não expõe data de publicação nem de atualização (verificado: sem `<time>`, sem meta `citation_*`, sem `dateModified`/`datePublished` em JSON-LD) — a data de acesso é a referência temporal disponível.
- **Data de acesso**: 2026-09-23
- **Nº de palavras (contado, `texto.split()`)**: 573
- **Nº de caracteres (contado, `len(texto)`)**: 3584
- **Repetições da fonte**: a própria página repete as linhas abaixo (conferido no HTML-fonte). **Mantidas repetidas no .txt** — remover repetição é alterar a obra (cláusula ND). Quem consumir este texto (mapa de conhecimento, contagem de termos) deve contar cada ocorrência uma vez só:
  - 2× — "Em idosos, o principal sintoma do infarto agudo do miocárdio pode ser a falta de ar. A dor…"
  - 3× — "Nos diabéticos e idosos, o infarto também pode ocorrer sem sinais específicos. Por isso, d…"
- **Processamento aplicado**: extração dos 13 blocos de conteúdo da página (`div.cover-richtext-tile` e `div.outstanding-header`, em ordem de documento, até o primeiro bloco de rodapé `cover-embed-tile`), um elemento-folha (`h1`–`h4`, `p`, `li`) por linha. Normalização de espaços em branco (mesma regra da Fase 1). **Nenhuma outra alteração** — obrigatório pela cláusula ND da CC BY-ND 3.0. Integridade verificada por script a cada execução: o multiconjunto de palavras do `.txt` é idêntico ao dos blocos de conteúdo da página.

## Texto 4 — Acidente Vascular Cerebral (AVC)

- **Arquivo**: `texto_04_avc-ministerio-saude.txt`
- **Doença coberta no mapa**: AVC
- **Título**: Acidente Vascular Cerebral (AVC)
- **Autor**: Ministério da Saúde (conteúdo institucional, sem autoria individual assinada)
- **Fonte**: Ministério da Saúde — Saúde de A a Z
- **URL**: https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/avc
- **Licença**: Todo o conteúdo deste site está publicado sob a licença Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada. (https://creativecommons.org/licenses/by-nd/3.0/deed.pt_BR)
- **Data de publicação/última atualização**: a página-fonte não expõe data de publicação nem de atualização (verificado: sem `<time>`, sem meta `citation_*`, sem `dateModified`/`datePublished` em JSON-LD) — a data de acesso é a referência temporal disponível.
- **Data de acesso**: 2026-09-23
- **Nº de palavras (contado, `texto.split()`)**: 872
- **Nº de caracteres (contado, `len(texto)`)**: 5753
- **Repetições da fonte**: nenhuma linha repetida na página.
- **Processamento aplicado**: extração dos 18 blocos de conteúdo da página (`div.cover-richtext-tile` e `div.outstanding-header`, em ordem de documento, até o primeiro bloco de rodapé `cover-embed-tile`), um elemento-folha (`h1`–`h4`, `p`, `li`) por linha. Normalização de espaços em branco (mesma regra da Fase 1). **Nenhuma outra alteração** — obrigatório pela cláusula ND da CC BY-ND 3.0. Integridade verificada por script a cada execução: o multiconjunto de palavras do `.txt` é idêntico ao dos blocos de conteúdo da página.
