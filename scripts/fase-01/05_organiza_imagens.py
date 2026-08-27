"""Organiza a amostra de imagens de ECG da Parte 3 (Visao Computacional) — Fase 1.

Fonte travada na conversa com o time: Mendeley Data, "ECG Images dataset of
Cardiac Patients", versao 2, DOI 10.17632/gwbz3fsgp8.2, licenca CC BY 4.0
(confirmada na propria pagina do dataset — nao e a CC BY-NC-ND do artigo
descritor na Data in Brief, que e um documento diferente). Equipamento EDAN
SERIES-3, Ch. Pervaiz Elahi Institute of Cardiology, Multan, Paquistao.

O zip ja foi baixado e descompactado FORA do repositorio pelo usuario, em
`ORIGEM_EXTERNA` abaixo. Este script LE de la (nunca escreve la) e grava:
  - a selecao final (120 imagens em resolucao original) numa pasta de saida
    FORA do repositorio, pronta pra upload manual ao Drive/OneDrive;
  - 12 amostras (3 por categoria) reduzidas a 900px de largura, em
    assets/imagens/amostras/, so para ilustrar o README;
  - o manifest completo das 120 em document/datasets/processed/manifest-imagens.csv.

ACHADO 1 — duplicata exata (MD5): dos 928 arquivos baixados (929 esperados
pelos nomes das pastas; falta MI(215).jpg), so 491 sao imagens de conteudo
unico. Por categoria: MI 239->30 (87% de redundancia), PMI 172->86,
Normal 284->142, HB 233->233 (nenhuma duplicata). Ou seja, nomes de arquivo
diferentes dentro da mesma categoria frequentemente apontam pro MESMO byte
a byte. Treinar um modelo sem deduplicar por MD5 infla a acuracia por
vazamento (a mesma imagem exata podia cair em treino E teste). Por isso a
deduplicacao por MD5 e o PRIMEIRO passo, antes de qualquer sorteio.

ACHADO 2 — quase-duplicata (perceptual hash / dHash), investigado ANTES de
escrever este script: computamos dHash de 256 bits (16x16) sobre as 491
imagens unicas por MD5 e olhamos os pares mais proximos por categoria.
A distancia minima encontrada foi de 14 a 19 bits em 256 (5,5%-7,4%) — BEM
acima do que um dHash de 64 bits (8x8) sugeria (chegava a distancia 0 para
arquivos com MD5 diferente, inclusive na categoria HB que nao tem NENHUMA
duplicata exata). Isso e um artefato conhecido deste dominio: todas as
imagens compartilham o mesmo template do aparelho EDAN (mesma grade, mesmo
cabecalho "ECG REPORT", mesma posicao de texto), entao um hash raso
(8x8=64 bits) capta o LAYOUT comum, nao o tracado do paciente. Confirmamos
manualmente (inspecao visual de 3 pares, um por categoria diferente, entre
os mais proximos por hash de 256 bits) que cada imagem no interior da
propria imagem imprime um "ID:" de paciente distinto, data/hora distinta e
frequencia cardiaca distinta — ou seja, sao pacientes genuinamente
diferentes, so compartilhando o template do equipamento. Por isso o limiar
de remocao automatica abaixo (LIMIAR_QUASE_DUPLICATA_BITS) e deliberadamente
apertado (2% dos bits): so remove o que for quase certeza duplicata: com os
dados atuais, NADA fica abaixo desse limiar — a checagem roda mas nao
remove nenhuma imagem alem das ja removidas por MD5.

Nao especulamos a CAUSA da duplicata por MD5 (pode ser artefato do pipeline
de digitalizacao dos autores, reuso proposital, etc.) — so registramos o
fato, medido e verificavel.
"""

from __future__ import annotations

import csv
import hashlib
import random
from pathlib import Path

import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
ORIGEM_EXTERNA = Path("/Users/cesar/Downloads/gwbz3fsgp8-2")
SAIDA_EXTERNA = Path("/Users/cesar/Downloads/cardioia-fase1-imagens-selecionadas")

AMOSTRAS_DIR = REPO_ROOT / "assets" / "imagens" / "amostras"
MANIFEST_PATH = REPO_ROOT / "document" / "datasets" / "processed" / "manifest-imagens.csv"

SEMENTE = 42
N_POR_CATEGORIA = 30
N_AMOSTRAS_POR_CATEGORIA = 3
LARGURA_AMOSTRA_PX = 900

