"""Baixa e extrai o dataset de ECG do Mendeley — Ir Alem 2 (MLP em Keras).

Fonte: Mendeley Data, "ECG Images dataset of Cardiac Patients", versao 2,
DOI 10.17632/gwbz3fsgp8.2, licenca CC BY 4.0 (a mesma base da Fase 1 —
proveniencia em document/datasets/README.md). URL publica da API:
    https://data.mendeley.com/public-api/zip/gwbz3fsgp8/download/2
Ela responde 302 para uma URL S3 pre-assinada (expira em 300 s); o urllib
segue o redirect sozinho.

O dado NUNCA vai para dentro do repositorio (regra inviolavel 2: 194 MB
comprimidos, 589 MB extraidos). Destino padrao: ~/.cache/cardioia/, que
existe tanto no macOS quanto no Colab (/root/.cache/cardioia/). Pode ser
trocado com --destino.

So biblioteca padrao, de proposito: o notebook do Colab chama este mesmo
codigo antes de qualquer pip install.

Idempotente: se o zip ja existe e passa na conferencia de estrutura, nao
baixa de novo. A conferencia e por CONTAGEM de .jpg por pasta (928 arquivos
esperados, 929 pelos nomes das pastas menos o MI(215).jpg ausente, achado
da Fase 1), nao por hash do zip — o Mendeley gera o zip no servidor e nao
publica checksum, entao um hash do zip fixado aqui poderia quebrar sem que
o conteudo mudasse. O hash que importa e o MD5 de cada imagem, conferido no
script 02.

Uso:
    python scripts/fase-02/ir-alem-2/01_baixa_ecg_mendeley.py [--destino DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
import zipfile
from pathlib import Path

URL_API = "https://data.mendeley.com/public-api/zip/gwbz3fsgp8/download/2"
DESTINO_PADRAO = Path.home() / ".cache" / "cardioia" / "mendeley-gwbz3fsgp8-v2"
NOME_ZIP = "gwbz3fsgp8-2.zip"

# Contagem de .jpg por pasta verificada na Fase 1 (scripts/fase-01/05_*.py).
CONTAGEM_ESPERADA = {
    "ECG Images of Myocardial Infarction Patients (240x12=2880)": 239,
    "ECG Images of Patient that have History of MI (172x12=2064)": 172,
    "ECG Images of Patient that have abnormal heartbeat (233x12=2796)": 233,
    "Normal Person ECG Images (284x12=3408)": 284,
}


def baixar(url: str, destino_zip: Path) -> None:
    parcial = destino_zip.with_suffix(".zip.parcial")
    req = urllib.request.Request(url, headers={"User-Agent": "cardioia-fiap/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp, open(parcial, "wb") as f:
        total = int(resp.headers.get("Content-Length", 0))
        baixado = 0
        while bloco := resp.read(1 << 20):
            f.write(bloco)
            baixado += len(bloco)
            if total:
                print(f"\r  {baixado / 2**20:6.1f} / {total / 2**20:.1f} MB", end="", flush=True)
    print()
    parcial.rename(destino_zip)


def sha256_de(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        while bloco := f.read(1 << 20):
            h.update(bloco)
    return h.hexdigest()


def localizar_raiz(extraido: Path) -> Path:
    """Acha a pasta que contem as 4 pastas de categoria, qualquer que seja
    o aninhamento que o zip do Mendeley use."""
    alvo = next(iter(CONTAGEM_ESPERADA))
    for p in extraido.rglob(alvo):
        if p.is_dir():
            return p.parent
    raise FileNotFoundError(f"pasta '{alvo}' nao encontrada dentro de {extraido}")


def conferir(raiz: Path) -> bool:
    ok = True
    for pasta, esperado in CONTAGEM_ESPERADA.items():
        n = len(list((raiz / pasta).glob("*.jpg")))
        marca = "ok" if n == esperado else "DIVERGE"
        print(f"  {n:4d} .jpg (esperado {esperado:4d}) [{marca}]  {pasta}")
        ok &= n == esperado
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--destino", type=Path, default=DESTINO_PADRAO)
    args = ap.parse_args()

    destino: Path = args.destino.expanduser().resolve()
    destino.mkdir(parents=True, exist_ok=True)
    zip_path = destino / NOME_ZIP
    extraido = destino / "extraido"

    if not zip_path.exists():
        print(f"Baixando {URL_API}\n  -> {zip_path}")
        baixar(URL_API, zip_path)
    else:
        print(f"Zip ja presente: {zip_path}")
    print(f"  tamanho: {zip_path.stat().st_size / 2**20:.1f} MB  sha256: {sha256_de(zip_path)}")

    if not extraido.exists():
        print(f"Extraindo em {extraido}")
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(extraido)
        # o zip do Mendeley pode conter zips internos por pasta
        for interno in sorted(extraido.rglob("*.zip")):
            print(f"  extraindo zip interno: {interno.relative_to(extraido)}")
            with zipfile.ZipFile(interno) as z:
                z.extractall(interno.parent)

    raiz = localizar_raiz(extraido)
    print(f"Raiz das categorias: {raiz}")
    if not conferir(raiz):
        print("ERRO: contagem de arquivos diverge da verificada na Fase 1.", file=sys.stderr)
        return 1
    print(f"OK — 928 arquivos, como na Fase 1. RAIZ={raiz}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
