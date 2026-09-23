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

Nenhum arquivo ainda. Os `.csv` entram na etapa seguinte à fundação.

## Git

O `.gitignore` do template ignora `*.csv`; a negação
`!document/datasets/fase-02/*.csv` libera **só** os `.csv` desta pasta.
Planilha (`.xlsx`) aqui continua ignorada.
