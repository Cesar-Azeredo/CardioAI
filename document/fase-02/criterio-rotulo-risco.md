# Critério de rótulo alto/baixo risco — Parte 2 (Fase 2)

Registrado em 2026-09-23 **antes** de escrever qualquer frase do dataset
rotulado. Vale para `document/datasets/fase-02/frases-rotuladas-risco.csv`
(treino e avaliação do classificador) e para
`document/datasets/fase-02/desafio-risco.csv` (conjunto-desafio, fora do
treino). Os trechos abaixo são citados literalmente das páginas do Ministério
da Saúde já coletadas (CC BY-ND 3.0 — citados, não reescritos); a presença
literal de cada trecho no `.txt` é conferida por
`scripts/fase-02/06_verifica_dataset_risco.py`.

> Projeto acadêmico. Este critério serve para rotular dado sintético de
> treino; não é protocolo de triagem e não serve para decisão médica.

## 1. Alto risco

**Definição:** a frase relata **pelo menos um sinal de alerta** listado nas
páginas do Ministério da Saúde de infarto (Texto 3) ou de AVC (Texto 4) —
páginas que orientam acionar o SAMU 192 ou buscar emergência diante desses
sinais.

### 1.1 Orientação de emergência (o que faz destes sinais "alerta")

- **Infarto** (`assets/textos/fase-02/texto_03_infarto-ministerio-saude.txt`):
  - "Tratamento: Infarto é uma emergência que exige cuidados médicos imediatos."
  - "Se sentir dor no peito, suor frio, palidez e sensação de desmaio," / "Ligue 192 SAMU" / "Ou procure uma Emergência Cardiológica mais próxima."
- **AVC** (`assets/textos/fase-02/texto_04_avc-ministerio-saude.txt`):
  - "Os principais sinais de alerta para qualquer tipo de AVC são:"
  - "Importante: Caso qualquer um desses sintomas apareçam, é fundamental ligar para o Serviço de Atendimento Médico de Urgência (SAMU - 192), Bombeiros (193) ou levar a pessoa imediatamente a um hospital para avaliação clínica detalhada."

### 1.2 Sinais de alerta — código usado na coluna `sinal_de_alerta`

| Código | Sinal | Trecho-fonte (literal) |
|---|---|---|
| I1 | Dor ou desconforto no peito, que pode irradiar para costas, rosto ou braço | "Dor ou desconforto na região peitoral, podendo irradiar para as costas, rosto, braço esquerdo e, raramente, braço direito." |
| I2 | Sensação de peso ou aperto no tórax | "acompanhada de sensação de peso ou aperto sobre o tórax" |
| I3 | Suor frio | "provocando suor frio, palidez, falta de ar e sensação de desmaio." |
| I4 | Palidez | "provocando suor frio, palidez, falta de ar e sensação de desmaio." |
| I5 | Falta de ar (inclusive como principal sintoma em idosos) | "provocando suor frio, palidez, falta de ar e sensação de desmaio." · "Em idosos, o principal sintoma do infarto agudo do miocárdio pode ser a falta de ar." |
| I6 | Sensação de desmaio | "provocando suor frio, palidez, falta de ar e sensação de desmaio." |
| I7 | Mal-estar súbito (destacado para diabéticos e idosos) | "Nos diabéticos e idosos, o infarto também pode ocorrer sem sinais específicos. Por isso, deve-se estar atento a qualquer mal-estar súbito." |
| A1 | Confusão mental | "Confusão mental;" |
| A2 | Alteração da fala ou da compreensão | "Alteração da falar ou compreensão;" (a página traz "da falar"; erro de digitação da fonte) |
| A3 | Alteração na visão, em um ou nos dois olhos | "Alteração na visão (em um ou ambos os olhos);" |
| A4 | Dor de cabeça súbita, intensa, sem causa aparente | "Dor de cabeça súbita, intensa, sem causa aparente;" |
| A5 | Alteração do equilíbrio, coordenação, tontura ou do andar | "Alteração do equilíbrio, coordenação, tontura ou alteração no andar;" |
| A6 | Fraqueza ou formigamento em um lado do corpo (rosto, braço ou perna) | "Fraqueza ou formigamento em um lado do corpo (rosto, braço ou perna)." |

