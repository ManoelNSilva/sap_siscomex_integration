import pytest

from src.core.product_manager import TProductManager

pytestmark = pytest.mark.unit


def test_product_manager_module_should_exist():
    """
    Testa se o módulo de gerenciamento de produtos existe.
    """
    assert TProductManager is not None
