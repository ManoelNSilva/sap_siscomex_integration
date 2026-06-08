from __future__ import annotations
from typing import Any, Callable
import pytest

import src.utils.logger as logger_mod

pytestmark = pytest.mark.unit


def _obter_funcao(nome: str) -> Callable[..., Any]:
    """
    Obtém função esperada no módulo de logger.

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
    funcao = getattr(logger_mod, nome, None)
    if not callable(funcao):
        pytest.xfail(f"{nome} ainda não implementado em src/utils/logger.py.")
    return funcao


def test_modulo_existe():
    """
    Garante que o módulo de logger está importável.

    Returns
    -------
    None
    """
    assert logger_mod is not None


def test_expoe_funcoes_basicas():
    """
    Verifica funções públicas básicas do logger.

    Returns
    -------
    None
    """
    _obter_funcao("get_logger")
    _obter_funcao("sanitize_payload")
    _obter_funcao("log_event")


def test_sanitiza_dados_sensiveis() -> None:
    """
    Valida a função de sanitização de dados sensíveis.

    Returns
    -------
    None
    """
    sanitize_payload = _obter_funcao("sanitize_payload")

    payload = {
        "username": "user_a",
        "password": "123456",
        "token": "abc.def.ghi",
        "client_secret": "segredo",
    }

    resultado = sanitize_payload(payload)

    assert resultado["username"] == "user_a"
    assert resultado["password"] != "123456"
    assert resultado["token"] != "abc.def.ghi"
    assert resultado["client_secret"] != "segredo"


def test_log_event_fail_safe():
    """
    Garante que log falho não interrompe o fluxo (fall-safe).

    Returns
    -------
    None
    """
    log_event = _obter_funcao("log_event")

    try:
        log_event("test_evento", {"chave": "valor"})
    except Exception as exc:
        pytest.fail(f"log_event não deve quebrar fluxo: {exc}")
