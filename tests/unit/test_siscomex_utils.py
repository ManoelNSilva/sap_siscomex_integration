import pytest

import src.siscomex.utils as siscomex_utils

pytestmark = pytest.mark.unit

def test_siscomex_utils_module_should_exist():
    """
    Testa se o módulo de utilitários Siscomex existe.
    """
    assert siscomex_utils is not None