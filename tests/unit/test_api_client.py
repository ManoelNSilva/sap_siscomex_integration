from __future__ import annotations
import pytest
from src.siscomex.api_client import TSISCOMEXClient

pytestmark = pytest.mark.unit


def test_cliente_expoe_metodos_esperados():
    """
    Verifica se o cliente SISCOMEX expõe os métodos públicos esperados

    Returns:
    --------
    None
    """
    expected_methods = {
        "get_required_attributes",
        "create_product",
        "update_product",
        "deactivate_product",
        "reactivate_product",
    }

    for method_name in expected_methods:
        assert hasattr(TSISCOMEXClient, method_name), method_name


def test_cliente_instancia_com_configuracao_minima() -> None:
    """
    Verifica se o cliente pode ser instanciado com a configuração mínima necessária.

    Returns:
    --------
    None
    """
    client = TSISCOMEXClient(
        base_url="https://portalunico.siscomex.gov.br/catp",
        timeout=(5, 30),
    )

    assert client is not None
