"""Coleta bruta do dataset UCI Heart Disease (id=45, base Cleveland).

Fonte travada na secao 5.3 do CLAUDE.md/AGENTS.md: archive.ics.uci.edu/dataset/45,
DOI 10.24432/C52P4X, licenca CC BY 4.0. Este script so coleta e grava o dado
exatamente como a fonte devolve — nenhum tratamento, renomeio ou imputacao
acontece aqui. Decisoes de tratamento sao tomadas depois, com base no
perfilamento (02_perfila_dataset_numerico.py).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[2] / "document" / "datasets" / "raw"
FALLBACK_CSV_URL = "https://archive.ics.uci.edu/static/public/45/data.csv"
UCI_DATASET_ID = 45

RAW_CSV_PATH = RAW_DIR / "heart-disease-raw.csv"
METADATA_JSON_PATH = RAW_DIR / "heart-disease-metadata.json"
VARIABLES_CSV_PATH = RAW_DIR / "heart-disease-variables.csv"


def _coletar_via_ucimlrepo() -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    from ucimlrepo import fetch_ucirepo

    dataset = fetch_ucirepo(id=UCI_DATASET_ID)
    dados_crus = pd.concat([dataset.data.features, dataset.data.targets], axis=1)
    return dados_crus, dataset.metadata, dataset.variables


def _coletar_via_csv_direto() -> pd.DataFrame:
    return pd.read_csv(FALLBACK_CSV_URL)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    metadata: dict | None = None
    variables: pd.DataFrame | None = None

    try:
        dados_crus, metadata, variables = _coletar_via_ucimlrepo()
        origem = "ucimlrepo (fetch_ucirepo)"
    except Exception as erro_ucimlrepo:
        print(f"[AVISO] ucimlrepo falhou: {erro_ucimlrepo!r}", file=sys.stderr)
        print("[INFO] tentando fallback via CSV direto...", file=sys.stderr)
        try:
            dados_crus = _coletar_via_csv_direto()
            origem = "CSV direto (fallback)"
        except Exception as erro_fallback:
            print(
                "[ERRO] Nao foi possivel coletar o dataset por nenhum dos dois "
                f"metodos.\n  ucimlrepo: {erro_ucimlrepo!r}\n  CSV direto: {erro_fallback!r}\n"
                "Verifique a conexao de rede e tente novamente. Este script nao "
                "gera dado sintetico como fallback — dado inventado nao entra "
                "neste projeto (regra inviolavel 1 do CLAUDE.md/AGENTS.md).",
                file=sys.stderr,
            )
            sys.exit(1)

    dados_crus.to_csv(RAW_CSV_PATH, index=False)
    print(f"[OK] Dado cru salvo em {RAW_CSV_PATH} (origem: {origem})")
    print(f"     {dados_crus.shape[0]} linhas x {dados_crus.shape[1]} colunas")
    print(f"     colunas: {list(dados_crus.columns)}")

    if metadata is not None:
        with open(METADATA_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2, default=str)
        print(f"[OK] Metadados oficiais salvos em {METADATA_JSON_PATH}")
    else:
        print(
            "[AVISO] Metadados oficiais do ucimlrepo nao disponiveis "
            "(coleta caiu no fallback de CSV direto).",
            file=sys.stderr,
        )

    if variables is not None:
        variables.to_csv(VARIABLES_CSV_PATH, index=False)
        print(f"[OK] Tabela de variaveis salva em {VARIABLES_CSV_PATH}")
    else:
        print(
            "[AVISO] Tabela de variaveis do ucimlrepo nao disponivel "
            "(coleta caiu no fallback de CSV direto).",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
