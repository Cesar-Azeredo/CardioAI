"""Testes de unidade pre-registrados do extrator — Fase 2.

Implementa a tabela 10.6 de document/fase-02/protocolo-extrator.md (U1 a U14).
As entradas sao frases sinteticas escritas para testar cada regra, DISTINTAS
das 10 frases de teste. Estes testes conferem se o codigo implementa o
protocolo; podem ser rodados quantas vezes for preciso. Sai com codigo 1 se
qualquer teste falhar — e, nesse caso, o extrator NAO roda nas frases.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("extrator", AQUI / "02_extrai_sintomas_sugere_diagnostico.py")
ext = importlib.util.module_from_spec(_spec)
sys.modules["extrator"] = ext  # dataclass com anotacoes adiadas exige o modulo registrado
_spec.loader.exec_module(ext)

ext.preparar_recursos_nltk()
NORM = ext.Normalizador()
MAPA = ext.carregar_mapa(NORM)


def metodo(texto):
    return ext.analisar(texto, NORM, MAPA, "metodo")


def baseline(texto):
    return ext.analisar(texto, NORM, MAPA, "baseline")


def casamento(r, termo):
    """Casamento aceito cujo grupo contem o termo do mapa (texto exato do CSV)."""
    for c in r["casamentos"]:
        if any(e.termo == termo for e in c.entradas):
            return c
    return None


def gatilhos(texto):
    """Gatilhos nao consumidos de todas as oracoes (para o U3)."""
    r = metodo(texto)
    achados = []
    for o, oracao in enumerate(NORM.oracoes(texto)):
        consumidos = {i for c in r["casamentos"] if c.oracao == o for i in c.posicoes}
        achados += [forma for _, forma in ext.gatilhos_nao_consumidos(oracao, consumidos)]
    return achados


TESTES = []


def teste(nome, regra):
    def registrar(f):
        TESTES.append((nome, regra, f))
        return f
    return registrar


@teste("U1", "4.3 — `sem` consumido pelo termo")
def u1():
    c = casamento(metodo("estou sem fôlego desde cedo"), "sem fôlego")
    assert c is not None, "sem fôlego não casou"
    assert c.negado_por is None, f"sem fôlego negado por {c.negado_por}"


@teste("U2", "4.3")
def u2():
    c = casamento(metodo("passei o dia sem forças"), "sem forças")
    assert c is not None, "sem forças não casou"
    assert c.negado_por is None, f"sem forças negado por {c.negado_por}"


@teste("U3", "3.2, 4.1, 4.3")
def u3():
    texto = "sem dor nenhuma no peito"
    c = casamento(metodo(texto), "dor no peito")
    assert c is not None, "dor no peito não casou (intervalo de 2)"
    assert c.negado_por is not None, "dor no peito deveria estar negado"
    g = gatilhos(texto)
    assert "sem" in g and "nenhuma" in g, f"gatilhos encontrados: {g}"


@teste("U4", "4.2, 5")
def u4():
    r = metodo("não tenho tontura, mas estou com dor de cabeça súbita")
    t = casamento(r, "tontura")
    assert t is not None and t.negado_por == "nao", f"tontura: {t and t.negado_por}"
    s = casamento(r, "dor de cabeça súbita")
    assert s is not None and s.negado_por is None, "dor de cabeça súbita não aceito"
    assert casamento(r, "dor de cabeça") is None, "dor de cabeça (Hipertensão) não deveria ser aceito"
    assert "Hipertensão" not in r["pontuacao"], f"pontuação: {r['pontuacao']}"


@teste("U5", "4.2 — `e` como fronteira")
def u5():
    r = metodo("não sinto palidez e estou com falta de ar")
    p = casamento(r, "palidez")
    assert p is not None and p.negado_por is not None, "palidez deveria estar negado"
    f = casamento(r, "falta de ar")
    assert f is not None and f.negado_por is None, "falta de ar não deveria estar negado"


@teste("U6", "6")
def u6():
    r = metodo("formigamento no braço esquerdo desde ontem")
    c = casamento(r, "braço esquerdo")
    assert c is not None and c.localizacao_descartada, "braço esquerdo deveria ser descartado"
    assert r["pontuacao"].get("Infarto", 0) == 0, f"pontuação: {r['pontuacao']}"


@teste("U7", "6")
def u7():
    r = metodo("uma dor forte que desce para o braço esquerdo")
    c = casamento(r, "braço esquerdo")
    assert c is not None and not c.localizacao_descartada, "braço esquerdo deveria contar"
    assert r["pontuacao"].get("Infarto") == 1, f"pontuação: {r['pontuacao']}"


@teste("U8", "6, 4.2")
def u8():
    r = metodo("não tenho dor, o braço esquerdo formiga")
    c = casamento(r, "braço esquerdo")
    assert c is not None and c.localizacao_descartada, "braço esquerdo deveria ser descartado"
    assert r["pontuacao"].get("Infarto", 0) == 0, f"pontuação: {r['pontuacao']}"


@teste("U9", "3.2")
def u9():
    c = casamento(metodo("um aperto bem forte sobre o tórax"), "aperto sobre o tórax")
    assert c is not None, "aperto sobre o tórax deveria casar (intervalo de 2)"


@teste("U10", "3.2")
def u10():
    c = casamento(metodo("um aperto que começou ontem à tarde sobre o tórax"), "aperto sobre o tórax")
    assert c is None, "aperto sobre o tórax não deveria casar (intervalo > 2)"


@teste("U11", "7.2")
def u11():
    r = metodo("fiquei tonto e com tontura o dia todo")
    assert r["pontuacao"].get("AVC") == 1, f"pontuação: {r['pontuacao']}"
    assert r["pontuacao"].get("Hipertensão") == 1, f"pontuação: {r['pontuacao']}"


@teste("U12", "7.1")
def u12():
    r = metodo("sinto sensação de peso")
    assert r["pontuacao"].get("Infarto") == 1, f"pontuação: {r['pontuacao']}"


@teste("U13", "2.4 — falso positivo declarado")
def u13():
    r = metodo("meus pais moram longe")
    c = casamento(r, "pálido")
    assert c is not None, "o over-stemming declarado (pais → pal) deveria aparecer"
    assert c.tokens_frase == "pais", f"tokens: {c.tokens_frase}"


@teste("U14", "10.1")
def u14():
    r = baseline("tive tonturas ontem")
    assert casamento(r, "tonturas") is not None, "baseline deveria casar tonturas"
    assert casamento(r, "tontura") is None, "baseline não deveria casar tontura"
    assert r["pontuacao"] == {"Hipertensão": 1}, f"pontuação: {r['pontuacao']}"


def main() -> int:
    falhas = 0
    for nome, regra, f in TESTES:
        try:
            f()
            print(f"[OK]    {nome:4} ({regra})")
        except AssertionError as erro:
            falhas += 1
            print(f"[FALHA] {nome:4} ({regra}): {erro}")
    print()
    print(f"{len(TESTES) - falhas}/{len(TESTES)} testes passaram.")
    if falhas:
        print("Há teste falhando: o extrator NÃO deve rodar nas frases.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
