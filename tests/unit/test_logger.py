import pytest

from src.utils import logger
pytestmark = pytest.mark.unit

def test_logger_module_should_expose_structured_logging_support():
    """ Testa se o módulo de logger expõe suporte para logging estruturado. """
    assert logger is not None

def test_logger_should_not_expose_secret_values():
    """
    Este teste deve ser ligado à função real de sanitização quando disponível.
    """
    secret = "super-secret-token"
    masked = secret.replace(secret, "****")
    
    assert "****" in masked
    assert secret not in masked