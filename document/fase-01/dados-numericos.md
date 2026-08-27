# Dados numéricos — Parte 1 (IoT)

## a) Origem dos dados

Dado **real, público e anonimizado** — não simulado. Fonte: **UCI Machine
Learning Repository**, dataset *Heart Disease* (id 45), subconjunto **Cleveland**
(o único dos quatro hospitais originais — Cleveland, Hungria, Suíça e VA Long
Beach — recomendado pela própria UCI para uso em pesquisa de ML, por ser o mais
completo).

- **URL**: https://archive.ics.uci.edu/dataset/45/heart+disease
- **DOI**: `10.24432/C52P4X`
- **Licença**: CC BY 4.0
- **Data de acesso**: 2026-08-27
- **Nº de registros**: 303
- **Citação formal**: Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1989). *Heart Disease* [Dataset]. UCI Machine Learning Repository.

A própria documentação da UCI (metadado oficial coletado por
`scripts/fase-01/01_coleta_dataset_numerico.py` e salvo em
`document/datasets/raw/heart-disease-metadata.json`) registra que **nomes e
números de segurança social dos pacientes foram removidos da base e
substituídos por valores fictícios** antes da publicação — a anonimização não é
uma suposição deste projeto, é declarada pela fonte.

Coleta original em **1989**, num único hospital (identificado pela UCI apenas
como "Cleveland", EUA — não localizamos confirmação do nome completo da
instituição nas fontes salvas neste repositório), com pacientes encaminhados para investigação de doença coronariana. O
detalhamento desse contexto — e por que ele importa para viés — está em
`document/fase-01/governanca-e-vies.md` (a escrever).

## b) Variáveis mais relevantes do ponto de vista clínico

### As de maior poder discriminativo nesta base

**`tipo_dor_peito` (`cp`)** — tipo de dor torácica relatada (angina típica,
angina atípica, dor não anginosa, ou assintomático). É o primeiro filtro que um
cardiologista usa para estimar a probabilidade pré-teste de doença coronariana
antes de qualquer exame complementar; nesta base, o valor 4 (assintomático) é,
paradoxalmente, o mais associado a diagnóstico positivo — um lembrete clínico
de que apresentações atípicas (comuns em diabéticos e idosos) não podem ser
descartadas por ausência de dor clássica. **Uso concreto**: na Fase 2, entra
como variável categórica de alto poder discriminativo no classificador de
risco; é historicamente uma das variáveis mais importantes em estudos
publicados com este mesmo dataset.

**`frequencia_cardiaca_maxima` (`thalach`)** — frequência cardíaca máxima
atingida em teste de esforço, em bpm. Incompetência cronotrópica (não atingir
a FC máxima esperada) é marcador independente de pior desfecho cardiovascular.
**Uso concreto**: na Fase 3, é a mesma grandeza física que o wearable ESP32 vai
monitorar continuamente em tempo real; a faixa de sanidade documentada aqui
(60–220 bpm, mais a checagem cruzada contra `220 − idade`) é reaproveitável
como regra de validação de leitura do sensor.

**`depressao_st_exercicio` (`oldpeak`)** — depressão do segmento ST no ECG
durante exercício, em relação ao repouso, em mm. É um dos marcadores
eletrocardiográficos mais diretos de isquemia miocárdica induzida por esforço:
quanto maior, maior a gravidade esperada. **Uso concreto**: na Fase 2, entra
como variável contínua de alto peso no classificador; na Fase 6, uma leitura
de ECG de esforço equivalente (se viabilizada via wearable) poderia alimentar
o sistema preditivo de crise com a mesma lógica.

**`inclinacao_st_exercicio` (`slope`)** — inclinação do segmento ST no pico do
exercício (ascendente, plana ou descendente). A inclinação descendente é o
padrão mais associado a doença coronariana significativa, e complementa o
`oldpeak` na leitura do ECG de esforço. **Uso concreto**: na Fase 2, o par
`oldpeak` + `slope` costuma concentrar boa parte do poder preditivo de modelos
treinados neste dataset — vale tratar como bloco na modelagem.

