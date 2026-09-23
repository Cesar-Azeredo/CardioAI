"""Adendo aos testes de unidade do extrator — ADICIONADO APOS A EXECUCAO UNICA.

U15 nao faz parte da bateria pre-registrada (U1-U14, tabela 10.6 do protocolo
congelado, que nao foi descongelado). Ele fecha uma lacuna de COBERTURA achada
pela checagem de mutacao (scripts/fase-02/05_checa_mutacao_testes.py): com a
regra 4.3 removida ("marcador consumido por termo casado tambem vira
gatilho"), nenhum dos 14 testes falhava, porque em U1 e U2 o `sem` e a
primeira palavra do proprio termo e nao negaria o termo de qualquer jeito.

U15 nao altera regra, codigo do extrator nem resultado: so testa a regra 4.3
num caso em que ela faz diferença — o `sem` de "sem fôlego" negaria OUTRO
termo da mesma oração se contasse como gatilho. Registro em
document/fase-02/adendo-pos-execucao.md.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("testes_pre_registrados", AQUI / "03_testa_extrator.py")
base = importlib.util.module_from_spec(_spec)
sys.modules["testes_pre_registrados"] = base
_spec.loader.exec_module(base)

TESTES_ADENDO = []


def teste(nome, regra):
    def registrar(f):
        TESTES_ADENDO.append((nome, regra, f))
        return f
    return registrar


@teste("U15", "4.3 — adicionado após a execução única")
def u15():
    r = base.metodo("fiquei sem fôlego com tontura")
    sem_folego = base.casamento(r, "sem fôlego")
    assert sem_folego is not None and sem_folego.negado_por is None, "sem fôlego deveria casar sem negação"
    tontura = base.casamento(r, "tontura")
    assert tontura is not None, "tontura não casou"
    assert tontura.negado_por is None, f"tontura negada por '{tontura.negado_por}' — o `sem` consumido virou gatilho"


def main() -> int:
    falhas = 0
    for nome, regra, f in TESTES_ADENDO:
        try:
            f()
            print(f"[OK]    {nome:4} ({regra})")
        except AssertionError as erro:
            falhas += 1
            print(f"[FALHA] {nome:4} ({regra}): {erro}")
    print(f"\n{len(TESTES_ADENDO) - falhas}/{len(TESTES_ADENDO)} teste(s) do adendo passaram.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
