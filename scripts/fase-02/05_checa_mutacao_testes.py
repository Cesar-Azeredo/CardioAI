"""Checagem de mutacao dos testes do extrator — Fase 2.

Pergunta que este script responde: os testes (U1-U14 pre-registrados + U15 do
adendo) conseguem FALHAR? Para cada regra do protocolo, aplica uma mutacao em
memoria (nenhum arquivo e alterado), roda todos os testes e lista quais
falharam. Mutacao que nenhum teste pega = lacuna de cobertura.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def carregar(nome, arquivo):
    spec = importlib.util.spec_from_file_location(nome, AQUI / arquivo)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome] = mod
    spec.loader.exec_module(mod)
    return mod


adendo = carregar("testes_adendo", "04_testa_extrator_adendo.py")
base = adendo.base
ext = base.ext
TESTES = base.TESTES + adendo.TESTES_ADENDO


def falhando() -> list[str]:
    base.MAPA = ext.carregar_mapa(base.NORM)
    nomes = []
    for nome, _, f in TESTES:
        try:
            f()
        except AssertionError:
            nomes.append(nome)
    return nomes


def gatilhos_sem_regra_43(oracao, consumidos):
    return [(i, t.forma) for i, t in enumerate(oracao) if t.forma in ext.NEGADORES]


MUTACOES = [
    ("janela = 1 (protocolo: 2)", "INTERVALO_MAXIMO", 1),
    ("janela = 5 (protocolo: 2)", "INTERVALO_MAXIMO", 5),
    ("`e` deixa de ser fronteira (4.2)", "PALAVRAS_FRONTEIRA", ext.PALAVRAS_FRONTEIRA - {"e"}),
    ("marcador consumido também vira gatilho (sem a regra 4.3)", "gatilhos_nao_consumidos", gatilhos_sem_regra_43),
    ("sem regra de localização (6)", "TERMOS_DE_LOCALIZACAO", []),
]


def main() -> int:
    sem_mutacao = falhando()
    print(f"Testes: {', '.join(n for n, _, _ in TESTES)}")
    print(f"sem mutação — falham: {sem_mutacao or 'nenhum'}\n")
    escaparam = 0
    for descricao, atributo, valor in MUTACOES:
        original = getattr(ext, atributo)
        setattr(ext, atributo, valor)
        try:
            pegos = falhando()
        finally:
            setattr(ext, atributo, original)
        if not pegos:
            escaparam += 1
        print(f"{descricao:60} → {'pega por ' + ', '.join(pegos) if pegos else 'NENHUM teste falha (lacuna)'}")
    base.MAPA = ext.carregar_mapa(base.NORM)
    print(f"\n{len(MUTACOES) - escaparam}/{len(MUTACOES)} mutações pegas.")
    return 1 if (sem_mutacao or escaparam) else 0


if __name__ == "__main__":
    sys.exit(main())
