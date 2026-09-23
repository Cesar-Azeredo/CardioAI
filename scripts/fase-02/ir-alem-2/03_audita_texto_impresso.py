"""Audita o texto impresso nas imagens de ECG e propoe o recorte — Ir Alem 2.

Cada imagem do Mendeley (EDAN SERIES-3, 2213x1572 RGB em todas as 491 unicas)
e um relatorio: cabecalho com ID do exame, sexo, campos vazios; rodape com
filtro, velocidade, FREQUENCIA CARDIACA (apos o simbolo de coracao), aviso
"Lead Off" (eletrodo solto) quando houve, e data/hora. O risco: uma MLP pode
aprender a LER o numero impresso em vez do tracado — e a categoria "batimento
anormal" e justamente a de frequencia alterada.

O script, sobre as 491 imagens unicas do indice do script 02:
  1. localiza a moldura vermelha da grade e as faixas de texto fora dela, e
     mostra se as coordenadas sao estaveis entre imagens;
  2. le a FC impressa por casamento de glifos (a fonte e fixa; sem OCR
     externo): recorta os glifos apos o coracao, agrupa bitmaps identicos
     (distancia de Hamming <= 10) e mapeia os 15 prototipos para digitos. O
     mapeamento ROTULO_PROTOTIPOS foi feito por inspecao visual de
     prototipos.png, que o script regrava; a ordem dos prototipos e
     deterministica (indice ordenado), e o script aborta se ela mudar;
  3. tabula FC, "Lead Off" e sexo impresso por categoria;
  4. mede o template fixo do aparelho dentro do recorte;
  5. grava o manifest do Ir Alem 2 (document/datasets/processed/manifest-ir-alem-2.csv)
     e exemplos antes/depois do recorte em --saida (fora do repo).

O recorte e o INTERIOR DA MOLDURA recuado 4 px em cada lado (Etapa 2A): a
borda direita da moldura fica em x=2175 em 52 imagens e em x=2176 nas
demais — lotes de digitalizacao, presentes nas 4 categorias; o resto do
template (barras separadoras, pulso de calibracao) nao se desloca. O recuo
tira a borda do recorte, e a variacao some da entrada da rede. Dentro dele so
resta texto constante do template (rotulos das derivacoes, pulso de
calibracao): sem informacao de classe, mas e o proprio template do aparelho.

Decisao LGPD: o manifest guarda FC e sexo impressos (metadado de avaliacao),
mas NAO o ID do exame nem a data/hora. Transformar texto impresso em dado
estruturado de identificacao cria exatamente o cruzamento que permite
reidentificar, mesmo sendo base publica (document/fase-01/governanca-e-vies.md).

Uso:
    python scripts/fase-02/ir-alem-2/03_audita_texto_impresso.py [--destino DIR] [--saida DIR]
"""

from __future__ import annotations

import argparse
import collections
import csv
import statistics as st
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

DESTINO_PADRAO = Path.home() / ".cache" / "cardioia" / "mendeley-gwbz3fsgp8-v2"
SAIDA_PADRAO = DESTINO_PADRAO / "auditoria-texto"

REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST = REPO_ROOT / "document" / "datasets" / "processed" / "manifest-ir-alem-2.csv"

# PIL (x0, y0, x1, y1), x1/y1 exclusivos. Moldura medida: y 283-1517, x 68-2176
# (2175 em 52 imagens); recuo de 4 px em cada lado.
MOLDURA = (68, 283, 2177, 1518)
RECUO = 4
RECORTE = (MOLDURA[0] + RECUO, MOLDURA[1] + RECUO, MOLDURA[2] - RECUO, MOLDURA[3] - RECUO)
FAIXA_RODAPE_Y = (1534, 1556)
ROTULO_PROTOTIPOS = "816257304094869"
LIMIAR_TINTA = 140
CATEGORIAS = ["MI", "PMI", "HB", "Normal"]


