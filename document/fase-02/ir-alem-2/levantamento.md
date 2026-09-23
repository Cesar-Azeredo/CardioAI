# Levantamento dos dados — Ir Além 2 (Etapas 1 e 2A)

> Verificações feitas **antes** do protocolo (`protocolo-mlp.md`) e antes de
> qualquer treino. Todo número abaixo sai de script em
> `scripts/fase-02/ir-alem-2/`, rodando sobre o download de 2026-09-23.
> Simulação acadêmica, sem validade clínica.

## 1. Download e deduplicação

- **Fonte:** Mendeley Data, *ECG Images dataset of Cardiac Patients*, v2,
  DOI `10.17632/gwbz3fsgp8.2`, CC BY 4.0 — a mesma base da Fase 1.
  Baixada de novo pela API pública
  (`https://data.mendeley.com/public-api/zip/gwbz3fsgp8/download/2`) pelo
  script 01, **fora do repositório**. Zip de 193,9 MB, com 928 `.jpg`, as
  mesmas contagens por pasta da Fase 1.
- **Deduplicação por MD5** (script 02, mesmo método de
  `scripts/fase-01/05_organiza_imagens.py`): **491 imagens únicas** — MI 30,
  PMI 86, HB 233, Normal 142, idêntico à Fase 1. **Nenhuma colisão de MD5
  entre categorias** (checagem nova: no problema binário, a mesma imagem com
  dois rótulos seria ruído e vazamento ao mesmo tempo). Os 120 MD5 do manifest
  da Fase 1 estão todos no download.
- **Por que a deduplicação é requisito aqui:** 47% dos arquivos são cópia
  byte a byte de outro (87% em MI). Um split sobre arquivos põe cópias da
  mesma imagem no treino e no teste, e o teste passa a medir memorização. O
  split do Ir Além 2 é feito sobre as 491 únicas.
- **Binário:** normal = 142 (28,9%); anormal = MI + PMI + HB = 349 (71,1%).
  Chute da classe majoritária = **71,1% de acurácia**, o piso de leitura.

## 2. Texto impresso nas imagens

Medido nas **491** imagens (script 03), não numa amostra.

| Região | Coordenadas (px) | Estabilidade |
|---|---|---|
| Imagem inteira | 2213 × 1572, RGB | 491/491 |
| Moldura vermelha da grade | y 283–1517, x 68–2176 | 439 com borda direita em 2176, 52 em 2175 (seção 3) |
| Cabeçalho: ID do exame, **sexo**, campos vazios | y 31–275 | 483/491; nas outras 8, um pico do traçado encosta na moldura (até y 280) |
| Rodapé: filtro, velocidade, **♥ FC**, **"Lead Off"**, data/hora | y 1538–1552 | 489/491; nas outras 2, um pico do traçado passa da moldura |

- **"Lead Off"** (eletrodo solto) aparece no rodapé de 35 imagens e desloca o
  ♥ de x = 550 para x = 659.
- **Dois formatos de data** (`2020-10-15` e `27-11-2019`): lotes ou
  configurações diferentes do aparelho, **misturados entre as classes**.
- **FC impressa** lida por casamento de glifos (fonte fixa, sem OCR externo;
  15 protótipos → 10 dígitos; pior casamento: 1 bit em 165):

| Categoria | n | mediana (bpm) | mín–máx | > 90 bpm |
|---|---|---|---|---|
| MI | 30 | 74,5 | 50–126 | 7 (23%) |
| PMI | 86 | 76,5 | 44–121 | 19 (22%) |
| HB | 233 | 105,0 | 60–213 | 197 (85%) |
| Normal | 142 | 71,5 | 48–90 | **0 (0%)** |

**Nenhuma imagem normal passa de 90 bpm.** A regra "FC impressa > 90 →
anormal" identifica **223 das 349 anormais (64%) com precisão de 100%**; nas
491, dá 74,3% de acurácia e 0,82 de acurácia balanceada. O atalho é real e
medido: uma rede que aprenda a ler o rodapé ganha isso sem olhar o traçado.
A FC também está no traçado (intervalo RR), e lá é sinal clínico legítimo,
não atalho.

**Recorte:** interior da moldura recuado 4 px, `(72, 287, 2173, 1514)` →
2101 × 1227 px. Todo texto variável fica fora. Custo: 9 imagens têm a ponta
de um pico passando da moldura e 11 têm traçado na faixa de 4 px do recuo;
esses poucos pixels são cortados.

