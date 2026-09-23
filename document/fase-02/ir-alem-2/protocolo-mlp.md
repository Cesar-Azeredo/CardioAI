# Protocolo pré-registrado da MLP sobre imagens de ECG — Ir Além 2

> **Estado: pré-registrado em 2026-09-23, antes de qualquer treino ou
> resultado.** Este arquivo é commitado sozinho, antes do notebook, para o
> histórico mostrar a ordem. Hipóteses, critérios e decisões abaixo não
> mudam depois de ver resultado. Simulação acadêmica, sem validade para
> decisão médica.

Entrega extra da Fase 2 (não faz parte da atividade principal). Contexto,
enunciado resumido e decisão de dataset: `AGENTS.md`, seção 5ter.

**Dados.** Mendeley Data, *ECG Images dataset of Cardiac Patients*, v2, DOI
`10.17632/gwbz3fsgp8.2`, CC BY 4.0 — a mesma base da Fase 1 (proveniência em
`document/datasets/README.md`). O zip é baixado fora do repositório por
`scripts/fase-02/ir-alem-2/01_baixa_ecg_mendeley.py`. A unidade de análise
são as **491 imagens únicas por MD5** (script 02), listadas em
`document/datasets/processed/manifest-ir-alem-2.csv`, com FC e sexo impressos
lidos pelo script 03 (validação da leitura: 43 imagens conferidas à mão,
0 erro em 86 campos — ver `levantamento.md`).

**Problema binário.** `anormal` = MI + PMI + HB (30 + 86 + 233 = 349),
classe positiva (rótulo 1); `normal` = 142 (rótulo 0).

**Notebook:** `notebooks/fase-02/ir-alem-2/ir-alem-2-mlp-ecg.ipynb`.

**Declaração de conhecimento prévio.** Antes deste protocolo, o grupo já
olhou as 491 imagens inteiras, incluindo as que vão cair no teste: mediu o
layout e leu a FC impressa. Nenhum modelo foi treinado. O limiar da regra de
atalho (90 bpm, seção 2.f) **veio dessa leitura das 491**, então o baseline
(b) é **otimista**: é o melhor que o atalho consegue com o limiar conhecido.
Ele não é reajustado por dobra.

## 1. Hipóteses

"CV" = validação cruzada da seção 2.d (15 dobras). "BA" = acurácia
balanceada (média dos recalls das duas classes). "Diferença pareada" =
métrica do modelo A menos a do modelo B **na mesma dobra**, com média e
desvio-padrão (DP) nas 15 dobras.

| # | Hipótese | Comparação | Critério de decisão (fixado antes) |
|---|---|---|---|
| H1 | **Piso.** A MLP principal supera o chute da classe majoritária | MLP-128 × baseline (a), BA na CV | **confirmada** se média − DP da BA da MLP > 0,5 (a BA do chute majoritário é 0,5 por definição) |
| H2 | **Atalho.** A MLP com recorte extrai do traçado mais do que uma linha de código que lê o número do rodapé | MLP-128 × baseline (b), diferença pareada de BA | **MLP supera** se média − DP > 0; **MLP perde** se média + DP < 0; **empate** nos demais casos. Se não superar, a leitura registrada é: *a rede extraiu menos do traçado do que uma linha de código lendo o número do rodapé* |
| H3 | **Controle.** Sem recorte, a rede se aproveita do que está fora da grade (texto, margens) | MLP-128 sem recorte × MLP-128 com recorte, diferença pareada de BA | **aproveitamento detectado** se média − DP > 0; **não detectado** nos demais casos (inclui ser pior sem recorte) |
| H4 | **Resolução.** A comparação única pré-declarada: 192×112 × 128×75 | MLP-192 × MLP-128, diferença pareada de BA | **só descrição.** O resultado principal é a MLP-128 **seja qual for o resultado** — não se escolhe resolução pelo teste |
| H5 | **Subcategoria.** HB, que se distingue por ritmo e frequência (visíveis mesmo em baixa resolução), tem recall maior que MI e PMI, que dependem de morfologia fina (segmento ST, onda Q), borrada em 128×75 | recall de `anormal` por subcategoria, predição fora da dobra de cada repetição da CV, MLP-128 | **confirmada** se recall(HB) > recall(MI) **e** recall(HB) > recall(PMI) nas 3 repetições |

## 2. Decisões de método

**a) Pré-processamento** (aprovado na Etapa 1, recorte ajustado na 2A), a
mesma função para treino, teste e exemplos:

1. abrir o `.jpg` e converter para tons de cinza (`PIL`, modo `L`);
2. **recortar** `(72, 287, 2173, 1514)` → 2101×1227 px — o interior da
   moldura vermelha da grade recuado 4 px em cada lado. Todo texto variável
   (ID, sexo, FC, "Lead Off", data/hora) fica fora. O recuo elimina a borda
   direita, que varia entre x = 2175 e 2176 por lote de digitalização;