Uma frase é alto risco com **um** sinal, como a fonte orienta ("caso
qualquer um desses sintomas"). Sinais pouco específicos isolados (I3, I4)
aparecem no dataset preferencialmente combinados com outros; quando sozinhos,
seguem a regra da fonte.

## 2. Baixo risco

**Definição:** queixa **leve e autolimitada** — com causa aparente e sem
piora, ou que melhora com repouso ou medida simples —, **sem nenhum** sinal
de alerta da seção 1.2 e **sem** sintoma da zona cinzenta (seção 3).

Sinal de alerta **negado** ("não sinto dor no peito") pode aparecer — é
justamente o caso que o classificador precisa aprender —, mas nunca um
sinal de alerta presente, mesmo que leve.

**Exclusões adicionais por segurança clínica** (valem para toda frase de
baixo risco, mesmo que o sintoma não esteja na lista de alerta):

- dor no abdome, estômago ou azia — a página de infarto registra:
  "A dor também pode ser no abdome, semelhante a dor de uma gastrite ou esofagite de refluxo, mas é pouco frequente.";
- formigamento ou dormência em qualquer parte do corpo; tontura ou vertigem
  de qualquer causa; qualquer alteração de visão; fraqueza; mal-estar;
  náusea ou vômito; palpitação.

Em caso de dúvida, a frase **não** entra como baixo risco: segurança clínica
vem antes da dificuldade do dataset.

## 3. Zona cinzenta — fora do treino

**Definição:** sintomas que a página de **hipertensão** lista e que **não**
são sinal de alerta de infarto ou AVC:

| Código | Sintoma | Trecho-fonte (literal, Texto 2) |
|---|---|---|
| Z | dor de cabeça sem ser súbita/intensa, zumbido no ouvido, sangramento nasal, fraqueza sem lado definido | "Os sintomas da hipertensão costumam aparecer somente quando a pressão sobe muito: podem ocorrer dores no peito, dor de cabeça, tonturas, zumbido no ouvido, fraqueza, visão embaçada e sangramento nasal." |

Os outros sintomas da mesma lista — `dores no peito`, `tonturas`, `visão
embaçada` — **coincidem** com sinais de alerta (I1, A5, A3) e, quando
presentes, fazem a frase ser alto risco.

A página de hipertensão **não** orienta emergência para esses sintomas —
a orientação dela é outra: "Medir a pressão regularmente é a única maneira de diagnosticar a hipertensão."
—, mas eles também **não** são benignos. Por isso:

- **não entram** no dataset de treino (`frases-rotuladas-risco.csv`);
- entram **só** no conjunto-desafio, com rótulo **"indefinido"**: ali não há
  resposta certa, só observação de como o classificador se comporta.

**Limitação registrada:** excluir a zona cinzenta do treino torna a tarefa
**mais fácil** que a triagem real, em que esses casos existem e são
frequentes. A acurácia medida no notebook **superestima** o desempenho em
uso real.

## 4. Conjunto-desafio

`desafio-risco.csv` usa o mesmo critério, com rótulo esperado
pré-registrado antes de qualquer treino, e **não entra no treino**. Cobre:
negação que um modelo de TF-IDF tende a errar; infarto atípico sem a palavra
"dor" (a hipótese pendente da frase 10 da Parte 1: esperado **alto risco**);
zona cinzenta (**indefinido**); e sinal de alerta em vocabulário que não
aparece no treino.

## 5. Atalho de estilo × sinal clínico (revisão de 2026-09-23, antes de qualquer treino)

A contagem de palavras de conteúdo que só aparecem numa classe
(`scripts/fase-02/06_verifica_dataset_risco.py`) separa dois tipos de
"palavra exclusiva". Eles recebem tratamento **oposto**:

**Atalho de estilo — balanceado** (a palavra não carrega informação clínica;
se o modelo a aprender, aprende o jeito de escrever do grupo):

| Palavra | Tratamento |
|---|---|
| `senti`, `meio`, `hora` | levadas também para frases de **baixo** risco |
| `esquerdo` | levada para o baixo risco **somente** com partes do corpo fora da zona de irradiação do infarto — tornozelo, joelho, pé, calcanhar. **Nunca** braço, ombro, peito, mandíbula, queixo ou rosto em baixo risco: isso ensinaria o modelo a desvalorizar o sinal clássico de irradiação (I1) |
| `dói`, `dolorido` | **risco de segurança**, não só estilo: "dói → baixo risco" triaria "meu peito dói muito" como baixo risco. Levadas para frases de **alto** risco (ex.: "O peito dói, o ar não vem…"), nunca o contrário |

**Sinal clínico — mantido, não balanceado** (a palavra É o sinal da fonte; o
modelo deve aprendê-la):

| Palavra | Sinal |
|---|---|
| `repente` | súbito — A4 ("Dor de cabeça súbita…"), I7 ("mal-estar súbito") |
| `ar` | falta de ar — I5 |
| `peso` | sensação de peso — I2 |
| `fala` | alteração da fala — A2 |

### 5.1 Regra de parada do balanceamento

Toda base finita tem palavras exclusivas de uma classe; balancear cada
candidata nova vira ciclo infinito, e o próprio balanceamento vira ajuste
fino. **Balancear SOMENTE:**

- **(a)** palavra de **estilo** presente em **4 ou mais** frases de uma só
  classe; ou
- **(b)** qualquer palavra com carga **demográfica** ou de **segurança**,
  independente da contagem.

Aplicação às candidatas que sobraram depois do primeiro balanceamento
(nenhuma outra é balanceada):

| Palavra | Decisão | Motivo |
|---|---|---|
| `toda` | **balancear** — levada também para o alto risco | carga **demográfica**: só aparecia no baixo risco e marcava voz feminina ("toda quebrada", "toda congestionada"); o modelo poderia aprender "voz feminina → baixo risco", o viés que a seção 6 quer eliminar, e justamente o lado perigoso do erro para mulheres. Introduzida pelas próprias edições de gênero. `todo` (e plurais) não aparece em nenhuma frase |
| `consegui` | manter | "não consegui" é marcador de incapacidade funcional — sinal de gravidade |
| `coçando` | manter | prurido é benigno de fato |
| `cabeça` | manter | efeito do critério: dor de cabeça que não é súbita está na zona cinzenta e fora do baixo risco. O erro esperado é **falso positivo** — o lado seguro |
| `tudo`, `tempo` | manter | abaixo do limiar da regra (a) |

Ambiguidade corrigida pela mesma lógica de segurança: "pulso" numa frase de
baixo risco ("Senti o pulso reclamar…") também é lido como batimento
cardíaco — e palpitação está nas exclusões da seção 2. Trocado por "punho".

## 6. Gênero da voz (viés herdado da Fase 1)

A base numérica da Fase 1 (UCI/Cleveland) é 68% masculina; o dataset da
Parte 2, antes desta revisão, repetia o padrão na voz das frases — por
concordância com quem fala, 5 masculinas e 1 feminina no alto risco, 3 e 0 no
baixo (contagem feita por léxico simples, que ainda confundia "suor gelado" e
"algo gelado" com a voz; a detecção corrigida, com verbo em 1ª pessoa, dá
**4 e 1** no alto e **2 e 0** no baixo).

- `marcador_genero` (`feminino`, `masculino`, `neutro`) é **metadado
  autoral**, depois das colunas literais `frase,situacao`, conferido por
  script contra a concordância: adjetivo do léxico até 4 palavras depois de um
  verbo em 1ª pessoa ("estou", "fiquei", "acordei"…) na mesma oração.
- Mínimo de **6 frases femininas e 6 masculinas marcadas em cada classe**;
  frases neutras continuam permitidas.
- **Teste contrafactual** no conjunto-desafio: 3 pares idênticos exceto pela
  concordância de gênero (`par_contrafactual` G1 — infarto atípico sem dor;
  G2 — alto risco clássico; G3 — baixo risco). **Esperado pré-registrado:
  predição idêntica dentro de cada par.** Predição diferente dentro de um par
  significa que o gênero da voz está influenciando a triagem — é o achado a
  medir no notebook.

**Referência clínica sobre infarto em mulheres.** Declaração científica da
American Heart Association: Mehta, L. S. et al. (2016). *Acute Myocardial
Infarction in Women*. Circulation, 133(9), 916–947. DOI
`10.1161/CIR.0000000000000351`. Metadados conferidos no Crossref; conteúdo
verificado pelo grupo na página da editora (2026-09-23).

- Seção *Symptoms of AMI*: comparadas aos homens, mulheres têm mais
  apresentações de alto risco e são "less likely to manifest central chest
  pain".
- Seção *Clinical Presentation*: a declaração lista falta de ar, fraqueza,
  fadiga e indigestão como sintomas equivalentes de angina frequentes em
  mulheres.

É o apoio de fonte para o par contrafactual **G1** (infarto atípico, sem dor)
e para a hipótese pendente da frase 10 da Parte 1: um classificador que
depende de "dor" para dar alto risco tende a errar justamente no perfil em
que a dor torácica central é menos frequente — hipótese a medir no notebook. O texto do artigo **não** é
reproduzido no repositório (conteúdo protegido da AHA); só a referência e a
citação curta acima.
