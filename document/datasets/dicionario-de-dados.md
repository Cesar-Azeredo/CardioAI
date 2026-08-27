# Dicionário de dados — dataset numérico (Fase 1)

Dataset processado: `document/datasets/processed/heart-disease-processed.csv` e
`heart-disease-processed.xlsx`. Gerado por
`scripts/fase-01/03_trata_dataset_numerico.py`, a partir do dado bruto do
**UCI Heart Disease (id 45, base Cleveland)** — proveniência completa em
`document/datasets/README.md`.

303 linhas, 15 colunas. Nenhuma linha foi removida: as 6 linhas com alguma
ausência (4 em `numero_vasos_fluoroscopia`, 2 em `talassemia`, sem
sobreposição) continuam no dataset processado, e nenhuma linha é descartada
por validação de plausibilidade — ver "Decisões de tratamento" ao final.

## Variáveis

| Nome novo | Nome original (UCI) | Tipo | Unidade | Faixa de sanidade | Nº de ausências | Significado clínico |
|---|---|---|---|---|---|---|
| `idade` | `age` | inteiro | anos | 18–100 | 0 | Idade do paciente; fator de risco cardiovascular não modificável, a prevalência de doença coronariana sobe com a idade. |
| `sexo` | `sex` | categórico (0/1) | — | — | 0 | Sexo biológico (0 = feminino, 1 = masculino). Homens têm maior prevalência e início mais precoce de doença coronariana, mas a base também carrega viés de encaminhamento — ver `document/fase-01/governanca-e-vies.md`. |
| `tipo_dor_peito` | `cp` | categórico (1–4) | — | — | 0 | Tipo de dor torácica relatada (1 = angina típica, 2 = angina atípica, 3 = dor não anginosa, 4 = assintomático); orienta a probabilidade pré-teste de doença coronariana. |
| `pressao_arterial_repouso` | `trestbps` | inteiro | mmHg | 60–250 | 0 | Pressão arterial sistólica em repouso, medida na admissão hospitalar; hipertensão é fator de risco cardiovascular maior. |
| `colesterol_serico` | `chol` | inteiro | mg/dL | 100–600 | 0 | Colesterol sérico total; dislipidemia favorece aterosclerose coronariana. |
| `glicemia_jejum_alta` | `fbs` | categórico (0/1) | — | — | 0 | Glicemia de jejum > 120 mg/dL (1 = sim); proxy de diabetes/pré-diabetes, fator de risco cardiovascular. |
| `eletrocardiograma_repouso` | `restecg` | categórico (0–2) | — | — | 0 | Resultado do ECG em repouso (0 = normal, 1 = anormalidade de onda ST-T, 2 = hipertrofia ventricular esquerda provável/definitiva); alterações sugerem dano estrutural ou isquemia prévia. |
| `frequencia_cardiaca_maxima` | `thalach` | inteiro | bpm | 60–220 (+ checagem cruzada contra 220−idade, margem 15 bpm — aviso, não rejeição) | 0 | Frequência cardíaca máxima atingida em teste de esforço; capacidade cronotrópica reduzida associa-se a pior prognóstico cardiovascular. |
| `angina_induzida_exercicio` | `exang` | categórico (0/1) | — | — | 0 | Angina induzida por esforço (1 = sim); sintoma direto de isquemia miocárdica sob demanda. |
| `depressao_st_exercicio` | `oldpeak` | decimal | mm | — | 0 | Depressão do segmento ST induzida por exercício em relação ao repouso; marcador eletrocardiográfico clássico de isquemia. |
| `inclinacao_st_exercicio` | `slope` | categórico (1–3) | — | — | 0 | Inclinação do segmento ST no pico do exercício (1 = ascendente, 2 = plana, 3 = descendente); a descendente é o padrão mais associado à doença coronariana. |
| `numero_vasos_fluoroscopia` | `ca` | inteiro | nº de vasos (0–3) | — | **4 (1,3%)** | Número de vasos coronarianos principais visualizados com obstrução por fluoroscopia com contraste; medida angiográfica direta da extensão da doença. Ausência **não imputada** — ver decisão abaixo. |
| `talassemia` | `thal` | categórico (3/6/7) | — | — | **2 (0,7%)** | Resultado da cintilografia de perfusão miocárdica com tálio (3 = normal, 6 = defeito fixo, 7 = defeito reversível); defeitos indicam isquemia ou infarto prévio. Ausência **não imputada** — ver decisão abaixo. |
| `num` | `num` (mantido sem renomeio) | inteiro | 0–4 | — | 0 | Alvo **original** da UCI: diagnóstico de doença coronariana por angiografia, 0 = ausência, 1–4 = presença com gravidade crescente (>50% de obstrução em ao menos um vaso principal, graduado). |
| `alvo_binario` | *derivada — não existe na UCI* | categórico (0/1) | — | — | 0 | Derivada de `num`: `0` se `num == 0`, `1` se `num > 0`. Simplifica para classificação binária de presença de doença coronariana; é o alvo principal previsto para a Fase 2. Regra de derivação exata em `03_trata_dataset_numerico.py`. |

