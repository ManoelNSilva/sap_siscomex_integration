import pytest

from src.sap.service_layer import TSAPServiceLayer

pytestmark = pytest.mark.integration


def test_sap_service_layer_integration_contract():
    """
    Testa a integração com o SAP Service Layer, verificando se a instância é criada corretamente.
    """
    service = TSAPServiceLayer()

    assert service is not None