# distancia de Hamming em 256 bits abaixo da qual uma quase-duplicata e
# removida automaticamente. 2% de 256 = ~5 bits — bem mais apertado que o
# menor par genuinamente-diferente que encontramos (14 bits, 5,5%), de
# proposito: so mexe se algo estiver quase identico de verdade.
LIMIAR_QUASE_DUPLICATA_BITS = 5
TAMANHO_DHASH = 16  # 16x16 = 256 bits

CATEGORIAS = [
    {
        "prefixo": "MI",
        "pasta_origem": "ECG Images of Myocardial Infarction Patients (240x12=2880)",
        "categoria_ptbr": "infarto",
    },
    {
        "prefixo": "PMI",
        "pasta_origem": "ECG Images of Patient that have History of MI (172x12=2064)",
        "categoria_ptbr": "historico_infarto",
    },
    {
        "prefixo": "HB",
        "pasta_origem": "ECG Images of Patient that have abnormal heartbeat (233x12=2796)",
        "categoria_ptbr": "batimento_anormal",
    },
    {
        "prefixo": "Normal",
        "pasta_origem": "Normal Person ECG Images (284x12=3408)",
        "categoria_ptbr": "normal",
    },
]

BASE_ORIGEM = (
    "Mendeley Data — ECG Images dataset of Cardiac Patients (v2), "
    "DOI 10.17632/gwbz3fsgp8.2, CC BY 4.0"
)


def md5_de(caminho: Path) -> str:
    return hashlib.md5(caminho.read_bytes()).hexdigest()


def dhash(caminho: Path, tamanho: int = TAMANHO_DHASH) -> np.ndarray:
    with Image.open(caminho) as im:
        im = im.convert("L").resize((tamanho + 1, tamanho), Image.LANCZOS)
        arr = np.asarray(im, dtype=np.int16)
    return (arr[:, 1:] > arr[:, :-1]).flatten()


def hamming(a: np.ndarray, b: np.ndarray) -> int:
    return int(np.count_nonzero(a != b))


def deduplicar_por_md5(pasta: Path) -> list[dict]:
    """Agrupa arquivos por MD5. Retorna 1 registro por conteudo unico,
    ordenado por nome do representante (o alfabeticamente/numericamente
    primeiro alias), com a lista de todos os aliases."""
    arquivos = sorted(pasta.glob("*.jpg"), key=lambda p: p.name)
    grupos: dict[str, list[Path]] = {}
    for fp in arquivos:
        grupos.setdefault(md5_de(fp), []).append(fp)

    registros = []
    for h, alias_paths in grupos.items():
        alias_paths_ordenados = sorted(alias_paths, key=lambda p: p.name)
        registros.append(
            {
                "md5": h,
                "representante": alias_paths_ordenados[0],
                "aliases": [p.name for p in alias_paths_ordenados],
            }
        )
    registros.sort(key=lambda r: r["representante"].name)
    return registros


def remover_quase_duplicatas(registros: list[dict]) -> tuple[list[dict], list[tuple]]:
    """Calcula dHash de cada representante e remove (mantendo so 1 de cada
    par) quem estiver a distancia <= LIMIAR_QUASE_DUPLICATA_BITS de outro.
    Retorna (registros_restantes, pares_removidos_para_log)."""
    hashes = [(r, dhash(r["representante"])) for r in registros]
    removidos_idx = set()
    pares_removidos = []
    n = len(hashes)
    for i in range(n):
        if i in removidos_idx:
            continue
        for j in range(i + 1, n):
            if j in removidos_idx:
                continue
            dist = hamming(hashes[i][1], hashes[j][1])
            if dist <= LIMIAR_QUASE_DUPLICATA_BITS:
                removidos_idx.add(j)
                pares_removidos.append(
                    (dist, hashes[i][0]["representante"].name, hashes[j][0]["representante"].name)
                )
    restantes = [r for k, (r, _) in enumerate(hashes) if k not in removidos_idx]
    return restantes, pares_removidos


def extrair_id_paciente(nome_arquivo: str) -> str:
    # "MI(102).jpg" -> "102"
    inicio = nome_arquivo.index("(") + 1
    fim = nome_arquivo.index(")")
    return nome_arquivo[inicio:fim]


