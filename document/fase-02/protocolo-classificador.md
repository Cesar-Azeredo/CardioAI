# Protocolo pré-registrado do classificador de risco — Fase 2, Parte 2

> **Estado: pré-registrado em 2026-09-23, antes de qualquer treino ou
> resultado.** Este arquivo é commitado sozinho, antes do notebook, para o
> histórico mostrar a ordem. Hipóteses e decisões abaixo não mudam depois de
> ver resultado. Simulação acadêmica, sem validade para decisão médica.

Dados (congelados, SHA-256 conferido por
`scripts/fase-02/06_verifica_dataset_risco.py`):

- treino e avaliação: `document/datasets/fase-02/frases-rotuladas-risco.csv`
  — 80 frases, 40 `alto risco` / 40 `baixo risco`;
- conjunto-desafio, **fora do treino**:
  `document/datasets/fase-02/desafio-risco.csv` — 18 frases com rótulo
  esperado pré-registrado;
- critério de rótulo: `document/fase-02/criterio-rotulo-risco.md`.

Notebook: `notebooks/fase-02/fase-02-tfidf-classificador-risco.ipynb`.

**Declaração de conhecimento prévio.** O dataset e o desafio foram escritos
pelo mesmo grupo que escreve estas hipóteses, sabendo delas (o desafio foi
desenhado para sondá-las). Isso é circularidade de autoria: um resultado
favorável no treino não prova generalização para relato real de paciente.

## 1. Hipóteses

| # | Hipótese | Conjunto | Critério de decisão (fixado antes) |
|---|---|---|---|
| H1 | **Negação.** TF-IDF é saco de palavras: frase com sinal de alerta **negado** tende a ser classificada como alto risco (falso positivo) | 3 frases `desafio-negacao` (rótulo esperado: baixo risco) | **confirmada** se ≥ 2 das 3 saírem `alto risco` |
| H2 | **Atípico.** Frase de infarto **sem "dor"** tende a baixo risco — **falso negativo, o erro perigoso**. Hipótese pendente desde a frase 10 da Parte 1 | 3 frases `desafio-atipico` (esperado: alto risco); o par G1 (atípico, sem dor) é reportado junto, à parte | **confirmada** se ≥ 2 das 3 `desafio-atipico` saírem `baixo risco` |
| H3 | **Gênero.** Os pares contrafactuais G1–G3 podem receber predições ou probabilidades diferentes | 3 pares `desafio-genero` | por par: **aprovado** se a predição é idêntica e a comparação é informativa (regra 2.h); **reprovado** se a predição difere; **inconclusivo** se as palavras que diferem estão fora do vocabulário |
| H4 | **Zona cinzenta.** Sem resposta certa | 3 frases `desafio-zona` (rótulo `indefinido`) | **só descrição**: predição e probabilidade de alto risco de cada frase; nada é contado como acerto ou erro |
| H5 | **Vocabulário novo.** Sinal de alerta em palavras ausentes do treino tende a falhar | 3 frases `desafio-vocabulario` (esperado: alto risco) | **confirmada** se ≥ 2 das 3 saírem `baixo risco` |

## 2. Decisões de método

**a) Pré-processamento: minúsculas e remoção de acentos, SEM remoção de
stopwords.** `TfidfVectorizer(lowercase=True, strip_accents="unicode",
stop_words=None)`. A lista de stopwords do português da NLTK (207 palavras)
contém **`não`, `nem` e `sem`** — verificado em 2026-09-23 e verificado de
novo no notebook, seção 4. Removê-la apagaria a negação, e H1 falharia pelo
pré-processamento, não pelo modelo. O IDF já reduz o peso das palavras
frequentes. Tokenização padrão do scikit-learn (`token_pattern` padrão,
palavras de 2 ou mais caracteres — descarta "é", "e", "a", "o"; nenhum
marcador de negação tem 1 caractere). Sem radicalização: o notebook testa o
TF-IDF como o enunciado pede, não o método do extrator.

**b) Pipeline do scikit-learn** (`Pipeline([TfidfVectorizer, classificador])`):
o vetorizador é ajustado **dentro** de cada divisão de treino. Ajustar o
TF-IDF nas 80 frases antes do split vazaria vocabulário e pesos IDF para o
teste — mesma família de erro da deduplicação antes do split da Fase 1.

**c) Modelo principal: `LogisticRegression(random_state=42, max_iter=1000)`**,
demais parâmetros no padrão (sem busca de hiperparâmetro — 80 frases não
sustentam busca sem sobreajuste). Escolhido por ser interpretável pelos
coeficientes. **Baseline: `DummyClassifier(strategy="most_frequent")`**,
que chuta sempre a mesma classe — o piso de 50% de acurácia neste dataset
balanceado (com 40/40, a classe "mais frequente" é a primeira na ordem, e o
recall de alto risco do baseline é 0 ou 1 conforme essa ordem; o notebook
mostra qual). Toda acurácia é lida contra esse piso.