**Template do aparelho:** dentro do recorte, os pixels escuros em ≥ 95% das
491 imagens (rótulos das derivações, pulso de calibração, barras
separadoras) somam **31% da tinta média de cada imagem**. O layout é o mesmo
em todas as imagens porque o aparelho é o mesmo. É o risco de *shortcut
learning* documentado na Fase 1 (`document/fase-01/governanca-e-vies.md`):
o recorte tira o texto, não o template, e este dataset não tem como separar
"assinatura do aparelho" de "patologia".

## 3. Etapa 2A — verificações antes do protocolo

### 3.1 Borda direita em x = 2175

| Categoria | borda em 2175 | % |
|---|---|---|
| MI | 2 de 30 | 7% |
| PMI | 5 de 86 | 6% |
| HB | 24 de 233 | 10% |
| Normal | 21 de 142 | 15% |

Aparece nas quatro categorias, em **números de arquivo consecutivos** (HB
18–21 e 45–64, Normal 162–167 e 183–196, PMI 102–106): assinatura de **lote
de digitalização**, não de classe. É um pouco mais frequente nas normais
(15% contra 9% das anormais) — fraco, mas é o tipo de variação que uma rede
pode explorar. **Só a borda se desloca:** as barras separadoras e o pulso de
calibração ficam nos mesmos pixels nos dois grupos. Por isso o recorte foi
**recuado 4 px em todos os lados**: a borda sai da entrada da rede e a
variação some.

### 3.2 Validação da leitura por glifo

O leitor de glifos não tem gabarito; os "100% de precisão" da regra dependem
dele. Script 04:

- **Amostra aleatória:** 20 imagens, semente 42. Conferência visual de cada
  campo contra a própria imagem: **FC 20/20, sexo 20/20.**
- **Amostra dirigida**, porque o sorteio pegou só 1 "Female" e nenhum
  "Lead Off", e a precisão da regra depende das normais perto do limiar:
  **todas as 13 normais com FC lida ≥ 85** (fora da amostra aleatória), mais
  5 "Female" e 5 "Lead Off". **FC 23/23, sexo 23/23.**
- **Total: 43 imagens, 86 campos, 0 erro.** Nenhuma normal com FC real acima
  de 90 foi lida como ≤ 90 entre as conferidas.

### 3.3 Metadados e LGPD

O manifest do Ir Além 2
(`document/datasets/processed/manifest-ir-alem-2.csv`, 491 linhas, gerado
pelo script 03) guarda por imagem: MD5, categoria, rótulo binário, arquivo
representante e aliases, **FC impressa, sexo impresso**, "Lead Off" e borda
da moldura. **Não guarda o ID do exame nem a data/hora.** Esses campos estão
impressos na imagem pública, mas transformá-los em dado estruturado de
identificação cria exatamente o cruzamento (ID + horário do exame) que a
Fase 1 apontou como caminho de reidentificação
(`document/fase-01/governanca-e-vies.md`, seção LGPD) — mesmo sendo base
pública. FC e sexo entram só como **metadados de avaliação**: o recorte os
remove da imagem, e nenhum dos dois é entrada do modelo.

### 3.4 Sexo impresso

| Categoria | F | M | % F |
|---|---|---|---|
| MI | 2 | 28 | 7% |
| PMI | 4 | 82 | 5% |
| HB | 23 | 210 | 10% |
| Normal | 15 | 127 | 11% |
| **Total** | **44** | **447** | **9%** |

**A base de imagens é 91% masculina** (447 de 491) — ainda mais
desequilibrada que a Cleveland da Fase 1 (68% masculina, 206 de 303). O
sexo não separa as classes (5–11% de mulheres em todas as categorias), mas
limita qualquer leitura por sexo: há **29 anormais femininas** no total.
Qualquer resultado do Ir Além 2 é, na prática, um resultado sobre ECG de
homens paquistaneses num único aparelho.

## 4. Teste de fumaça do notebook

Antes da execução única, o código do notebook foi convertido para script e
rodado com o treino reduzido a **1 época** e **toda a saída descartada**, só
para achar erro de código (terminou sem erro). Nenhuma métrica dessa rodada
foi lida.

## 5. Scripts

| Script | Faz |
|---|---|
| `01_baixa_ecg_mendeley.py` | baixa e extrai o zip fora do repositório; confere 928 arquivos (só biblioteca padrão, roda no Colab) |
| `02_deduplica_e_monta_binario.py` | MD5, 491 únicas, colisões entre categorias, binário, `indice-unicos.csv` (fora do repo) |
| `03_audita_texto_impresso.py` | layout, FC, sexo, "Lead Off", template, borda; grava o manifest e os exemplos antes/depois |
| `04_amostra_validacao_glifos.py` | painéis aleatório e dirigido para a conferência visual da leitura por glifo |
