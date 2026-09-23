# AGENTS.md — Contexto operacional do projeto CardioIA

> **Este arquivo é a fonte única do contexto do projeto.** É lido diretamente pelo GitHub Copilot, Cursor, Codex e afins.
> O `CLAUDE.md` da raiz contém apenas `@AGENTS.md` — ele importa este arquivo para o Claude Code, como recomenda a documentação oficial do Claude Code para repositórios que usam `AGENTS.md` (code.claude.com/docs/en/memory). Edite só este arquivo.

---

## 1. O que é este projeto

**CardioIA — A Nova Era da Cardiologia Inteligente.**
Projeto acadêmico do curso de Inteligência Artificial da **FIAP**, conduzido pelo método **PBL (Project Based Learning)**. O objetivo é construir, ao longo de **7 fases**, uma plataforma digital que simule o ecossistema de uma cardiologia moderna, integrando dados clínicos, Machine Learning, Visão Computacional, IoT, NLP e agentes inteligentes.

Contexto que justifica o projeto (usar nas justificativas dos documentos): doenças cardiovasculares são a principal causa de morte no mundo, com aproximadamente **17,9 milhões de óbitos anuais**; infartos, arritmias, insuficiência cardíaca e AVCs são comuns e podem ser prevenidos com diagnóstico precoce.

### Regra estrutural mais importante

**Este é um monorepo incremental.** Cada fase é uma entrega avaliada separadamente, mas **todas vivem no mesmo repositório e as fases posteriores consomem os artefatos das anteriores**.

Consequências práticas, que valem como regra:

- **Nunca apague, renomeie ou reescreva artefatos de fases já entregues.** As fases são **aditivas**.
- **Nunca organize o repositório como "uma pasta isolada por fase".** Organize por **função** (`data/`, `docs/`, `notebooks/`, `scripts/`, `src/`) e use subpastas por fase **dentro** dessas pastas. Motivo: a Fase 2 vai treinar modelos sobre o CSV da Fase 1, a Fase 4 vai processar as imagens da Fase 1 e a Fase 5 vai usar os textos da Fase 1. Duplicar dado por fase quebra isso.
- Ao iniciar uma fase nova, **leia primeiro o que as fases anteriores produziram** antes de escrever qualquer código.

---

## 2. Estado atual

| Campo | Valor |
|---|---|
| **Fase em andamento** | **Fase 2 — Diagnóstico Automatizado** — todos os entregáveis prontos e integrados na `main` (merge `--no-ff` da branch `fase-02/nlp-triagem`, 2026-09-23); **falta só o vídeo** (ver 5bis.6) |
| Entrega extra em andamento | **Ir Além 2 — MLP em Keras sobre ECG** (branch `ir-alem-2/mlp-ecg`) — notebook executado, README e exemplos prontos, integrado na `main` (merge `--no-ff` da branch `ir-alem-2/mlp-ecg`, 2026-09-23); **falta o vídeo e a confirmação do tutor** (ver 5ter.6) |
| Fases concluídas | **Fase 1 — Batimentos de Dados** (dado coletado, tratado e documentado nas três partes; links públicos publicados no Google Drive) |
| Ambiente | VS Code local, repositório já criado a partir do template FIAP e conectado ao GitHub |
| Idioma dos entregáveis | **Português do Brasil** |

> **Mantenha esta tabela atualizada.** Ao concluir uma fase, mova-a para "concluídas" e atualize a fase em andamento. Este é o primeiro lugar que qualquer agente olha.

---

## 3. Estrutura de diretórios

Esta árvore parte do **template FIAP** já existente no repositório (não substitui nada dele). `[F1]` = criado/preenchido na Fase 1; `[F2]` = criado na Fase 2; `[IA2]` = criado no Ir Além 2 (entrega extra da Fase 2, seção 5ter); `[futuro]` = reservado para próximas fases; `[template]` = já existia antes da Fase 1 e permanece como está.

```
CardioIA/
├── AGENTS.md                          # este arquivo                         [F1]
├── CLAUDE.md                          # só `@AGENTS.md` (importa este arquivo) [F1]
├── README.md                          # ENTREGÁVEL AVALIADO — template FIAP  [F1]
├── requirements.txt                                                          [F1]
├── requirements-ir-alem-2.txt         # -r requirements.txt + TF/Keras       [IA2]
├── .gitignore                                                                [F1]
│
├── assets/
│   ├── logo-fiap.png                                                    [template]
│   ├── mapa-mental/                   # SVG/PNG do mapa mental da jornada    [F1]
│   ├── textos/                        # ENTREGÁVEL: os .txt para NLP         [F1]
│   │   └── fase-02/                   # fontes do mapa (gov.br) + frases     [F2]
│   └── imagens/
│       ├── amostras/                  # ~12 imagens leves p/ ilustrar README [F1]
│       ├── ir-alem-2/                 # 4 pares antes/depois do pré-proc.    [IA2]
│       └── LEIA-ME.md                 # explica que o conjunto está no Drive [F1]
│
├── config/                            # parâmetros de sensores (ESP32) e modelos
│   └── readme.md                                          [futuro: fase-03, fase-06]
│
├── document/
│   ├── ai_project_document_fiap.md    # DOCUMENTO RESUMO AVALIADO (rubrica)   [F1]
│   ├── datasets/
│   │   ├── raw/                       # dado como baixado, sem tratamento     [F1]
│   │   ├── processed/                 # dataset final .csv e .xlsx            [F1]
│   │   ├── fase-02/                   # dado primário autoral sintético .csv  [F2]
│   │   ├── dicionario-de-dados.md     # variável, tipo, unidade, faixa        [F1]
│   │   └── README.md                  # proveniência: fonte, licença, DOI...  [F1]
│   ├── fase-01/
│   │   ├── dados-numericos.md                                                 [F1]
│   │   ├── dados-textuais.md                                                  [F1]
│   │   ├── dados-visuais.md                                                   [F1]
│   │   └── governanca-e-vies.md                                               [F1]
│   ├── fase-02/                       # governança, decisões, autoavaliação   [F2]
│   │   └── ir-alem-2/                 # protocolo da MLP, levantamento       [IA2]
│   ├── fase-03/ ... fase-07/                                            [futuro]
│   └── other/
│       └── readme.md                                                    [template]
│
├── notebooks/
│   ├── fase-01/                       # vazia (só .gitkeep) — a EDA da Fase 1
│   │                                  # foi feita por script, não notebook:
│   │                                  # scripts/fase-01/02_perfila_...py     [F1]
│   ├── fase-02/                       # TF-IDF + classificador de risco      [F2]
│   │   └── ir-alem-2/                 # MLP em Keras sobre ECG               [IA2]
│   └── fase-03/ ...                                                     [futuro]
│
├── scripts/
│   ├── readme.md                                                        [template]
│   ├── fase-01/                       # coleta, tratamento, validação        [F1]
│   └── fase-02/                       # coleta das fontes, extrator          [F2]
│       └── ir-alem-2/                 # download, dedup e auditoria do ECG   [IA2]
│
└── src/
    ├── readme.md                                                        [template]
    └── cardioia/                      # código reutilizável entre fases  [futuro]
```

Regras sobre a estrutura:

