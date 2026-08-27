# Governança de dados e viés — Fase 1

Documento consolidado das três bases (numérica, textual, visual) coletadas
nesta fase. Complementa `document/fase-01/dados-numericos.md`,
`dados-textuais.md` e `dados-visuais.md` — aqui o foco é proveniência,
LGPD, viés medido e mitigação, não a descrição técnica de cada base.

## Proveniência e licença

| Base | Fonte | Licença verificada | Data de acesso |
|---|---|---|---|
| UCI Heart Disease (Cleveland) | UCI Machine Learning Repository | **CC BY 4.0** | 2026-08-27 |
| Texto 1 — Trajetórias da Saúde Cardiovascular | SciELO / Arq. Bras. Cardiol. | **CC BY-NC 3.0** | 2026-08-27 |
| Texto 2 — Hipertensão (pressão alta) | Ministério da Saúde | **CC BY-ND 3.0** (SemDerivações) | 2026-08-27 |
| ECG Images dataset of Cardiac Patients v2 | Mendeley Data | **CC BY 4.0** | 2026-08-27 |

Todas as licenças acima foram **verificadas na própria página de origem**,
não assumidas. Isso importa registrar porque nós mesmos erramos uma vez: a
primeira versão deste projeto (seção 5.3 do `CLAUDE.md`/`AGENTS.md`, antes da
verificação) assumia que o dataset Mendeley era CC BY-NC-ND. Essa licença
existe, mas pertence ao **artigo descritor** (Khan, Hussain & Malik, 2021,
*Data in Brief*, DOI `10.1016/j.dib.2021.106762`) — um documento diferente,
com licença diferente. **O dataset em si é CC BY 4.0**, confirmado no bloco
JSON-LD `schema.org` e no bloco de metadados da página do Mendeley. A
correção só aconteceu porque a licença foi verificada na fonte primária em
vez de herdada do artigo relacionado — é o próprio caso de uso que esta
seção do documento existe para prevenir.

## LGPD (Lei 13.709/2018)

Dado de saúde é dado pessoal **sensível** (art. 5º, II c/c art. 11 da LGPD).
Nenhuma das quatro bases contém identificador direto de pessoa:

- **UCI Heart Disease**: a documentação oficial da fonte (`heart-disease-metadata.json`,
  campo `additional_info.summary`) declara explicitamente que nomes e números
  de segurança social dos pacientes **foram removidos e substituídos por
  valores fictícios** antes da publicação.
- **ECG Images (Mendeley)**: cada imagem imprime, dentro do próprio traçado,
  um campo `ID:` numérico (ex.: `177333`, `168592`), além de data/hora do
  exame e frequência cardíaca. **Esse ID é interno ao equipamento EDAN
  SERIES-3** (numeração sequencial de exame, não CPF, não prontuário, não
  nome), e a base é pública, distribuída pelos próprios autores sob licença
  aberta — não há identificação de pessoa aqui. **Isso não elimina o
  princípio geral**: em qualquer contexto de captura real (não apenas nesta
  base pública já tratada), um ID de equipamento associado a data/hora é
  metadado com potencial de reidentificação — cruzado com registro de
  agendamento do exame, ele reconstrói quem esteve na clínica naquele
  horário. Qualquer captura própria do projeto nas fases seguintes (ex.:
  wearable da Fase 3) precisa mascarar ou não registrar esse tipo de metadado
  junto da imagem/leitura.
- **Textos**: nenhum dos dois é relato de paciente identificável — um é
  editorial científico, outro é conteúdo institucional do Ministério da
  Saúde.

**Restrição de licença que já afetou o processamento**: o Texto 2 está sob
CC BY-ND 3.0 (SemDerivações). Isso não é uma questão de LGPD, mas de direito
autoral, e teve efeito prático direto: o texto foi extraído e salvo **sem
nenhuma alteração de conteúdo** (só normalização de espaço em branco da
conversão HTML→texto) — nada de resumir, reescrever ou cortar trecho. Essa
restrição se propaga para a Fase 5: qualquer chatbot que reescreva ou resuma
automaticamente trechos deste texto específico ao paciente está, no limite,
criando obra derivada sob uma licença que a proíbe.

## Finalidade

