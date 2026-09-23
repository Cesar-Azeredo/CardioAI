# Governança de dados e viés — Fase 2

Complementa `document/fase-01/governanca-e-vies.md` (que continua valendo
para as bases da Fase 1) com as decisões de governança tomadas na Fase 2.
Decisões numeradas conforme a seção 5bis do `CLAUDE.md`/`AGENTS.md`.

## Fontes do mapa de conhecimento

| Doença | Fonte | Licença verificada | Data de acesso |
|---|---|---|---|
| Hipertensão | Texto 2 da Fase 1 — Ministério da Saúde, "Hipertensão (pressão alta)" | **CC BY-ND 3.0** | 2026-08-27 |
| Infarto | Texto 3 — Ministério da Saúde, "Infarto" (Saúde de A a Z) | **CC BY-ND 3.0** | 2026-09-23 |
| AVC | Texto 4 — Ministério da Saúde, "Acidente Vascular Cerebral (AVC)" (Saúde de A a Z) | **CC BY-ND 3.0** | 2026-09-23 |

Fichas completas em `assets/textos/PROVENIENCIA.md` (Texto 2) e
`assets/textos/fase-02/PROVENIENCIA.md` (Textos 3 e 4). Licença lida do link
`rel="license"` de cada página no momento da coleta, não assumida.

### Fontes complementares da BVS — retiradas do escopo

**Fontes complementares da BVS inacessíveis (HTTP 503 em todo o domínio,
verificado por script e navegador em 2026-09-23), retiradas do escopo.**

- Páginas: `https://bvsms.saude.gov.br/ataque-cardiaco-infarto/` e
  `https://bvsms.saude.gov.br/avc-acidente-vascular-cerebral/`.
