"""Sorteia imagens para validar a leitura por glifo da FC e do sexo — Ir Alem 2.

O leitor de glifos do script 03 nao tem gabarito: os "100% de precisao" da
regra "FC impressa > 90 -> anormal" so valem se a leitura estiver certa. Este
script monta dois paineis a partir do manifest do Ir Alem 2:

  - aleatorio: N imagens sorteadas (semente fixa);
  - dirigido: os casos de que a regra mais depende e que o sorteio quase nao
    pega — TODAS as Normais com FC lida >= 85 (se alguma Normal com FC real
    > 90 foi lida <= 90, a "precisao de 100%" cai), mais 5 "Female" e 5 com
    "Lead Off" (rodape deslocado), sorteadas fora da amostra aleatoria.

Cada linha do painel mostra, para cada uma, o recorte do campo de sexo e do campo de FC da
propria imagem ao lado do valor que o leitor extraiu. A conferencia e humana
(visual); o resultado fica registrado em document/fase-02/ir-alem-2/.

O painel NAO inclui ID do exame nem data/hora (decisao LGPD, ver o protocolo).
Sai fora do repositorio (--saida).

Uso:
    python scripts/fase-02/ir-alem-2/04_amostra_validacao_glifos.py [--n 20] [--saida DIR]
"""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

from PIL import Image, ImageDraw

DESTINO_PADRAO = Path.home() / ".cache" / "cardioia" / "mendeley-gwbz3fsgp8-v2"
REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST = REPO_ROOT / "document" / "datasets" / "processed" / "manifest-ir-alem-2.csv"
SEMENTE = 42

CAMPO_SEXO = (380, 62, 640, 104)       # palavra "Male"/"Female" do cabecalho
CAMPO_FC = (480, 1530, 820, 1560)      # "...4*2.5s+1r <coracao>NN"
DESLOC_LEAD_OFF = 109                  # "Lead Off" empurra o coracao de x=550 para x=659


def painel(linhas: list[dict], raiz: Path, destino: Path) -> None:
    esc = 2
    alt = (CAMPO_FC[3] - CAMPO_FC[1]) * esc + 10
    larg = (CAMPO_SEXO[2] - CAMPO_SEXO[0]) + (CAMPO_FC[2] - CAMPO_FC[0]) * esc + 420
    out = Image.new("RGB", (larg, alt * len(linhas)), "white")
    d = ImageDraw.Draw(out)
    for i, r in enumerate(linhas):
        im = Image.open(raiz / r["representante"]).convert("RGB")
        y = i * alt
        d.text((5, y + 12), f"{i + 1:2d} {r['categoria_original']:6s} leitor: sexo={r['sexo_impresso']}  "
                            f"FC={r['fc_impressa']}  LO={r['lead_off']}", fill="black")
        sexo = im.crop(CAMPO_SEXO)
        out.paste(sexo, (220, y + 5))
        dx = DESLOC_LEAD_OFF if r["lead_off"] == "1" else 0
        fc = im.crop((CAMPO_FC[0] + dx, CAMPO_FC[1], CAMPO_FC[2] + dx, CAMPO_FC[3]))
        out.paste(fc.resize((fc.width * esc, fc.height * esc)), (220 + sexo.width + 20, y + 5))
    out.save(destino)


def grava(linhas: list[dict], destino: Path) -> None:
    with open(destino, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ordem", "md5", "categoria_original", "fc_impressa", "sexo_impresso", "lead_off"])
        for i, r in enumerate(linhas, 1):
            w.writerow([i, r["md5"], r["categoria_original"], r["fc_impressa"], r["sexo_impresso"], r["lead_off"]])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--destino", type=Path, default=DESTINO_PADRAO)
    ap.add_argument("--saida", type=Path, default=DESTINO_PADRAO / "validacao-glifos")
    ap.add_argument("--n", type=int, default=20)
    args = ap.parse_args()
    raiz = args.destino.expanduser().resolve() / "extraido"
    saida = args.saida.expanduser().resolve()
    saida.mkdir(parents=True, exist_ok=True)

    with open(MANIFEST, encoding="utf-8") as f:
        linhas = sorted(csv.DictReader(f), key=lambda r: r["md5"])
    amostra = random.Random(SEMENTE).sample(linhas, args.n)
    resto = [r for r in linhas if r not in amostra]
    rng = random.Random(SEMENTE)  # gerador proprio para a dirigida, independente do sorteio acima
    dirigida = [r for r in resto if r["categoria_original"] == "Normal" and int(r["fc_impressa"]) >= 85]
    dirigida += rng.sample([r for r in resto if r["sexo_impresso"] == "F" and r not in dirigida], 5)
    dirigida += rng.sample([r for r in resto if r["lead_off"] == "1" and r not in dirigida], 5)

    painel(amostra, raiz, saida / "painel-aleatorio.png")
    grava(amostra, saida / "amostra-aleatoria.csv")
    painel(dirigida, raiz, saida / "painel-dirigido.png")
    grava(dirigida, saida / "amostra-dirigida.csv")
    print(f"aleatoria: {len(amostra)} imagens (semente {SEMENTE}); dirigida: {len(dirigida)} imagens -> {saida}")

if __name__ == "__main__":
    main()
