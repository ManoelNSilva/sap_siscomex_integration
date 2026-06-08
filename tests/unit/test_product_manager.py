from __future__ import annotations
from typing import Any, Callable
import pytest
import src.core.product_manager as product_manager

pytestmark = pytest.mark.unit


def _obter_funcao(nome: str) -> Callable[..., Any]:
    """
    Obtém função do módulo `product_manager` para contrato TDD.

    Parameters
    ----------
    nome: str
        Nome da função esperada no módulo.

    Returns
    -------
    Callable[..., Any]
        Referência chamável para a função solicitada.

    Notes
    -----
    - Se a função não existir, marca o teste como xfail
    para manter o fluxo TDD sem falso positivo.
    """
    fn = getattr(product_manager, nome, None)
    if not callable(fn):
        pytest.xfail(f"{nome} ainda não implementado em src/core/product_manager.py.")
    return fn


def test_modulo_existe() -> None:
    """
    Garante que o módulo `product_manager` está importável.

    Returns
    -------
    None
    """
    assert product_manager is not None


def test_regras_condicionais_basicas() -> None:
    """
    Valida resolução de regra condicional simples.

    Contrato esperado:
    - Função: `resolve_conditional_rules`
    - Entrada: lista de regras + contexto de valores
    - Saída: lista de atributos obrigatórios resultantes

    Returns
    -------
    None
    """
    resolve_conditional_rules = _obter_funcao("resolve_conditional_rules")

    rules = [
        {
            "if": {"atributo": "usa_lote", "operador": "==", "valor": True},
            "then": {"atributo_obrigatorio": "numero_lote"},
        }
    ]
    contexto = {"usa_lote": True}

    resultado = resolve_conditional_rules(rules, contexto)
    assert "numero_lote" in resultado


def test_status_integracao_sucesso():
    """
    Valida transição de status para sucesso.

    Contrato esperado:
    - Função: `set_integration_status`
    - Entrada: status atual + evento
    - Saída: novo status

    Returns
    -------
    None
    """
    set_integration_status = _obter_funcao("set_integration_status")

    novo_status = set_integration_status(status_atual="PENDENTE", evento="ENVIO_OK")
    assert novo_status == "INTEGRADO"


def test_status_integracao_falha() -> None:
    """
    Valida transição de status para falha.

    Returns
    -------
    None
    """
    set_integration_status = _obter_funcao("set_integration_status")

    novo_status = set_integration_status(status_atual="PENDENTE", evento="ENVIO_ERRO")
    assert novo_status == "ERRO"


def test_idempotencia_mesmo_payload():
    """
    Garante chave idempotente estável para mesmo payload.

    Contrato esperado:
    - Função: `build_idempotency_key`
    - Entrada: payload (dict)
    - Saída: chave determinística (str)

    Returns
    -------
    None
    """
    build_idempotency_key = _obter_funcao("build_idempotency_key")

    payload = {"codigo": "PROD-001", "ncm": "12345678", "versao": 1}
    key1 = build_idempotency_key(payload)
    key2 = build_idempotency_key(payload)

    assert isinstance(key1, str)
    assert key1 == key2


def test_idempotencia_payload_diferente():
    """
    Garante chave idempotente diferente para payloads distintos.

    Returns
    -------
    None
    """
    build_idempotency_key = _obter_funcao("build_idempotency_key")

    payload_a = {"codigo": "PROD-001", "ncm": "12345678", "versao": 1}
    payload_b = {"codigo": "PROD-001", "ncm": "12345678", "versao": 2}

    key_a = build_idempotency_key(payload_a)
    key_b = build_idempotency_key(payload_b)

    assert key_a != key_b
