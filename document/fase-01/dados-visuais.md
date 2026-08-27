# Dados visuais — Parte 3 (Visão Computacional)

## a) Origem dos dados

Dado **real, público, de imagens de ECG anonimizadas** — não simulado. Fonte:
**Mendeley Data**, *ECG Images dataset of Cardiac Patients*, versão 2.

- **URL**: https://data.mendeley.com/datasets/gwbz3fsgp8/2
- **DOI**: `10.17632/gwbz3fsgp8.2`
- **Licença do dataset**: **CC BY 4.0**, confirmada na própria página (bloco de
  metadados e JSON-LD `schema.org`). Isto **não** é a mesma licença do artigo
  descritor abaixo — são dois documentos distintos com licenças distintas.
- **Contribuidores do dataset** (conforme a página): Ali Haider Khan e
  Muzammil Hussain, University of Management and Technology, Lahore.
- **Artigo descritor** (contexto científico, licença própria — CC BY-NC-ND):
  Khan, A. H., Hussain, M., & Malik, M. K. (2021). *ECG images dataset of
  Cardiac and COVID-19 patients*. Data in Brief, 34, 106762. DOI
  `10.1016/j.dib.2021.106762`. Nota: o artigo descreve a v1 do dataset, que
  incluía uma categoria COVID-19; **a v2 usada aqui não tem essa categoria**.
- **Coleta**: equipamento EDAN SERIES-3, no Ch. Pervaiz Elahi Institute of
  Cardiology, Multan, Paquistão.
- **Data de acesso**: 2026-08-27.

## b) Justificativa para Visão Computacional

O ECG impresso é, por natureza, um sinal fisiológico convertido em imagem —
um traçado 1D (voltagem × tempo) sobre um grid milimetrado. Isso o torna um
caso quase didático para as três frentes que o enunciado pede:

- **Identificação de bordas**: o traçado é uma curva de alto contraste sobre
  fundo quadriculado; algoritmos de detecção de borda (Sobel, Canny) ou a
  primeira camada de uma CNN aprendem literalmente a separar a linha do
  sinal da grade de fundo antes de qualquer análise clínica — é o pré-
  processamento mais básico e mais necessário aqui.
- **Detecção de padrões**: cada uma das 12 derivações tem morfologia
  característica (complexo QRS, onda T, segmento ST); um infarto ou uma
  arritmia alteram esse padrão de forma reconhecível — é exatamente o tipo
  de regularidade geométrica repetida que uma CNN explora bem.
- **Reconhecimento de anomalias**: a tarefa fim (classificar infarto vs.
  histórico de infarto vs. batimento anormal vs. normal) é, em si, detecção
  de anomalia sobre um padrão de referência (o traçado normal).

**Importância para IA em saúde**: um sistema que triasse ECGs automaticamente
poderia sinalizar exames suspeitos para revisão prioritária de um cardiologista
— relevante num sistema de saúde com poucos especialistas por habitante, como
é o caso do SUS em muitas regiões do Brasil.

## c) Preparação da amostra (script `scripts/fase-01/05_organiza_imagens.py`)

O dataset completo (929 pacientes anunciados nos nomes das 4 pastas) foi
baixado fora do repositório. A preparação teve duas checagens de qualidade
**antes** de qualquer sorteio:

**Deduplicação por MD5** — dos **928 arquivos reais** encontrados (929
esperados; falta `MI(215).jpg`, um arquivo ausente na fonte), **apenas 491
são imagens de conteúdo único** (hash MD5 distinto):

| Categoria | Arquivos | Únicos por MD5 | Redundância |
|---|---|---|---|
| Infarto (MI) | 239 | 30 | 87% |
| Histórico de infarto (PMI) | 172 | 86 | 50% |
| Batimento anormal (HB) | 233 | 233 | 0% |
| Normal | 284 | 142 | 50% |

Nomes de arquivo diferentes dentro da mesma categoria frequentemente apontam
para o **mesmo byte a byte** — sem deduplicar, um treino na Fase 4 correria
risco real de ter a mesma imagem exata em treino e teste.

**Checagem de quase-duplicata (hash perceptual dHash, 256 bits)** — rodada
sobre as 491 imagens já únicas por MD5, para pegar o que MD5 não pega (mesma
imagem reexportada com compressão ou reamostragem diferentes). O limiar de
remoção automática (≤2% dos bits) não encontrou nenhum caso. Os pares mais
próximos encontrados foram inspecionados visualmente: cada imagem imprime
internamente um "ID" de paciente, data/hora e frequência cardíaca — em todos
os pares inspecionados esses três valores eram diferentes, confirmando que
são pacientes distintos que só compartilham o template visual do aparelho
EDAN (mesma grade, mesmo cabeçalho). Nenhuma imagem foi removida por
quase-duplicata.

**Amostragem final: 120 imagens, balanceadas 30/30/30/30 por categoria.** A
categoria "infarto" tem só 30 imagens únicas por conteúdo — esse é o teto que
define a cota igual das outras três (todas têm ≥30 disponíveis). Onde a cota
coube inteira no universo (infarto: 30 de 30), todas entraram; nas demais, o
sorteio usou semente fixa (42) para reprodutibilidade.

**Nada foi recomprimido ou redimensionado na seleção entregável** — os 120
arquivos são cópia byte a byte do original (2213×1572, ~650 KB médios,
~76 MB no total), porque a nitidez do grid milimetrado é exatamente o que a
Fase 4 vai precisar para detecção de bordas; recomprimir destruiria esse
sinal. Só as 12 amostras em `assets/imagens/amostras/` (3 por categoria, só
para ilustrar o README) foram reduzidas a 900 px de largura.

O manifest completo (`document/datasets/processed/manifest-imagens.csv`)
registra, por imagem selecionada: nome novo, nome original, categoria,
dimensões, formato, tamanho, hash MD5 e a lista de **todos os nomes-alias**
que apontam para o mesmo conteúdo no dataset-fonte — a duplicação não fica
escondida.

## d) Limitações

Apontamento apenas — a análise completa de governança e viés (cobrindo as
três bases da Fase 1) vai para `document/fase-01/governanca-e-vies.md`
(ainda não escrita):

- Coleta num **único país** (Paquistão) com **um único modelo de
  equipamento** (EDAN SERIES-3) — risco de *shortcut learning* (o modelo
  aprender a assinatura do aparelho, não a patologia).
- **47% de redundância por conteúdo no dataset original** (928 arquivos → 491
  únicos), com distribuição muito desigual entre categorias (infarto: 87% de
  redundância; batimento anormal: 0%) — isso por si só é um viés de
  representatividade que precisa ser registrado.
- `MI(215).jpg` ausente do dataset-fonte — 239 arquivos onde o nome da pasta
  anuncia 240 pacientes.

## e) Como reproduzir

```bash
python scripts/fase-01/05_organiza_imagens.py
```

Lê o dataset extraído em `/Users/cesar/Downloads/gwbz3fsgp8-2` (fora do
repositório), deduplica por MD5 e por dHash, sorteia 30 imagens únicas por
categoria (semente 42), copia a seleção (sem recomprimir) para
`/Users/cesar/Downloads/cardioia-fase1-imagens-selecionadas`, gera as 12
amostras reduzidas em `assets/imagens/amostras/` e grava
`document/datasets/processed/manifest-imagens.csv`.
