"""Verificacao do mapa de conhecimento e das 10 frases — Fase 2.

NAO e o extrator de sintomas. So confere, por maquina, as regras que o mapa
e as frases (dado primario autoral, decisao 3 da secao 5bis do CLAUDE.md)
prometem cumprir, e sai com codigo 1 se alguma falhar.

MAPA (document/datasets/fase-02/mapa-conhecimento-sintomas.csv)
  - CONGELADO: o SHA-256 do arquivo tem que ser SHA256_MAPA_CONGELADO (regra
    em document/fase-02/gabarito-frases.md) — o mapa nao recebe variantes
    para acertar frases de teste;
  Cada linha e um CONCEITO de sintoma com um sinonimo (formato dos exemplos do
  enunciado: "dor no peito", "aperto no tórax" -> Infarto).
  - as tres primeiras colunas sao exatamente "Sintoma 1", "Sintoma 2",
    "Doença Associada";
  - so tres doencas (Hipertensao, Infarto, AVC) e so as tres fontes gov.br;
  - todo trecho de `trecho_literal` (separados por " | ") existe EXATAMENTE
    no .txt indicado (maiusculas, acentos e pontuacao iguais);
  - Sintoma 1 e SEMPRE literal: aparece, como palavra inteira, dentro de um
    dos trechos (sem diferenciar maiuscula, porque o termo vem em minuscula e
    a pagina comeca item de lista com maiuscula). Unica excecao: correcao
    documentada de erro de digitacao da fonte — `observacao` diz
    `Sintoma 1 = correção de "<forma da página>"`, a forma da pagina esta no
    trecho, o termo corrigido NAO esta na pagina e difere dela em no maximo
    MAX_EDICOES_CORRECAO caracteres;
  - `tipo_termo` descreve a coluna Sintoma 2: "literal" -> Sintoma 2 tambem
    aparece num dos trechos; "variante_leiga" -> Sintoma 2 NAO aparece em
    lugar nenhum do .txt (se aparecesse, seria literal, nao variante);
  - Sintoma 1 diferente de Sintoma 2; nenhum par repetido na mesma doenca.
  Tambem lista os conceitos compartilhados entre doencas — nao e erro, e a
  ambiguidade que o extrator vai ter que resolver.

PROTOCOLO (document/fase-02/protocolo-extrator.md)
  - CONGELADO: o SHA-256 do arquivo tem que ser SHA256_PROTOCOLO_CONGELADO —
    regras do extrator pre-registradas nao mudam depois de ver resultado.

FRASES (assets/textos/fase-02/frases-sintomas-pacientes.txt)
  - CONGELADAS: o SHA-256 do arquivo tem que ser SHA256_FRASES_CONGELADAS
    (regra em document/fase-02/gabarito-frases.md) — casos de teste nao mudam
    para acomodar o extrator;
  - exatamente 10 linhas, UTF-8;
  - sem idade exata ("NN anos") e sem sequencia de 3+ digitos (identificador);
  - clausula ND: maior sequencia de palavras em comum com cada pagina-fonte
    abaixo de LIMITE_NGRAMA_ND — frase de paciente e redacao propria, nao
    trecho copiado da pagina;
  - lista os termos do mapa que aparecem literalmente em cada frase (so para
    conferir o desenho dos casos de teste; nao e extracao).
"""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
MAPA_PATH = RAIZ / "document" / "datasets" / "fase-02" / "mapa-conhecimento-sintomas.csv"
FRASES_PATH = RAIZ / "assets" / "textos" / "fase-02" / "frases-sintomas-pacientes.txt"
PROTOCOLO_PATH = RAIZ / "document" / "fase-02" / "protocolo-extrator.md"