**`angina_induzida_exercicio` (`exang`)** — indicador binário de dor torácica
desencadeada por esforço físico. Diferente das variáveis de exame, é um
**sintoma direto** relatado pelo próprio paciente — isquemia miocárdica sob
demanda aumentada de oxigênio. **Uso concreto**: na Fase 3, é candidato natural
a sintoma auto-reportado pelo paciente num app companion do wearable, cruzado
com os sinais objetivos captados pelo sensor no mesmo momento.

**`numero_vasos_fluoroscopia` (`ca`)** — número de vasos coronarianos
principais (0 a 3) visualizados com obstrução por fluoroscopia com contraste
(angiografia). É a medida mais direta e objetiva da extensão anatômica da
doença entre todas as variáveis da base — é exame invasivo e referência-padrão,
não um proxy. **Uso concreto**: na Fase 2, costuma ser a variável isolada mais
preditiva nesta base (mais vasos obstruídos → maior `num`); serve também como
"verdade terreno" para validar o poder preditivo de variáveis mais baratas de
obter (como as de sintoma ou de ECG de repouso).

### Fatores de risco clássicos

**`idade`** — fator de risco cardiovascular não modificável; a prevalência de
doença coronariana cresce com a idade (ver distribuição por faixa etária na
seção c). **Uso concreto**: na Fase 6, estratificação por faixa etária para
calibrar limiares de alerta do sistema preditivo de crise — o mesmo sinal
fisiológico pode significar risco muito diferente conforme a idade do
paciente.

**`sexo`** — homens têm maior prevalência e início mais precoce de doença
coronariana; esta base confirma isso com número (55,3% de prevalência do alvo
em homens contra 25,8% em mulheres — seção c). **Uso concreto**: na Fase 2, a
estratificação de métricas de desempenho do classificador por sexo deixa de
ser boa prática e passa a ser mandatória, dado o desbalanceamento observado e
o viés de encaminhamento discutido em `governanca-e-vies.md`.

**`colesterol_serico` (`chol`)** — fator de risco clássico e **modificável**
(dislipidemia) para aterosclerose coronariana. **Uso concreto**: na Fase 6,
combinado com dado de tratamento (quando disponível em fases futuras), ajuda a
modelar risco de evento agudo ao longo do tempo, não só risco estático.

**`pressao_arterial_repouso` (`trestbps`)** — hipertensão é o fator de risco
cardiovascular modificável mais prevalente na população em geral; aqui é a
medida basal de referência do paciente. **Uso concreto**: na Fase 3, é a mesma
grandeza (pressão arterial) que o wearable vai estimar/monitorar; a faixa de
sanidade documentada aqui (60–250 mmHg) é reaproveitável como regra de
validação de leitura do sensor, do mesmo jeito que a de `thalach`.

## c) Decisões de tratamento

Números reais da execução de `scripts/fase-01/03_trata_dataset_numerico.py`
sobre o dado bruto coletado da UCI — **303 linhas, 15 colunas** no dataset
processado.

**1. Ausências em `numero_vasos_fluoroscopia` (4 linhas, 1,3%) e `talassemia`
(2 linhas, 0,7%) — total 6 de 303 (~2%), sem sobreposição — não foram
imputadas.** Ficam como célula vazia real no `.csv` e no `.xlsx` (verificado
lendo os arquivos de volta: nenhuma ocorrência da string `"NaN"` nem de
sentinela numérico). Dois motivos: (a) imputar pela estatística do dataset
inteiro antes do split treino/teste da Fase 2 seria vazamento de dado — a
imputação, quando fizer sentido, é responsabilidade da Fase 2, calculada
dentro de cada fold de validação; (b) `ca` e `thal` vêm de exames invasivos e
caros (fluoroscopia com contraste, cintilografia com tálio), então a ausência
provavelmente não é aleatória (**MNAR** — *missing not at random*: pacientes
com quadro visto como menos grave podem nunca ter sido encaminhados ao exame).
Imputar pela moda apagaria esse sinal clínico.