Uso **exclusivamente acadêmico**, sem validação clínica. Nada neste
repositório foi avaliado por autoridade regulatória de saúde e nada aqui
deve informar decisão médica real, diagnóstico ou tratamento de paciente.

## Viés — nomeado e medido

### UCI Heart Disease (Cleveland)

- **Coleta de 1989**, um único hospital nos EUA. Um modelo treinado aqui
  carrega o perfil epidemiológico e a prática clínica americana de há 37
  anos, não a população brasileira de 2026.
- **Base de encaminhamento para angiografia**: os 303 pacientes não são uma
  amostra da população geral — são pacientes que já haviam sido encaminhados
  para investigação invasiva de doença coronariana, isto é, uma amostra
  pré-filtrada por suspeita clínica.
- **68% masculina** (206 de 303) e **prevalência do alvo desigual por sexo**:
  25,8% em mulheres (25 de 97) contra 55,3% em homens (114 de 206) — mais que
  o dobro.
- **Viés de encaminhamento, não só epidemiologia**: parte dessa diferença é
  epidemiológica de fato (doença coronariana é mais prevalente e mais
  precoce em homens), mas a literatura de cardiologia documenta que mulheres
  com dor torácica são historicamente **menos encaminhadas** para
  investigação invasiva do que homens com sintoma equivalente. Isso significa
  que a base já chega sub-representando casos femininos que existiam mas não
  foram investigados.
- **Consequência prática**: um classificador treinado sem correção tende a
  **subdetectar em mulheres** — aprende que "mulher" correlaciona com "menor
  prevalência do alvo" mesmo quando a apresentação clínica é equivalente à de
  um homem positivo. Numa triagem real, isso é falso negativo sistemático
  no subgrupo já historicamente sub-investigado.

### ECG Images dataset (Mendeley)

- **Um único país** (Paquistão), **um único modelo de equipamento** (EDAN
  SERIES-3), um único centro (Ch. Pervaiz Elahi Institute of Cardiology,
  Multan). Nenhuma variação de aparelho, template de relatório ou população
  na base inteira.
- **Redundância de conteúdo medida, não estimada**: dos 928 arquivos
  baixados, apenas **491 são imagens de conteúdo único por hash MD5** — 47%
  de redundância. Por categoria: infarto do miocárdio 239→30 (**87%** de
  redundância), histórico de infarto 172→86 (50%), pessoa normal 284→142
  (50%), batimento anormal 233→233 (**0%**, nenhuma duplicata). A
  redundância não é uniforme entre categorias — a categoria "infarto" tem
  quase 9 em cada 10 arquivos como cópia exata de outro arquivo já contado.
- **Arquivo ausente**: `MI(215).jpg` não existe no download, apesar do nome
  da pasta anunciar 240 pacientes (239 encontrados).

### Shortcut learning — evidência empírica própria, não hipotética

Este é o achado mais forte deste documento porque não é uma preocupação
teórica: **nós reproduzimos o mecanismo do viés durante a preparação dos
dados.**

Ao investigar quase-duplicatas por hash perceptual (dHash) antes de
sortear a amostra, a primeira tentativa usou um hash de 8×8 (64 bits) — um
tamanho comum para esse tipo de checagem. O resultado foi **distância 0
(hashes idênticos) entre pares de imagens da categoria "batimento anormal"
que sabíamos, por MD5, serem arquivos byte a byte diferentes** — ou seja,
comprovadamente exames diferentes, marcados pelo hash raso como
"imagem idêntica". A causa: com resolução tão baixa, o hash captura só o
**layout compartilhado por todo o dataset** (a grade do papel milimetrado,
a posição do cabeçalho "ECG REPORT", a moldura vermelha) — não o traçado do
paciente, que é onde a patologia realmente vive.

Isso é, na prática, a definição de *shortcut learning*: um extrator de
características (aqui, um hash; numa rede neural, os primeiros filtros
convolucionais) pode aprender a reconhecer o **template do equipamento**
como se fosse o sinal clínico, porque o template é mais fácil de aprender
e está perfeitamente correlacionado com a origem do dado. Uma CNN treinada
sobre este dataset sem cuidado pode aprender a reconhecer "imagem produzida
pelo EDAN SERIES-3 de Multan" em vez de "sinal de infarto" — e como todo
exemplo de todas as 4 categorias vem do mesmo aparelho, o modelo não tem
como aprender a distinguir as duas coisas a partir só destes dados.

