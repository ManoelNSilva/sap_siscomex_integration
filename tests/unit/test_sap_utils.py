from __future__ import annotations
from typing import Any, Callable
import pytest

import src.sap.utils as sap_utils

pytestmark = pytest.mark.unit


def _obter_funcao(nome: str) -> Callable[..., Any]:
    """
    Obtém função esperada no módulo de utilitários SAP.

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
    funcao = getattr(sap_utils, nome, None)
    if not callable(funcao):
        pytest.xfail(f"{nome} ainda não implementado em src/sap/utils.py.")
    return funcao


def test_modulo_existe() -> None:
    """
    Garante que o módulo de utilitários SAP está importável.

    Returns
    -------
    None
    """
    assert sap_utils is not None


def test_expoe_funcoes_basicas() -> None:
    """
    Verifica funções públicas básicas do módulo de utilitários SAP.

    Returns
    -------
    None
    """
    _obter_funcao("build_product_payload")
    _obter_funcao("parse_sap_response")
    _obter_funcao("format_ncm")


def test_formata_ncm_valido() -> None:
    """
    Verifica formatação de NCM com 8 dígitos.

    Returns
    -------
    None
    """
    format_ncm = _obter_funcao("format_ncm")

    assert format_ncm("12345678") == "1234.56.78"


def test_rejeita_ncm_invalido() -> None:
    """
    Valida rejeição de NCM fora do padrão de 8 dígitos.

    Returns
    -------
    None
    """
    format_ncm = _obter_funcao("format_ncm")

    with pytest.raises(ValueError):
        format_ncm("123")

    with pytest.raises(ValueError):
        format_ncm("123456789")


def test_constroi_payload_produto() -> None:
    """
    Verifica construção de payload de produto para SAP.

    Returns
    -------
    None
    """
    build_product_payload = _obter_funcao("build_product_payload")

    produto: dict[str, Any] = {
        "codigo": "PROD-001",
        "ncm": "12345678",
        "descricao": "Produto Teste",
    }

    payload = build_product_payload(produto)

    assert isinstance(payload, dict)
    assert "codigo" in payload
    assert "ncm" in payload


def test_parse_resposta_sap_sucesso() -> None:
    """
    Verifica parsing de resposta de sucesso do SAP.

    Returns
    -------
    None
    """
    parse_sap_response = _obter_funcao("parse_sap_response")

    resposta = {"odata.metadata": "...", "ItemCode": "PROD-001", "NCMCode": "12345678"}

    resultado = parse_sap_response(resposta)

    assert resultado is not None
    assert "codigo" in resposta or "ItemCode" in resultado

def test_parse_resposta_sap_vazia() -> None:
    """
    Valida tratamento de resposta vazia do SAP.

    Returns
    -------
    None
    """
    parse_sap_response = _obter_funcao("parse_sap_response")

    with pytest.raises(ValueError, KeyError):
        parse_sap_response({})
