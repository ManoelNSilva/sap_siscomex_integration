from __future__ import annotations
from typing import Any
import pytest
import src.siscomex.utils as siscomex_utils

pytestmark = pytest.mark.unit


def _require_callable(name: str):
    """
    Helper para garantir que uma função existe e é chamável, ou falhar o teste com mensagem clara.

    :param name: Nome da função a ser verificada.
    :return: A função se ela existir e for chamável.
    """
    fn = getattr(siscomex_utils, name, None)
    if not callable(fn):
        pytest.xfail(f"{name} ainda não implementado em src/siscomex/utils.py.")
    return fn


def test_siscomex_utils_module_should_exist():
    """
    Testa se o módulo de utilitários Siscomex existe.
    """
    assert siscomex_utils is not None


def test_module_should_expose_attribute_type_normalizer():
    """
    Contrato mínimo esperado pelo SRS/documentação técnica.
    """
    normalize_attribute_type = _require_callable("normalize_attribute_type")

    assert normalize_attribute_type("booleano") == "BOOLEANO"
    assert normalize_attribute_type("lista_estatica") == "LISTA_ESTATICA"
    assert normalize_attribute_type("texto") == "TEXTO"
    assert normalize_attribute_type("numero_inteiro") == "NUMERO_INTEIRO"
    assert normalize_attribute_type("numero_real") == "NUMERO_REAL"
    assert normalize_attribute_type("data") == "DATA"
    assert normalize_attribute_type("composto") == "COMPOSTO"
    assert normalize_attribute_type("MULTIVALORADO") == "MULTIVALORADO"


def test_module_should_identify_supported_attribute_types():
    """
    Contrato mínimo esperado pelo SRS/documentação técnica.
    """
    is_supported_attribute_type = _require_callable("is_supported_attribute_type")

    assert is_supported_attribute_type("BOOLEANO") is True
    assert is_supported_attribute_type("LISTA_ESTATICA") is True
    assert is_supported_attribute_type("TEXTO") is True
    assert is_supported_attribute_type("NUMERO_INTEIRO") is True
    assert is_supported_attribute_type("NUMERO_REAL") is True
    assert is_supported_attribute_type("DATA") is True
    assert is_supported_attribute_type("COMPOSTO") is True
    assert is_supported_attribute_type("MULTIVALORADO") is True
    assert is_supported_attribute_type("TIPO_INEXISTENTE") is False


def test_module_should_validate_boolean_attribute_value():
    """
    Contrato mínimo esperado pelo SRS/documentação técnica.
    """
    validate_attribute_value = _require_callable("validate_attribute_value")

    assert validate_attribute_value("BOOLEANO", True) is True
    assert validate_attribute_value("BOOLEANO", False) is True

    with pytest.raises((ValueError, TypeError)):
        validate_attribute_value("BOOLEANO", "sim")


def test_module_should_validate_list_attribute_value():
    """
    Contrato mínimo esperado pelo SRS/documentação técnica.
    """
    validate_attribute_value = _require_callable("validate_attribute_value")

    assert validate_attribute_value("LISTA_ESTATICA", "A", domain=["A", "B"]) is True

    with pytest.raises((ValueError, TypeError)):
        validate_attribute_value("LISTA_ESTATICA", "C", domain=["A", "B"])


def test_module_should_validate_text_numeric_and_date_values():
    """
    Contrato mínimo esperado pelo SRS/documentação técnica.
    """

    validate_attribute_value = _require_callable("validate_attribute_value")

    assert validate_attribute_value("TEXTO", "ABC", max_length=10) is True
    assert validate_attribute_value("NUMERO_INTEIRO", 10) is True
    assert validate_attribute_value("NUMERO_REAL", 10.15) is True
    assert validate_attribute_value("DATA", "2024-06-01") is True


def test_module_should_validate_composite_and_multivalued_attributes():
    """
    Contrato mínimo esperado pelo SRS/documentação técnica.
    """
    validate_attribute_value = _require_callable("validate_attribute_value")

    assert (
        validate_attribute_value(
            "COMPOSTO",
            {"ATTR_1": "X", "ATTR_2": 1},
            schema={"ATTR_1": "TEXTO", "ATTR_2": "NUMERO_INTEIRO"},
        )
        is True
    )

    assert (
        validate_attribute_value(
            "MULTIVALORADO",
            ["A", "B", "C"],
            domain=["A", "B", "C", "D"],
        )
        is True
    )


def test_module_should_resolve_conditional_attributes():
    """
    Contrato mínimo esperado pelo SRS/documentação técnica.
    """
    resolve_conditional_attributes = _require_callable("resolve_conditional_attributes")

    base_attributes: list[dict[str, Any]] = [
        {"codigo_atributo": "ATTR_BASE", "obrigatorio": True},
        {
            "codigo_atributo": "ATTR_COND",
            "obrigatorio": False,
            "condicoes": [
                {
                    "atributo_origem": "ATTR_BASE",
                    "operador": "==",
                    "valor": "SIM",
                }
            ],
        },
    ]
    values = {"ATTR_BASE": "SIM"}

    resolved = resolve_conditional_attributes(base_attributes, values)

    assert resolved is not None