def moldura(rgb: np.ndarray) -> tuple[int, int, int, int]:
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    vermelho = (r > 180) & (r - g > 40) & (r - b > 40)
    linhas = np.where(vermelho.mean(1) > 0.5)[0]
    colunas = np.where(vermelho.mean(0) > 0.5)[0]
    return int(linhas.min()), int(linhas.max()), int(colunas.min()), int(colunas.max())


def faixas(tinta: np.ndarray, y0: int, y1: int, lacuna: int = 4) -> list[tuple[int, int]]:
    ys = np.where(tinta[y0:y1].any(1))[0] + y0
    if len(ys) == 0:
        return []
    out, ini, ant = [], ys[0], ys[0]
    for y in ys[1:]:
        if y - ant > lacuna:
            out.append((int(ini), int(ant)))
            ini = y
        ant = y
    out.append((int(ini), int(ant)))
    return out


def glifos(cinza: np.ndarray, y0: int, y1: int, x0: int, x1: int):
    m = cinza[y0:y1, x0:x1] < LIMIAR_TINTA
    col = m.any(0)
    out, i = [], 0
    while i < len(col):
        if col[i]:
            j = i
            while j < len(col) and col[j]:
                j += 1
            sub = m[:, i:j]
            rows = np.where(sub.any(1))[0]
            out.append((x0 + i, x0 + j - 1, sub[rows.min(): rows.max() + 1]))
            i = j
        else:
            i += 1
    return out


def normaliza(s: np.ndarray) -> np.ndarray:
    z = np.zeros((15, 11), bool)
    h, w = s.shape
    z[: min(h, 15), : min(w, 11)] = s[:15, :11]
    return z


def digitos_da_fc(cinza: np.ndarray) -> tuple[list[np.ndarray], int]:
    g = glifos(cinza, *FAIXA_RODAPE_Y, 60, 900)
    # coracao: glifo cheio de ~13x14 px
    k = next(k for k, (_, _, s) in enumerate(g)
             if 12 <= s.shape[1] <= 15 and 12 <= s.shape[0] <= 14 and s.mean() > 0.55)
    dig, ant = [], g[k][1]
    for x0, x1, s in g[k + 1:]:
        if x0 - ant > 12:
            break
        if s.shape[1] > 12:  # dois digitos encostados: corta na coluna de menos tinta
            w = s.shape[1]
            c = w // 2 - 2 + int(np.argmin(s[:, w // 2 - 2: w // 2 + 3].sum(0)))
            dig += [normaliza(s[:, :c]), normaliza(s[:, c:])]
        else:
            dig.append(normaliza(s))
        ant = x1
    return dig, g[k][0]


