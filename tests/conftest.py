from __future__ import annotations 

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable
import sys
import pytest

try:
    from requests import exceptions as requests_exceptions
except ImportError:
    requests_exceptions = None  # type: ignore[assignment]

# Garante import absoluto de "src.*" em execução local/CI sem instalação do pacote.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

class FakeHTTPError(Exception):
    def __init__(self, message: str, response: "FakeResponse") -> None:
        super().__init__(message)
        self.response = response

@dataclass(slots=True)
class FakeResponse:
    status_code: int = 200
    json_data: dict[str, Any] | list[Any] | None = None
    text: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    reason: str = "OK"
    url: str = "https://portalunico.siscomex.gov.br/catp/api"

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 400

    def json(self) -> dict[str, Any] | list[Any]:
        if self.json_data is None:
            raise ValueError("Response does not contain JSON content.")
        return self.json_data
    
    def raise_for_status(self) -> None:
        if not self.ok:
            raise FakeHTTPError(
                f"{self.status_code} {self.reason} for url: {self.url}", response = self)


@pytest.fixture
def correlation_id() -> str:
    return "11111111-1111-1111-1111-111111111111"

@pytest.fixture
def idempotency_key() -> str:
    return "idem-22222222-2222-2222-2222-222222222222"

@pytest.fixture
def request_headers(correlation_id: str, idempotency_key: str) -> dict[str, str]:
    return {
        "X-Correlation-ID": correlation_id,
        "X-Idempotency-Key": idempotency_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

@pytest.fixture
def sample_ncm() -> str:
    return "12345678"


@pytest.fixture
def sample_required_attributes() -> list[dict[str, Any]]:
    return [
        {
            "codigo_atributo": "ATTR_BOOL",
            "nome": "Atributo Booleano",
            "tipo": "BOOLEANO",
            "obrigatorio": True,
        },
        {
            "codigo_atributo": "ATTR_TXT",
            "nome": "Atributo Texto",
            "tipo": "TEXTO",
            "obrigatorio": True,
        },
        {
            "codigo_atributo": "ATTR_COMP",
            "nome": "Atributo Composto",
            "tipo": "COMPOSTO",
            "obrigatorio": False,
            "subatributos": [
                {"codigo_atributo": "ATTR_COMP_1", "tipo": "INTEIRO", "obrigatorio": True},
                {"codigo_atributo": "ATTR_COMP_2", "tipo": "TEXTO", "obrigatorio": False},
            ],
        },
        {
            "codigo_atributo": "ATTR_MULTI",
            "nome": "Atributo Multivalorado",
            "tipo": "MULTIVALORADO",
            "obrigatorio": False,
        },


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
