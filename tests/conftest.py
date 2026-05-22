from dataclasses import dataclass
from typing import Any

import pytest


@dataclass
class FakeResponse:
    status_code: int = 200
    json_data: dict[str, Any] | list[Any] | None = None
    text: str = ""
    headers: dict[str, str] | None = None

    def json(self) -> dict[str, Any] | list[Any]:
        return self.json_data or {}


@pytest.fixture
def correlation_id() -> str:
    return "11111111-1111-1111-1111-111111111111"


@pytest.fixture
def sample_ncm() -> str:
    return "12345678"


@pytest.fixture
def sample_required_attributes() -> list[dict[str, Any]]:
    return [
        {
            "codigo_atributo": "ATTR_001",
            "nome": "Atributo Booleano",
            "tipo": "BOOLEANO",
            "obrigatorio": True,
        },
        {
            "codigo_atributo": "ATTR_002",
            "nome": "Atributo Texto",
            "tipo": "TEXTO",
            "obrigatorio": True,
        },
    ]


@pytest.fixture
def sample_product_payload() -> dict[str, Any]:
    return {
        "codigo": "PROD-001",
        "ncm": "12345678",
        "descricao": "Produto de Teste",
        "atributos": [
            {"codigo_atributo": "ATTR_001", "valor": True},
            {"codigo_atributo": "ATTR_002", "valor": "ABC"},
        ],
    }


@pytest.fixture
def siscomex_success_response() -> FakeResponse:
    return FakeResponse(
        status_code=201,
        json_data={
            "status_http": 201,
            "mensagem": "Operação realizada com sucesso",
            "sequencial": "12345",
            "payload_resumo": {},
        },
    )


@pytest.fixture
def siscomex_error_response() -> FakeResponse:
    return FakeResponse(
        status_code=422,
        json_data={
            "status_http": 422,
            "mensagem": "Falha de validação",
            "codigo_erro_externo": "VALIDATION_ERROR",
        },
    )
