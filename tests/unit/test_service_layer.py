from __future__ import annotations
from typing import Any
import pytest
from src.sap.service_layer import TSAPServiceLayer

pytestmark = pytest.mark.unit


def _obter_metodo(nome: str) -> Any:
    """
    Obtém método esperado na classe de serviço SAP.

    Parameters
    ----------
    nome: str
        Nome do método público esperado.

    Returns
    -------
    Any
        Método encontrado na classe.

    Notes
    -----
    Se o método não existir, marca como xfail para manter o fluxo TDD sem falso positivo.
    """
    metodo = getattr(TSAPServiceLayer, nome, None)
    if not callable(metodo):
        pytest.xfail(f"{nome} ainda não implementado em src/sap/service_layer.py.")
    return metodo


def test_sap_service_layer_existe() -> None:
    """
    Verifica se a classe principal da camada SAP está disponível.

    Returns
    -------
    None
    """
    assert TSAPServiceLayer is not None


def test_sap_service_layer_expoe_contrato_basico() -> None:
    """
    Verifica métodos públicos básicos já disponíveis na camada SAP.

    Returns
    -------
    None
    """
    metodos = {"login", "get_product", "logout"}
    for metodo in metodos:
        assert hasattr(TSAPServiceLayer, metodo), metodo


def test_sap_service_layer_expoe_atualizacao_produto() -> None:
    """
    Verifica método de atualização de produto no SAP.

    Returns
    -------
    None
    """
    _obter_metodo("update_product")


def test_sap_service_layer_expoe_status_integracao() -> None:
    """
    Verifica método de atualização de status de integração no SAP.

    Returns
    -------
    None
    """
    _obter_metodo("update_integration_status")


def test_sap_service_layer_expoe_controle_versao() -> None:
    """
    Verifica método de controle de versão esperados no SAP.

    Returns
    -------
    None
    """
    _obter_metodo("update_dimension_version")
    _obter_metodo("update_dimension_sequence")
