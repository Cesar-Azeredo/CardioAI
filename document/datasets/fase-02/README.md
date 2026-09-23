# Dados da Fase 2 — dado primário autoral sintético

Esta pasta guarda os `.csv` da Fase 2 (mapa de conhecimento sintoma → doença
e frases rotuladas em alto/baixo risco). Ela é separada de `raw/` e
`processed/` de propósito:

- `raw/` é dado **como baixado** de uma fonte externa;
- `processed/` é dado **derivado por pipeline** a partir de `raw/`;
- aqui fica dado **primário, escrito pelo grupo** — sintético, sem paciente
  real por trás. Não foi baixado de lugar nenhum nem derivado de outro
  arquivo.

Misturar os três confundiria quem chegar nas fases seguintes: um `.csv` em
`processed/` promete que existe um script que o regenera a partir de `raw/`;
os daqui não têm essa origem.

## Exceção à regra 4 (nada de dado editado à mão)

A regra 4 do `CLAUDE.md`/`AGENTS.md` proíbe **transformar** dado à mão. Os
arquivos daqui não são transformação — são a **origem**: frase, rótulo e
entrada do mapa são decisões de autoria do grupo. A exceção vale só para o
dado primário; **tudo que for derivado dele sai de script**. Registro
completo da exceção e do motivo em `document/fase-02/`.

## Ficha obrigatória de cada arquivo

Todo arquivo que entrar aqui recebe, nesta seção, uma ficha com:

- autores (integrantes do grupo que escreveram) e data de criação;
- critério de redação (como as frases foram escritas, o que foi evitado);
- critério de rotulagem (regra de alto/baixo risco e a fonte que a ancora);
- para o mapa: fonte e trecho literal de cada linha, apontando para os textos
  em `assets/textos/` e `assets/textos/fase-02/` (fichas em
  `PROVENIENCIA.md` de cada pasta);
- nº de linhas contado por script.

Verificação por máquina de tudo que abaixo é checável:
`python scripts/fase-02/01_verifica_mapa_e_frases.py` (sai com código 1 se
alguma regra falhar).

### Ficha — `mapa-conhecimento-sintomas.csv`

- **Autoria**: Grupo Zion (integrantes listados no `README.md` da raiz).
  Redação inicial preparada com apoio de assistente de IA (Claude Code) e
  submetida à revisão do grupo antes do commit.
- **Data de criação**: 2026-09-23.
- **Nº de linhas** (contado pelo script de verificação): **53**, cobrindo
  **26 conceitos de sintoma** — Hipertensão 15 linhas / 7 conceitos, Infarto
  19 / 10, AVC 19 / 9. Sintoma 2 é literal em 2 linhas e variante leiga em 51.
- **Congelado desde 2026-09-23** (SHA-256 conferido pelo verificador): o mapa
  não recebe variantes para acertar frases de teste. Regra em
  `document/fase-02/gabarito-frases.md`.
- **Estrutura**: as três primeiras colunas são exatamente `Sintoma 1`,
  `Sintoma 2`, `Doença Associada` (estrutura mostrada no enunciado); depois
  vêm as colunas de proveniência `tipo_termo`, `fonte`, `trecho_literal`,
  `observacao`.
