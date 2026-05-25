import pytest

from src.sap.service_layer import TSAPServiceLayer

pytestmark = pytest.mark.unit


def test_sap_service_layer_should_expose_basic_contract():
    """
    Testa se o módulo de camada de serviço SAP existe.
    """
    assert TSAPServiceLayer is not None
