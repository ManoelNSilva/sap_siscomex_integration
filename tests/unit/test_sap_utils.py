import pytest

import src.sap.utils as sap_utils 

pytestmark = pytest.mark.unit

def test_sap_utils_module_should_exist():
    """
    Testa se o módulo de utilitários SAP existe.
    """
    assert sap_utils is not None