- **O que uma linha significa**: **um conceito de sintoma com um
  sinônimo** — Sintoma 1 e Sintoma 2 são duas formas de dizer o mesmo
  sintoma, como nos exemplos do enunciado ("dor no peito", "aperto no tórax"
  → Infarto). Um conceito pode ter várias linhas, uma por sinônimo
  ("sangramento nasal | sangue pelo nariz", "sangramento nasal | nariz
  sangrando"); cada linha faz sentido sozinha.
- **Fontes**: só as três páginas do Ministério da Saúde da decisão 1
  (Texto 2 — hipertensão; Textos 3 e 4 — infarto e AVC). Fichas em
  `assets/textos/PROVENIENCIA.md` e `assets/textos/fase-02/PROVENIENCIA.md`.
- **Critério de inclusão de linhas**:
  1. **Sintoma 1 é sempre termo literal da página.** `trecho_literal` traz o
     trecho exato que o ancora (vários trechos separados por ` | `); o script
     confere que cada trecho existe **exatamente** no `.txt` e que Sintoma 1
     aparece dentro dele como palavra inteira. Linha que não passa não entra.
  2. **`tipo_termo` descreve a coluna Sintoma 2**:
     - `literal` — outro termo da mesma página para o mesmo sintoma (ex.:
       "dor no peito | desconforto na região peitoral" → Infarto); o script
       confere que ele também está no trecho. Sempre que a página traz dois
       termos equivalentes, a linha com os dois literais existe;
     - `variante_leiga` — redação do grupo, no jeito que o paciente fala
       ("sangue pelo nariz", "aperto no peito", "tontura"). O script confere
       que a variante **não** existe na página (se existisse, seria literal).
  3. **Correção documentada de erro de digitação da fonte**: a página de AVC
     traz "Alteração da **falar** ou compreensão". Sintoma 1 usa o termo
     corrigido "alteração da fala ou compreensão" — o termo com erro não
     serve para casar com fala de paciente —, `trecho_literal` preserva o
     texto com o erro exatamente como está na página, e `observacao` declara
     `Sintoma 1 = correção de "..."`. O script aceita a correção só se a forma
     da página estiver no trecho, o termo corrigido **não** existir na página
     e a diferença for de no máximo 2 caracteres.
  4. **Variante só entra se preserva o sentido do termo da fonte.** Exemplo
     recusado: `mal-estar` sozinho como variante de `mal-estar súbito` — o
     "súbito" é o que faz o termo ser alerta de infarto na fonte.
  5. **Página que se repete conta uma vez**: a página de infarto repete dois
     itens da lista de sintomas (2× e 3×); eles não geram linhas extras.
  6. **Sem par repetido** para a mesma doença (conferido por script).
  7. **Conceito compartilhado não é escondido**: tontura, fraqueza e dor de
     cabeça (Hipertensão e AVC) e dor no peito (Hipertensão e Infarto) têm
     linhas em cada doença, inclusive com as mesmas variantes leigas
     ("tonto", "cabeça rodando", "peito doendo"), e `observacao` registra o
     compartilhamento. É a ambiguidade que o extrator vai ter que resolver.
  8. **Local de irradiação como termo literal**: `braço esquerdo` entra como
     Sintoma 1 porque é contínuo e literal na página de infarto — como LOCAL
     para onde a dor no peito pode irradiar, não como sintoma isolado
     (explicado em `observacao`). Justificativa: fonte e relevância clínica,
     não frase de teste. `dor na barriga` fica fora: a página diz "a dor
     também pode ser no abdome", e "abdome" não forma termo contínuo de
     sintoma.
  9. **Flexão de gênero** ("pálido/pálida", "tonto/tonta", "confuso/confusa")
     não vira linha: fica para a normalização do extrator, registrada em
     `observacao`.
- **Lacuna documentada — insuficiência cardíaca e angina**: fora do mapa por
  decisão de governança. Não há página equivalente do Ministério da Saúde
  para essas duas condições, só fontes de hospital privado, sem o mesmo peso
  institucional; preferimos três doenças com proveniência oficial a cinco com
  metade sem fonte verificável. O enunciado as cita só como exemplo de
  formato. Detalhe em `document/fase-02/governanca-e-vies.md`.
- **Licença das fontes**: CC BY-ND 3.0. O mapa **analisa** as páginas
  (extrai o termo e cita o trecho que o ancora); não reescreve nem resume.

### Ficha — `assets/textos/fase-02/frases-sintomas-pacientes.txt`

(O `.txt` fica em `assets/textos/fase-02/`, junto dos demais textos para NLP;
a ficha fica aqui, com a dos demais dados autorais da Fase 2.)

- **Autoria**: Grupo Zion. Redação inicial preparada com apoio de assistente
  de IA (Claude Code) e submetida à revisão do grupo antes do commit.
- **Data de criação**: 2026-09-23.
- **Nº de frases** (contado pelo script de verificação): **10**, uma por linha.
- **Natureza**: dado **sintético**. Nenhuma frase é relato de paciente real.
- **Critério de redação**:
  1. cada frase diz **o que o paciente sente**, **quando começou** e **como
     afeta a rotina** (exigência do enunciado);
  2. linguagem de paciente, em primeira pessoa, com as imprecisões de quem
     fala ("faz uns dez minutos", "sem fôlego");
  3. **redação própria, sem paráfrase das páginas gov.br** (cláusula ND):
     o script mede a maior sequência de palavras em comum entre cada frase e
     cada página — máximo encontrado: 4 palavras (limite de reprovação: 6);
     o que coincide é vocabulário de sintoma ("dor no peito", "falta de ar"),
     não frase da página;
  4. **nenhum identificador** (LGPD): sem nome, sem idade exata, sem número
     de documento, sem lugar identificável. O script reprova idade no formato
     "NN anos" e qualquer sequência de 3+ dígitos. Condição de saúde como
     perfil ("sou diabética") é permitida — é o que define o caso atípico;
  5. cada frase é um **caso de teste** do extrator, com comportamento sondado
     e diagnóstico esperado em `document/fase-02/gabarito-frases.md`.
- **Congeladas desde 2026-09-23**: as frases não mudam para acomodar o
  extrator; falha em linguagem natural é resultado a reportar. O verificador
  reprova se o SHA-256 do arquivo mudar. Regra e histórico em
  `document/fase-02/gabarito-frases.md`.
- **Distribuição**: 2 casos claros de infarto, 2 de AVC, 2 de hipertensão,
  1 de sintoma compartilhado, 1 só com variante leiga, 1 com negação
  explícita, 1 de infarto atípico (sem dor no peito).

## Git

O `.gitignore` do template ignora `*.csv`; a negação
`!document/datasets/fase-02/*.csv` libera **só** os `.csv` desta pasta.
Planilha (`.xlsx`) aqui continua ignorada.