Subimos a resolução do hash para 16×16 (256 bits) e o piso de distância
real, entre as imagens mais parecidas de cada categoria, subiu para
14–19 bits (5,5%–7,4%) — ainda assim inspecionamos visualmente os pares
mais próximos e confirmamos, pelo ID de paciente, data/hora e frequência
cardíaca impressos em cada imagem, que eram pacientes diferentes. Ou seja:
mesmo no hash mais discriminativo, a "distância mínima entre pacientes
diferentes" (~5,5%) continua dominada pela semelhança de template, não de
conteúdo — o que reforça, e não resolve, o risco de shortcut learning para
a Fase 4.

### Corpus textual

Dois textos apenas — 1.608 e 858 palavras, ambos de fontes brasileiras
(SciELO e Ministério da Saúde), nenhum sendo relato de paciente.

- **O que isso impede**: treinar ou validar um classificador de sentimento.
  Sentimento pressupõe texto que carregue opinião, queixa ou estado
  emocional de quem fala; um editorial científico revisado por pares e uma
  página institucional informativa são, os dois, escritos em registro
  neutro. Nenhuma técnica de análise de sentimento tem o que aprender aqui.
- **O que isso permite**: um baseline de vocabulário e de registro —
  documenta como o mesmo domínio clínico (risco cardiovascular) é descrito
  em linguagem técnica (Texto 1: "aterosclerose", "síndrome metabólica") e
  em linguagem leiga-institucional (Texto 2: "pressão alta", "14 por 9").
  Esse baseline é o que a Fase 5 usa para calibrar a tradução clínico→leigo
  do chatbot, não para treinar reconhecimento de emoção.

## Assimetria de custo

Um falso negativo numa triagem cardiológica **não é um erro estatístico
neutro** — é um paciente com quadro real mandado para casa enquanto o
evento cardíaco está em curso ou iminente. Um falso positivo custa um exame
adicional; um falso negativo pode custar a vida do paciente. Essa assimetria
não é simétrica em nenhuma das bases desta fase: o viés de subdetecção em
mulheres (UCI) e o risco de shortcut learning por equipamento (Mendeley)
empurram o erro exatamente para o lado mais caro — falso negativo em
subgrupo já sub-investigado. **Acurácia global não pode ser a métrica única
em nenhum modelo treinado sobre estas bases** — ela pondera os dois tipos de
erro como se custassem o mesmo, o que aqui é falso.

## Mitigações propostas (amarradas à fase que as aplica)

| Mitigação | Fase | Por quê |
|---|---|---|
| Deduplicação por conteúdo (MD5 + hash perceptual) obrigatória antes de qualquer split treino/teste | **Fase 4** | Sem isso, a mesma imagem exata (ou quase) pode cair nos dois lados do split — acurácia inflada por vazamento, não por aprendizado real. |
| Split por conteúdo (hash), nunca por nome de arquivo | **Fase 4** | Nomes de arquivo diferentes já provaram apontar para o mesmo conteúdo nesta base (47% de redundância) — split por nome não impede vazamento. |
| Métricas estratificadas por sexo e por faixa etária, não só acurácia global | **Fase 2** | É a única forma de expor a subdetecção em mulheres já medida (25,8% vs. 55,3% de prevalência do alvo) em vez de escondê-la atrás de uma média. |
| Imputação de `ca`/`thal` (se houver) calculada dentro de cada fold de validação, nunca sobre o dataset inteiro antes do split | **Fase 2** | Imputar antes do split é vazamento de informação do conjunto de teste para o de treino — infla a métrica reportada. |
| Validação externa, com dados de outra fonte/população antes de qualquer conclusão | **Fase 6** | Um modelo validado só internamente (mesma base de 1989, mesmo hospital, mesmo país) não tem evidência de que generaliza — validação externa é o teste real de robustez antes de um sistema preditivo de crise. |

## Aviso

Este projeto é **exclusivamente acadêmico**. Nada aqui foi submetido a
validação clínica, comitê de ética em pesquisa com seres humanos (além da
anonimização já feita pelos autores originais das bases públicas) ou
qualquer processo regulatório de dispositivo médico. **Nenhum artefato deste
repositório deve ser usado para decisão médica real.**