- Toda pasta versionada mas ainda vazia recebe um `.gitkeep`.
- **`README.md` da raiz é o entregável avaliado.** Ele já foi ajustado manualmente pelo dono do repositório e **segue o template da FIAP**. Preserve as seções do template (cabeçalho, nome do grupo, professores, licença, histórico de versões). **Acrescente**, não reescreva. Se precisar reorganizar algo estrutural nele, **pergunte antes**.
- **`document/ai_project_document_fiap.md` é o "documento resumo" da rubrica** (2 dos 10 pontos). Governança e viés entram nele em versão condensada, **além** da versão completa em `document/fase-01/governanca-e-vies.md`.
- **Os `.txt` da Parte 2 (NLP) vivem em `assets/textos/`**, não em `docs/` — essa pasta não existe neste repositório; o enunciado aceita `assets` ou `docs`, e o template já usa `assets` para conteúdo não-estruturado.
- **O dataset numérico vive em `document/datasets/`** (`raw/` e `processed/`), não em `data/` — mantém tudo relativo a dado dentro de `document/`, ao lado do documento resumo que o referencia.
- **`config/` não é usado na Fase 1.** Fica reservado para parâmetros de sensores simulados (Fase 3 — ESP32) e de modelos preditivos (Fase 6).
- Os `readme.md` placeholder do template FIAP (`scripts/readme.md`, `src/readme.md`, `document/other/readme.md`, `config/readme.md`) **permanecem intactos**, mesmo os que instruem "apagar ao final do módulo" — não remover nada do template por iniciativa própria.
- Nomes de arquivos e pastas: `kebab-case`, **sem acentos e sem espaços**. O conteúdo é em pt-BR com acentuação normal, em UTF-8.

---

## 4. Regras invioláveis

Estas regras valem mais que qualquer instrução de conveniência. Se cumprir uma delas atrasar a tarefa, cumpra a regra e avise.

1. **Nunca invente URL, DOI, citação, autor, nome de artigo ou link de Drive.**
   Se um link é necessário e você não o tem verificado, escreva literalmente:
   `> ⚠️ TODO(humano): colar aqui o link público de <descrição>`
   e liste todos os TODOs pendentes no final da sua resposta. Link inventado num trabalho acadêmico é falta grave e pode caracterizar má conduta.

2. **Nunca comite dado volumoso.** Limite prático: **nada acima de ~5 MB e nenhum lote de imagens** no Git. As 100+ imagens ficam hospedadas no Drive/OneDrive (é o que o enunciado exige); o repositório guarda apenas as amostras em `assets/imagens/amostras/`. O CSV numérico é pequeno (~20 KB) e **deve** ser versionado, além de linkado.

3. **Nunca use dado identificável de paciente.** Só bases públicas anonimizadas, dado sintético ou dado de formulário com consentimento. Nada de nome, CPF, prontuário, data de nascimento completa ou qualquer identificador direto. Referência: **LGPD (Lei 13.709/2018)**, que trata dado de saúde como dado pessoal **sensível**.

4. **Nunca edite arquivos de dados manualmente.** Toda transformação de dado tem que sair de um **script reprodutível** em `scripts/`, com semente fixa quando houver aleatoriedade. Se o dado não puder ser regerado rodando um comando, está errado.

5. **Registre a proveniência de todo dado.** Fonte, URL, DOI quando existir, licença, data de acesso, número de registros e citação formal. Sem isso o dado não entra no repositório.

6. **Não faça `git push`, não abra PR e não force nada em `main`** sem pedido explícito. Você pode preparar commits e sugerir a mensagem.

7. **Não instale dependência sem registrar** em `requirements.txt`.

8. **Se um requisito do enunciado for ambíguo, pergunte.** Não "resolva" inventando escopo. O trabalho é avaliado contra uma rubrica fechada.

9. **Arquivo pré-existente do template FIAP não se sobrescreve.** Se um arquivo do template (`.gitignore`, `.gitattributes`, `README.md`, `ai_project_document_fiap.md`, os `readme.md` de pasta, `.github/`) precisar mudar, **preserve o conteúdo original e estenda** com o mínimo necessário. Convenção do template é decisão da instituição até prova em contrário — se ela parecer conflitar com o pedido, **pare e pergunte antes de alterar**. Ao alterar um desses arquivos, anuncie a mudança em destaque na resposta.

---

## 5. Fase 1 — Batimentos de Dados

**Papel assumido:** cientista de dados hospitalar. A missão é levantar, organizar e entender dados cardiológicos que vão alimentar os módulos inteligentes das fases seguintes — com atenção explícita a **Governança de Dados** e **viés**.

### 5.1 Requisitos literais do enunciado

**Parte 1 — Dados numéricos (IoT)**
- Dataset com **mínimo de 100 linhas**.
- Formato **obrigatoriamente `.csv` ou `.xlsx`**.
- Variáveis do tipo: idade, sexo, pressão arterial, colesterol, histórico de doença cardíaca, sintomas, frequência cardíaca etc.
- No `README.md`: link para os dados hospedados em serviço público (Drive/OneDrive), explicação clara da **origem** (real ou simulado) e destaque das **variáveis mais relevantes do ponto de vista clínico, com justificativa** do porquê importam para um projeto de IA em saúde.

**Parte 2 — Dados textuais (NLP)**
- **No mínimo 2 arquivos `.txt`** sobre doenças cardíacas, saúde pública, sintomas ou tratamentos.
- Fontes sugeridas pelo enunciado: **SciELO, BVS, artigos do SUS/Ministério da Saúde, ou literatura clássica via Projeto Gutenberg**.
- Ficam em subpasta **`docs`** ou **`assets`** → neste repositório: **`docs/textos/`**.
- No `README.md`: explicar como esses textos podem ser explorados por algoritmos de NLP (ex.: análise de sentimentos, extração de sintomas, classificação de tópicos) e **justificar a relevância** para IA em saúde.

**Parte 3 — Dados visuais (VC)**
- **No mínimo 100 imagens** `.jpg` ou `.png` de **um tipo** de exame cardiológico (ECG, angiograma ou raio-X torácico).
- Link público para o conjunto hospedado (Drive/OneDrive).
- No `README.md`: justificar como as imagens poderão ser analisadas por Visão Computacional (ex.: detecção de padrões, identificação de bordas, reconhecimento de anomalias) e a importância disso para IA em saúde.

**Entregáveis**
- `README.md` detalhado explicando o projeto, descrevendo as três partes e indicando objetivos e fontes.
- Subpasta `docs` ou `assets` com conteúdo.
- **Links públicos acessíveis a qualquer pessoa** — o time da FIAP precisa abrir sem pedir permissão. Testar em janela anônima.

### 5.2 Rubrica de avaliação (10 pontos) — otimizar contra isto

| Critério | Pontos |
|---|---|
| Parte 1 — Dataset numérico entregue corretamente, organizado e explicado | **3** |
| Parte 2 — Textos selecionados e contextualizados corretamente | **2** |
| Parte 3 — Imagens entregues e bem justificadas em seu potencial para análise por IA | **2** |
| Documento resumo com explicações claras, objetivas e bem estruturadas | **2** |
| Cumprimento das orientações gerais e prazo de entrega | **1** |

Leitura da rubrica: **4 dos 10 pontos são de escrita e organização** (o critério de 2 pontos do documento resumo + boa parte dos critérios de cada parte, que exigem "explicado", "contextualizado", "bem justificado"). Ou seja, **texto bem-feito vale tanto quanto dado coletado**. Justificativa genérica derruba nota mesmo com dado perfeito. Toda justificativa precisa amarrar em **relevância clínica** e **uso concreto nas fases seguintes**.

