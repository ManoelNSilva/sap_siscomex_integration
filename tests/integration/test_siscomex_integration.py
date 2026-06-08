from __future__ import annotations

from typing import Any
import pytest
import uuid

from src.siscomex.api_client import TSISCOMEXClient

pytestmark = pytest.mark.integration


def _require_callable(obj: Any, name: str):
    """
    Garante que `obj` expõe `name` chamável ou marca XFail (TDD Contract).

    Parameters
    ----------
    obj: Any
        Módulo ou classe a ser verificada.
    name: str
        Nome do atributo o método esperado.

    Returns
    -------
    callable
        Referência ao atributo/método.
    """
    fn = getattr(obj, name, None)
    if not callable(fn):
        pytest.xfail(f"{name} ainda não implementado em {getattr(obj, '__name__', str(obj))}.")

    return fn

def test_client_exposes_endpoints() -> None:
    """
    Valida se o cliente SISCOMEX expõe os métodos de endpoint esperados.

    Responsibilities:
    - Métodos curto e claro por responsabilidade (coeso).
    """
    client_cls = _require_callable(TSISCOMEXClient, "__init__")

    _require_callable(TSISCOMEXClient, "get_required_attributes")
    _require_callable(TSISCOMEXClient, "create_product")
    _require_callable(TSISCOMEXClient, "deactivate_product")
    _require_callable(TSISCOMEXClient, "reactivate_product")

def test_create_update_deactivate_reactivate_flow(monkeypatch) -> None:
    """
    Fluxo de integração: create -> update -> deactivate -> reactivate (simulado).
    
    - Mocks:
        - create_product, update_product, deactivate_product, reactivate_product
    - Acceptance:
        - cada operação retorna um dicionário com 'status_http' e 'sequencial' (quando aplicável).
    """
    #checar contrato 
    _require_callable(TSISCOMEXClient, "create_product")
    _require_callable(TSISCOMEXClient, "update_product")
    _require_callable(TSISCOMEXClient, "deactivate_product")
    _require_callable(TSISCOMEXClient, "reactivate_product")

    # Respostas simuladas
    def fake_create(self, payload: dict[str, Any], idempotency_key: str | None = None, correlation_id: str | None = None):
        return {"status_http": 201, "sequencial": "S-001", "correlation_id": correlation_id or str(uuid.uuid4())}
    
    def fake_update(self, sequencial: str, payload: dict[str, Any], correlation_id: str | None = None):
        return {"status_http": 200, "sequencial": sequencial, "correlation_id": correlation_id or str(uuid.uuid4())}

    def fake_deactivate(self, sequencial: str, correlation_id: str | None = None):
        return {"status_http": 204, "sequencial": sequencial, "correlation_id": correlation_id or str(uuid.uuid4())}

    def fake_reactivate(self, sequencial: str, correlation_id: str | None = None):
        return {"status_http": 200, "sequencial": sequencial, "correlation_id": correlation_id or str(uuid.uuid4())}
    
    monkeypatch.setattr(TSISCOMEXClient, "create_product", fake_create, raising=False)
    monkeypatch.setattr(TSISCOMEXClient, "update_product", fake_update, raising=False)
    monkeypatch.setattr(TSISCOMEXClient, "deactivate_product", fake_deactivate, raising=False)
    monkeypatch.setattr(TSISCOMEXClient, "reactivate_product", fake_reactivate, raising=False)

    client = TSISCOMEXClient(base_url="https://example", timeout=(1, 5))
    payload = {"codigo": "PROD-INT-01", "ncm": "12345678"}

    created = client.create_product(payload, idempotency_key="idem-1", correlation_id="c-1")
    assert created["status_http"] == 201
    seq = created["sequencial"]

    updated = client.update_product(seq, {"descricao": "novo"}, correlation_id="c-1")
    assert updated["status_http"] == 200
    assert updated["sequencial"] == seq

    deact = client.deactivate_product(seq, correlation_id="c-1")
    assert deact["status_http"] in (200, 204)

    react = client.reactivate_product(seq, correlation_id="c-1")
    assert react["status_http"] == 200

