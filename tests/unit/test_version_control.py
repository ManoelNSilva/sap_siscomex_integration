from __future__ import annotations
from typing import Any, Callable
import pytest

import src.core.version_control as version_control

pytestmark = pytest.mark.unit


def _obter_modulo(nome: str) -> Callable[..., Any]:
    """
    Obtém função esperada no módulo de controle de versão.

    Parameters
    ----------
    nome: str
        Nome da função esperada.

    Returns
    -------
    Callable[..., Any]
        Função encontrada no módulo.

    Notes
    -----
    Se a função não existir, marca como xfail para manter o fluxo TDD sem falso positivo.
    """
    funcao = getattr(version_control, nome, None)
    if not callable(funcao):
        pytest.xfail(f"{nome} ainda não implementado em src/core/version_control.py.")
    return funcao


def test_modulo_existe() -> None:
    """
    Garante que o módulo de controle de versão está importável.

    Returns
    -------
    None
    """
    assert version_control is not None


def test_expoe_funcoes_basicas() -> None:
    """
    Verifica se o módulo de controle de versão expõe as funções básicas esperadas.

    Returns
    -------
    None
    """
    _obter_modulo("bump_version")
    _obter_modulo("next_sequence")


def test_incrementa_versao_major():
    """
    Valida incremento de versão major.

    Returns
    -------
    None
    """
    bump_version = _obter_modulo("bump_version")
    assert bump_version("1.2.3", "major") == "2.0.0"


def test_incrementa_versao_minor():
    """
    Valida incremento de versão minor.

    Returns
    -------
    None
    """
    bump_version = _obter_modulo("bump_version")
    assert bump_version("1.2.3", "minor") == "1.3.0"


def test_incrementa_versao_patch():
    """
    Valida incremento de versão patch.

    Returns
    -------
    None
    """
    bump_version = _obter_modulo("bump_version")
    assert bump_version("1.2.3", "patch") == "1.2.4"


def test_incrementa_sequencia():
    """
    Valida incremento de sequência numérica.

    Returns
    -------
    None
    """
    next_sequence = _obter_modulo("next_sequence")
    assert next_sequence(10) == 11


def test_rejeita_versao_invalida():
    """
    Valida rejeição de versão fora do padrão esperado.

    Returns
    -------
    None
    """
    bump_version = _obter_modulo("bump_version")
    with pytest.raises(ValueError):
        bump_version("1.2", "major")
