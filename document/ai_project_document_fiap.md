
<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=30% height=30%>

# AI Project Document - Módulo 1 - FIAP

## Nome do Grupo

Grupo Zion

#### Nomes dos integrantes do grupo

- Carlos Costato
- Phellype Flaibam
- Cesar Azeredo

## Sumário

[1. Introdução](#c1)

[2. Visão Geral do Projeto](#c2)

[3. Desenvolvimento do Projeto](#c3)

[4. Resultados e Avaliações](#c4)

[5. Conclusões e Trabalhos Futuros](#c5)

[6. Referências](#c6)

[Anexos](#c7)

<br>

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto da Inteligência Artificial

Doenças cardiovasculares são a principal causa de morte no mundo, com
aproximadamente 17,9 milhões de óbitos anuais (dado usado como justificativa
em todos os documentos desta entrega). Infartos, arritmias, insuficiência
cardíaca e AVCs são comuns e, em grande parte, preveníveis com diagnóstico
precoce — o que torna cardiologia um dos domínios onde IA aplicada à saúde
(triagem assistida, visão computacional sobre exames, NLP sobre prontuário e
literatura médica, IoT para monitoramento contínuo) tem valor concreto e
mensurável. É um segmento de abrangência internacional, com forte produção
acadêmica nacional (SciELO, Ministério da Saúde) e bases públicas
internacionais (UCI, Mendeley Data) já disponíveis para pesquisa.

### 1.1.2. Descrição da Solução Desenvolvida

**CardioIA** é um projeto acadêmico de 7 fases que constrói, incrementalmente,
uma plataforma que simula o ecossistema de uma cardiologia moderna:
diagnóstico assistido por Machine Learning, monitoramento por IoT/wearable,
Visão Computacional sobre exames de imagem, um assistente virtual por NLP e
previsão de crises por séries temporais.

Esta entrega corresponde à **Fase 1 — Batimentos de Dados**, na qual o grupo
assume o papel de cientista de dados hospitalar para levantar, tratar e
documentar as três bases fundamentais que todas as fases seguintes vão
consumir: um dataset numérico de fatores de risco cardíaco, um corpus textual
técnico/leigo sobre saúde cardiovascular, e um conjunto de imagens de ECG.
Cada base foi coletada de fonte pública verificada, tratada por script
reprodutível e documentada com proveniência, licença e viés medido —
detalhamento completo em `document/fase-01/`.

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

Preparar, para as fases 2 a 7, três bases de dados cardiológicos prontas para
uso em IA — organizadas, com proveniência registrada e vieses documentados —
sem ainda treinar modelo algum (isso começa na Fase 2). Concretamente:

1. Dataset numérico com ≥100 pacientes e variáveis de risco cardiovascular
   (idade, sexo, pressão arterial, colesterol, frequência cardíaca etc.).
2. Corpus textual (≥2 textos) que contraste vocabulário técnico e leigo sobre
   saúde cardiovascular.
3. Conjunto de imagens de ECG (≥100) rotuladas por categoria diagnóstica.
4. Documentação de governança de dados e viés que as fases seguintes
   precisam respeitar ao consumir essas bases.

## 2.2. Público-Alvo

Nesta fase, o "usuário" é a própria equipe do projeto nas fases seguintes
(Fases 2 a 7) e o corpo avaliador da FIAP. No horizonte final da plataforma
(Fase 7), o público-alvo é a equipe clínica de uma unidade de cardiologia
(triagem e monitoramento assistidos) e, no módulo de assistente virtual
(Fase 5), o próprio paciente em acompanhamento domiciliar.

## 2.3. Metodologia

Método PBL (Project Based Learning) em monorepo incremental — cada fase é
avaliada separadamente, mas todas as fases posteriores consomem os artefatos
das anteriores, então a organização do repositório é por função (`document/`,
`scripts/`, `notebooks/`, `assets/`) e não por fase isolada. Para cada uma
das três partes desta entrega, o processo foi: (1) travar a fonte com o
time e verificar proveniência/licença na própria página, nunca de memória;
(2) escrever um script reprodutível de coleta; (3) perfilar/investigar o
dado bruto antes de qualquer tratamento; (4) tratar com decisões explícitas
e justificadas (nunca editar dado manualmente); (5) documentar variáveis,
justificativa clínica e viés. Detalhe completo de cada etapa em
`document/fase-01/dados-numericos.md`, `dados-textuais.md`, `dados-visuais.md`
e `governanca-e-vies.md`.

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

Python 3.12 (travado para paridade com o runtime do Google Colab, que passa
a importar a partir da Fase 4 — TensorFlow/PyTorch). Bibliotecas: `pandas`,
`numpy`, `openpyxl` (dataset numérico), `ucimlrepo` (coleta UCI),
`beautifulsoup4` + `requests` (extração de texto web), `Pillow` + `numpy`
(processamento e hash perceptual de imagem), `matplotlib` e `jupyter`
(reservados para EDA em notebook). Versões travadas em `requirements.txt`.

## 3.2. Modelagem e Algoritmos

Não aplicável nesta fase — a Fase 1 é de coleta, tratamento e documentação de
dados, sem modelo preditivo. A modelagem propriamente dita começa na Fase 2
(classificadores supervisionados sobre o dataset numérico) e na Fase 4 (CNN
sobre o conjunto de imagens de ECG). A única técnica algorítmica usada nesta
fase foi de **preparação de dado**, não de modelagem: hash perceptual (dHash)
para detectar quase-duplicata nas imagens antes da amostragem — descrita em
`document/fase-01/dados-visuais.md` e `governanca-e-vies.md`.

## 3.3. Treinamento e Teste

Não aplicável nesta fase, pelo mesmo motivo acima. As bases entregues aqui —
com split ainda não definido — são o insumo que a Fase 2 (dataset numérico)
e a Fase 4 (imagens) vão usar para treinar e testar modelos supervisionados.
As mitigações de viés já deixadas prontas para essas fases (deduplicação
antes do split, split por conteúdo e não por nome de arquivo, imputação
dentro do fold) estão detalhadas em `document/fase-01/governanca-e-vies.md`.

# <a name="c4"></a>4. Resultados e Avaliações

## 4.1. Análise dos Resultados

**Parte 1 — Dataset numérico** ([detalhe completo](fase-01/dados-numericos.md)):
UCI Heart Disease, base Cleveland, 303 pacientes, 15 colunas após tratamento,
licença CC BY 4.0. Ausências em `numero_vasos_fluoroscopia` (4) e
`talassemia` (2) preservadas deliberadamente (MNAR — imputar apagaria sinal
clínico, e imputar antes do split seria vazamento de dado). Alvo mantido em
duas formas: `num` (severidade original, 0–4) e `alvo_binario` (derivado,
54,1%/45,9%). Cruzamento sexo × alvo: 25,8% de prevalência em mulheres
contra 55,3% em homens — achado levado à seção de viés.

**Parte 2 — Corpus textual** ([detalhe completo](fase-01/dados-textuais.md)):
dois textos, contraste deliberado de registro — um técnico-científico
(SciELO, 1.608 palavras, CC BY-NC 3.0) e um de comunicação em saúde pública
(Ministério da Saúde, 858 palavras, CC BY-ND 3.0, salvo sem alteração de
conteúdo por exigência da licença). Justificativa das três técnicas de NLP
do enunciado (extração de sintomas, classificação de tópicos, análise de
sentimento) com exemplo real de cada texto no documento completo.

**Parte 3 — Imagens de ECG** ([detalhe completo](fase-01/dados-visuais.md)):
Mendeley Data, *ECG Images dataset of Cardiac Patients* v2, CC BY 4.0. Do
dataset completo (928 arquivos), **apenas 491 são imagens de conteúdo único
por hash MD5** (47% de redundância) — achado medido, não estimado, que
motivou deduplicação obrigatória antes da amostragem. Seleção final: 120
imagens, balanceadas 30/30/30/30 por categoria, semente fixa 42, sem
recompressão.

**Governança e viés** ([detalhe completo](fase-01/governanca-e-vies.md)):
proveniência e licença das quatro fontes verificadas na própria página (não
assumidas — corrigimos nós mesmos um erro de licença do dataset Mendeley
durante a verificação); LGPD e a distinção entre ID interno de equipamento e
identificação de pessoa; viés de encaminhamento por sexo medido na base UCI;
e uma demonstração empírica própria de *shortcut learning* nas imagens de
ECG (hash raso confundiu template do aparelho com conteúdo clínico).

## 4.2. Feedback dos Usuários

Não aplicável nesta fase: o projeto ainda não tem usuário final nem protótipo
em uso — a entrega é a base de dados que sustenta as fases seguintes. O
"feedback" desta fase foi o processo iterativo de verificação dentro do
próprio grupo (ex.: a correção da licença do dataset Mendeley e do valor real
de FC nas checagens de plausibilidade, ambos descritos em
`governanca-e-vies.md`).

# <a name="c5"></a>5. Conclusões e Trabalhos Futuros

A Fase 1 entregou as três bases exigidas, todas com proveniência verificada
na fonte, tratamento reprodutível por script e viés medido em vez de
presumido. O ponto forte da entrega é metodológico: cada decisão de
tratamento (preservar ausência, manter alvo em duas formas, deduplicar antes
de amostrar) tem justificativa escrita e ligada à fase que vai consumi-la.

Pontos a melhorar, encaminhados como trabalho futuro: (1) os links públicos
dos conjuntos completos (numérico e imagens) ainda não foram publicados —
ver TODOs no `README.md`; (2) a data de publicação do Texto 2 não foi
localizada na página-fonte; (3) a mitigação de viés proposta
(estratificação por sexo/idade, deduplicação por conteúdo antes do split,
validação externa) precisa ser efetivamente implementada nas Fases 2, 4 e 6
— aqui ela só foi especificada.

# <a name="c6"></a>6. Referências

- Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1989). *Heart
  Disease* [Dataset]. UCI Machine Learning Repository. DOI `10.24432/C52P4X`.
- Pellanda, L. C. (2014). Trajetórias da Saúde Cardiovascular: Epidemiologia
  do Curso da Vida no Brasil [editorial]. *Arquivos Brasileiros de
  Cardiologia*, 102(5), 418–419. DOI `10.5935/abc.20140065`.
- Ministério da Saúde. *Hipertensão (pressão alta)*. Saúde de A a Z.
  Disponível em: https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/h/hipertensao
- Khan, A. H., & Hussain, M. (2021). *ECG Images dataset of Cardiac Patients*
  (Version 2) [Data set]. Mendeley Data. DOI `10.17632/gwbz3fsgp8.2`.
- Khan, A. H., Hussain, M., & Malik, M. K. (2021). ECG images dataset of
  Cardiac and COVID-19 patients. *Data in Brief*, 34, 106762. DOI
  `10.1016/j.dib.2021.106762`. (Artigo descritor da v1 do dataset acima —
  licença própria, CC BY-NC-ND, diferente da licença do dataset.)

# <a name="c7"></a>Anexos

## Dicionário de dados

`document/datasets/dicionario-de-dados.md` — variável, tipo, unidade, faixa
de sanidade, nº de ausências e significado clínico de cada coluna do
dataset numérico, incluindo a legenda completa dos códigos categóricos
extraída da documentação oficial da UCI.

## Manifest de imagens

`document/datasets/processed/manifest-imagens.csv` — as 120 imagens
selecionadas, com nome original, categoria, dimensões, hash MD5 e os
*aliases* (nomes de arquivo duplicados por conteúdo no dataset-fonte).

## Tabela de proveniência

`document/datasets/README.md` — fonte, URL, DOI, licença, data de acesso, nº
de registros e citação formal das quatro bases.

## Scripts reprodutíveis

`scripts/fase-01/01` a `05` — coleta e perfilamento do dataset numérico,
tratamento, preparação dos textos e organização das imagens, nessa ordem.
Passo a passo de execução no `README.md` da raiz.