def main() -> None:
    if not ORIGEM_EXTERNA.exists():
        raise FileNotFoundError(
            f"{ORIGEM_EXTERNA} nao existe. Este script espera o dataset ja "
            "baixado e descompactado fora do repositorio nesse caminho."
        )

    SAIDA_EXTERNA.mkdir(parents=True, exist_ok=True)
    AMOSTRAS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    linhas_manifest = []
    contagem_amostras_por_categoria: dict[str, int] = {}

    for cat in CATEGORIAS:
        prefixo = cat["prefixo"]
        pasta = ORIGEM_EXTERNA / cat["pasta_origem"]
        categoria_ptbr = cat["categoria_ptbr"]

        print(f"=== {prefixo} ({cat['pasta_origem']}) ===")

        registros_unicos = deduplicar_por_md5(pasta)
        n_arquivos_totais = sum(len(r["aliases"]) for r in registros_unicos)
        print(f"  arquivos totais: {n_arquivos_totais}  |  unicos por MD5: {len(registros_unicos)}")

        registros_limpos, pares_removidos = remover_quase_duplicatas(registros_unicos)
        if pares_removidos:
            print(f"  [ATENCAO] {len(pares_removidos)} quase-duplicata(s) removida(s) (dist <= {LIMIAR_QUASE_DUPLICATA_BITS}/256 bits):")
            for dist, a, b in pares_removidos:
                print(f"    dist={dist}  {a}  ~=  {b} (removido)")
        else:
            print(f"  quase-duplicatas (dHash 256 bits, limiar <= {LIMIAR_QUASE_DUPLICATA_BITS} bits): nenhuma")
        print(f"  universo amostravel apos MD5 + quase-duplicata: {len(registros_limpos)}")

        rng = random.Random(SEMENTE)
        se_disponiveis = len(registros_limpos)
        alvo = min(N_POR_CATEGORIA, se_disponiveis)
        if alvo < N_POR_CATEGORIA:
            print(
                f"  [AVISO] universo ({se_disponiveis}) menor que o alvo "
                f"({N_POR_CATEGORIA}) — usando o universo inteiro."
            )
        selecionados = sorted(registros_limpos, key=lambda r: r["representante"].name)
        selecionados = rng.sample(selecionados, alvo) if alvo < se_disponiveis else selecionados
        selecionados.sort(key=lambda r: r["representante"].name)

        print(f"  selecionados: {len(selecionados)}")

        for indice, reg in enumerate(selecionados, start=1):
            origem = reg["representante"]
            nome_novo = f"ecg_{categoria_ptbr}_{indice:02d}.jpg"
            destino = SAIDA_EXTERNA / nome_novo
            destino.write_bytes(origem.read_bytes())  # copia byte a byte, sem recomprimir

            with Image.open(origem) as im:
                largura, altura = im.size
                formato = im.format

            tamanho_kb = origem.stat().st_size / 1024

            linhas_manifest.append(
                {
                    "nome_arquivo": nome_novo,
                    "nome_original": origem.name,
                    "categoria_original": prefixo,
                    "categoria_ptbr": categoria_ptbr,
                    "id_paciente": extrair_id_paciente(origem.name),
                    "largura": largura,
                    "altura": altura,
                    "formato": formato,
                    "tamanho_kb": round(tamanho_kb, 1),
                    "md5": reg["md5"],
                    "aliases": ";".join(reg["aliases"]),
                    "base_origem": BASE_ORIGEM,
                }
            )

            if contagem_amostras_por_categoria.get(prefixo, 0) < N_AMOSTRAS_POR_CATEGORIA:
                nome_amostra = f"ecg_{categoria_ptbr}_amostra_{contagem_amostras_por_categoria.get(prefixo, 0) + 1:02d}.jpg"
                with Image.open(origem) as im:
                    proporcao = LARGURA_AMOSTRA_PX / im.width
                    nova_altura = round(im.height * proporcao)
                    im_reduzida = im.convert("RGB").resize(
                        (LARGURA_AMOSTRA_PX, nova_altura), Image.LANCZOS
                    )
                    im_reduzida.save(AMOSTRAS_DIR / nome_amostra, quality=85)
                contagem_amostras_por_categoria[prefixo] = (
                    contagem_amostras_por_categoria.get(prefixo, 0) + 1
                )
        print()

    with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
        campos = [
            "nome_arquivo",
            "nome_original",
            "categoria_original",
            "categoria_ptbr",
            "id_paciente",
            "largura",
            "altura",
            "formato",
            "tamanho_kb",
            "md5",
            "aliases",
            "base_origem",
        ]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(linhas_manifest)

    tamanho_total_saida_mb = sum(
        p.stat().st_size for p in SAIDA_EXTERNA.glob("*.jpg")
    ) / 1024 / 1024

    print("=" * 78)
    print("RESUMO FINAL")
    print("=" * 78)
    print(f"Total selecionado: {len(linhas_manifest)} imagens")
    print(f"Pasta de saida (fora do repo): {SAIDA_EXTERNA}  ({tamanho_total_saida_mb:.1f} MB)")
    print(f"Amostras em {AMOSTRAS_DIR}: {sum(contagem_amostras_por_categoria.values())} arquivos")
    print(f"Manifest: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
