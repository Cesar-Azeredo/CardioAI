# Imagens — Parte 3 (Dados Visuais)

Este repositório versiona apenas uma **amostra leve** (~12 imagens) em
`assets/imagens/amostras/`, só para ilustrar o `README.md` e o documento resumo.

O conjunto selecionado (120 imagens, resolução original 2213×1572, ~76 MB — 30
por categoria: infarto, histórico de infarto, batimento anormal, normal) **não
fica no Git** — conforme a regra inviolável 2 do `CLAUDE.md`/`AGENTS.md` (nada acima
de ~5 MB e nenhum lote de imagens no repositório). Foi gerado por
`scripts/fase-01/05_organiza_imagens.py` em
`/Users/cesar/Downloads/cardioia-fase1-imagens-selecionadas` (fora do repositório,
pronto para upload) e precisa ser hospedado em serviço externo (Drive/OneDrive);
o link de acesso vai ser registrado no `README.md` da raiz e em
`document/datasets/README.md`.

> ⚠️ TODO(humano): fazer upload da pasta `cardioia-fase1-imagens-selecionadas`
> (120 imagens) para Drive/OneDrive, colar aqui o link público, e replicar o
> mesmo link no `README.md` e em `document/datasets/README.md`.

O rótulo (categoria), a origem, dimensões, hash MD5 e os nomes de arquivo
originais (incluindo os *aliases* — arquivos duplicados por conteúdo no
dataset-fonte) de cada imagem selecionada estão em
`document/datasets/processed/manifest-imagens.csv`.
