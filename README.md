# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto

CardioIA: A Nova Era da Cardiologia Inteligente

## Nome do grupo

Grupo Zion

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/cesar-azeredo">Cesar Martinho de Azeredo — RM568140</a>
- <a href="https://www.linkedin.com/in/carlos-costato/">Carlos Alberto Florindo Costato — RM567005</a>
- <a href="https://www.linkedin.com/in/phellype-massarente-13739810a/">Phellype Matheus Giacoia Flaibam Massarente — RM566826</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Andre Godoy</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Ana Cristina dos Santos</a>


## 📜 Descrição

Este repositório é o **monorepo incremental do CardioIA**: reúne as entregas de todas as fases do projeto, e as fases posteriores reaproveitam o que as anteriores produziram. Cada entrega tem seu bloco próprio neste README — [Entrega 1 (Fase 1 — Batimentos de Dados)](#-escopo-da-entrega-1-fase-1) e [Entrega 2 (Fase 2 — Diagnóstico Automatizado)](#-entrega-2--fase-2-diagnóstico-automatizado-ia-no-estetoscópio-digital).

O CardioIA e um projeto academico que conecta tecnologia, ciencia de dados e saude para simular o ecossistema de uma cardiologia moderna. A proposta integra dados clinicos, modelos de Machine Learning, Visao Computacional, IoT e agentes inteligentes para apoiar triagem, diagnostico, monitoramento, assistencia remota e previsoes medicas.

Esta primeira etapa corresponde a Fase 1 - Batimentos de Dados: Mapeando o Coracao Moderno. Nela, o grupo assume o papel de cientista de dados hospitalar para levantar, organizar e compreender dados cardiologicos que servirao de base para as proximas fases do projeto.

O foco da entrega e montar uma base inicial robusta com pensamento critico, considerando desde ja principios de Governanca de Dados, qualidade dos dados, vies e privacidade. A dificuldade em encontrar dados publicos, especialmente em saude, faz parte do processo real de projetos de IA. Por isso, persistencia, criatividade e combinacao de fontes (incluindo dados simulados quando necessario) sao elementos esperados nesta fase.

> Governanca de dados e vies desta entrega, com numeros medidos (nao estimados) para cada uma das quatro bases: [`document/fase-01/governanca-e-vies.md`](document/fase-01/governanca-e-vies.md).

### Objetivo geral da Entrega 1

Buscar e preparar tres tipos de dados fundamentais para uso futuro no projeto:

1. Dados numericos (simulados ou reais) relacionados a pacientes cardiacos.
2. Dados textuais medicos ou literarios relacionados a saude cardiovascular.
3. Dados visuais medicos representando exames ou sinais do coracao.

### Mapa mental da jornada (7 fases)

Referencia apresentada no enunciado:

- [Mapa mental — CardioIA: A Nova Era da Cardiologia Inteligente](assets/mapa-mental/imagem-mapa-mental.png)

## ✅ Escopo da Entrega 1 (Fase 1)

### Parte 1 - Dados Numericos (IoT)

- Montar dataset com minimo de 100 linhas.
- Incluir variaveis como: idade, sexo, pressao arterial, colesterol, historico cardiaco, sintomas, frequencia cardiaca, entre outras.
- Disponibilizar link publico para os dados completos (OneDrive, Google Drive ou similar).
- Explicar no README a origem dos dados (reais ou simulados).
- Justificar as variaveis clinicamente mais relevantes para IA em saude.

**Entregue**: UCI Heart Disease, base Cleveland — dado real (nao simulado), 303 pacientes, licenca CC BY 4.0. Variaveis mais relevantes clinicamente: tipo de dor toracica, frequencia cardiaca maxima, depressao do segmento ST, numero de vasos por fluoroscopia (maior poder discriminativo nesta base), alem dos fatores de risco classicos (idade, sexo, colesterol, pressao em repouso). Justificativa individual de cada variavel e as decisoes de tratamento (auséncias preservadas, alvo em duas formas) em [`document/fase-01/dados-numericos.md`](document/fase-01/dados-numericos.md). Dados completos (CSV + XLSX) tambem no [Google Drive](https://drive.google.com/drive/folders/1eTMQ1dnlVJRoTAAd39kqipLyDX-iuLCB?usp=drive_link).

### Parte 2 - Dados Textuais (NLP)

- Baixar no minimo 2 textos em formato .txt sobre doencas cardiacas, saude publica, sintomas ou tratamentos.
- Usar fontes confiaveis, como SciELO, BVS, SUS ou Projeto Gutenberg.
- Armazenar os textos em subpasta do repositorio (assets ou docs/document).
- Explicar como os textos poderao ser usados em NLP:
    - analise de sentimentos
    - extracao de sintomas
    - classificacao de topicos
- Justificar relevancia dessas analises no contexto de IA aplicada a saude.

**Entregue**: 2 textos em `assets/textos/` — um tecnico-cientifico (SciELO, Arquivos Brasileiros de Cardiologia, 1.608 palavras, CC BY-NC 3.0) e um de comunicacao em saude publica (Ministerio da Saude, 858 palavras, CC BY-ND 3.0). O contraste de registro entre os dois e o proprio exemplo do problema que a Fase 5 (chatbot) precisa resolver: traduzir termo clinico para linguagem de paciente. Analise de sentimento nao se aplica a nenhum dos dois (nenhum e relato de paciente) — o corpus serve de baseline de vocabulario. Detalhe das 3 tecnicas de NLP com exemplo real de cada texto em [`document/fase-01/dados-textuais.md`](document/fase-01/dados-textuais.md). Textos disponiveis tanto versionados em `assets/textos/` quanto no [Google Drive](https://drive.google.com/drive/folders/1IKF4nawS7BT8J5obI0AqoAviMeqFcsh1?usp=drive_link).

### Parte 3 - Dados Visuais (Visao Computacional)

- Reunir no minimo 100 imagens (.jpg ou .png) de exames cardiologicos (ECG, angiograma, raio-X toracico etc.).
- Disponibilizar link publico para o conjunto completo de imagens.
- Explicar possibilidades de analise por Visao Computacional:
    - deteccao de padroes
    - identificacao de bordas
    - reconhecimento de anomalias
- Destacar importancia dessas analises para solucoes de IA em saude.

**Entregue**: ECG Images dataset of Cardiac Patients v2 (Mendeley Data, CC BY 4.0). Do dataset completo (928 arquivos), apenas 491 sao imagens de conteudo unico por hash MD5 (47% de redundancia, medida nao estimada) — deduplicado antes de qualquer amostragem. Selecao final: 120 imagens, balanceadas 30/30/30/30 por categoria, semente fixa, sem recompressao. Justificativa de deteccao de bordas/padroes/anomalias e o achado de *shortcut learning* (hash raso confundiu template do aparelho com conteudo clinico) em [`document/fase-01/dados-visuais.md`](document/fase-01/dados-visuais.md). Conjunto completo de 120 imagens no [Google Drive](https://drive.google.com/drive/folders/12YhReksoB8K-aWQsubtUIaEx4zK9EuF3?usp=drive_link).

## 📦 Entregaveis obrigatorios

O repositorio deve conter:

1. README.md detalhado com descricao da fase, objetivos, fontes e justificativas das tres partes.
2. Subpasta com conteudos textuais (assets e/ou document).
3. Links publicos acessiveis com os conjuntos completos de dados numericos e visuais.

Status: os 3 itens entregues (documentacao completa em `document/fase-01/`; textos em `assets/textos/`; links publicos na secao "Links publicos da Entrega 1" acima).

## ⚠️ Orientacoes importantes da atividade

- Verificar o arquivo antes do upload final (nao e possivel reenviar apos fechamento/correcao).
- Nao deixar envio para os ultimos minutos do prazo.
- Nao compartilhar respostas em grupos para evitar plagio.
- Prazo de ate 15 dias apos publicacao da nota para solicitar revisao.

## 🧭 Boas praticas para esta fase

- Priorizar fontes eticas e legais para dados de saude.
- Registrar claramente se os dados sao reais, anonimizados ou simulados.
- Organizar desde ja a estrutura para notebooks futuros (Colab/Jupyter).
- Manter padrao de nomes e versionamento dos arquivos de dados.

## 📊 Criterios de avaliacao (10 pontos)

1. Dataset numerico entregue corretamente, organizado e explicado - 3 pontos.
2. Textos selecionados e contextualizados corretamente - 2 pontos.
3. Imagens entregues e bem justificadas em seu potencial para analise por IA - 2 pontos.
4. Documento resumo com explicacoes claras, objetivas e bem estruturadas - 2 pontos.
5. Cumprimento das orientacoes gerais e prazo de entrega - 1 ponto.

## 🗂 Organização dos dados da Entrega 1

Organizacao adotada (dentro do padrao atual do template, sem pastas novas na raiz):

- assets/textos/ -> arquivos .txt da Parte 2 (NLP)
- assets/imagens/amostras/ -> ~12 imagens de amostra da Parte 3; conjunto completo hospedado externamente (ver assets/imagens/LEIA-ME.md)
- assets/mapa-mental/ -> SVG/PNG do mapa mental da jornada de 7 fases
- document/datasets/raw/ e document/datasets/processed/ -> dataset numerico (Parte 1), bruto e tratado (.csv e .xlsx)
- document/datasets/README.md -> proveniencia (fonte, URL, DOI, licenca, data de acesso) das tres bases
- document/fase-01/ -> documentos tecnicos da fase (dados numericos, textuais, visuais, governanca e vies)
- document/ai_project_document_fiap.md -> documento resumo avaliado pela rubrica
- links publicos no README -> dados completos (numericos e visuais)

## 🔗 Links publicos da Entrega 1

Pasta-mae com todo o conteudo da Fase 1 no Google Drive:
[CardioIA - Fase 1](https://drive.google.com/drive/folders/1kKpAlFfaA06UMaPxirurEwRaDQi6ySbg?usp=drive_link)

- **Dataset numerico — CSV e XLSX** (303 linhas, os dois formatos na mesma pasta):
  [Google Drive](https://drive.google.com/drive/folders/1eTMQ1dnlVJRoTAAd39kqipLyDX-iuLCB?usp=drive_link)
- **Imagens** (120 selecionadas, ~76 MB):
  [Google Drive](https://drive.google.com/drive/folders/12YhReksoB8K-aWQsubtUIaEx4zK9EuF3?usp=drive_link)
- **Fontes textuais (.txt)**: disponiveis de duas formas — versionadas neste repositorio em `assets/textos/`, e tambem no
  [Google Drive](https://drive.google.com/drive/folders/1IKF4nawS7BT8J5obI0AqoAviMeqFcsh1?usp=drive_link) (util para quem preferir baixar sem clonar o repositorio).


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.
  - <b>assets/textos/</b>: os 2 arquivos `.txt` da Parte 2 (NLP).
  - <b>assets/imagens/amostras/</b>: ~12 imagens de amostra da Parte 3 (o conjunto completo de 120 fica hospedado externamente — ver `assets/imagens/LEIA-ME.md`).
  - <b>assets/mapa-mental/</b>: SVG/PNG do mapa mental da jornada de 7 fases.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto. Não usado na Fase 1; reservado para parâmetros de sensores simulados (Fase 3) e de modelos preditivos (Fase 6).

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.
  - <b>document/datasets/</b>: dataset numérico bruto e tratado (`raw/`, `processed/`), dicionário de dados e tabela de proveniência das quatro bases.
  - <b>document/fase-01/</b>: documentação técnica da Fase 1 — dados numéricos, textuais, visuais, governança e viés, e autoavaliação contra a rubrica.

- <b>notebooks</b>: notebooks de EDA/exploração, organizados por fase (`notebooks/fase-01/` reservado para a Fase 1).

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.
  - <b>scripts/fase-01/</b>: os 5 scripts reprodutíveis desta entrega (coleta, perfilamento e tratamento do dataset numérico, preparação dos textos, organização das imagens) — ver "Como executar o código" abaixo.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

**Pré-requisitos**: Python 3.12 (versão travada para paridade com o runtime do Google Colab — ver seção 7 do `CLAUDE.md`/`AGENTS.md`).

```bash
# 1. Criar e ativar um ambiente virtual
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Instalar as dependências travadas
pip install -r requirements.txt
```

**Fase 1 — Batimentos de Dados**, nesta ordem:

```bash
# Parte 1 — dataset numérico (UCI Heart Disease)
python scripts/fase-01/01_coleta_dataset_numerico.py
python scripts/fase-01/02_perfila_dataset_numerico.py
python scripts/fase-01/03_trata_dataset_numerico.py

# Parte 2 — textos (SciELO + Ministério da Saúde)
python scripts/fase-01/04_prepara_textos.py

# Parte 3 — imagens de ECG (Mendeley Data)
# pré-requisito: dataset já baixado e descompactado fora do repositório
# (ver cabeçalho do script para o caminho esperado)
python scripts/fase-01/05_organiza_imagens.py
```

Cada script imprime um relatório da execução (contagens, validações,
decisões aplicadas) e é idempotente — pode ser rodado de novo sem
efeito colateral. Detalhe de cada etapa em `document/fase-01/`.


## 🩺 Entrega 2 — Fase 2: Diagnóstico Automatizado (IA no Estetoscópio Digital)

> ⚠️ **Simulação acadêmica, sem validade clínica.** Frases, rótulos e mapa de conhecimento são sintéticos ou derivados de páginas públicas do Ministério da Saúde. Nada nesta entrega serve para triagem, diagnóstico ou decisão médica real.

Um paciente descreve o que sente; o sistema **extrai os sintomas** e sugere um diagnóstico (Parte 1) e **classifica o risco** da frase em alto ou baixo (Parte 2). As regras do extrator e as hipóteses do classificador foram **pré-registradas antes de qualquer resultado** e congeladas por SHA-256.

### 📦 Entregáveis da Entrega 2

| Entregável (enunciado) | Arquivo |
|---|---|
| `.txt` com 10 frases de sintomas relatados por pacientes | [`assets/textos/fase-02/frases-sintomas-pacientes.txt`](assets/textos/fase-02/frases-sintomas-pacientes.txt) |
| `.csv` com o mapa de conhecimento sintoma → doença | [`document/datasets/fase-02/mapa-conhecimento-sintomas.csv`](document/datasets/fase-02/mapa-conhecimento-sintomas.csv) |
| Código Python que lê as frases, extrai sintomas e sugere diagnóstico | [`scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py`](scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py) — resultado em [`document/fase-02/resultado-extrator.md`](document/fase-02/resultado-extrator.md) |
| `.csv` com frases e rótulos (alto/baixo risco) | [`document/datasets/fase-02/frases-rotuladas-risco.csv`](document/datasets/fase-02/frases-rotuladas-risco.csv) |
| `.ipynb` com TF-IDF, classificação e avaliação | [`notebooks/fase-02/fase-02-tfidf-classificador-risco.ipynb`](notebooks/fase-02/fase-02-tfidf-classificador-risco.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Cesar-Azeredo/CardioAI/blob/main/notebooks/fase-02/fase-02-tfidf-classificador-risco.ipynb) |
| Repositório público | [github.com/Cesar-Azeredo/CardioAI](https://github.com/Cesar-Azeredo/CardioAI) |
| Vídeo no YouTube (não listado), até 4 min | > ⚠️ TODO(humano): colar aqui o link público do vídeo no YouTube (não listado) |

Fontes, critério de rótulo e decisões: [mapa e frases](document/datasets/fase-02/README.md) · [critério de rótulo](document/fase-02/criterio-rotulo-risco.md) · [governança e viés](document/fase-02/governanca-e-vies.md) · [autoavaliação](document/fase-02/autoavaliacao.md).

### 📊 Resultados

**Parte 1 — extrator** ([protocolo](document/fase-02/protocolo-extrator.md) · [resultado](document/fase-02/resultado-extrator.md) · [gabarito](document/fase-02/gabarito-frases.md)). Nas 10 frases de teste, o casamento exato (baseline) acertou **8/10** e o método (RSLP + proximidade + negação) **9/10**. Nas 7 frases não contaminadas pelo conhecimento prévio, **empate em 6/7**: a melhora vem inteira da frase 3, que já se sabia falhar no casamento exato — não é evidência de que o método generaliza.

**Parte 2 — classificador** ([protocolo](document/fase-02/protocolo-classificador.md) · [notebook](notebooks/fase-02/fase-02-tfidf-classificador-risco.ipynb)). Baseline (chuta sempre a mesma classe): acurácia **0,50**. TF-IDF + regressão logística na validação cruzada 5×10: acurácia **0,812 ± 0,084** e **recall de alto risco 0,828 ± 0,143** (métrica principal, pela assimetria de custo da Fase 1). O split fixo 75/25 deu 0,85 — caiu do lado bom da variação.

**Distorções encontradas** (detalhe na seção 9 do notebook):
- **"mas" é o critério de rótulo vazando para a sintaxe:** aparece em 0 frases de alto risco e 10 de baixo; o modelo aprendeu que quem relativiza o sintoma está bem, e o falso negativo perigoso é um paciente que minimizou ("…mas não dói nada").
- **"eu" é efeito Clever Hans:** 7 frases de alto risco, 0 de baixo; um acerto do desafio veio desse pronome, não do sinal clínico.
- **Erro concentrado em AVC:** 4 dos 7 falsos negativos são de AVC; recall 0,783 em sinais de AVC contra 0,864 em sinais de infarto (sem poder estatístico com n de 22 e 23).
- **Teste contrafactual de gênero:** os 3 pares tiveram predição idêntica, mas em cada par a palavra de gênero de um dos lados está fora do vocabulário — a aprovação é fraca ([critério, seção 6](document/fase-02/criterio-rotulo-risco.md)).

### 🔧 Como executar a Entrega 2

Pré-requisito: Python 3.12.

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1. Verificadores (mapa, frases, protocolos e dataset — congelados por SHA-256)
python scripts/fase-02/01_verifica_mapa_e_frases.py
python scripts/fase-02/06_verifica_dataset_risco.py

# 2. Extrator nas 10 frases (regenera document/fase-02/resultado-extrator.md)
python scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py
#    ou numa frase avulsa (só imprime):
python scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py --frase "Estou com dor no peito e suando frio"

# 3. Testes do extrator (U1–U14 pré-registrados + U15 adicionado depois)
python scripts/fase-02/03_testa_extrator.py
python scripts/fase-02/04_testa_extrator_adendo.py

# 4. Notebook do classificador, executado de ponta a ponta
jupyter nbconvert --to notebook --execute notebooks/fase-02/fase-02-tfidf-classificador-risco.ipynb --output /tmp/notebook-executado.ipynb
```

Os recursos da NLTK (stemmer RSLP e stopwords) são baixados pelo extrator para `.cache/nltk_data` e conferidos por SHA-256. **No Google Colab:** abra o notebook pelo badge acima — ele detecta o Colab e lê os CSVs direto do GitHub (branch `main`).


## 🫀 Ir Além 2 — Diagnóstico visual de ECG com rede neural (MLP em Keras)

> ⚠️ **Simulação acadêmica, sem validade clínica.** As imagens vêm de uma base pública de um único aparelho, hospital e país. Nada nesta entrega serve para triagem, diagnóstico ou decisão médica real.

Entrega extra da Fase 2 (não faz parte da atividade principal). Uma **MLP em Keras** classifica imagens de eletrocardiograma em **normal** ou **anormal**, depois de pré-processá-las (recorte, tons de cinza, redimensionamento para 128×75, normalização para [0, 1]). As hipóteses foram **pré-registradas antes de qualquer treino** ([protocolo](document/fase-02/ir-alem-2/protocolo-mlp.md)).

### 📦 Entregáveis do Ir Além 2

| Entregável (enunciado) | Arquivo |
|---|---|
| Notebook comentado e funcional | [`notebooks/fase-02/ir-alem-2/ir-alem-2-mlp-ecg.ipynb`](notebooks/fase-02/ir-alem-2/ir-alem-2-mlp-ecg.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Cesar-Azeredo/CardioAI/blob/main/notebooks/fase-02/ir-alem-2/ir-alem-2-mlp-ecg.ipynb) |
| Exemplos de imagens | [`assets/imagens/ir-alem-2/`](assets/imagens/ir-alem-2/) — 4 pares antes/depois do pré-processamento, um por categoria |
| README explicativo | este bloco · [levantamento dos dados](document/fase-02/ir-alem-2/levantamento.md) · [protocolo](document/fase-02/ir-alem-2/protocolo-mlp.md) |
| Vídeo no YouTube (não listado), até 4 min | > ⚠️ TODO(humano): colar aqui o link público do vídeo do Ir Além 2 no YouTube (não listado) |

### 🗂 Dataset: por que o Mendeley, e não o Kaggle

Usamos o *ECG Images dataset of Cardiac Patients*, v2, do Mendeley Data (DOI [10.17632/gwbz3fsgp8.2](https://doi.org/10.17632/gwbz3fsgp8.2), CC BY 4.0), a mesma base de imagens da Entrega 1, **no lugar** do `shayanfazeli/heartbeat` do Kaggle recomendado no enunciado. O dataset do Kaggle é de **sinais segmentados em CSV**, não de imagens: não há o que redimensionar nem converter para tons de cinza, e o critério de avaliação pede o pré-processamento correto das imagens. As imagens do Mendeley cumprem o texto do enunciado e reaproveitam a auditoria de duplicatas da Entrega 1.

> ⚠️ **Pendência:** confirmar com o tutor se a substituição é aceita. Se o Kaggle for exigido, o plano B é desenhar cada sinal do CSV como imagem e então pré-processá-la.

Cuidados com o dado, todos por script e documentados no [levantamento](document/fase-02/ir-alem-2/levantamento.md):
- **Deduplicação por MD5:** dos 928 arquivos, só **491 imagens são únicas** (47% de cópias exatas). O split é feito sobre as únicas; sem isso, a mesma imagem cairia no treino e no teste.
- **Texto impresso removido por recorte:** cada imagem traz a frequência cardíaca impressa no rodapé, e **nenhuma imagem normal passa de 90 bpm**. A regra "FC impressa > 90 → anormal" é um atalho que a rede poderia aprender lendo o número em vez do traçado. O recorte fica só com a grade do traçado.
- **Binário:** normal = 142; anormal = infarto (30) + histórico de infarto (86) + batimento anormal (233) = 349. Base **91% masculina**.

### 📊 Resultados

Validação cruzada estratificada 5 dobras × 3 repetições sobre as 491 imagens únicas (média ± desvio-padrão). A **métrica principal é o recall de anormal**: o erro perigoso é o ECG anormal classificado como normal.

| Modelo | Acurácia | Acurácia balanceada | **Recall anormal** | Recall normal |
|---|---|---|---|---|
| Baseline (a): classe majoritária | 0,711 | 0,500 | 1,000 | 0,000 |
| Baseline (b): regra "FC impressa > 90" | 0,743 ± 0,034 | 0,819 ± 0,024 | 0,639 ± 0,049 | 1,000 |
| **MLP 128×75 com recorte** | **0,831 ± 0,034** | 0,797 ± 0,028 | **0,878 ± 0,057** | 0,716 ± 0,061 |

Recall de anormal por subcategoria (MLP): batimento anormal 0,920 · histórico de infarto 0,822 · **infarto 0,711**. Detalhes, split fixo, matriz de confusão, controle sem recorte e recorte por sexo: [notebook, seções 8 a 12](notebooks/fase-02/ir-alem-2/ir-alem-2-mlp-ecg.ipynb).

- **Um split único engana.** No split fixo, a versão **sem recorte** parecia muito melhor (0,920 contra 0,844 de acurácia balanceada). Na validação cruzada, a diferença some (−0,004 ± 0,031). Com um único split, a conclusão seria a errada: "a rede lê o rodapé".
- **Acurácia balanceada × clínica.** Pelo critério pré-registrado, a MLP **não superou** a regra do texto impresso na acurácia balanceada (empate). Mas essa métrica pesa falso negativo e falso positivo igualmente, e a clínica não. A regra nunca erra um normal, mas perde 36% dos anormais e pega só 0,23 dos infartos; a MLP pega 0,71. No recall de anormal, a MLP é muito superior (0,878 × 0,639). *(Interpretação pós-execução.)*
- **O modelo erra mais onde há menos dado:** no infarto, com 30 imagens únicas (recall 0,711), e nas mulheres, com 44 imagens, das quais metade das normais sai como anormal. Com n = 15 normais femininas, isso é hipótese, não conclusão. É o mesmo padrão da base Cleveland da Entrega 1 (68% masculina); esta base é 91% masculina.

### 🔧 Como executar o Ir Além 2

Pré-requisito: Python 3.12. O TensorFlow fica num arquivo de dependências separado, para quem roda só as Entregas 1 e 2 não precisar instalá-lo.

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-ir-alem-2.txt   # inclui o requirements.txt + TensorFlow 2.21.0 / Keras 3.13.2

# Notebook de ponta a ponta (baixa o zip do Mendeley, ~194 MB, para ~/.cache/cardioia/)
jupyter nbconvert --to notebook --execute notebooks/fase-02/ir-alem-2/ir-alem-2-mlp-ecg.ipynb --output /tmp/ir-alem-2-executado.ipynb

# Opcional: scripts de preparação (o manifest já está versionado)
python scripts/fase-02/ir-alem-2/01_baixa_ecg_mendeley.py
python scripts/fase-02/ir-alem-2/02_deduplica_e_monta_binario.py
python scripts/fase-02/ir-alem-2/03_audita_texto_impresso.py
```

**No Google Colab:** abra o notebook pelo badge acima. Ele detecta o Colab, clona o repositório (branch `main`) e baixa as imagens pelo mesmo script de download. Os resultados podem diferir levemente entre a CPU local e a GPU do Colab.


## 🗃 Histórico de lançamentos

* 0.5.0 - XX/XX/2024
    * 
* 0.4.0 - XX/XX/2024
    * 
* 0.3.0 - XX/XX/2024
    * 
* 0.2.0 - 23/09/2026
    * Fase 2 — Diagnóstico Automatizado: 10 frases de teste e mapa de conhecimento (3 doenças, 53 linhas, fontes do Ministério da Saúde), extrator de sintomas com protocolo pré-registrado, dataset rotulado de 80 frases com conjunto-desafio, e notebook TF-IDF + regressão logística com hipóteses pré-registradas e análise das distorções.
* 0.1.0 - 27/08/2026
    * Fase 1 — Batimentos de Dados: dataset numérico (UCI Heart Disease, 303 pacientes), corpus textual (2 textos, técnico + leigo) e conjunto de imagens de ECG (120 selecionadas de 928, deduplicadas) coletados, tratados e documentados, com governança de dados e viés registrados.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