def sexo_impresso(cinza: np.ndarray) -> str:
    cols = np.where((cinza[70:100, 400:590] < LIMIAR_TINTA).any(0))[0]
    ini = ant = cols[0]
    for c in cols[1:]:
        if c - ant > 20:
            break
        ant = c
    return "F" if ant - ini > 65 else "M"  # "Male" ~55 px, "Female" ~81 px


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--destino", type=Path, default=DESTINO_PADRAO)
    ap.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    args = ap.parse_args()
    destino = args.destino.expanduser().resolve()
    saida = args.saida.expanduser().resolve()
    saida.mkdir(parents=True, exist_ok=True)
    raiz = destino / "extraido"
    with open(destino / "indice-unicos.csv", encoding="utf-8") as f:
        indice = list(csv.DictReader(f))

    regs = []
    for x in indice:
        rgb = np.asarray(Image.open(raiz / x["representante"]).convert("RGB")).astype(int)
        cinza = np.asarray(Image.open(raiz / x["representante"]).convert("L")).astype(int)
        t, b, l, r = moldura(rgb)
        tinta = rgb.max(-1) < 110
        dig, x_coracao = digitos_da_fc(cinza)
        # tracado (tinta escura; a moldura vermelha nao conta) na faixa entre a moldura e o recorte
        faixa = np.zeros(tinta.shape, bool)
        faixa[MOLDURA[1]:MOLDURA[3], MOLDURA[0]:MOLDURA[2]] = True
        faixa[RECORTE[1]:RECORTE[3], RECORTE[0]:RECORTE[2]] = False
        regs.append(dict(x=x, tam=(rgb.shape[1], rgb.shape[0]), moldura=(t, b, l, r),
                         topo=faixas(tinta, 0, t - 2), rodape=faixas(tinta, b + 2, rgb.shape[0]),
                         dig=dig, lead_off=x_coracao != 550, sexo=sexo_impresso(cinza),
                         tracado_no_recuo=bool((tinta & faixa).any())))

    protos: list[np.ndarray] = []
    for z in regs:
        for d in z["dig"]:
            if not any((d != p).sum() <= 10 for p in protos):
                protos.append(d)
    folha = Image.new("L", (len(protos) * 40, 50), 255)
    for i, p in enumerate(protos):
        folha.paste(Image.fromarray(((~p) * 255).astype("uint8")).resize((33, 45), Image.NEAREST), (i * 40 + 3, 3))
    folha.save(saida / "prototipos.png")
    if len(protos) != len(ROTULO_PROTOTIPOS):
        print(f"ERRO: {len(protos)} prototipos (esperado {len(ROTULO_PROTOTIPOS)}); "
              f"reinspecione {saida / 'prototipos.png'}", file=sys.stderr)
        return 1
    pior = 0
    for z in regs:
        lidos = []
        for d in z["dig"]:
            dist = [int((d != p).sum()) for p in protos]
            i = int(np.argmin(dist))
            pior = max(pior, dist[i])
            lidos.append(ROTULO_PROTOTIPOS[i])
        z["fc"] = int("".join(lidos))

    print("== 1. Layout (491 imagens unicas) ==")
    print("tamanho:", collections.Counter(z["tam"] for z in regs).most_common())
    print("moldura (topo, base, esq, dir):", collections.Counter(z["moldura"] for z in regs).most_common())
    print("fim da ultima faixa de texto do cabecalho (y):",
          collections.Counter(z["topo"][-1][1] for z in regs).most_common())
    print("faixas do rodape:", collections.Counter(tuple(z["rodape"]) for z in regs).most_common())
    fora = sum(z["topo"][-1][1] > z["moldura"][0] - 8 or len(z["rodape"]) > 1 for z in regs)
    print(f"imagens com pico do tracado passando da moldura (cortado pelo recorte): {fora}")
    print(f"imagens com tracado na faixa de {RECUO} px do recuo (tambem cortado): "
          f"{sum(z['tracado_no_recuo'] for z in regs)}")
    print("borda direita da moldura em x=2175, por categoria:")
    for c in CATEGORIAS:
        q = [z for z in regs if z["x"]["categoria_original"] == c]
        n = sum(z["moldura"][3] == 2175 for z in q)
        print(f"  {c:6s} {n:3d} de {len(q):3d} ({n / len(q):.0%})")

    print(f"\n== 2. FC impressa (pior distancia de casamento: {pior} bits de 165) ==")
    for c in CATEGORIAS:
        f = [z["fc"] for z in regs if z["x"]["categoria_original"] == c]
        acima = sum(v > 90 for v in f)
        print(f"  {c:6s} n={len(f):3d} mediana={st.median(f):5.1f} min={min(f):3d} max={max(f):3d} "
              f">90 bpm: {acima:3d} ({acima / len(f):.0%})")
    max_normal = max(z["fc"] for z in regs if z["x"]["rotulo_binario"] == "normal")
    an = [z for z in regs if z["x"]["rotulo_binario"] == "anormal"]
    n_atalho = sum(z["fc"] > max_normal for z in an)
    print(f"  FC maxima entre as normais: {max_normal} bpm -> 'FC impressa > {max_normal}' "
          f"identifica {n_atalho}/{len(an)} anormais ({n_atalho / len(an):.0%}) com precisao de 100%")

    print("\n== 3. Outros campos impressos por categoria ==")
    for c in CATEGORIAS:
        q = [z for z in regs if z["x"]["categoria_original"] == c]
        nf = sum(z["sexo"] == "F" for z in q)
        nl = sum(z["lead_off"] for z in q)
        print(f"  {c:6s} sexo F={nf:3d} M={len(q) - nf:3d} ({nf / len(q):.0%} F)  "
              f"'Lead Off'={nl:3d} ({nl / len(q):.0%})")
    nf = sum(z["sexo"] == "F" for z in regs)
    print(f"  total  sexo F={nf} M={len(regs) - nf} ({(len(regs) - nf) / len(regs):.1%} masculino)")

    campos = ["md5", "categoria_original", "rotulo_binario", "representante", "n_aliases", "aliases",
              "fc_impressa", "sexo_impresso", "lead_off", "borda_direita_x"]
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for z in sorted(regs, key=lambda z: z["x"]["md5"]):
            w.writerow({**{k: z["x"][k] for k in campos[:6]}, "fc_impressa": z["fc"],
                        "sexo_impresso": z["sexo"], "lead_off": int(z["lead_off"]),
                        "borda_direita_x": z["moldura"][3]})

    # 4. template dentro do recorte: pixel escuro em >=95% das imagens = impresso
    # pelo aparelho (rotulos, pulso de calibracao, barras separadoras), nao pelo paciente
    escuro = np.zeros((RECORTE[3] - RECORTE[1], RECORTE[2] - RECORTE[0]), np.int32)
    tinta_total = 0
    for z in regs:
        g = np.asarray(Image.open(raiz / z["x"]["representante"]).convert("L").crop(RECORTE)) < 110
        escuro += g
        tinta_total += g.sum()
    fixo = escuro >= 0.95 * len(regs)
    print("\n== 4. Template do aparelho dentro do recorte ==")
    print(f"  pixels escuros em >=95% das imagens (template fixo): {fixo.sum():,} "
          f"= {fixo.sum() / (tinta_total / len(regs)):.0%} da tinta media por imagem")

    exemplos = [
        max((z for z in regs if z["x"]["categoria_original"] == "HB"), key=lambda z: z["fc"]),
        next(z for z in regs if z["x"]["categoria_original"] == "MI"),
        next(z for z in regs if z["x"]["categoria_original"] == "PMI" and z["lead_off"]),
        max((z for z in regs if z["x"]["categoria_original"] == "Normal"), key=lambda z: z["fc"]),
    ]
    for i, z in enumerate(exemplos, 1):
        caminho = raiz / z["x"]["representante"]
        antes = Image.open(caminho).convert("RGB")
        d = ImageDraw.Draw(antes)
        d.rectangle((0, 25, antes.width, 278), outline=(0, 90, 255), width=6)
        d.rectangle((0, 1532, antes.width, 1558), outline=(0, 90, 255), width=6)
        d.rectangle(RECORTE, outline=(0, 170, 0), width=6)
        depois = Image.open(caminho).convert("L").crop(RECORTE)
        painel = Image.new("RGB", (antes.width + 40 + depois.width, antes.height), "white")
        painel.paste(antes, (0, 0))
        painel.paste(depois.convert("RGB"), (antes.width + 40, (antes.height - depois.height) // 2))
        nome = Path(z["x"]["representante"]).stem.replace("(", "_").replace(")", "")
        painel.resize((painel.width // 2, painel.height // 2), Image.LANCZOS).save(
            saida / f"{i}_{nome}_fc{z['fc']}.png")
    print(f"\nRecorte proposto {RECORTE} -> {RECORTE[2] - RECORTE[0]}x{RECORTE[3] - RECORTE[1]} px")
    print(f"Manifest: {MANIFEST.relative_to(REPO_ROOT)} ({len(regs)} linhas)")
    print(f"Exemplos antes/depois e prototipos em {saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