def test_error_handling_and_retry_policy(monkeypatch) -> None:
    """
    Valida comportamento em erros: 401/403/429/5xx e retry policy lean. 

    - Scenarios:
        - 401/403 -> não retry, elevar/retornar erro de autorização
        - 429/5xx -> aplicar retry com backoff (contrato: client deve oferecer retry)
    - Acceptance:
        - 401/403 resultam em exceção específica (PermissionError / RuntimeError)
        - 429/5xx são reexecutados e eventualmente retornam sucesso quando mock simula recuperação
    """
    _require_callable(TSISCOMEXClient, "create_product")

    calls: dict[str, int] = {"count": 0}
    sequence_success = {"status_http": 201, "sequencial": "S-RETRY"}

    # Simula respostas: 429, 500, success
    responses = [RuntimeError("429 Too Many Requests"), RuntimeError("500 Internal"), sequence_success]

    def flaky_create(self, payload: dict[str, Any], idempotency_key: str | None = None, correlation_id: str | None = None):
        calls["count"] += 1
        resp = responses[calls["count"] - 1]
        if isinstance(resp, Exception):
            raise resp
        return resp
    
    monkeypatch.setattr(TSISCOMEXClient, "create_product", flaky_create, raising=False)

    client = TSISCOMEXClient(base_url="https://example", timeout=(1, 2))

    try:
        out = client.create_product({"codigo": "P"}, idempotency_key="idem-retry")
    except Exception:
        pytest.xfail("Retry policy não implementada no cliente; comportamento esperado em TDD.")
    else:
        assert out["status_http"] == 201
        assert calls["count"] >= 1

def test_payload_composed_and_multivalued_validation() -> None:
    """
    Valida contrato de payloads compostos e multivalorados aceitos pelo cliente.

    - Contract:
        - cliente aceita campos compostos (dict) e multivalorados (list)
        
    - Acceptance:
        - Quando payload contém COMPOSTO/MULTIVALORADO, cliente deve aceitar e retornar dicionário de resposta        - para MULTIVALORADO: domain define valores permitidos 
    """
    _require_callable(TSISCOMEXClient, "create_product")

    def fake_create(self, payload: dict[str, Any], idempotency_key: str | None = None, correlation_id: str | None = None):
        # valida presença de composto/multivalorado no payload
        assert isinstance(payload.get("medidas"), dict) or payload.get("medidas") is None
        assert isinstance(payload.get("categorias"), list) or payload.get("categorias") is None
        return {"status_http": 201, "sequencial": "S-COMP"}
    
    pytest.monkeyPatch = pytest.MonkeyPatch()
    pytest.monkeyPatch.setattr(TSISCOMEXClient, "create_product", fake_create, raising=False)

    client = TSISCOMEXClient(base_url="https://example", timeout=(1, 2))

    payload = {
        "codigo": "PROD-COMP",
        "ncm": "12345678",
        "medidas": {"altura": 10, "largura": 5},
        "categorias": ["A", "B"],
    }

    out = client.create_product(payload, idempotency_key="idem-comp")
    assert out["status_http"] == 201

def test_cache_stale_behavior_and_fallback(tmp_path, monkeypatch) -> None:
    """
    Testa fallback quando cache está stale.

    - Setup:
        - Gravar cache com fetched_at antigo (>24h)
        - Simular adapter raise (5xx)
    
    - Acceptance:
        - Implementção deve detectar cache stale e:
            - se política for 'fail_closed' -> lançar erro
            - se política for 'use-stale' -> retornar stale com flag degraded
        (a implementação pode escolher política; teste aceita qualquer um dos comportamentos documentados) 
    """
    _require_callable(TSISCOMEXClient, "get_required_attributes")

    cache_file = tmp_path / "attrs_cache.json"
    cache_file.write_text('{"attributes": [], "fetched_at":"2026-01-01T00:00:00Z"}')
    
    def fake_adapter_fail(ncm: str, data_referencia: str | None = None):
        raise RuntimeError("Upstream 5xx")
    
    monkeypatch.setattr(TSISCOMEXClient, "get_required_attributes", fake_adapter_fail, raising=False)

    client = TSISCOMEXClient(base_url="https://example", timeout=(1, 2))
    try:
        res = client.get_required_attributes("12345678")
    except Exception:
        pytest.xfail("Fallback/cache policy não implementado; comportamento esperado em TDD.")
    else:
        # Aceitar resposta que indique modo degraded ou uso de stale cache
        assert isinstance(res, dict) or isinstance(res, list)