- O servidor devolveu a página de bloqueio do WAF ("The requested URL was
  rejected") para qualquer URL do domínio, inclusive a home — via `requests`
  com cabeçalhos de navegador e via navegador real (Playwright).
- Eram **complementares**: infarto e AVC já têm fonte primária do Ministério
  da Saúde no gov.br. Por isso a decisão foi retirar, não contornar.
- Consequência: **nenhuma linha do mapa se apoia nelas**, e o script de
  coleta (`scripts/fase-02/00_coleta_fontes_mapa.py`) não tenta mais
  baixá-las, para não depender de domínio fora do ar.

### Lacuna documentada: insuficiência cardíaca e angina

O mapa cobre **três doenças — hipertensão, infarto e AVC**. Não cobre
insuficiência cardíaca nem angina, e isso é decisão, não esquecimento:

- não há página equivalente do Ministério da Saúde (Saúde de A a Z) para
  insuficiência cardíaca nem para angina; as fontes encontradas pelo grupo
  para essas duas condições são de hospital privado, sem o mesmo peso
  institucional;
- **preferimos três doenças com proveniência oficial a cinco com metade sem
  fonte verificável.** Num mapa de conhecimento que alimenta sugestão de
  diagnóstico, uma linha sem fonte é uma afirmação clínica sem lastro — e o
  extrator a usaria com o mesmo peso das linhas com fonte;
- o enunciado cita insuficiência cardíaca e angina **apenas como exemplo de
  formato**, não como requisito de cobertura.

Efeito prático a registrar desde já: um relato típico de insuficiência
cardíaca ou de angina **não tem para onde ser mapeado** — o extrator só
pode sugerir uma das três doenças do mapa, ou nenhuma. Isso é limitação
conhecida do escopo, não erro do extrator.

**Observação sobre a restrição de licença:** as três páginas são CC BY-ND
3.0. O mapa de conhecimento **analisa** os textos (extrai o termo e cita o
trecho literal que o ancora), o que a licença permite; as frases de paciente
são redação própria do grupo, sem paráfrase de trecho das páginas.

## Exceção à regra 4 — dado primário autoral sintético

A regra 4 do `CLAUDE.md`/`AGENTS.md` ("nunca edite arquivos de dados
manualmente") proíbe **transformar** dado à mão: todo dado derivado precisa
sair de script reprodutível. Os artefatos da Fase 2 abaixo **não são
transformação — são a origem**:

- `assets/textos/fase-02/frases-sintomas-pacientes.txt` (10 frases);
- `document/datasets/fase-02/mapa-conhecimento-sintomas.csv`;
- o `.csv` de frases rotuladas em alto/baixo risco (80 frases, 40/40).

Cada frase, cada rótulo e cada linha do mapa é uma **decisão de autoria** do
grupo — não existe arquivo anterior do qual eles pudessem ser derivados por
script. Tratá-los como dado primário sintético autoral é a descrição honesta
do que eles são.

A exceção tem limites:

1. vale **só** para o dado primário; qualquer derivado dele (extração de
   sintomas, features TF-IDF, métricas) sai de script;
2. todo arquivo autoral tem ficha em `document/datasets/fase-02/README.md`:
   autores, data, critério de redação, critério de rotulagem/inclusão;
3. o que puder ser checado por máquina é checado por script — no mapa, todo
   termo marcado como vindo da fonte é verificado literalmente contra o
   `.txt` indicado; linha que não passa não entra.

## Compromissos assumidos na Fase 1

A tabela de mitigações de `document/fase-01/governanca-e-vies.md` atribuiu
duas mitigações à Fase 2. As duas foram escritas quando o roadmap previa que
a Fase 2 modelaria o dataset numérico (UCI); o enunciado real da Fase 2 é de
NLP. Situação de cada uma, **sem fingir cumprimento**:

| Compromisso da Fase 1 | Situação na Fase 2 |
|---|---|
| Métricas estratificadas por sexo e faixa etária, não só acurácia global | **Transferido em espírito** para o classificador de texto. Não há sexo nem idade nas frases (e inventar essas variáveis em dado sintético seria estratificação de fachada), mas o princípio — não esconder o erro caro atrás de uma média — se aplica integralmente. O notebook reporta matriz de confusão, recall e F1 **por classe**, com destaque para o **recall de "alto risco"**, e explica por que acurácia global é insuficiente, retomando a assimetria de custo da Fase 1: um falso negativo em alto risco é um paciente mandado para casa durante um evento cardíaco. |
| Imputação de `ca`/`thal` dentro de cada fold, nunca antes do split | **Adiado formalmente.** Nenhum entregável da Fase 2 modela o UCI, então não há split nem fold onde cumpri-lo. O compromisso segue para a **Fase 6**, primeira fase do roadmap que consome o dataset numérico. `document/datasets/dicionario-de-dados.md` foi atualizado para refletir isso. |

## Reprodutibilidade dos artefatos da Fase 1

Ao avaliar a subida do `numpy` de `2.0.2` para `2.1.3` (versão atual do
Colab), os scripts 01–05 da Fase 1 foram rodados de ponta a ponta em venv
limpa, nas duas versões, e os artefatos regerados foram comparados com os
versionados (2026-09-23):

- **Byte-idênticos nas duas versões:** `heart-disease-processed.csv`, os
  dois `.txt` da Fase 1, `assets/textos/PROVENIENCIA.md`,
  `manifest-imagens.csv`, as 12 amostras de `assets/imagens/amostras/` e as
  120 imagens selecionadas.
- **`heart-disease-processed.xlsx` não é byte-reprodutível**, com nenhuma
  versão de numpy: o único arquivo interno do `.xlsx` que difere é
  `docProps/core.xml`, onde o openpyxl grava a data e hora de criação do
  arquivo (`dcterms:created`/`dcterms:modified`). A planilha em si
  (`xl/worksheets/sheet1.xml`), estilos, workbook e demais partes são
  idênticos. **Isso não afeta os dados** — só o carimbo de quando o arquivo
  foi gerado.

Decisão: **numpy permanece em `2.0.2`.** A regressão de conteúdo passou, mas
a subida não traz benefício — quando o notebook for aberto no Colab, ele usa
o numpy do próprio Colab, não o do `requirements.txt`. Nenhum artefato da
Fase 1 foi alterado nesta verificação (tudo rodou em cópias do repositório,
fora da árvore versionada).

Consequência para quem comparar hashes no futuro: comparar o `.xlsx` por
conteúdo (planilha e estilos), não pelo MD5 do arquivo inteiro.

## Viés de gênero: apoio de fonte aos achados da Fase 1

Referência: Mehta, L. S. et al. (2016). *Acute Myocardial Infarction in
Women*. Circulation, 133(9), 916–947. DOI `10.1161/CIR.0000000000000351`
(declaração científica da American Heart Association; conteúdo verificado
pelo grupo na página da editora em 2026-09-23; o texto do artigo não é
reproduzido no repositório). Os dois achados abaixo estão em paráfrase.

1. **Escores de risco desenvolvidos em populações masculinas.** A seção
   *Prognostic Factors* da declaração afirma que os escores de risco para
   síndrome coronariana aguda foram desenvolvidos em populações pelo menos
   dois terços masculinas e que o desempenho deles em mulheres não está bem
   estabelecido. É o mesmo padrão da base Cleveland usada na Fase 1 (68%
   masculina — ver `document/fase-01/governanca-e-vies.md`) e o risco que o
   teste contrafactual de gênero do conjunto-desafio (pares G1–G3,
   `document/datasets/fase-02/desafio-risco.csv`) vai medir no classificador
   da Fase 2.
2. **Mulheres encaminhadas menos para investigação invasiva.** A declaração
   relata que mulheres com síndrome coronariana aguda passam menos por
   cateterismo e angiografia, em parte porque o risco delas é subestimado.
   Isso dá apoio de fonte à hipótese de **viés de encaminhamento** levantada
   na Fase 1 para a base Cleveland (pacientes encaminhados para angiografia;
   mulheres sub-representadas entre os casos investigados).

A Fase 1 foi entregue e avaliada e **não é alterada**: este registro fica só
na Fase 2 e remete ao documento da Fase 1.

Consequência prática nesta fase: o dataset rotulado da Parte 2 balanceia a
voz de gênero por classe (mínimo de 6 femininas e 6 masculinas marcadas em
cada uma) e o conjunto-desafio traz pares contrafactuais com predição
esperada idêntica — critério em `document/fase-02/criterio-rotulo-risco.md`,
seção 6.