**d) Avaliação em duas camadas.**

- **Split estratificado fixo 75/25** (`train_test_split`, `stratify`,
  `random_state=42`): 60 frases de treino, 20 de teste. Matriz de confusão e
  relatório por classe — é o que o enunciado pede e o que vai para o vídeo.
- **Validação cruzada estratificada repetida**
  (`RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)`):
  média e desvio-padrão de cada métrica, para mostrar quanto o número do split
  único oscila. Com 80 frases, o split deixa só 20 no teste; cada frase vale 5
  pontos percentuais de acurácia.

**e) Métricas.** Acurácia (o enunciado pede); **recall de `alto risco` como
métrica principal**, pela assimetria de custo documentada na Fase 1 (falso
negativo em triagem cardiológica = paciente mandado para casa durante um
evento); precisão e F1 de cada classe; matriz de confusão. **Toda frase de
alto risco classificada como baixo risco é listada por extenso**: as do teste
do split fixo e, para cobrir as 80, as da predição fora-da-dobra de uma
validação estratificada de 5 dobras (`StratifiedKFold(5, shuffle=True,
random_state=42)`).

**f) Interpretação.** Modelo ajustado nas 80 frases; os **15 maiores
coeficientes de cada classe**, cada termo classificado por regra fixa:

- **sinal clínico** — palavra da lista de sinal clínico do critério (seção 5:
  `repente`, `ar`, `peso`, `fala`) ou palavra de conteúdo de algum termo do
  mapa de conhecimento (`Sintoma 1`/`Sintoma 2`);
- **atalho de estilo** — palavra da lista de estilo do critério (seção 5:
  `senti`, `meio`, `hora`, `esquerdo`, `doi`, `dolorido`, `toda`);
- **negação** — `nao`, `nem`, `nunca`, `sem`, `nenhum`, `nenhuma`;
- **fora das listas** — qualquer outro; discutido no texto, sem
  reclassificação automática.

Comparação feita sem acento, como o vetorizador vê o termo.

**g) Desafio.** Modelo final ajustado nas 80 frases e aplicado às 18 do
desafio. Resultado por categoria (`tipo_frase`), com a probabilidade de alto
risco de cada frase. H1, H2, H4 e H5 decididas pelos critérios da seção 1.

**h) Contrafactual — regra crítica.** Para cada par G1–G3, o notebook
reporta: (1) as duas predições; (2) as duas probabilidades de alto risco e a
diferença; (3) para **cada palavra que difere** entre os lados (depois do
pré-processamento), se ela está no vocabulário de treino do modelo final.
Se **todas** as palavras que diferem estiverem **fora** do vocabulário, o
TF-IDF as ignora: as duas frases viram o mesmo vetor e as predições saem
idênticas **por cegueira, não por justiça** — o par é **INCONCLUSIVO** e é
reportado assim, **não** como aprovação. Se ao menos uma palavra que difere
estiver no vocabulário, a comparação é informativa: predição idêntica =
aprovado; diferente = reprovado.

**i) Análises secundárias pré-declaradas** (não substituem o modelo principal):

- **unigramas × unigramas+bigramas** (`ngram_range=(1, 1)` × `(1, 2)`), na
  mesma validação cruzada repetida e nas 3 frases de H1, para testar se
  bigramas como "nao sinto" e "sem dor" mitigam H1;
- **recall e precisão de alto risco em três limiares fixos — 0,5 / 0,4 /
  0,3** — sobre a probabilidade fora-da-dobra de cada uma das 10 repetições
  da validação cruzada (média e desvio-padrão), para mostrar o trade-off de
  triagem. **Nenhum limiar é "escolhido" com base no resultado**; o modelo
  principal usa 0,5.

## 3. Execução e desvios

- Notebook executado **uma vez**, de cima a baixo, num kernel limpo
  (`jupyter nbconvert --execute`), numa venv nova criada a partir do
  `requirements.txt`, e salvo **com os outputs** (notebook entregável: o
  corretor precisa ver os resultados no GitHub sem executar).
- Hipótese, critério e decisão desta página **não mudam** depois de ver
  resultado.
- Bug de código (o notebook não faz o que este protocolo diz): corrige-se,
  roda-se de novo, e **as duas execuções são registradas**.
- Semente fixa (`42`) em split, validação cruzada e modelo.
- No Colab, os CSVs são lidos da URL raw do GitHub na branch `main`
  (`https://raw.githubusercontent.com/Cesar-Azeredo/CardioAI/main/...`); os
  SHA-256 são conferidos contra os congelados — divergência gera **aviso**,
  não interrompe.
