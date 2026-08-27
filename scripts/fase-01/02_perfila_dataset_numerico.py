"""Perfilamento do dataset bruto do UCI Heart Disease.

Le document/datasets/raw/heart-disease-raw.csv e imprime um relatorio.
Nao altera, nao trata, nao imputa e nao grava nada — as decisoes de
tratamento saem de uma conversa humana em cima deste relatorio, nao daqui.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_CSV_PATH = (
    Path(__file__).resolve().parents[2]
    / "document"
    / "datasets"
    / "raw"
    / "heart-disease-raw.csv"
)

MINIMO_LINHAS_EXIGIDO = 100
COLUNA_ALVO = "num"
COLUNAS_BAIXA_CARDINALIDADE = [
    "sex",
    "cp",
    "fbs",
    "restecg",
    "exang",
    "slope",
    "ca",
    "thal",
    COLUNA_ALVO,
]

# Faixas etarias definidas so para leitura deste relatorio — nao sao gravadas
# em lugar nenhum nem viram coluna do dataset.
LIMITES_FAIXAS_ETARIAS = [0, 39, 49, 59, 69, 200]
ROTULOS_FAIXAS_ETARIAS = ["<40", "40-49", "50-59", "60-69", "70+"]


def carregar_dado_cru() -> pd.DataFrame:
    if not RAW_CSV_PATH.exists():
        raise FileNotFoundError(
            f"{RAW_CSV_PATH} nao existe. Rode 01_coleta_dataset_numerico.py primeiro."
        )
    return pd.read_csv(RAW_CSV_PATH)


def imprimir_visao_geral(df: pd.DataFrame) -> None:
    print("=" * 78)
    print("1. VISAO GERAL")
    print("=" * 78)
    n_linhas, n_colunas = df.shape
    print(f"Linhas: {n_linhas}")
    print(f"Colunas: {n_colunas}")
    atende = n_linhas >= MINIMO_LINHAS_EXIGIDO
    status = "ATENDE" if atende else "NAO ATENDE"
    print(
        f"Minimo de {MINIMO_LINHAS_EXIGIDO} linhas exigido pelo enunciado: "
        f"{status} ({n_linhas} linhas)"
    )
    print()


def imprimir_perfil_por_coluna(df: pd.DataFrame) -> None:
    print("=" * 78)
    print("2. PERFIL POR COLUNA (nome original, dtype, nulos, distintos, min/mediana/max)")
    print("=" * 78)
    n_linhas = len(df)
    for coluna in df.columns:
        serie = df[coluna]
        n_nulos = int(serie.isna().sum())
        pct_nulos = 100 * n_nulos / n_linhas
        n_distintos = int(serie.nunique(dropna=True))
        linha = (
            f"- {coluna:<10} dtype={str(serie.dtype):<8} "
            f"nulos={n_nulos:>3} ({pct_nulos:5.1f}%) "
            f"distintos={n_distintos:>3}"
        )
        if pd.api.types.is_numeric_dtype(serie):
            minimo = serie.min()
            mediana = serie.median()
            maximo = serie.max()
            linha += f"  min={minimo} mediana={mediana} max={maximo}"
        print(linha)
    print()


def imprimir_valores_unicos_baixa_cardinalidade(df: pd.DataFrame) -> None:
    print("=" * 78)
    print("3. VALORES UNICOS — COLUNAS CATEGORICAS / BAIXA CARDINALIDADE")
    print("=" * 78)
    for coluna in COLUNAS_BAIXA_CARDINALIDADE:
        if coluna not in df.columns:
            continue
        valores = sorted(df[coluna].dropna().unique().tolist())
        print(f"- {coluna}: {valores}")
    print()


def imprimir_distribuicao_alvo(df: pd.DataFrame) -> None:
    print("=" * 78)
    print("4. DISTRIBUICAO DO ALVO (num)")
    print("=" * 78)
    print("-- 5 niveis (0 a 4) --")
    contagem = df[COLUNA_ALVO].value_counts().sort_index()
    percentual = df[COLUNA_ALVO].value_counts(normalize=True).sort_index() * 100
    for nivel in contagem.index:
        print(f"  num={nivel}: {contagem[nivel]:>4}  ({percentual[nivel]:5.1f}%)")

    print("-- binario (0 = ausencia, 1-4 -> 1 = presenca) --")
    alvo_binario = (df[COLUNA_ALVO] > 0).astype(int)
    contagem_bin = alvo_binario.value_counts().sort_index()
    percentual_bin = alvo_binario.value_counts(normalize=True).sort_index() * 100
    for nivel in contagem_bin.index:
        print(
            f"  alvo_binario={nivel}: {contagem_bin[nivel]:>4}  ({percentual_bin[nivel]:5.1f}%)"
        )
    print()


def imprimir_distribuicao_sexo_idade(df: pd.DataFrame) -> None:
    print("=" * 78)
    print("5. DISTRIBUICAO POR SEXO E POR FAIXA ETARIA")
    print("=" * 78)
    print("-- sexo (valor cru: documentacao UCI diz 1=masculino, 0=feminino) --")
    contagem_sexo = df["sex"].value_counts().sort_index()
    percentual_sexo = df["sex"].value_counts(normalize=True).sort_index() * 100
    for valor in contagem_sexo.index:
        print(f"  sex={valor}: {contagem_sexo[valor]:>4}  ({percentual_sexo[valor]:5.1f}%)")

    print("-- faixa etaria (bins so deste relatorio, definidos abaixo no codigo) --")
    faixa = pd.cut(df["age"], bins=LIMITES_FAIXAS_ETARIAS, labels=ROTULOS_FAIXAS_ETARIAS)
    contagem_faixa = faixa.value_counts().sort_index()
    percentual_faixa = faixa.value_counts(normalize=True).sort_index() * 100
    for rotulo in contagem_faixa.index:
        print(
            f"  {rotulo:<6}: {contagem_faixa[rotulo]:>4}  ({percentual_faixa[rotulo]:5.1f}%)"
        )
    print()


def imprimir_cruzamento_alvo_sexo(df: pd.DataFrame) -> None:
    print("=" * 78)
    print("6. CRUZAMENTO: ALVO BINARIO x SEXO")
    print("=" * 78)
    alvo_binario = (df[COLUNA_ALVO] > 0).astype(int)
    tabela_contagem = pd.crosstab(
        df["sex"], alvo_binario, margins=True, margins_name="total"
    )
    tabela_percentual_linha = pd.crosstab(df["sex"], alvo_binario, normalize="index") * 100
    print("Contagem (linhas=sex, colunas=alvo_binario, 0=ausencia 1=presenca):")
    print(tabela_contagem.to_string())
    print()
    print("Percentual dentro de cada sexo (linhas=sex, colunas=alvo_binario):")
    print(tabela_percentual_linha.round(1).to_string())
    print()


def main() -> None:
    df = carregar_dado_cru()
    imprimir_visao_geral(df)
    imprimir_perfil_por_coluna(df)
    imprimir_valores_unicos_baixa_cardinalidade(df)
    imprimir_distribuicao_alvo(df)
    imprimir_distribuicao_sexo_idade(df)
    imprimir_cruzamento_alvo_sexo(df)


if __name__ == "__main__":
    main()