## Legenda dos códigos categóricos

Extraída literalmente da documentação oficial da UCI (`document/datasets/raw/heart-disease-metadata.json`, campo `additional_info.variable_info`, e `heart-disease-variables.csv`) — nenhum rótulo foi deduzido. Onde a fonte não detalha um código, está marcado como tal.

| Variável | Código | Significado (fonte UCI) |
|---|---|---|
| `sexo` (`sex`) | 0 | feminino |
| | 1 | masculino |
| `tipo_dor_peito` (`cp`) | 1 | angina típica |
| | 2 | angina atípica |
| | 3 | dor não anginosa |
| | 4 | assintomático |
| `glicemia_jejum_alta` (`fbs`) | 0 | glicemia de jejum ≤ 120 mg/dL (falso) |
| | 1 | glicemia de jejum > 120 mg/dL (verdadeiro) |
| `eletrocardiograma_repouso` (`restecg`) | 0 | normal |
| | 1 | anormalidade de onda ST-T (inversão de onda T e/ou elevação/depressão de ST > 0,05 mV) |
| | 2 | hipertrofia ventricular esquerda provável ou definitiva, pelos critérios de Estes |
| `angina_induzida_exercicio` (`exang`) | 0 | não |
| | 1 | sim |
| `inclinacao_st_exercicio` (`slope`) | 1 | ascendente (*upsloping*) |
| | 2 | plana (*flat*) |
| | 3 | descendente (*downsloping*) |
| `talassemia` (`thal`) | 3 | normal |
| | 6 | defeito fixo |
| | 7 | defeito reversível |

`numero_vasos_fluoroscopia` (`ca`) é contagem direta (0 a 3 vasos), não código categórico — sem legenda a aplicar. `num` e `alvo_binario` já estão descritos por extenso na tabela de variáveis acima.

## Decisões de tratamento (resumo — raciocínio completo nos comentários de `03_trata_dataset_numerico.py`)

- **Ausências em `numero_vasos_fluoroscopia` (4) e `talassemia` (2), total 6 linhas de 303 (~2%): não imputadas, ficam como célula vazia.** Motivos: (a) imputar antes do split treino/teste da Fase 2 seria vazamento de dado — imputação, quando fizer sentido, é responsabilidade da Fase 2, dentro de cada fold; (b) são exames invasivos/caros, então a ausência provavelmente não é aleatória (MNAR) — imputar pela moda apagaria esse sinal.
- **Alvo mantido em duas colunas** (`num` original + `alvo_binario` derivada) para servir tanto a Fase 2 (classificação binária de risco) quanto a Fase 6 (previsão de crise, que pode querer a severidade original).
- **Faixas de sanidade são checagem de erro de digitação/sensor, não critério clínico.** Nenhuma linha foi removida por cair fora delas — o script de tratamento só relata. Na execução real sobre este dataset, nenhuma linha caiu fora das faixas numéricas absolutas; 10 linhas dispararam o aviso da checagem cruzada de `frequencia_cardiaca_maxima` contra a estimativa `220 − idade` (+ margem de 15 bpm). **Os 10 são benignos, não erro de dado**: `thalach` é a FC máxima atingida em teste de esforço, e `220 − idade` é estimativa populacional com desvio de ~10–12 bpm — um paciente bem condicionado a ultrapassa com naturalidade. O maior excesso sobre o limiar (já com a margem somada) foi de 14 bpm (índice 188, idade 54, `thalach` 195). Nenhuma linha se aproxima de um valor fisiologicamente impossível.