3. **redimensionar** para **128×75** (largura × altura; razão 1,71 mantida)
   com `Image.BOX` (média de área: a linha de ~3 px do traçado vira cinza,
   não some);
4. converter para `float32` em [0, 1] e **inverter** (`x = 1 − pixel/255`):
   traçado ≈ 1, fundo ≈ 0.

A MLP recebe a imagem **achatada**: 128 × 75 = 9.600 entradas.

**b) Split fixo** — para matriz de confusão e vídeo. Manifest ordenado por
MD5; `train_test_split(test_size=0.20, stratify=categoria_original,
random_state=42)` → teste de 99; do restante,
`train_test_split(test_size=0.15, stratify=categoria_original,
random_state=42)` → validação de 59 e treino de 333. A estratificação é pela
**categoria original**, e não pelo rótulo binário, para as 30 MI não caírem
todas de um lado. O teste é usado **uma vez por modelo**.

**c) Nenhum MD5 em mais de uma parte, em nenhuma divisão** — o notebook
confere por asserção no split fixo e em cada uma das 15 dobras da CV, e
recalcula o MD5 das 491 imagens contra o manifest antes de tudo.

**d) Validação cruzada** — `RepeatedStratifiedKFold(n_splits=5,
n_repeats=3, random_state=42)` sobre as 491, estratificada pela categoria
original. Em cada dobra, a parte de treino é dividida de novo
(`train_test_split(test_size=0.15, stratify=categoria_original,
random_state=42)`) para a validação da parada antecipada; a dobra de teste
nunca é vista no treino nem na parada. Reporta-se média e DP de cada métrica
nas 15 dobras. Mesmo princípio da Parte 2: o split único deixa 99 imagens no
teste (IC 95% ≈ ±9 p.p. na acurácia), e a CV mostra quanto ele oscila.

**e) Modelo — MLP em Keras**, a mesma arquitetura em todas as variantes:

```
Input(75, 128) → Flatten → Dense(128, relu) → Dropout(0,5)
               → Dense(32, relu) → Dropout(0,3) → Dense(1, sigmoid)
```

- `Adam(learning_rate=1e-3)`, `binary_crossentropy`, `batch_size=32`,
  até 200 épocas;
- **parada antecipada** na perda de validação: `EarlyStopping(monitor=
  "val_loss", patience=15, restore_best_weights=True)`;
- **`class_weight` balanceado**, calculado na parte de treino de cada divisão
  (`n / (2 · n_classe)`; no split fixo ≈ normal 1,73, anormal 0,70). **Sem
  sobreamostragem**: ela duplica imagens, exatamente o que a deduplicação
  removeu;
- **limiar de decisão fixo em 0,5.** Nenhum limiar é ajustado olhando teste;
- nenhuma busca de hiperparâmetro (333 imagens de treino não a sustentam sem
  sobreajuste à validação).

Parâmetros: 1.228.928 na primeira camada, 1.233.089 no total (MLP-128) —
≈ 3.700 por imagem de treino. É por isso que dropout e parada antecipada são
obrigatórios.

**f) Dois baselines, lidos lado a lado com a MLP**, nas mesmas divisões:

- **(a) classe majoritária** — sempre `anormal`: acurácia 71,1% nas 491,
  BA 0,5, **recall de anormal 1,0**. Por isso o recall de anormal nunca é lido
  sozinho: o chute que não olha a imagem tem recall perfeito;
- **(b) atalho do texto impresso** — `anormal` se a FC impressa (manifest)
  for > 90 bpm, senão `normal`. Nas 491: acurácia 74,3%, BA ≈ 0,82 (recall
  de anormal 223/349 = 0,64; recall de normal 142/142 = 1,0). Recalculado em
  cada divisão, **sem treino e sem reajuste do limiar**.

**g) Experimento controlado — sem recorte.** A mesma MLP, a mesma resolução
(128×75), o mesmo split fixo e as mesmas 15 dobras, com a mesma semente,
treinada na **imagem inteira** (2213×1572 → 128×75; a razão muda de 1,41
para 1,71 — distorção declarada, aceita para manter o mesmo número de
entradas e de parâmetros). Só a etapa 2 do pré-processamento muda. A
diferença entre com e sem recorte estima quanto a rede se aproveita do que
está fora da grade.

*Limite declarado:* em 128×75 os dígitos da FC têm menos de 1 px de altura e
não são legíveis. O que sobrevive é a **mancha** do campo: 2 dígitos
(FC < 100) ou 3 dígitos (FC ≥ 100), além de "Lead Off" e "Female". Por isso
H3 mede o aproveitamento do que resta **nesta resolução** — um piso do risco,
não o risco em resolução maior.

