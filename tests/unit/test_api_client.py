import pytest
from src.siscomex.api_client import TSISCOMEXClient

pytestmark = pytest.mark.unit


def test_module_contract_should_expose_expected_client_methods():
    """
    Contrato mínimo esperado pelo SRS/documentação técnica.
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


def test_client_should_be_able_to_instantiated_with_configuration():
    """
    O cliente deve ser instanciável com a configuração mínima necessária.
    """
    client = TSISCOMEXClient(
        base_url="https://portalunico.siscomex.gov.br/catp",
        timeout=(5, 30),
    )

    assert client is not None