CABECALHO = [
    "Sintoma 1",
    "Sintoma 2",
    "Doença Associada",
    "tipo_termo",
    "fonte",
    "trecho_literal",
    "observacao",
]
DOENCAS = {"Hipertensão", "Infarto", "AVC"}
FONTES = {
    "assets/textos/texto_02_hipertensao-pressao-alta-ministerio-saude.txt",
    "assets/textos/fase-02/texto_03_infarto-ministerio-saude.txt",
    "assets/textos/fase-02/texto_04_avc-ministerio-saude.txt",
}
N_FRASES = 10
# Mapa, frases e protocolo congelados em 2026-09-23 — ver document/fase-02/gabarito-frases.md
# e document/fase-02/protocolo-extrator.md.
SHA256_PROTOCOLO_CONGELADO = "90ed4cf356de81d400f25dd3b2f2cc303b01d9cb3bac67880b1a7a4aeaea2da4"
SHA256_MAPA_CONGELADO = "79fae46c6cfd8418eaed30b39f8c84f8eca80b9f0e3ac086ceedac18b91d63c3"
SHA256_FRASES_CONGELADAS = "e124a24e4532e5f008fdfe0d47b6e5638c3cc53409350c39bf96bf731e48c91b"
MAX_EDICOES_CORRECAO = 2
LIMITE_NGRAMA_ND = 6  # 6+ palavras seguidas iguais a pagina = suspeita de copia

RE_CORRECAO = re.compile(r'Sintoma 1 = correção de "(?P<original>[^"]+)"')


def contem_termo(texto: str, termo: str) -> bool:
    """Termo como palavra(s) inteira(s), sem diferenciar maiuscula:
    "tontura" nao casa com "tonturas"."""
    padrao = r"(?<!\w)" + re.escape(termo.casefold()) + r"(?!\w)"
    return re.search(padrao, texto.casefold()) is not None


def ler_fonte(caminho_relativo: str, cache: dict[str, str]) -> str:
    if caminho_relativo not in cache:
        cache[caminho_relativo] = (RAIZ / caminho_relativo).read_text(encoding="utf-8")
    return cache[caminho_relativo]


def distancia_edicao(a: str, b: str) -> int:
    """Levenshtein simples — so para limitar o tamanho de uma correcao."""
    anterior = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        atual = [i]
        for j, cb in enumerate(b, start=1):
            atual.append(min(anterior[j] + 1, atual[j - 1] + 1, anterior[j - 1] + (ca != cb)))
        anterior = atual
    return anterior[-1]


def verificar_linha(linha: dict, cache: dict[str, str]) -> list[str]:
    erros = []
    s1, s2 = linha["Sintoma 1"].strip(), linha["Sintoma 2"].strip()
    doenca, tipo = linha["Doença Associada"], linha["tipo_termo"]
    fonte, trecho, obs = linha["fonte"], linha["trecho_literal"], linha["observacao"]

    if not s1 or not s2:
        erros.append("Sintoma 1 e Sintoma 2 são obrigatórios")
    if s1.casefold() == s2.casefold():
        erros.append("Sintoma 1 e Sintoma 2 são o mesmo termo")
    if doenca not in DOENCAS:
        erros.append(f"doença fora do escopo: {doenca!r}")
    if fonte not in FONTES:
        return erros + [f"fonte não autorizada: {fonte!r}"]
    texto = ler_fonte(fonte, cache)

    trechos = [t.strip() for t in trecho.split(" | ") if t.strip()]
    if not trechos:
        erros.append("trecho_literal vazio — Sintoma 1 é sempre literal e precisa de âncora")
    for t in trechos:
        if t not in texto:
            erros.append(f"trecho não existe literalmente na fonte: {t[:60]!r}")

    # Sintoma 1: literal, ou correcao documentada de erro de digitacao da fonte
    correcao = RE_CORRECAO.search(obs)
    if correcao:
        original = correcao["original"]
        if not any(original in t for t in trechos):
            erros.append(f"forma da página {original!r} não está no trecho_literal")
        if contem_termo(texto, s1):
            erros.append(f"Sintoma 1 {s1!r} já existe na página — não há o que corrigir")
        if distancia_edicao(s1.casefold(), original.casefold()) > MAX_EDICOES_CORRECAO:
            erros.append(f"correção muda mais de {MAX_EDICOES_CORRECAO} caracteres: {original!r} → {s1!r}")
    elif not any(contem_termo(t, s1) for t in trechos):
        erros.append(f"Sintoma 1 {s1!r} não está no trecho_literal")

    # tipo_termo descreve Sintoma 2
    if tipo == "literal":
        if not any(contem_termo(t, s2) for t in trechos):
            erros.append(f"Sintoma 2 {s2!r} marcado como literal, mas não está no trecho_literal")
    elif tipo == "variante_leiga":
        if contem_termo(texto, s2):
            erros.append(f"Sintoma 2 {s2!r} aparece literalmente na fonte — é literal, não variante")
    else:
        erros.append(f"tipo_termo inválido: {tipo!r}")
    return erros