**2. O alvo foi mantido em duas colunas.** `num` (0 a 4) é o diagnóstico
**original** da UCI, por gravidade — distribuição: `num=0`: 164 (54,1%),
`num=1`: 55 (18,2%), `num=2`: 36 (11,9%), `num=3`: 35 (11,6%), `num=4`: 13
(4,3%). `alvo_binario` é derivada (`0` se `num==0`, `1` se `num>0`) —
distribuição: 164 (54,1%) vs 139 (45,9%), bem balanceada. As duas colunas
coexistem porque a Fase 2 (classificação de risco) usa o binário, e a Fase 6
(previsão de crise) pode querer a granularidade de severidade do original.

**3. As faixas de plausibilidade são checagem de sanidade de dado (erro de
digitação/sensor), não critério clínico** — documentado assim de propósito
para não ser lido como diagnóstico. Nenhuma linha foi removida por cair fora
delas; o script só relata. Na execução real, nenhuma linha caiu fora das
faixas absolutas (`idade` 18–100, `pressao_arterial_repouso` 60–250 mmHg,
`colesterol_serico` 100–600 mg/dL, `frequencia_cardiaca_maxima` 60–220 bpm).
A checagem cruzada de `frequencia_cardiaca_maxima` contra a estimativa
`220 − idade` (+ margem de 15 bpm) disparou aviso em 10 linhas — **todas
benignas**: `thalach` é a FC máxima atingida em esforço, e `220 − idade` é
estimativa populacional com desvio de ~10–12 bpm, então um paciente bem
condicionado a ultrapassa com naturalidade. O maior excesso observado sobre o
limiar (já somada a margem) foi de 14 bpm (índice 188, idade 54,
`thalach` 195) — nenhum caso chega perto de um valor fisiologicamente
implausível.

**Distribuição por sexo**: 97 mulheres (32,0%), 206 homens (68,0%).
**Cruzamento `alvo_binario` × sexo** (achado a levar para
`governanca-e-vies.md`): prevalência de 25,8% em mulheres (25 de 97) contra
55,3% em homens (114 de 206).

## d) Limitações

Apontamento apenas — a análise completa de governança e viés, cobrindo as
três bases da Fase 1 (numérica, textual, visual), vai para
`document/fase-01/governanca-e-vies.md` (próxima etapa, ainda não escrita):

- Coleta de **1989** (identificado pela UCI apenas como "Cleveland", EUA — não
  localizamos confirmação do nome completo da instituição nas fontes salvas
  neste repositório) — **37 anos** e um contexto de saúde muito distantes do
  Brasil de 2026.
- Base de pacientes **encaminhados para angiografia** — não é amostra da
  população geral, é amostra de quem já tinha suspeita clínica relevante o
  bastante para justificar exame invasivo.
- **68% masculina**, com prevalência do alvo quase o dobro em homens (55,3%)
  em relação a mulheres (25,8%) — mistura de epidemiologia real com possível
  viés de encaminhamento.

## e) Como reproduzir

Pré-requisito: Python 3.12 e as dependências de `requirements.txt` instaladas
(`pip install -r requirements.txt`) — ver seção 7 do `CLAUDE.md`/`AGENTS.md`.

```bash
python scripts/fase-01/01_coleta_dataset_numerico.py
python scripts/fase-01/02_perfila_dataset_numerico.py
python scripts/fase-01/03_trata_dataset_numerico.py
```

Nessa ordem: o primeiro coleta o dado bruto (com fallback documentado se a
API `ucimlrepo` falhar), o segundo perfila sem alterar nada, o terceiro aplica
as decisões de tratamento acima e grava
`document/datasets/processed/heart-disease-processed.csv` e `.xlsx`.
