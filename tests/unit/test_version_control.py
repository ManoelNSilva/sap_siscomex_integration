import pytest

from src.core.version_control import TVersioncontrol


pytestmark = pytest.mark.unit

def test_version_control_module_should_exist():
    """
    Testa se o módulo de controle de versão existe.
    """
    assert TVersioncontrol is not None