def verificar_mapa() -> tuple[bool, list[dict]]:
    with MAPA_PATH.open(encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        cabecalho = leitor.fieldnames
        linhas = list(leitor)

    print("=" * 78)
    print(f"MAPA — {MAPA_PATH.relative_to(RAIZ)}")
    print("=" * 78)
    ok = True
    if cabecalho != CABECALHO:
        print(f"[FALHA] cabeçalho {cabecalho} != {CABECALHO}")
        return False, linhas
    print(f"[OK]    cabeçalho: {', '.join(cabecalho)}")
    sha = hashlib.sha256(MAPA_PATH.read_bytes()).hexdigest()
    if sha != SHA256_MAPA_CONGELADO:
        print(f"[FALHA] mapa alterado: SHA-256 {sha[:12]}… ≠ congelado "
              f"{SHA256_MAPA_CONGELADO[:12]}… — o mapa não recebe variantes para acertar frases de teste")
        ok = False
    else:
        print(f"[OK]    mapa congelado (SHA-256 {sha[:12]}…)")

    cache: dict[str, str] = {}
    pares = defaultdict(list)
    for i, linha in enumerate(linhas, start=2):  # linha 1 do arquivo = cabeçalho
        if None in linha or any(v is None for v in linha.values()):
            print(f"[FALHA] linha {i}: número de colunas diferente de {len(CABECALHO)}")
            ok = False
            continue
        erros = verificar_linha(linha, cache)
        par = frozenset({linha["Sintoma 1"].casefold(), linha["Sintoma 2"].casefold()})
        pares[(linha["Doença Associada"], par)].append(i)
        rotulo = f"{linha['Sintoma 1']} + {linha['Sintoma 2']} → {linha['Doença Associada']} [{linha['tipo_termo']}]"
        if erros:
            ok = False
            print(f"[FALHA] linha {i}: {rotulo}")
            for e in erros:
                print(f"          - {e}")
        else:
            print(f"[OK]    linha {i:2}: {rotulo}")

    for (doenca, par), numeros in pares.items():
        if len(numeros) > 1:
            ok = False
            print(f"[FALHA] par repetido para {doenca}: {sorted(par)} nas linhas {numeros}")

    print()
    contagem = defaultdict(lambda: defaultdict(int))
    for linha in linhas:
        contagem[linha["Doença Associada"]][linha["tipo_termo"]] += 1
    conceitos = defaultdict(set)
    for linha in linhas:
        conceitos[linha["Doença Associada"]].add(linha["Sintoma 1"].casefold())
    print("Sintoma 2 por tipo:")
    print(f"{'Doença':12} {'conceitos':>9} {'literal':>8} {'variante':>9} {'linhas':>7}")
    for d in ("Hipertensão", "Infarto", "AVC"):
        c = contagem[d]
        print(f"{d:12} {len(conceitos[d]):>9} {c['literal']:>8} {c['variante_leiga']:>9} "
              f"{c['literal'] + c['variante_leiga']:>7}")
    print(f"{'TOTAL':12} {sum(len(v) for v in conceitos.values()):>9} "
          f"{sum(c['literal'] for c in contagem.values()):>8} "
          f"{sum(c['variante_leiga'] for c in contagem.values()):>9} {len(linhas):>7}")

    print()
    print("Termos compartilhados entre doenças (termo igual, ou um contido no outro):")
    termos = defaultdict(set)  # termo -> doenças
    for linha in linhas:
        for col in ("Sintoma 1", "Sintoma 2"):
            termos[linha[col].casefold()].add(linha["Doença Associada"])
    for a in sorted(termos):
        if len(termos[a]) > 1:
            print(f"  - {a!r}: {', '.join(sorted(termos[a]))}")
        for b in sorted(termos):
            if a != b and contem_termo(b, a) and termos[b] - termos[a]:
                print(f"  - {a!r} ({', '.join(sorted(termos[a]))}) ⊂ {b!r} ({', '.join(sorted(termos[b]))})")
    return ok, linhas


def maior_ngrama_comum(frase: str, texto: str) -> int:
    palavras = lambda s: re.findall(r"\w+", s.casefold())
    f, t = palavras(frase), " " + " ".join(palavras(texto)) + " "
    maior = 0
    for i in range(len(f)):
        for j in range(i + maior + 1, len(f) + 1):
            if " " + " ".join(f[i:j]) + " " in t:
                maior = j - i
            else:
                break
    return maior


def verificar_frases(linhas_mapa: list[dict]) -> bool:
    print()
    print("=" * 78)
    print(f"FRASES — {FRASES_PATH.relative_to(RAIZ)}")
    print("=" * 78)
    sha = hashlib.sha256(FRASES_PATH.read_bytes()).hexdigest()
    ok = True
    if sha != SHA256_FRASES_CONGELADAS:
        print(f"[FALHA] frases alteradas: SHA-256 {sha[:12]}… ≠ congelado "
              f"{SHA256_FRASES_CONGELADAS[:12]}… — casos de teste não mudam para acomodar o extrator")
        ok = False
    else:
        print(f"[OK]    frases congeladas (SHA-256 {sha[:12]}…)")
    frases = [l for l in FRASES_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(frases) != N_FRASES:
        print(f"[FALHA] {len(frases)} frases (esperado {N_FRASES})")
        ok = False
    else:
        print(f"[OK]    {N_FRASES} frases")

    textos_fonte = {f: (RAIZ / f).read_text(encoding="utf-8") for f in sorted(FONTES)}
    termos_fonte = sorted({(l["Sintoma 1"], l["Doença Associada"]) for l in linhas_mapa}
                          | {(l["Sintoma 2"], l["Doença Associada"]) for l in linhas_mapa
                             if l["tipo_termo"] == "literal"})
    termos_variante = sorted({(l["Sintoma 2"], l["Doença Associada"]) for l in linhas_mapa
                              if l["tipo_termo"] == "variante_leiga"} - set(termos_fonte))
    for n, frase in enumerate(frases, start=1):
        problemas = []
        if re.search(r"\d+\s*anos", frase):
            problemas.append("idade exata")
        if re.search(r"\d{3,}", frase):
            problemas.append("sequência de 3+ dígitos")
        ngramas = {Path(f).name[:8]: maior_ngrama_comum(frase, t) for f, t in textos_fonte.items()}
        if max(ngramas.values()) >= LIMITE_NGRAMA_ND:
            problemas.append(f"trecho de {max(ngramas.values())} palavras igual à fonte (ND)")
        achados_fonte = sorted({f"{t} ({d})" for t, d in termos_fonte if contem_termo(frase, t)})
        achados_var = sorted({f"{t} ({d})" for t, d in termos_variante if contem_termo(frase, t)})
        status = "FALHA" if problemas else "OK"
        ok = ok and not problemas
        print(f"[{status}]    frase {n:2}: maior n-grama comum com as fontes = "
              + ", ".join(f"{k} {v}" for k, v in ngramas.items())
              + (f" — {'; '.join(problemas)}" if problemas else ""))
        print(f"            termos literais presentes: {', '.join(achados_fonte) or '—'}")
        print(f"            variantes leigas presentes: {', '.join(achados_var) or '—'}")
    return ok


def verificar_protocolo() -> bool:
    print()
    print("=" * 78)
    print(f"PROTOCOLO — {PROTOCOLO_PATH.relative_to(RAIZ)}")
    print("=" * 78)
    sha = hashlib.sha256(PROTOCOLO_PATH.read_bytes()).hexdigest()
    if sha != SHA256_PROTOCOLO_CONGELADO:
        print(f"[FALHA] protocolo alterado: SHA-256 {sha[:12]}… ≠ congelado "
              f"{SHA256_PROTOCOLO_CONGELADO[:12]}… — regra pré-registrada não muda depois de ver resultado")
        return False
    print(f"[OK]    protocolo congelado (SHA-256 {sha[:12]}…)")
    return True


def main() -> int:
    ok_mapa, linhas = verificar_mapa()
    ok_frases = verificar_frases(linhas)
    ok_protocolo = verificar_protocolo()
    print()
    if ok_mapa and ok_frases and ok_protocolo:
        print("RESULTADO: todas as verificações passaram.")
        return 0
    print("RESULTADO: há falhas — linha do mapa que falha não entra.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
