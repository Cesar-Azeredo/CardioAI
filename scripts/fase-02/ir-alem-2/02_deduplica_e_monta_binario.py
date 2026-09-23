"""Deduplica por MD5 e monta o problema binario — Ir Alem 2 (MLP em Keras).

Reaplica a deduplicacao da Fase 1 (scripts/fase-01/05_organiza_imagens.py,
funcao deduplicar_por_md5: agrupa por MD5, representante = alias de menor
nome) sobre o download do script 01, e confere que chega as mesmas 491
imagens unicas (MI 30, PMI 86, HB 233, Normal 142).

Por que a deduplicacao e REQUISITO aqui, nao cuidado opcional: 47% dos
arquivos sao copia byte a byte de outro (87% na categoria infarto). Sem
deduplicar, o split treino/teste sorteia ARQUIVOS, e copias da mesma imagem
caem dos dois lados — o teste passa a medir memorizacao, nao generalizacao.
O split do Ir Alem 2 e feito sobre as 491 imagens unicas.

Acrescimo em relacao a Fase 1: la a deduplicacao era por categoria, porque a
amostra era por categoria. Aqui as quatro categorias viram duas classes, entao
o script confere tambem colisao de MD5 ENTRE categorias — a mesma imagem com
dois rotulos seria ruido de rotulo e vazamento ao mesmo tempo.

Binario: normal = Normal; anormal = MI + PMI + HB.

Saida (FORA do repositorio, ao lado do download): indice-unicos.csv, uma
linha por imagem unica, com md5, categoria original, rotulo binario,
representante e aliases. E a entrada do split.

Uso:
    python scripts/fase-02/ir-alem-2/02_deduplica_e_monta_binario.py [--destino DIR]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

DESTINO_PADRAO = Path.home() / ".cache" / "cardioia" / "mendeley-gwbz3fsgp8-v2"
REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_FASE1 = REPO_ROOT / "document" / "datasets" / "processed" / "manifest-imagens.csv"

CATEGORIAS = [
    # prefixo, pasta, rotulo binario, unicos esperados (Fase 1)
    ("MI", "ECG Images of Myocardial Infarction Patients (240x12=2880)", "anormal", 30),
    ("PMI", "ECG Images of Patient that have History of MI (172x12=2064)", "anormal", 86),
    ("HB", "ECG Images of Patient that have abnormal heartbeat (233x12=2796)", "anormal", 233),
    ("Normal", "Normal Person ECG Images (284x12=3408)", "normal", 142),
]


def md5_de(caminho: Path) -> str:
    return hashlib.md5(caminho.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--destino", type=Path, default=DESTINO_PADRAO)
    args = ap.parse_args()
    raiz = args.destino.expanduser().resolve() / "extraido"

    linhas = []
    md5_para_categorias: dict[str, set[str]] = {}
    ok = True
    print(f"{'categoria':8s} {'arquivos':>8s} {'unicos':>7s} {'esperado':>8s}  binario")
    for prefixo, pasta, binario, esperado in CATEGORIAS:
        grupos: dict[str, list[str]] = {}
        arquivos = sorted((raiz / pasta).glob("*.jpg"), key=lambda p: p.name)
        for fp in arquivos:
            grupos.setdefault(md5_de(fp), []).append(fp.name)
        for h, aliases in grupos.items():
            aliases.sort()
            md5_para_categorias.setdefault(h, set()).add(prefixo)
            linhas.append({
                "md5": h,
                "categoria_original": prefixo,
                "rotulo_binario": binario,
                "representante": f"{pasta}/{aliases[0]}",
                "n_aliases": len(aliases),
                "aliases": ";".join(aliases),
            })
        marca = "ok" if len(grupos) == esperado else "DIVERGE"
        ok &= len(grupos) == esperado
        print(f"{prefixo:8s} {len(arquivos):8d} {len(grupos):7d} {esperado:8d}  {binario}  [{marca}]")

    cruzados = {h: c for h, c in md5_para_categorias.items() if len(c) > 1}
    print(f"\nTotal unico por categoria: {len(linhas)}  |  MD5 distintos no dataset inteiro: {len(md5_para_categorias)}")
    print(f"Colisoes de MD5 entre categorias: {len(cruzados)}")
    for h, c in cruzados.items():
        print(f"  {h}  {sorted(c)}")
    ok &= not cruzados

    n_normal = sum(r["rotulo_binario"] == "normal" for r in linhas)
    n_anormal = len(linhas) - n_normal
    print(f"\nBinario: normal={n_normal}  anormal={n_anormal}  "
          f"({n_normal / len(linhas):.1%} / {n_anormal / len(linhas):.1%})")
    print(f"Baseline de classe majoritaria (sempre 'anormal'): {n_anormal / len(linhas):.1%} de acuracia")

    # as 120 imagens da Fase 1 tem de estar entre as unicas
    with open(MANIFEST_FASE1, encoding="utf-8") as f:
        md5_fase1 = {r["md5"] for r in csv.DictReader(f)}
    faltando = md5_fase1 - set(md5_para_categorias)
    print(f"MD5 do manifest da Fase 1 (120) presentes no download: {120 - len(faltando)}/120")
    ok &= not faltando

    saida = args.destino.expanduser().resolve() / "indice-unicos.csv"
    with open(saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    print(f"Indice: {saida}")

    if not ok:
        print("ERRO: resultado diverge da Fase 1.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