**h) Comparação de resolução (H4)** — a mesma MLP com recorte em **192×112**
(21.504 entradas; 2.752.640 parâmetros na primeira camada), no mesmo split e
nas mesmas dobras. É a única comparação de resolução, e não muda o resultado
principal.

**i) Métricas.**

- **Recall de `anormal` — métrica principal.** O erro perigoso é o ECG
  anormal classificado como normal (assimetria de custo documentada na Fase
  1: o falso negativo é o paciente mandado para casa);
- acurácia (o enunciado pede) e **acurácia balanceada** (a acurácia com 71%
  de anormais premia o chute majoritário);
- recall de `normal`;
- **recall de `anormal` por subcategoria** (MI, PMI, HB) — no split fixo o
  teste tem só **6 MI, 17 PMI e 47 HB**; por isso também na predição fora
  da dobra de cada repetição da CV (cada imagem é testada uma vez por
  repetição: 30 MI, 86 PMI, 233 HB), média e DP nas 3 repetições;
- **matriz de confusão** do split fixo, para cada modelo e baseline.

**j) Avaliação estratificada por sexo impresso** — o sexo é **metadado de
avaliação, não entrada**: o recorte o remove da imagem, e ele não entra no
modelo por nenhum outro caminho. Recall de `anormal` e de `normal` por sexo,
na predição fora da dobra de cada repetição da CV (média e DP nas 3), e no
split fixo.

| grupo | total (CV) | teste do split fixo |
|---|---|---|
| anormal, F | 29 | 7 |
| anormal, M | 320 | 63 |
| normal, F | 15 | 2 |
| normal, M | 127 | 27 |

**Não há poder estatístico** para concluir nada sobre diferença entre
sexos: com 29 anormais femininas, um erro muda o recall em 3,4 p.p.; no
teste fixo, com 7, muda 14 p.p. É **demonstração de método**: cumpre de novo
o compromisso 1 da Fase 1 (métricas estratificadas, não só a média global —
`document/fase-01/governanca-e-vies.md`). A base de imagens é **91%
masculina** (447 de 491), mais desequilibrada que a Cleveland da Fase 1
(68%).

**k) Reprodutibilidade.**

- `keras.utils.set_random_seed(42)` antes de **cada** treino (split fixo e
  cada dobra), e `tf.config.experimental.enable_op_determinism()` no setup;
- semente 42 em todos os splits e na CV;
- mesmo com isso, **os resultados podem diferir levemente entre a CPU local
  (macOS arm64) e a GPU do Colab**: operações de ponto flutuante em hardware
  diferente não são bit a bit idênticas, e uma diferença mínima numa época
  pode mudar em que época a parada antecipada para. O resultado de
  referência é o da execução local registrada;
- versões: `requirements-ir-alem-2.txt` (TensorFlow 2.21.0 e Keras 3.13.2,
  as do Colab em 2026-09-23).

## 3. Execução e desvios

- Notebook executado **uma vez**, de cima a baixo, num kernel limpo
  (`jupyter nbconvert --execute`), numa venv nova criada a partir de
  `requirements-ir-alem-2.txt`, e salvo **com os outputs** (notebook
  entregável).
- As **conclusões** são texto escrito **depois** da execução, numa célula
  markdown ao final, sem reexecutar nada. As decisões de H1–H5 são
  **calculadas pelo notebook** com os critérios da seção 1, não escritas à
  mão.
- Hipótese, critério e decisão desta página **não mudam** depois de ver
  resultado. Análise que surgir depois entra numa seção marcada como
  **pós-hoc, não pré-registrada**.
- Bug de código (o notebook não faz o que este protocolo diz): corrige-se,
  roda-se de novo, e **as duas execuções são registradas**.
- No Colab, o notebook clona o repositório (manifest e script 01) e baixa o
  zip do Mendeley pelo script 01; localmente, usa o repositório e o cache em
  `~/.cache/cardioia/`.

## 4. Gancho para a Fase 4

A MLP recebe a imagem **achatada**: o pixel (10, 20) e o (10, 21) são duas
entradas sem relação entre si para a primeira camada, que precisaria
aprender do zero, com 333 exemplos, que pixels vizinhos formam uma linha.
Ela perde a vizinhança entre pixels, e com ela a forma da onda — justamente
onde está a morfologia do infarto. Redes convolucionais, com filtros locais
compartilhados por toda a imagem, são o passo seguinte e o tema da **Fase 4
(Visão Computacional)**, que consome este mesmo conjunto de imagens. O
risco de *shortcut learning* pelo template do aparelho (31% da tinta de cada
imagem é template fixo, mesmo depois do recorte) vai junto para lá.