### 5.3 Fontes verificadas (usar estas; não substituir por links inventados)

**Numérico — UCI Heart Disease**
- Página: `https://archive.ics.uci.edu/dataset/45/heart+disease`
- CSV direto: `https://archive.ics.uci.edu/static/public/45/data.csv`
- Via Python: `pip install ucimlrepo` → `fetch_ucirepo(id=45)`
- 303 instâncias (base Cleveland), 13 atributos + alvo `num` (0 = ausência, 1–4 = presença). Há valores faltantes.
- Licença **CC BY 4.0**. DOI `10.24432/C52P4X`.
- Citação: Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1989). *Heart Disease* [Dataset]. UCI Machine Learning Repository.
- Atende o mínimo de 100 linhas com folga (303).

**Visual — ECG Images dataset of Cardiac Patients, versão 2 (Mendeley Data)**
- Página: `https://data.mendeley.com/datasets/gwbz3fsgp8/2` — DOI `10.17632/gwbz3fsgp8.2`
- **Licença do dataset (confirmada na própria página, bloco JSON-LD e bloco de metadados): CC BY 4.0** — não confundir com a licença do artigo descritor abaixo, que é um documento diferente com licença diferente (CC BY-NC-ND).
- **Contribuidores do dataset (conforme a página): Ali Haider Khan e Muzammil Hussain** (University of Management and Technology, Lahore). Malik, M. K. é coautor do artigo descritor na Data in Brief, não consta como contribuidor do dataset em si.
- **A v2 NÃO tem categoria COVID-19** (isso era a v1). São 4 categorias: infarto do miocárdio (240 pacientes anunciados), histórico prévio de infarto (172), batimento cardíaco anormal (233), pessoa normal (284) — capturadas com equipamento EDAN SERIES-3 no Ch. Pervaiz Elahi Institute of Cardiology, Multan, Paquistão. Cada arquivo é o ECG completo de 12 derivações num único composite (não 1 arquivo por derivação).
- **Tamanho real extraído: 589 MB** (194 MB é o `.zip` comprimido para download, não o conteúdo extraído).
- **Volume real verificado: 928 arquivos** (929 esperados pelos nomes das pastas; falta `MI(215).jpg`) — dos quais **apenas 491 são imagens de conteúdo único por MD5** (47% de redundância; por categoria: MI 239→30, PMI 172→86, Normal 284→142, HB 233→233 sem duplicata). Checagem de quase-duplicata por hash perceptual (dHash 256 bits) não encontrou nada abaixo do limiar de quase-certeza — os pares mais próximos, inspecionados visualmente, são pacientes genuinamente diferentes que só compartilham o template do aparelho.
- Artigo descritor (documento e licença separados do dataset): Khan, A. H., Hussain, M., & Malik, M. K. (2021). *ECG images dataset of Cardiac and COVID-19 patients*. Data in Brief, 34, 106762. DOI `10.1016/j.dib.2021.106762`. **CC BY-NC-ND** — restringe obra derivada; adequado para uso acadêmico com atribuição, mas essa licença é do artigo, não do dataset.
- Atende o mínimo de 100 imagens com muita folga. Amostra selecionada: **120 imagens, balanceadas 30/30/30/30 por categoria** (o teto de imagens únicas da categoria "infarto" — 30 — definiu a cota igual das demais), deduplicada por MD5, com seleção reprodutível por semente fixa. Registrar a licença e a proveniência em `document/datasets/README.md`.

**Textual — escolher no mínimo 2**
- SciELO Brasil (`https://www.scielo.br`) — buscar em *Arquivos Brasileiros de Cardiologia*; artigos em acesso aberto.
- BVS / Biblioteca Virtual em Saúde (`https://bvsalud.org`).
- Ministério da Saúde / SUS — publicações e cadernos de atenção básica sobre hipertensão e doenças cardiovasculares.
- Projeto Gutenberg (`https://www.gutenberg.org`) — domínio público, útil para um texto de perfil histórico/literário que contraste com o texto técnico.
- ⚠️ **O agente não deve fabricar título, autor ou URL de artigo.** Deixar TODO para o humano colar o link e, ao receber o link, extrair o texto, salvar como `.txt` em UTF-8 e registrar a proveniência.

Sugestão de composição que rende na rubrica: **um texto técnico-científico** (SciELO/BVS) + **um texto de comunicação em saúde pública** (Ministério da Saúde). O contraste de registro linguístico entre os dois é argumento forte na justificativa de NLP — permite comparar vocabulário técnico vs. leigo, o que é exatamente o problema da Fase 5 (chatbot que precisa traduzir termo clínico para o paciente).

### 5.4 Governança de dados e viés — obrigatório documentar

O enunciado cobra explicitamente os conceitos iniciais de Governança de Dados e de viés. Cobrir em `docs/fase-01/governanca-e-vies.md`:

- **Proveniência e licença** de cada uma das três bases, com data de acesso.
- **Finalidade** do uso (acadêmico, sem aplicação clínica real) e um aviso claro de que nada aqui serve para decisão médica.
- **LGPD**: dado de saúde é dado pessoal sensível; como a anonimização das bases públicas endereça isso.
- **Viés identificado, de forma concreta e quantificada.** Não escrever "pode haver viés"; medir e nomear. Nas bases escolhidas há vieses reais e verificáveis:
  - *UCI/Cleveland*: coleta de **1989**, hospital único nos EUA, forte desbalanceamento por sexo, faixa etária concentrada, valores faltantes em atributos como `ca` e `thal`. Um modelo treinado nisso não generaliza para a população brasileira de 2026.
  - *ECG Images*: coleta em **um único país (Paquistão)** com **um único modelo de equipamento**. O modelo pode aprender a assinatura visual do aparelho em vez da patologia — problema clássico de *shortcut learning* em imagem médica.
- **Consequência clínica do viés**: um falso negativo em triagem cardiológica é um paciente mandado para casa infartando. Assimetria de custo entre os tipos de erro precisa estar escrita.
- **Mitigações propostas** para as fases seguintes: estratificação por sexo e faixa etária, métricas por subgrupo, validação externa, e não usar acurácia global como métrica única.

### 5.5 Definition of Done da Fase 1

Só considerar a fase pronta quando **todos** os itens estiverem verdadeiros.
Status verificado em 2026-08-27 (caminhos corrigidos abaixo — a versão
anterior desta lista referenciava `data/` e `docs/`, pastas que a seção 3
não usa mais desde a correção da árvore de diretórios). Atualizado após a
publicação dos 4 links no Google Drive:

- [x] Dataset em `document/datasets/processed/` em `.csv` **e** `.xlsx`, com **≥ 100 linhas** (303, contagem verificada por script, não estimada).
- [x] `document/datasets/dicionario-de-dados.md` com variável, tipo, unidade, faixa válida e significado clínico de cada coluna.
- [x] Script reprodutível de coleta/tratamento em `scripts/fase-01/`, rodando de ponta a ponta sem erro em ambiente limpo (testado em venv Python 3.12 recriado do zero).
- [x] **≥ 2** arquivos `.txt` em `assets/textos/`, em UTF-8, com proveniência registrada (2 arquivos, `PROVENIENCIA.md`).
- [x] **≥ 100** imagens organizadas (120) e hospedadas, com `manifest-imagens.csv` (nome do arquivo, categoria, dimensões, origem, hash e aliases) versionado no repositório. Hospedagem: [Google Drive](https://drive.google.com/drive/folders/12YhReksoB8K-aWQsubtUIaEx4zK9EuF3?usp=drive_link).
- [x] ~12 imagens de amostra em `assets/imagens/amostras/`.
- [x] Links públicos testados **em janela anônima** e funcionando sem login — confirmado pelo humano: os 4 links do Drive abrem corretamente, incluindo abertura de imagem individual dentro da pasta de ECG.
- [x] `README.md` da raiz cobrindo as três partes, com as justificativas clínicas e de IA exigidas, e integrado ao template FIAP sem quebrá-lo.
- [x] `document/fase-01/governanca-e-vies.md` completo.
- [x] Nenhum TODO de link pendente — os 4 links (dataset numérico, imagens, textos, pasta-mãe) foram publicados e substituídos no `README.md`, `assets/imagens/LEIA-ME.md` e `document/datasets/README.md`. A única observação restante (data de publicação do Texto 2) deixou de ser TODO — é nota de proveniência definitiva, porque a página-fonte não expõe esse campo.
- [x] Autoavaliação escrita contra a rubrica da seção 5.2, critério por critério (`document/fase-01/autoavaliacao.md`).

**11 de 11 itens verdadeiros. Fase 1 completa.**

---

## 5bis. Fase 2 — Diagnóstico Automatizado (IA no Estetoscópio Digital)

**Papel assumido:** construir um primeiro módulo de triagem por linguagem
natural — o paciente descreve o que sente, o sistema extrai sintomas, cruza
com um mapa de conhecimento e sugere diagnóstico e nível de risco.

### 5bis.1 Enunciado — resumo

> O texto literal do enunciado não está registrado neste arquivo. O resumo
> abaixo foi montado a partir da lista de entregáveis e da rubrica informadas
> pelo humano em 2026-09-23. Se o enunciado literal for colado depois, ele
> prevalece sobre este resumo.

**Entregáveis obrigatórios:**

1. `.txt` com **10 frases** de sintomas relatados por pacientes.
2. `.csv` com **mapa de conhecimento sintoma → doença**.
3. **Código Python** que lê as frases, extrai sintomas e sugere diagnóstico.
4. `.csv` com **frases rotuladas em alto/baixo risco**.
5. `.ipynb` com **TF-IDF, classificador e avaliação**.
6. **`README.md` atualizado** e **vídeo de até 4 min no YouTube (não listado)**, com link no GitHub.

Itens "Ir Além": **não entram no DoD da Fase 2.** O **Ir Além 2** foi
decidido em 2026-09-23 e tem seção própria (5ter); os demais seguem não
decididos. Se entrarem, o lugar é `notebooks/fase-02/ir-alem-*.ipynb`
e `document/fase-02/ir-alem.md`.

### 5bis.2 Rubrica de avaliação (10 pontos) — otimizar contra isto

| Critério | Pontos |
|---|---|
| Relatos e mapa de conhecimento organizados | **2** |
| Código de extração de informações funcional | **2** |
| Dataset simples criado corretamente | **1** |
| Classificador treinado e testado corretamente | **2** |
| Documentação clara e repositório público com README completo | **1** |
| Vídeo de demonstração no YouTube (não listado) com link no GitHub | **2** |

Leitura da rubrica: **2 dos 10 pontos dependem só do vídeo**, que é trabalho
humano (gravar, publicar, colar o link). O vídeo precisa mostrar o extrator
rodando e o notebook avaliando — é demonstração, não slide.

### 5bis.3 Decisões registradas (2026-09-23)

**Decisão 1 — Fontes do mapa de conhecimento.** Fontes verificadas pelo
humano; não substituir nem acrescentar outras:

| Doença | Fonte | Situação |
|---|---|---|
| Hipertensão | `assets/textos/texto_02_hipertensao-pressao-alta-ministerio-saude.txt` (Fase 1) | já no repositório |
| Infarto | `https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto` | coletado → `assets/textos/fase-02/texto_03_infarto-ministerio-saude.txt` |
| AVC | `https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/avc` | coletado → `assets/textos/fase-02/texto_04_avc-ministerio-saude.txt` |
| Infarto (complementar) | `https://bvsms.saude.gov.br/ataque-cardiaco-infarto/` | **fora do escopo** |
| AVC (complementar) | `https://bvsms.saude.gov.br/avc-acidente-vascular-cerebral/` | **fora do escopo** |

**Fontes complementares da BVS inacessíveis (HTTP 503 em todo o domínio,
verificado por script e navegador em 2026-09-23), retiradas do escopo**
(decisão do humano em 2026-09-23). O gov.br é a fonte primária das duas
doenças; o script de coleta não tenta mais a BVS.

O mapa cobre **três doenças: hipertensão, infarto e AVC**. **Lacuna
documentada, não preenchida:** não há página equivalente do Ministério da
Saúde para insuficiência cardíaca nem para angina — só fontes de hospital
privado, sem o mesmo peso institucional. Decisão de governança: **três
doenças com proveniência oficial valem mais que cinco com metade sem fonte
verificável.** O enunciado cita IC e angina só como exemplo de formato, não
como requisito. Registrar em `document/fase-02/`.

As páginas do gov.br são **CC BY-ND 3.0**, mesma restrição do Texto 2:
salvas sem alterar conteúdo (a página de infarto repete itens da própria
lista de sintomas — repetição mantida, registrada em
`assets/textos/fase-02/PROVENIENCIA.md`). As frases de paciente são redação
própria, não paráfrase dessas páginas.

**Decisão 2 — CSVs da Fase 2 em `document/datasets/fase-02/`**, com README
próprio, e não em `processed/`. Motivo: `processed/` significa "derivado de
pipeline a partir de `raw/`"; os artefatos da Fase 2 são **dado primário
autoral sintético** — nem raw nem processed. `.gitignore` estendido com
`!document/datasets/fase-02/*.csv` (a negação de `processed/` foi adicionada
pelo grupo na Fase 1, não é regra do template; as quatro regras globais do
template ficam intactas). Comprovado com `git add --dry-run`.

**Decisão 3 — Dado autoral vs. regra 4.** Frases, rótulos e mapa são **dado
primário sintético autoral**, com ficha de proveniência (autores, data,
critério de rotulagem, critério de redação). A regra 4 proíbe *transformar*
dado à mão; aqui o arquivo é a origem. **Todo derivado sai de script.**
Exceção e motivo registrados em `document/fase-02/`.

**Decisão 4 — Compromissos da Fase 1** (tabela de mitigações de
`document/fase-01/governanca-e-vies.md`). **Não fingir cumprimento.**

- *Compromisso 1 — métricas estratificadas, não só acurácia global:*
  **transfere em espírito** para o classificador de texto. O notebook **deve**
  reportar matriz de confusão, recall e F1 por classe, com destaque para o
  **recall de "alto risco"**, e explicar por que acurácia global é
  insuficiente aqui, retomando a assimetria de custo da Fase 1.
- *Compromisso 2 — imputação de `ca`/`thal` dentro do fold:* **adiado
  formalmente**, porque nenhum entregável da Fase 2 modela o UCI. Registrar
  em `document/fase-02/` e atualizar `document/datasets/dicionario-de-dados.md`
  (hoje diz que `alvo_binario` é "o alvo principal previsto para a Fase 2" —
  desatualizado), apontando para a **Fase 6**, primeira fase do roadmap que
  consome o dataset numérico.

**Decisão 5 — `README.md`:** bloco "Entrega 2" **em paralelo** ao da Entrega
1, sem tocar no da Entrega 1, e linha `0.2.0` no histórico de lançamentos.

**Decisão 6 — Árvore da seção 3:** anunciava EDA em `notebooks/fase-01/`,
mas a pasta está vazia. **Corrigida a árvore** para a realidade; o notebook
não é criado.

### 5bis.4 Convenções técnicas da Fase 2

- Dependências novas: `scikit-learn==1.6.1` e `scipy==1.16.3`, versões do
  `pip-freeze` oficial do Colab (commit de 2026-09-21), wheel cp312,
  instalação testada em venv limpa.
- **numpy segue em `2.0.2`** (o Colab está em `2.1.3`). Critério do humano:
  subir só se os scripts 01–05 da Fase 1, regerados em venv limpa com a
  versão nova, produzirem artefatos **byte-idênticos** aos versionados.
  Resultado (2026-09-23): CSV, `.txt`, `PROVENIENCIA.md`, manifest, 12
  amostras e 120 selecionadas idênticos; o `.xlsx` diverge **só** em
  `docProps/core.xml` (carimbo de data/hora do openpyxl) — e diverge igual
  no controle com `2.0.2`. O critério byte-idêntico estava mal especificado
  (o `.xlsx` carrega carimbo de criação e diverge com qualquer versão); a
  regressão de **conteúdo** passou. **Decisão encerrada: numpy fica em
  `2.0.2`** — a subida não traz benefício, porque no Colab o notebook usa o
  numpy do próprio Colab. Registrado em `document/fase-02/governanca-e-vies.md`.
- Textos coletados por `scripts/fase-02/00_coleta_fontes_mapa.py`, que prova a
  cada execução que o `.txt` tem exatamente as palavras da página (cláusula ND).
  Proveniência em `assets/textos/fase-02/PROVENIENCIA.md` — arquivo separado
  do da Fase 1, que é gerado por outro script e não é tocado.

- **`.csv` rotulado: 80 frases, 40 alto risco e 40 baixo risco** (decisão do
  humano em 2026-09-23). Conjunto próprio, distinto das 10 frases do `.txt`.
- **Mapa:** `document/datasets/fase-02/mapa-conhecimento-sintomas.csv`. As três
  primeiras colunas são **literalmente** `Sintoma 1`, `Sintoma 2`,
  `Doença Associada` (estrutura mostrada no enunciado); as de proveniência
  (`tipo_termo`, `fonte`, `trecho_literal`, `observacao`) vêm depois.
  **Cada linha é um conceito de sintoma com um sinônimo** (como nos exemplos
  do enunciado: "dor no peito", "aperto no tórax" → Infarto) — não um par de
  sintomas diferentes. Sintoma 1 é sempre termo literal da página;
  `tipo_termo` descreve Sintoma 2 (`literal` ou `variante_leiga`); um
  conceito pode ter várias linhas, uma por sinônimo. Correção de erro de
  digitação da fonte ("da falar" → "da fala") só com o texto original
  preservado em `trecho_literal` e a correção declarada em `observacao`.
  Conceito compartilhado entre doenças tem uma linha por doença. Tudo
  verificado por `scripts/fase-02/01_verifica_mapa_e_frases.py`. **Mapa
  congelado** desde 2026-09-23 (53 linhas, 26 conceitos; SHA-256 conferido):
  não recebe variantes para acertar frases de teste — melhorias legítimas
  estão no método de casamento, e só valem se decididas antes de rodar nas
  frases.
- **10 frases = casos de teste do extrator**, com gabarito em
  `document/fase-02/`: 2 infarto, 2 AVC, 2 hipertensão, 1 sintoma
  compartilhado, 1 só variante leiga, 1 negação, 1 infarto atípico (idoso ou
  diabético sem dor no peito). **Frases congeladas** desde 2026-09-23: não
  mudam para acomodar o extrator (o verificador confere o SHA-256); falha em
  linguagem natural é resultado a reportar.
- **Extrator reporta quantos sintomas casou e um nível de confiança.** Não se
  adota número mínimo de sintomas para forçar ou evitar falha. Esperado da
  frase 10: "Infarto, baixa confiança (1 sintoma)"; a falha perigosa desse
  perfil (frase sem "dor" → baixo risco) é demonstrada na Parte 2, no
  classificador de risco.

- **Protocolo do extrator pré-registrado e congelado** em
  `document/fase-02/protocolo-extrator.md` (SHA-256 conferido pelo
  verificador): RSLP (`nltk==3.9.1`, recursos em `.cache/nltk_data` conferidos
  por hash — divergência vira aviso, não interrupção), proximidade ordenada
  com intervalo de 2, negação estilo NegEx, sobreposição por termo mais longo,
  localização só com dor na oração, pontuação por conceito, níveis de
  confiança fixos. Extrator: `scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py`;
  testes U1–U14: `scripts/fase-02/03_testa_extrator.py`. Execução única nas
  10 frases feita em 2026-09-23 → `document/fase-02/resultado-extrator.md`
  (baseline exato 8/10, método 9/10; nas 7 frases não contaminadas, 6/7 os
  dois). Rodar de novo nas frases só por bug, reportando os dois resultados.

- **Adendo pós-execução** (`document/fase-02/adendo-pos-execucao.md`),
  sem descongelar o protocolo: U15 em arquivo próprio
  (`scripts/fase-02/04_testa_extrator_adendo.py`) fecha a lacuna de cobertura
  achada pela checagem de mutação (`05_checa_mutacao_testes.py`: 5/5
  mutações pegas); limitação documentada — a oração que limita a negação
  também limita o casamento (frase 9); explicações da divergência em
  `document/fase-02/explicacoes-divergencia.md` (autoria humana), mescladas
  pelo gerador — rodar o extrator ao vivo não apaga nada.
- **Parte 2 — dataset rotulado.** Critério registrado antes das frases em
  `document/fase-02/criterio-rotulo-risco.md`: alto risco = ≥1 sinal de
  alerta das páginas de infarto/AVC (códigos I1–I7, A1–A6, com trecho
  literal); baixo risco = queixa leve sem sinal de alerta presente e com
  exclusões de segurança. **Zona cinzenta** (só hipertensão) fora do treino,
  só no desafio com rótulo `indefinido` — limitação: a acurácia medida
  superestima o uso real. Arquivos: `frases-rotuladas-risco.csv` (80, 40/40,
  cabeçalho `frase,situacao`) e `desafio-risco.csv` (18, fora do treino, com 3 pares contrafactuais de gênero).
  Verificação: `scripts/fase-02/06_verifica_dataset_risco.py`. Voz de gênero
  balanceada por classe (≥6 F e ≥6 M; coluna `marcador_genero`), atalhos de
  estilo balanceados com regra de parada (critério, seção 5.1). **Dataset e
  desafio congelados** (SHA-256 no script 06) desde 2026-09-23.

- **Classificador de risco (Parte 2).** Protocolo pré-registrado e commitado
  sozinho antes do notebook: `document/fase-02/protocolo-classificador.md`
  (H1–H5 com critério fixado antes). Notebook entregável
  `notebooks/fase-02/fase-02-tfidf-classificador-risco.ipynb`, executado uma
  vez numa venv nova (kernel limpo) e salvo com outputs; a seção 9.2 é texto
  escrito depois da execução. Seção **pós-hoc, não pré-registrada**, adicionada
  depois; na reexecução as seções 0–8 saíram idênticas à execução 1. Achado
  principal, **registrado como resultado — sem versão 2 do dataset** (decisão
  do humano): "mas" (0 alto / 10 baixo) e "eu" (7 / 0) viraram atalhos que a
  tabela de atalhos do script 06 não via, porque ela excluía stopwords e o
  classificador as mantém. Lição: a verificação do dado usa a mesma
  representação do modelo — o script 06 ganhou seção informativa de palavras
  funcionais por classe.

### 5bis.5 Decisões ainda em aberto

- Itens "Ir Além" além do Ir Além 2 (este está na seção 5ter).

### 5bis.6 Definition of Done da Fase 2

Só considerar a fase pronta quando **todos** os itens estiverem verdadeiros.

- [x] Branch `fase-02/nlp-triagem` e estrutura de pastas criadas (`assets/textos/fase-02/`, `document/datasets/fase-02/`, `document/fase-02/`, `scripts/fase-02/`, `notebooks/fase-02/`).
- [x] `.gitignore` estendido para `document/datasets/fase-02/*.csv`, comprovado com `git add --dry-run`.
- [x] `scikit-learn` registrado em `requirements.txt` e instalação testada de verdade em venv limpa.
- [x] Fontes gov.br de infarto e AVC coletadas por script reprodutível, com licença lida da página, contagem de palavras por script e integridade (ND) verificada.
- [x] Fontes BVS retiradas do escopo por decisão registrada (HTTP 503 em todo o domínio, 2026-09-23).
- [x] `.csv` do mapa de conhecimento em `document/datasets/fase-02/`, cobrindo hipertensão, infarto e AVC, com **fonte e trecho literal em cada linha** (53 linhas, 26 conceitos, congelado).
- [x] `.txt` com **10 frases** de paciente, redação própria, sem identificador pessoal, com ficha de redação (congelado).
- [x] Código Python de extração rodando de ponta a ponta em venv limpa: lê as frases, extrai sintomas, sugere diagnóstico, com aviso de uso exclusivamente acadêmico (U1–U14 + U15 passando).
- [x] `.csv` de frases rotuladas alto/baixo risco — **80 frases, 40/40** —, com critério de rotulagem escrito e ancorado em fonte; nº de linhas contado por script (congelado; desafio de 18 frases fora do treino).
- [x] `.ipynb` com TF-IDF, classificador e avaliação — matriz de confusão, recall e F1 por classe, **recall de "alto risco" em destaque**, explicação de por que acurácia global não basta; commitado **executado** (notebook entregável — seção 7). Colab: leitura dos CSVs pela URL raw da `main` conferida por HTTP; **execução no Colab não testada**.
- [x] `document/datasets/fase-02/README.md` com a ficha de cada arquivo.
- [x] `document/fase-02/` com: lacuna IC/angina, exceção à regra 4, compromisso 1 transferido, compromisso 2 adiado (`governanca-e-vies.md`), vieses novos da Fase 2 — circularidade autor/rótulo (`protocolo-classificador.md`, `autoavaliacao.md`), n pequeno (`autoavaliacao.md`), negação e variantes lexicais (`gabarito-frases.md`, `adendo-pos-execucao.md`), atalhos "mas"/"eu" (notebook, seção 9).
- [x] `document/datasets/dicionario-de-dados.md` atualizado (`alvo_binario` → Fase 6).
- [x] `README.md` com bloco "Entrega 2" em paralelo e linha `0.2.0`, sem alterar o bloco da Entrega 1.
- [x] Repositório **público** — verificado por HTTP sem autenticação (200) em 2026-09-23; a conferência em janela anônima fica para o humano.
- [ ] Vídeo de até 4 min no YouTube (não listado), link no `README.md` — conferido em janela anônima.
- [ ] Nenhum `TODO(humano)` de link pendente.

**16 de 18 itens verdadeiros.** Pendentes, os dois do vídeo: gravar e publicar, e colar o link — o único `TODO(humano)` de link aberto.
- [x] Autoavaliação contra a rubrica da seção 5bis.2 (`document/fase-02/autoavaliacao.md`).

---

## 5ter. Ir Além 2 — Diagnóstico visual com rede neural (MLP em Keras)

**Entrega extra, fora da atividade principal da Fase 2** (que está concluída
e não é tocada). Vive neste mesmo repositório, na branch `ir-alem-2/mlp-ecg`.

### 5ter.1 Enunciado — resumo

> Resumo informado pelo humano em 2026-09-23; o texto literal não está
> registrado aqui. Se for colado depois, prevalece sobre este resumo.

Dataset público de imagens de ECG com **classificação binária (normal vs.
anormal)**; pré-processar (**redimensionar, tons de cinza**); **MLP em
Keras**; treinar, testar, avaliar acurácia.

**Entregáveis:** notebook comentado e funcional; exemplos de imagens; README
explicativo; vídeo de até 4 min no YouTube (não listado).

**Critérios de avaliação:** pré-processamento correto das imagens; MLP
funcional; treino e avaliação com resultados; organização do notebook.

### 5ter.2 Decisão de dataset (2026-09-23)

**Usamos as imagens de ECG da Fase 1** (Mendeley `gwbz3fsgp8` v2, DOI
`10.17632/gwbz3fsgp8.2`, CC BY 4.0), **não** o `shayanfazeli/heartbeat` do
Kaggle recomendado pelo enunciado. Motivo, a registrar no README: o dataset
do Kaggle é de **sinais segmentados em CSV**, não de imagens — não há o que
redimensionar nem converter para tons de cinza. As imagens da Fase 1 cumprem
o texto do enunciado e reaproveitam o manifest e a auditoria de duplicatas.

> ⚠️ **PENDÊNCIA A VERIFICAR:** Confirmar com o tutor (André Godoy) se o uso
> das imagens do Mendeley no lugar do dataset recomendado do Kaggle é
> aceito. Argumento: o Kaggle `shayanfazeli/heartbeat` é de sinais em CSV e
> não permite o "pré-processamento correto das imagens" exigido nos
> critérios. **Plano B**, se o tutor exigir o Kaggle: converter cada sinal do
> CSV em imagem desenhando o traçado, e então aplicar o pré-processamento —
> cumpre as duas exigências ao pé da letra, mas é artificial, porque desenha
> um sinal só para a MLP achatá-lo de novo.

**Binário:** normal = `Normal` (142); anormal = `MI` + `PMI` + `HB`
(30 + 86 + 233 = 349). 28,9% / 71,1%.

### 5ter.3 Etapa 1 — levantamento (2026-09-23, sem treino)

Scripts em `scripts/fase-02/ir-alem-2/`; dado **fora do repositório**, em
`~/.cache/cardioia/mendeley-gwbz3fsgp8-v2/` (mesmo caminho no Colab:
`/root/.cache/...`).

- **01 — download** pela API pública
  (`https://data.mendeley.com/public-api/zip/gwbz3fsgp8/download/2` → 302
  para S3 pré-assinado). Só biblioteca padrão, para o Colab chamar antes de
  qualquer `pip`. Idempotente. Confere **contagem por pasta** (928 `.jpg`),
  não hash do zip: o Mendeley gera o zip no servidor e não publica checksum.
  Zip de 2026-09-23: 193,9 MB, SHA-256
  `016ab954e9b1392dcea1e2b5638752593ec30feda07281a00b5b8f2e13618c50`
  (registro, não critério).
- **02 — deduplicação por MD5**, mesmo método da Fase 1: **491 únicas
  (MI 30, PMI 86, HB 233, Normal 142)**, idêntico à Fase 1; **0 colisões
  de MD5 entre categorias** (checagem nova — no binário, a mesma imagem com
  dois rótulos); 120/120 MD5 do manifest da Fase 1 presentes. **A
  deduplicação é requisito, não cuidado:** 47% dos arquivos são cópia byte
  a byte (87% em MI); split sobre arquivos põe a mesma imagem no treino e
  no teste, e o teste passa a medir memorização. Gera
  `indice-unicos.csv` (fora do repo), entrada do split.
- **03 — auditoria do texto impresso** (as 491, não amostra):
  - Layout **fixo**: 491/491 em 2213×1572 RGB; moldura vermelha da grade em
    y 283–1517, x 68–2176 (52 imagens em 2175 — lotes de digitalização
    consecutivos, irrelevante). Texto do cabeçalho em y 31–275 (ID do
    exame, sexo, campos vazios); rodapé em y 1538–1552 (filtro, ♥ **FC**,
    aviso **"Lead Off"** em 35 imagens, data/hora — dois formatos de data,
    lotes de 2019 e 2020, misturados entre as classes).
  - **FC impressa lida por casamento de glifos** (fonte fixa, pior casamento
    1 bit em 165): **nenhuma Normal passa de 90 bpm**; HB mediana 105, 85%
    acima de 90. **"FC impressa > 90" identifica 223 das 349 anormais (64%)
    com precisão de 100%** — o atalho é real e medido, não hipotético.
  - Sexo impresso (≈90% "Male") e "Lead Off" **não** separam as classes
    (F: 5–11%; Lead Off: 0–10% por categoria).
  - **Recorte proposto: interior da moldura, `(68, 283, 2177, 1518)` →
    2109×1235.** Todo texto variável fica fora. Custo: 9 imagens têm a
    ponta de um pico passando alguns pixels da moldura, cortada.
  - **Template do aparelho dentro do recorte:** pixels escuros em ≥95% das
    491 imagens (rótulos das derivações, pulso de calibração, barras
    separadoras) = **31% da tinta média de cada imagem**. O recorte tira o
    texto, mas não o template — é o risco de *shortcut learning* da Fase 1
    (um aparelho, um centro, um país) e não se resolve com este dado.
  - A FC continua no traçado (intervalo RR). Isso é sinal clínico legítimo,
    não atalho — mas implica que a separação HB × Normal pode ser "fácil" por
    ritmo, e o recall por subcategoria precisa ser reportado.
- **Dependência testada em venv limpa (Python 3.12, macOS arm64):**
  `tensorflow==2.21.0`, `keras==3.13.2`, `protobuf==6.33.6` — versões do
  pip-freeze oficial do Colab (commit `ac5f3b6`, 2026-09-23), registradas em
  `requirements-ir-alem-2.txt`, não no `requirements.txt`. Wheel cp312
  `macosx_12_0_arm64` existe. Instala junto do `requirements.txt` inteiro
  **mantendo numpy 2.0.2**, `pip check` limpo; import e `predict` de MLP em
  CPU testados.

### 5ter.4 Etapa 2A — verificações antes do protocolo (2026-09-23)

Registro completo em `document/fase-02/ir-alem-2/levantamento.md`.

- **Borda x = 2175** (52 imagens): nas 4 categorias (MI 7%, PMI 6%, HB 10%,
  Normal 15%), em números de arquivo consecutivos — lote de digitalização.
  Só a borda se desloca; o template não. **Recorte recuado 4 px em todos os
  lados: `(72, 287, 2173, 1514)` → 2101×1227.**
- **Leitura por glifo validada à mão:** 20 aleatórias (semente 42) + 23
  dirigidas (as 13 normais com FC ≥ 85, 5 "Female", 5 "Lead Off"):
  **86 campos, 0 erro** (script 04).
- **Manifest** `document/datasets/processed/manifest-ir-alem-2.csv` (491
  linhas, em `processed/` porque é derivado por script de base externa, como
  o `manifest-imagens.csv` da Fase 1): FC e sexo impressos, "Lead Off",
  borda. **Sem ID do exame e sem data/hora (decisão LGPD).**
- **Sexo impresso: 91% masculino** (447/491), mais que a Cleveland (68%);
  29 anormais femininas no total.

### 5ter.5 Decisões aprovadas pelo humano para a Etapa 2 (2026-09-23)

Recorte, resolução (**128×75 principal, 192×112 como comparação única
pré-declarada**) e `class_weight` aprovados. Protocolo pré-registrado e
commitado sozinho: `document/fase-02/ir-alem-2/protocolo-mlp.md` (H1–H5;
split fixo + CV 5×3; baselines majoritário e "FC impressa > 90"; controle sem
recorte; avaliação por sexo como metadado). As propostas da Etapa 1, como
foram apresentadas:

- **Pré-processamento:** recorte → tons de cinza (`L`) → redimensionar com
  `BOX` (média de área; não some com a linha de ~3 px) mantendo a razão
  1,71 → **inverter** (`1 − x/255`: traçado ≈ 1, fundo ≈ 0) → [0, 1].
  Parâmetros da 1ª camada `Dense(128)` (conferidos por `count_params`):
  64×37 → 303 mil; **128×75 → 1,23 mi**; **192×112 → 2,75 mi**;
  256×150 → 4,92 mi; 128×128 (distorce) → 2,10 mi. Treino ≈ 333 imagens:
  mesmo em 128×75 são ~3.700 parâmetros por imagem de treino → dropout e
  early stopping obrigatórios.
- **Split:** sobre as 491 únicas, ordenadas por MD5, estratificado pela
  **categoria original** (para as 30 MI não caírem todas de um lado),
  semente 42: teste 20% (99: 70 anormal / 29 normal; MI 6, PMI 17, HB 47),
  validação 15% do resto (59) para early stopping, treino 333. Zero MD5 em
  comum entre partições (verificado).
- **Desbalanceamento:** `class_weight` balanceado (normal 1,73; anormal
  0,70), **não oversampling** — oversampling duplica imagens, exatamente o
  que a deduplicação removeu.
- **Leitura dos resultados:** baseline de classe majoritária = **71,1% de
  acurácia** (sempre "anormal"): piso, não conquista. Reportar acurácia
  (exigida), acurácia balanceada, matriz de confusão, recall por classe e
  **recall de "anormal" por subcategoria (MI/PMI/HB)**. Teste com n = 99:
  IC 95% ≈ ±9 p.p. na acurácia; MI tem 6 imagens no teste.

### 5ter.6 Etapa 2C — notebook executado (2026-09-23)

`notebooks/fase-02/ir-alem-2/ir-alem-2-mlp-ecg.ipynb`, venv nova de
`requirements-ir-alem-2.txt`, kernel limpo. **Duas execuções registradas**
(protocolo, seção 3): a 1 rodou com `MPLBACKEND=Agg` no ambiente e saiu sem
figuras; a 2, sem a variável e com o código inalterado, é a salva. **As
métricas saíram idênticas nas duas.** Antes, um teste de fumaça com 1 época e
saída descartada (`levantamento.md`, seção 4). Conclusões escritas depois da
execução (seção 12 do notebook).

Resultado (CV 5×3, média ± DP): MLP-128 com acurácia 0,831 ± 0,034, BA
0,797 ± 0,028, **recall de anormal 0,878 ± 0,057**; regra FC > 90 com BA
0,819 ± 0,024 e recall de anormal 0,639. **H1 confirmada; H2 empate** (a MLP
não supera a regra em BA, mas tem recall de anormal muito maior); **H3 não
detectado** (o split fixo sugeria o contrário, e a CV desmentiu); H4 sem
diferença; **H5 confirmada** (recall HB 0,92 > PMI 0,82 > **MI 0,71**).
Exemplos antes/depois em `assets/imagens/ir-alem-2/` (8 arquivos, ~560 KB,
gerados pelo próprio notebook).

Resultados e conclusões aprovados pelo humano (2026-09-23). A seção 12 do
notebook foi reescrita depois disso **só em markdown**: as 16 células de código
(código, outputs e `execution_count`) foram conferidas idênticas por
comparação. Bloco "Ir Além 2" no `README.md`, em paralelo aos blocos das
Entregas 1 e 2, sem alterar nenhuma linha existente.

**Pendente (humano):**
- vídeo de até 4 min no YouTube (não listado) e o link no `README.md` — é o
  `TODO(humano)` da tabela de entregáveis do Ir Além 2;
- confirmação do tutor sobre o Mendeley no lugar do Kaggle (5ter.2);
- execução no Colab não testada (o notebook clona a `main`; a leitura dos
  arquivos pela `main` foi conferida por HTTP depois do push).

---

## 6. Roadmap das fases 2 a 7

Referência para não tomar decisão na Fase 1 que atrapalhe depois.

| Fase | Título | Escopo | Consome da Fase 1 |
|---|---|---|---|
| **2** | Diagnóstico Automatizado — IA no Estetoscópio Digital | Modelos de IA para identificar risco de doença; classificadores supervisionados; reflexão sobre responsabilidade da IA na medicina | **dataset numérico** |
| **3** | Monitoramento Contínuo — IoT no Peito do Paciente | Simulação de wearable médico com sensores **ESP32** em tempo real; dashboard de apresentação | esquema de variáveis (FC, PA) |
| **4** | Coração em Imagens — Diagnóstico com Visão Computacional | Sistema para interpretar imagens de exames; treinar modelos para detectar alterações suspeitas; módulos de visualização | **conjunto de imagens** |
| **5** | Suporte Digital ao Paciente — Assistente Cardiológico Virtual | Chatbot para acompanhamento domiciliar; NLP; discussão de ética e empatia no atendimento virtual | **corpus textual** |
| **6** | Coração Sob Controle — Previsão de Crises com IA | Sistema preditivo de eventos cardíacos por **séries temporais**; prever picos de risco; protocolos de emergência | dataset + dados do wearable |
| **7** | CardioIA — Plataforma de Inteligência Cardíaca Total | Integração de todos os módulos numa plataforma funcional; foco em usabilidade, fluxo de informação e arquitetura final | tudo |

> **Nota (2026-09-23):** esta tabela foi escrita antes do enunciado da Fase 2 e fica como registro. O enunciado real da Fase 2 é de **NLP** (frases de paciente, extração de sintomas, TF-IDF) e consome o **corpus textual** (Texto 2), não o dataset numérico — ver seção 5bis. Nenhum entregável obrigatório da Fase 2 modela o UCI; a primeira fase do roadmap que o consome é a **Fase 6**.

Implicações para decisões tomadas agora:

- A escolha de **ECG** como tipo de exame na Fase 1 amarra a Fase 4. ECG é boa escolha: é imagem de sinal, com padrão geométrico regular, o que facilita tanto detecção de bordas quanto CNN, e conversa diretamente com o wearable ESP32 da Fase 3.
- O `manifest.csv` das imagens com rótulo por categoria é o que vai permitir treino supervisionado na Fase 4 sem retrabalho. Fazer isso bem agora economiza dias depois.
- Manter as variáveis de frequência cardíaca e pressão arterial bem documentadas em unidades explícitas, porque a Fase 3 vai gerar leituras que precisam ser compatíveis com esse esquema.

---

## 7. Convenções técnicas

**Stack:** Python 3.12, `pandas`, `numpy`, `matplotlib`, `openpyxl`, `ucimlrepo`, `Pillow`. Notebooks compatíveis com **Jupyter e Google Colab**. Não adicionar dependência pesada sem necessidade.

**Versão do Python travada em 3.12** — paridade com o runtime padrão do Google Colab (3.12.13 à data de escrita, com `numpy` 2.0.2 e PyTorch 2.11; **TensorFlow 2.21.0 / Keras 3.13.2** conferidos no pip-freeze do Colab em 2026-09-23). TensorFlow, Keras e protobuf ficam em **`requirements-ir-alem-2.txt`** (que inclui o `requirements.txt` com `-r`), não no principal: quem só roda as Fases 1 e 2 não precisa instalar o TensorFlow. Isso importa a partir da Fase 4 (Visão Computacional), quando o projeto passa a depender de TensorFlow/PyTorch e qualquer notebook rodado localmente precisa continuar compatível com o que roda no Colab.

**Encoding:** UTF-8 em tudo. CSV com separador `,` e decimal `.`.

**Commits:** Conventional Commits com escopo de fase, descrição em pt-BR, imperativo:

```
feat(fase-01): adiciona dataset numerico tratado em csv e xlsx
docs(fase-01): documenta governanca de dados e vies das bases
chore: cria estrutura de pastas para as sete fases
```

Commits pequenos e temáticos. Não juntar coleta de dado, documentação e estrutura no mesmo commit.

**Branches:** `main` protegida na prática. Trabalho em `fase-01/<assunto>`, integrado via PR.

**Notebooks:** notebook **exploratório** tem os outputs limpos antes de commitar. Notebook **entregável** (o que o corretor avalia, ex.: `notebooks/fase-02/fase-02-tfidf-classificador-risco.ipynb`) é commitado **executado** — rodado de cima a baixo num kernel limpo — porque o corretor precisa ver os resultados no GitHub sem executar.

---

## 8. Trabalho em grupo

O repositório é compartilhado por uma equipe; quem escreveu este arquivo deu o start.

- Um documento gera um dono. Antes de reescrever seção de documento que não é da tarefa atual, **pergunte**.
- Não faça refactor amplo por iniciativa própria: conflito de merge em trabalho de grupo custa mais que o ganho estético.
- `README.md` da raiz é o arquivo de maior contenção. Alterações nele: cirúrgicas e anunciadas.

---

## 9. Checklist antes de encerrar qualquer tarefa

1. Cumpri as regras invioláveis da seção 4?
2. Todo dado novo tem proveniência, licença e data de acesso registradas?
3. Todo link que eu não verifiquei está marcado como `TODO(humano)` e listado na minha resposta?
4. Se a fase avançou de estado, atualizei a tabela da seção 2?
5. Listei explicitamente o que ficou pendente para o humano fazer?
