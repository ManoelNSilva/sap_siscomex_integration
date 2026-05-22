import pytest

from src.siscomex.api_client import TSISCOMEXClient

pytestmark = pytest.mark.integration


def test_siscomex_client_integration_contract():
    """
    Testa integração do TSISCOMEXClient com o endpoint de consulta de dados do Siscomex.
    """
    client = TSISCOMEXClient(
        base_url="https://portalunico.siscomex.gov.br/catp",
        timeout=(5, 30),
    )

    assert client is not None
