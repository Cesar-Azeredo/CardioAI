# Protocolo pré-registrado do extrator de sintomas — Fase 2

> **Estado: CONGELADO em 2026-09-23**, depois de aprovado com três ajustes
> (2.5: hash de recurso vira aviso, caminho do cache local/Colab testado;
> referências verificadas). O SHA-256 deste arquivo é conferido por
> `scripts/fase-02/01_verifica_mapa_e_frases.py`, como o mapa e as frases.
> Nenhuma regra abaixo foi executada sobre as 10 frases de teste antes do
> congelamento.

## 0. Princípio de pré-registro e declaração de conhecimento prévio

Todas as regras de casamento, negação, desempate e confiança estão escritas
e justificadas **antes** de qualquer execução do extrator nas 10 frases de
`assets/textos/fase-02/frases-sintomas-pacientes.txt`. Depois de aprovado o
protocolo, o extrator roda **uma vez** nas frases e o resultado é reportado
como saiu.

**Declaração de conhecimento prévio (transparência obrigatória).** Este
protocolo foi escrito por quem já conhece:

1. o texto das 10 frases e o gabarito (`document/fase-02/gabarito-frases.md`);
2. a saída do verificador (`scripts/fase-02/01_verifica_mapa_e_frases.py`),
   que mostra quais termos do mapa aparecem **literalmente** em cada frase —
   em particular, que o casamento exato **falha na frase 3** ("minha fala
   ficou enrolada" não casa "fala enrolada"), que a frase 10 tem **um único**
   termo casado (`falta de ar`) e que a frase 1 cita o braço esquerdo ao lado
   de dor no peito.

Não dá para desaprender isso. As proteções adotadas:

- **(a) técnica padrão e citável antes de regra sob medida.** Onde existe
  técnica estabelecida (stemmer RSLP, lista de stopwords da NLTK, negação no
  estilo NegEx, casamento por proximidade ordenada), ela é usada como é, sem
  ajuste fino; parâmetros numéricos são derivados do **vocabulário do mapa**
  ou de um **corpus de referência neutro**, nunca das frases;
- **(b) baseline exato reportado ao lado do método** (seção 10), com a mesma
  pontuação, negação e confiança — só o casamento muda. Assim o efeito de
  cada decisão fica isolado e visível;
- **(c) frases contaminadas marcadas na avaliação.** Toda decisão cujo
  efeito numa frase de teste era previsível pelo conhecimento acima está
  listada na seção 10.3, e aquela frase **não conta como evidência** a favor
  da decisão.

Toda avaliação de risco (over-stemming, tamanho de janela) foi feita sobre o
**vocabulário do mapa** e sobre o **corpus de referência** formado pelos
Textos 1 a 4 (`assets/textos/*.txt` e `assets/textos/fase-02/*.txt`, 1.377
palavras distintas) — nunca sobre as frases.

---

## 1. Normalização

Aplicada igualmente aos termos do mapa e às frases, nesta ordem:

1. **Minúsculas** (`str.lower`).
2. **Segmentação em orações** (seção 4.2) *antes* de remover pontuação,
   porque vírgula e ponto são fronteiras de oração.
3. **Tokenização** por palavras: sequências de letras, com hífen interno
   preservado — `mal-estar` é **um** token. Justificativa: na ortografia do
   português, o hífen em compostos como *mal-estar* une uma única unidade
   lexical (é um substantivo, não "mal" + "estar"); separar produziria
   `estar`, que é stopword, e deixaria o termo `mal-estar súbito` reduzido a
   `mal … súbito`. Dígitos e demais sinais de pontuação são descartados.
4. **Radicalização** (seção 2), **com acento**.
5. **Remoção de acentos** do radical (decomposição NFD e descarte das marcas
   combinantes).

**Por que o acento sai depois do stemmer, e não antes.** Medido sobre o
vocabulário do mapa (97 palavras distintas): em 6 palavras o radical muda se
o acento for removido antes, porque as regras do RSLP para `-ção`/`-são`
dependem do til — `alteração → alter` (com acento) vira `alteraca` (sem);
idem `compreensão`, `confusão`, `região`, `sensação`, `visão`. Tirar o acento
primeiro quebraria justamente os sufixos nominais mais produtivos.

## 2. Variação morfológica (plural, gênero, flexão verbal)

### 2.1 Opções comparadas

| Critério | RSLP (NLTK) | Regras de sufixo escritas à mão |
|---|---|---|
| Origem | Algoritmo publicado para o português (Orengo & Huyck, 2001), implementado em `nltk.stem.RSLPStemmer` | Escritas por nós, para este projeto |
| Citável / reprodutível por terceiros | Sim | Não |
| Risco de overfitting | Baixo: as regras existem independentemente deste projeto e não são editadas | **Alto**: seriam escritas por quem já viu as frases (seção 0); uma regra que "por acaso" conserta a frase 3 é indistinguível de overfitting |
| Controle fino | Nenhum (aceita-se o algoritmo como é) | Total — que é exatamente o problema |

### 2.2 Over-stemming medido sobre o vocabulário do mapa

- **Conflações dentro do mapa** (palavras diferentes → mesmo radical): 15
  grupos, **todos do mesmo lexema** — `andando/andar → and`,
  `apertado/aperto → apert`, `confuso/confusão → confus`,
  `desmaiando/desmaiei/desmaio → desmai`, `dor/dores → dor`,
  `fala/falar → fal`, `falta/faltando → falt`,
  `formigamento/formigando → formig`, `fraca/fraco → frac`,
  `repentina/repentino → repentin`, `sangramento/sangrando → sangr`,
  `suando/suor → su`, `súbita/súbito → subit`,
  `tonto/tontura/tonturas → tont`, `zumbido/zumbindo → zumb`. Nenhuma junta
  dois sintomas diferentes.
- **Colisões entre conceitos**: as únicas sequências de radicais
  compartilhadas por conceitos diferentes são as **já declaradas no mapa**:
  mesmo termo em duas doenças (`tontura`, `tonto`, `fraqueza`,
  `cabeça rodando`, `dor no peito`, `peito doendo`) ou termo literal
  equivalente dentro da mesma doença (`sensação de peso`,
  `desconforto na região peitoral`; ver 7.1). O stemmer não cria colisão
  nova dentro do mapa.
- **Sub-radicalização (under-stemming) dentro do mapa** — pares do mesmo
  campo que o RSLP **não** junta: `palidez → palid` × `pálido → pal`;
  `fraqueza → fraqu` × `fraco → frac`; `sangue → sang` ×
  `sangramento → sangr`; `repente → repent` × `repentina → repentin`. O mapa
  já cobre esses casos com linhas de variante; não se acrescenta regra.

### 2.3 Over-stemming medido contra o corpus de referência (Textos 1–4)

Palavras do corpus que **não** estão no mapa mas caem num radical de conteúdo
do mapa:

| Palavra do corpus | Radical | Termo do mapa atingido | Avaliação |
|---|---|---|---|
| alterar, alterações | alter | alteração | mesmo lexema — conflação correta |
| entenda | entend | entender | mesmo lexema — conflação correta |
| **pais** | pal | pálido | **colisão indevida** |
| **sus** | su | suor, suando | **colisão indevida** |
| **visa** | vis | visão | **colisão indevida** |
| **sensíveis** | sens | sensação | **colisão indevida** |
| **and** (inglês, nas referências) | and | andar, andando | **colisão indevida** |

Exposição real: uma colisão só produz falso positivo se completar o termo
inteiro. Para termos de várias palavras, as demais palavras de conteúdo
também precisam estar na janela (ex.: `sus` só atinge `suor frio` se houver
`frio` a até 2 tokens). O único termo de **uma** palavra de conteúdo com
radical curto é **`pálido` (radical `pal`)**, exposto a `pais`/`país`.

### 2.4 Decisão

**RSLP, aplicado como é.** Considerada e **rejeitada** uma proteção para
radicais curtos (usar só os passos de plural e de feminino do próprio RSLP
quando o radical tiver menos de 4 letras): medida sobre o vocabulário do mapa,
ela é inconsistente — `dores → dore` deixa de casar com `dor`, `tonta` não é
reduzida a `tonto`, `frias → fria` deixa de casar com `frio` — e qualquer
limiar escolhido seria uma regra artesanal. O risco medido (5 colisões
indevidas em 1.377 palavras de referência, uma única exposição relevante em
termo de uma palavra) fica **declarado**: a saída mostra o token que casou
com cada termo (seção 9), então um falso positivo por over-stemming fica
visível na avaliação em vez de escondido.

### 2.5 Reprodutibilidade

- `nltk==3.9.1` — versão do `pip-freeze` oficial do Colab (commit de
  2026-09-21), wheel `py3-none-any`, registrada no `requirements.txt`.
- **Onde os recursos ficam.** Diretório = variável de ambiente
  `CARDIOIA_NLTK_DATA`, se definida; senão `<raiz do repo>/.cache/nltk_data`,
  com a raiz resolvida **pela localização do próprio script**
  (`Path(__file__).resolve().parents[2]`), não pelo diretório atual. O
  diretório é inserido no início de `nltk.data.path`, para que a cópia
  conferida tenha precedência sobre qualquer cópia do sistema.
- **Download só se ausente.** `nltk.download(<recurso>, download_dir=...)`
  roda apenas quando o `.zip` do recurso não existe; execuções seguintes não
  dependem de rede.
- **Hash conferido, divergência não interrompe.** Depois do download (ou
  do reaproveitamento), o SHA-256 do `.zip` é comparado com o
  pré-registrado. Se divergir, o extrator **continua**, imprime um aviso em
  destaque no terminal (stderr) e registra a divergência — hash esperado e
  encontrado — no cabeçalho de `document/fase-02/resultado-extrator.md`.
  Motivo: o entregável precisa rodar na máquina ou no Colab do corretor, e um
  recurso atualizado na origem não pode fazer o extrator se recusar a rodar;
  a divergência fica visível para quem avaliar o resultado.

  | Recurso | Arquivo | SHA-256 pré-registrado |
  |---|---|---|
  | `rslp` | `stemmers/rslp.zip` (3.805 bytes) | `f482f9666a2a76cdd4acab16b01a44b002550ebaac29906dbd5a1bbc281e4f8b` |
  | `stopwords` | `corpora/stopwords.zip` (37.733 bytes) | `48c0e52d8b52546e827f53761fb30300c0ab94f70660d28bd65ba0a86270946b` |

- `.cache/` está no `.gitignore` (bloco da Fase 2): recurso baixado não é
  versionado.

**Teste da lógica de caminho (2026-09-23).** Feito chamando só a função de
preparação de recursos — sem ler as frases:

| Cenário | Situação simulada | Diretório usado | Resultado |
|---|---|---|---|
| C1 | Local, executando da raiz do repo | `<repo>/.cache/nltk_data` | download; 2 hashes conferem |
| C2 | Local, executando de outro diretório (`/tmp`) | `<repo>/.cache/nltk_data` | mesmo diretório de C1 — independe do diretório atual |
| C3 | Layout do Colab: repo clonado em `…/content/CardioAI`, diretório atual `…/content`, `HOME` trocado | `…/content/CardioAI/.cache/nltk_data` | download; 2 hashes conferem |
| C3b | Segunda execução no layout de C3 | idem | não baixa de novo (data de modificação do `.zip` inalterada) |
| C4 | `CARDIOIA_NLTK_DATA` definida | o diretório da variável | download; 2 hashes conferem |
| C5 | `.zip` do `rslp` adulterado de propósito | o diretório da variável | aviso em destaque com hash esperado e encontrado; **execução continua** (código de saída 0) |

**Limite do teste:** o Colab foi **simulado** pelo layout de diretórios
(clone em `/content/<repo>`, execução a partir de `/content`), não executado
de fato. No Colab o uso previsto é clonar o repositório e rodar
`!python <repo>/scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py`;
como a raiz vem de `__file__` e `/content` é gravável no Colab, a lógica é a
mesma de C3.

## 3. Casamento de termo multipalavra

### 3.1 Palavras de conteúdo

Palavras de conteúdo de um termo = seus tokens **menos** a lista de
stopwords `portuguese` do corpus `stopwords` da NLTK (207 palavras), **exceto
os marcadores de negação**, que nunca são removidos. A lista da NLTK contém
`não`, `nem` e `sem`; se esses saíssem, `sem fôlego` viraria só `fôlego` e
casaria com "com fôlego". No mapa, as palavras que caem como stopword são:
`da, de, do, em, na, no, o, ou, para, pelo, que, um` (e `sem`, mantida por
ser marcador). As stopwords do termo são **opcionais** na frase.

### 3.2 Decisão: proximidade ordenada com intervalo máximo de 2 tokens

Um termo casa numa oração quando **todas as suas palavras de conteúdo**
aparecem **na mesma ordem** do termo, com **no máximo 2 tokens quaisquer
entre duas palavras de conteúdo consecutivas**, sem cruzar fronteira de
oração (4.2). É o casamento por proximidade ordenada usado em recuperação de
informação (ex.: `SpanNearQuery` com `inOrder=true` e `slop` no Apache
Lucene) — técnica padrão, não regra sob medida.

**Justificativa linguística do intervalo (independente das frases).**

1. **O próprio mapa exige 2.** O maior intervalo entre palavras de conteúdo
   *dentro de um termo do mapa* é 2 — `formigamento [em um] lado`,
   `dor que vai [para o] braço`, `formigando [de um] lado`. Com intervalo
   menor que 2, o método não reconheceria nem os próprios termos do mapa
   com preposição e artigo trocados.
2. **Inserção entre núcleo e predicado é regular em português falado.**
   Entre um substantivo de sintoma e o adjetivo ou verbo que o qualifica
   entram, tipicamente, um verbo de ligação e um intensificador
   ("[está muito]", "[ficou meio]", "[anda bem]"), e entre núcleo e
   complemento entram preposição + artigo ("[sobre o]", "[em um]"). Os dois
   padrões somam até 2 tokens.
3. **Ordem preservada.** Inversão ("enrolada, a fala") é marcada e rara;
   aceitar qualquer ordem aumentaria o falso positivo por coincidência de
   palavras soltas. Fica como limitação declarada.

**Transparência.** Esta é a decisão que mais afeta a frase 3: com intervalo
de 2, "fala [ficou] enrolada" casa `fala enrolada`. A decisão foi justificada
pelos itens 1–3 acima, mas foi tomada por quem sabe disso — por isso a frase
3 está marcada como **contaminada** (10.3) e não conta como evidência a
favor da janela.

### 3.3 Detalhes do algoritmo

- Um token da frase casa uma palavra de conteúdo do termo quando os
  **radicais normalizados** (seções 1–2) são iguais.
- Para cada termo, procura-se a ocorrência mais à esquerda e mais curta em
  cada oração; ocorrências do mesmo termo que não se sobreponham são todas
  registradas.
- **Tokens consumidos** por um casamento = as posições das suas palavras de
  conteúdo (os tokens do intervalo não são consumidos).

## 4. Negação (estilo NegEx)

Adaptação para o português do algoritmo NegEx (Chapman et al., 2001):
lista fechada de gatilhos de negação, escopo limitado e termos de terminação
de escopo.

### 4.1 Gatilhos

| Gatilho | Tipo | Escopo |
|---|---|---|
| `não`, `nem`, `nunca`, `sem` | pré-negação | termos **depois** do gatilho, até o fim da oração |
| `nenhum`, `nenhuma` | pós-negação | termos **antes** do gatilho, desde o início da oração ("dor nenhuma") |

Formas comparadas depois da normalização (sem acento: `nao`). Nenhum outro
gatilho é usado (ex.: `nada` fica de fora — limitação declarada).

### 4.2 Fronteira de oração (fim do escopo e limite do casamento)

- Sinais de pontuação: `,` `.` `;` `:` `!` `?`
- Conjunções adversativas: `mas`, `porém`, `contudo`, `entretanto`, `todavia`
- Conjunção aditiva: **`e`** — sempre fronteira.

**Critério para o `e`.** Sem etiquetador morfossintático não se distingue
coordenação de sintagmas ("não sinto dor **e** falta de ar", em que a
negação se distribui) de coordenação de orações ("não tenho febre **e**
estou com dor", em que não se distribui). Diante da ambiguidade, a escolha
segue a **assimetria de custo da Fase 1**: tratar `e` como fronteira faz o
erro cair do lado de **não negar** (conta um sintoma a mais — falso positivo,
custo de um exame), e não do lado de **negar demais** (descarta um sintoma
real — falso negativo, custo potencial de um infarto mandado para casa).
Nenhum termo do mapa contém a palavra `e`, então tratá-la como fronteira não
impede nenhum casamento.

### 4.3 Regra crítica: marcador que faz parte do termo não nega

Ordem do algoritmo:

1. casar todos os termos (seção 3) e resolver sobreposições (seção 5);
2. **só então** identificar gatilhos: um token de negação é gatilho **apenas
   se não foi consumido** por um casamento aceito;
3. aplicar o escopo de cada gatilho aos casamentos da mesma oração.

Como `sem` é palavra de conteúdo obrigatória de `sem fôlego` e `sem forças`
(3.1), o casamento consome o `sem` e ele deixa de ser gatilho. Em "sem dor
nenhuma", nenhum termo do mapa consome o `sem` (`dor` sozinho não é termo),
então `sem` e `nenhuma` são gatilhos — e negam o que houver de termo no
escopo. As duas coisas funcionam juntas pela ordem das etapas, sem exceção
escrita à mão.

Complementos:

- gatilho não consumido que fique **dentro do intervalo** de um casamento
  (entre suas palavras de conteúdo) nega esse casamento;
- dupla negação não é tratada (limitação declarada): "não estou sem
  fôlego" → `sem fôlego` fica negado pelo `não`, o que coincide com o
  sentido; outras combinações podem não coincidir.

## 5. Sobreposição: casamento mais longo vence

Os casamentos candidatos de uma oração são ordenados por: (1) número de
palavras de conteúdo, decrescente; (2) extensão em tokens, crescente;
(3) posição inicial. Aceita-se cada candidato cujos tokens consumidos não
estejam já consumidos por um aceito. Assim, os tokens de
`dor de cabeça súbita` não contam também para `dor de cabeça`.

Candidatos com **exatamente as mesmas posições consumidas e a mesma
sequência de radicais** são aceitos **juntos**: é o mesmo termo presente em
mais de um conceito ou doença (ex.: `tontura` em Hipertensão e AVC). É assim
que o sintoma compartilhado conta para cada doença (seção 7).

## 6. Termo de localização

**Configuração do extrator, separada do mapa congelado:**

```
TERMOS_DE_LOCALIZACAO = ["braço esquerdo"]         # conceito (Sintoma 1) do mapa
RADICAIS_DE_DOR       = ["dor", "doend"]           # radicais RSLP de dor, dores, doendo — as formas de dor presentes no mapa
```

Um casamento de qualquer linha do conceito `braço esquerdo` **só conta** se a
mesma oração tiver um token com radical em `RADICAIS_DE_DOR` **não negado**
(o token pode estar dentro do próprio casamento, como em `dor no braço
esquerdo`). Justificativa: no mapa, `braço esquerdo` é o **local** da
irradiação da dor no peito, não um sintoma isolado; sem dor, "braço esquerdo"
numa frase ("formigamento no braço esquerdo") não é evidência de infarto.

`RADICAIS_DE_DOR` vem das formas de dor do próprio mapa (`dor`, `dores`,
`doendo`). Limitação declarada: `dói`/`doer` têm radicais `doi`/`do` e não
contam; não se acrescentam formas fora do mapa.

## 7. Pontuação

### 7.1 Conceito

Unidade de pontuação = **conceito**, identificado pelo `Sintoma 1` dentro de
uma doença. Linhas `tipo_termo = literal` declaram, por definição do mapa,
que dois termos literais da mesma página nomeiam **o mesmo sintoma**; por
isso os conceitos ligados por uma linha `literal` são **unidos** (componente
conexo, por doença). No mapa congelado isso une, em Infarto,
{`dor no peito`, `desconforto na região peitoral`} e
{`aperto sobre o tórax`, `sensação de peso`}. Sem essa união, uma única
menção a "sensação de peso" contaria dois conceitos (ela é Sintoma 1 de um e
Sintoma 2 literal de outro) — medido no vocabulário do mapa (2.2), não nas
frases.

### 7.2 Regra

- Pontuação de uma doença = **número de conceitos distintos** dessa doença
  com pelo menos um casamento aceito, **não negado** e válido (regra de
  localização). "tontura" e "tonto" na mesma frase contam **uma** vez.
- Sintoma compartilhado conta **1 para cada doença** a que pertence.
- **Peso igual (1) para conceito exclusivo e compartilhado.** Justificativa:
  qualquer peso diferente (ex.: inverso do número de doenças do conceito)
  seria um parâmetro livre sem dado para estimá-lo — 10 frases de teste não
  servem para calibrar peso, e calibrar nelas seria overfitting. O efeito do
  compartilhamento aparece onde deve: na margem entre doenças (seção 8).

## 8. Confiança e ambiguidade

Sejam `p1` a maior pontuação, `p2` a segunda maior (0 se não houver) e
`margem = p1 − p2`.

| Nível | Regra exata |
|---|---|
| **sem sugestão** | `p1 = 0` |
| **ambíguo** | `p1 ≥ 1` e `margem = 0` — reporta todas as doenças empatadas em `p1` |
| **baixa** | `p1 = 1` e `p2 = 0` |
| **média** | `p1 ≥ 2`, `margem ≥ 1`, e não é alta |
| **alta** | `p1 ≥ 3` e `margem ≥ 2` |

As regras são mutuamente exclusivas e cobrem todos os casos. Os limiares são
os menores inteiros com leitura direta ("um único indício", "vence por um",
"vence por dois com três indícios") e foram fixados sem otimização.
**Valem para as 10 frases como vier: se o resultado divergir do gabarito, a
divergência é resultado a reportar, não motivo para mexer na regra.**

## 9. Saída por frase

Para cada frase, o extrator imprime e grava em
`document/fase-02/resultado-extrator.md` (arquivo gerado, não editado à mão):

- número e texto da frase;
- **termos casados**: termo do mapa, linha do CSV, doença, conceito, tokens
  da frase que casaram (para expor over-stemming e janela) e método
  (baseline exato / método);
- **termos negados**: termo, linha do mapa e gatilho responsável;
- **termos de localização descartados** (sem dor na oração);
- **pontuação por doença**;
- **sugestão** (doença ou empatadas) e **confiança**;
- o aviso: *"Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade
  para diagnóstico ou decisão médica."*

No cabeçalho do resultado: data da execução; SHA-256 do protocolo, do mapa,
das frases e do código; e, para cada recurso da NLTK, hash esperado,
encontrado e se confere (2.5).

## 10. Avaliação

### 10.1 Baseline exato

Idêntico ao método em **tudo** (normalização de caixa e acento, fronteiras,
negação, sobreposição, localização, pontuação, confiança), **exceto**:
sem radicalização e casamento por **sequência exata e contígua de todos os
tokens do termo** (inclusive stopwords). Assim a diferença entre as duas
colunas isola o efeito das seções 2 e 3.

### 10.2 Critério de acerto

| Frase | Acerto de doença | Acerto de confiança |
|---|---|---|
| 1–6, 8, 9 | sugestão única = doença esperada no gabarito | não avaliado (reportado) |
| 7 | nível **ambíguo** com empate exatamente entre Hipertensão e AVC | — |
| 10 | sugestão = Infarto | confiança = **baixa** |

Empate que inclui a doença esperada, quando o gabarito espera doença única,
conta como **erro** (ambíguo onde se esperava decisão).

### 10.3 Frases contaminadas

Decisões cujo efeito numa frase de teste era previsível pelo conhecimento
declarado na seção 0. Nessas frases, um acerto do método **não conta como
evidência** a favor da decisão; é reportado, mas marcado.

| Frase | Decisão | O que já se sabia |
|---|---|---|
| 3 | Janela de 2 tokens (3.2) | O casamento exato falha em "minha fala ficou enrolada" |
| 1 | Regra de localização (6) | A frase cita braço esquerdo ao lado de dor no peito |
| 10 | Nível "baixa" = 1 conceito (8) | A frase tem um único termo casado literalmente |

### 10.4 Tabela de resultado

Gerada pelo extrator, uma linha por frase:

| # | Gabarito | Baseline exato (sugestão, confiança) | Método (sugestão, confiança) | Acerto baseline | Acerto método | Contaminada | Explicação da divergência |
|---|---|---|---|---|---|---|---|

A coluna "Explicação da divergência" é escrita **depois** da execução, pelo
grupo, a partir da saída — sem alterar regra, mapa ou frase.

### 10.5 Execução única e desvios

1. Antes da execução nas frases, o código passa pelos **testes de unidade
   pré-registrados** abaixo — frases sintéticas escritas para testar cada
   regra, **distintas das 10 frases de teste**. Esses testes podem ser
   rodados quantas vezes for preciso: testam se o código implementa o
   protocolo, não o desempenho.
2. O extrator roda **uma vez** nas 10 frases. A saída é gravada como saiu.
3. Se depois disso for encontrado um **bug** (o código não faz o que o
   protocolo diz), a correção é permitida, mas os **dois** resultados (antes
   e depois) são reportados, com a descrição do bug. **Mudança de regra do
   protocolo não é bug** e não é permitida depois da execução.

### 10.6 Testes de unidade pré-registrados

| # | Entrada sintética | Esperado | Regra testada |
|---|---|---|---|
| U1 | "estou sem fôlego desde cedo" | `sem fôlego` casado, **não** negado | 4.3 — `sem` consumido pelo termo |
| U2 | "passei o dia sem forças" | `sem forças` casado, **não** negado | 4.3 |
| U3 | "sem dor nenhuma no peito" | `dor no peito` casado (intervalo de 2: `nenhuma no`) e **negado** — `sem` é gatilho (não consumido) e `nenhuma` é gatilho dentro do intervalo | 3.2, 4.1, 4.3 |
| U4 | "não tenho tontura, mas estou com dor de cabeça súbita" | `tontura` negado; `dor de cabeça súbita` (AVC) aceito; `dor de cabeça` (Hipertensão) **não** aceito | 4.2, 5 |
| U5 | "não sinto palidez e estou com falta de ar" | `palidez` negado; `falta de ar` **não** negado | 4.2 — `e` como fronteira |
| U6 | "formigamento no braço esquerdo desde ontem" | `braço esquerdo` descartado (sem dor na oração) | 6 |
| U7 | "uma dor forte que desce para o braço esquerdo" | `braço esquerdo` conta | 6 |
| U8 | "não tenho dor, o braço esquerdo formiga" | `braço esquerdo` descartado (vírgula separa; dor da outra oração está negada) | 6, 4.2 |
| U9 | "um aperto bem forte sobre o tórax" | `aperto sobre o tórax` casado (intervalo de 2 entre `aperto` e `sobre`) | 3.2 |
| U10 | "um aperto que começou ontem à tarde sobre o tórax" | `aperto sobre o tórax` **não** casado (intervalo > 2) | 3.2 |
| U11 | "fiquei tonto e com tontura o dia todo" | conceito `tontura` (AVC) e `tonturas` (Hipertensão) contam **1** cada | 7.2 |
| U12 | "sinto sensação de peso" | Infarto soma **1** conceito, não 2 | 7.1 |
| U13 | "meus pais moram longe" | `pálido` casado por over-stemming (`pais → pal`) — **falso positivo esperado e declarado** | 2.4 |
| U14 | "tive tonturas ontem" (baseline) | baseline casa `tonturas` (Hipertensão) e não casa `tontura` (AVC) | 10.1 |

U13 existe para provar que o risco declarado em 2.3 é real e aparece na
saída — não para ser corrigido.

## Referências

- Chapman, W. W., Bridewell, W., Hanbury, P., Cooper, G. F., & Buchanan, B. G.
  (2001). A simple algorithm for identifying negated findings and diseases in
  discharge summaries. *Journal of Biomedical Informatics*, 34(5), 301–310.
  DOI `10.1006/jbin.2001.1029`.
- Orengo, V. M., & Huyck, C. (2001). A stemming algorithm for the Portuguese
  language. In *Proceedings of the 8th International Symposium on String
  Processing and Information Retrieval (SPIRE 2001)*, pp. 186–193. IEEE
  Computer Society. DOI `10.1109/SPIRE.2001.989755`.

  > **Nota sobre o DOI:** há pacotes de R que citam este trabalho com o DOI
  > `10.1109/SPIRE.2001.10024`. O DOI registrado no DBLP e confirmado pelo
  > Crossref é `10.1109/SPIRE.2001.989755`, que é o usado aqui (verificação
  > feita pelo grupo em 2026-09-23).
- Bird, S.; Klein, E.; Loper, E. (2009). *Natural Language Processing with
  Python*. O'Reilly — documentação de referência da NLTK (RSLPStemmer,
  corpus `stopwords`).
- Apache Lucene — `SpanNearQuery` (casamento por proximidade com `slop` e
  `inOrder`), documentação da API.
