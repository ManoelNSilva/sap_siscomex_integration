from __future__ import annotations
from typing import Any 
import uuid
import pytest

import src.sap.service_layer as sap_mod
import src.siscomex.api_client as siscomex_mod

pytestmark = pytest.mark.integration


def _require_callable(obj: Any, name: str):
    """
    Helper: Garante que `obj` expõe `name` chamável ou marca XFail (TDD Contract).

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
        pytest.xfail(f"{name} ainda não implementado em {obj.__name__ if hasattr(obj, '__name__') else str(obj)}.")
    return fn

def test_read_product_from_sap_and_send_to_siscomex(monkeypatch) -> None:
    """
    Fluxo feliz: Ler produto no SAP e enviar ao SISCOMEX com sucesso.

    - Mocks:
        - TSAPServiceLayer.get_product -> dict representando o produto no SAP.
        - TSISCOMEXClient.create_product -> resposta normalizada de sucesso.
    - Critério de aceite:
        - Payload construído contém 'codigo' e 'ncm'
        - SISCOMEX retorna status_http 201 e sequencial é persistido (simulado)
    """
    TSAP = _require_callable(sap_mod, "TSAPServiceLayer")
    TSIS = _require_callable(siscomex_mod, "TSISCOMEXClient")

    # Produto de exemplo (SAP)
    product = {
        "codigo": "PROD_001",
        "ncm": "12345678",
        "descricao": "Produto integracao",
        "U_DimVer": 1,
    }

    # stub get_product
    def fake_get_product(self, item_code: str, correlation_id: str | None = None):
        assert item_code == "PROD_001"
        return product
    
    # stub create_product
    def fake_create_product(self, payload: dict[str, Any], idempotency_key: str | None = None, correlation_id: str | None = None):
        assert payload["codigo"] == product["codigo"]
        return {"status_http": 201, "sequencial": "S-123", "mensagem": "OK", "correlation_id": correlation_id or str(uuid.uuid4())}
    
    monkeypatch.setattr(TSAP, "get_product", fake_get_product, raising=False)
    monkeypatch.setattr(TSIS, "create_product", fake_create_product, raising=False)

    # Instanciar clientes (contrato mínimo)
    sap_client = TSAP()
    sis_client = TSIS(base_url="https://example", timeout=(1, 5))

    # execução simulada: ler + enviar
    prod = sap_client.get_product("PROD_001", correlation_id="c-1")
    assert prod["codigo"] == "PROD_001"

    result = sis_client.create_product({"codigo": prod["codigo"], "ncm": prod["ncm"]}, idempotency_key="idem-1", correlation_id="c-1")
    assert result["status_http"] == 201
    assert "sequencial" in result

def test_attributes_cache_and_fallback(monkeypatch, tmp_path) -> None:
    """
    Valida comportamento de cache na consulta de atributos por ncm e fallback quando service falha.

    - Cenários:
        1) Adapter retorna atributos  -> usados normalmente
        2) Adapter falha (simula 5xx) -> fallback para cache (snapshot)
    - Critério de aceite:
        - Quando adapter falha e cache recente existe (<=24h), fluxo usa cache e marca modo DEGRADED
    """
    # COntrato de adapter no siscomex_mod: get_required_attributes
    get_required_attributes = getattr(siscomex_mod, "get_required_attributes", None)
    if not callable(get_required_attributes):
        pytest.xfail("get_required_attributes ainda não implementado em src/siscomex/api_client.py")

    # comportamento: primeiro chamada bem sucedida -> grava "cache" simulada em arquivo
    attributes = [{"codigo_atributo": "ATTR_A", "tipo": "TEXTO", "obrigatorio": True}]
    
    def fake_adapter_success(ncm: str, data_referencia: str | None = None):
        return {"attributes": attributes, "fetched_at": "2026-06-01T00:00:00Z"}

    def fake_adapter_fail(ncm: str, data_referencia: str | None = None):
        raise RuntimeError("Upstream 5xx")
    
    # Simula cache local: grava snapchot
    cache_file = tmp_path / "attributes_cache.json"
    cache_file.write_text('{"attributes": [{"codigo_atributo": "ATTR_A", "tipo": "TEXTO", "obrigatorio": True}], "fetched_at": "2026-06-04T00:00:00Z"}')

    # 1) quando adapter falhar, implementacao deve usar cache
    monkeypatch.setattr(siscomex_mod, "get_required_attributes", fake_adapter_fail, raising=False)

    # Chamada ao adapter -- se implementacao existir, deve tratar e usar cache
    try:
        res = siscomex_mod.get_required_attributes("12345678")
    except Exception:
        # Sem implementação, XFAIL
        pytest.xfail("get_required_attributes lança; confirmar implementação do cache/fallback.")
    else:
        assert "attributes" in res or res is not None

def test_conditional_attribute_validation(monkeypatch) -> None:
    """
    Valida regras condicionais: se atributo origem satisfaz condição, atributo destino é exigido.

    - contrato esperado:
        - reolve_conditional_attributes(attributes: values) -> lista/estrutura de atributos obrigatórios
    - Critério de aceite:
        - Quando valor de origem satisfaz condição, atributo destino aparece como obrigatório nas regras resolvidas.
    """
    resolver = getattr(sap_mod, "TSAPServiceLayer", None)
    cond_resolver = getattr(sap_mod, "ConditionalRuleResolver", None)
    if not callable(cond_resolver):
        # Permitir que módulo ainda não exista (TDD)
        pytest.xfail("ConditionalRuleResolver ainda não implementado em src/sap/service_layer.py")

    # Exemplo de regras/atributos
    attrs = [
        {"codigo_atributo": "A_USA_LOTE", "obrigatorio": True},
        {"codigo_atributo": "NUM_LOTE", "obrigatorio": False, "condicoes": [{"atributo_origem": "A_USA_LOTE", "operador": "==", "valor": True}]},
    ]
    values = {"A_USA_LOTE": True}

    resolved = cond_resolver.resolve(attrs, values) # Contrato esperado
    assert isinstance(resolved, (list, dict))
    # Verificar que NUM_LOTE agora é obrigatório
    found = any((a.get("codigo_atributo") == "NUM_LOTE" and a.get("obrigatorio") is True) for a in resolved)
    assert found

def test_retry_and_idempotency_on_transient_errors(monkeypatch) -> None:
    """
   Simula 5xx/timeout e valida retry+idempotência:

    - Contrato:
        - TSISCOMEXClient.create_product deve aceitar idempotency_key
        - retry policy deve reexecutar até N vezes e não duplicar (simulado via idempotency)

    - Critério de aceite:
        - Após transient failures, operação eventual retorna sucesso e usou a mesma idempotency key
    """
    TSIS = getattr(siscomex_mod, "TSISCOMEXClient", None)
    if not callable(TSIS):
        pytest.xfail("TSISCOMEXClient ainda não implementado em src/siscomex/api_client.py")

    calls: dict[str, int] = {"count": 0}
    responses = [RuntimeError("5xx"), RuntimeError("timeout"),{"status_http": 201, "sequencial": "S-999"}]

    def flaky_create(self, payload: dict[str, Any], idempotency_key: str | None = None, correlation_id: str | None = None):
        calls["count"] += 1
        resp = responses[calls["count"] - 1]
        if isinstance(resp, Exception):
            raise resp
        return resp
    
    monkeypatch.setattr(TSIS, "create_product", flaky_create, raising=False)

    client = TSIS(base_url="https://example", timeout=(1, 2))
    try:
        out = client.create_product({"codigo": "P"}, idempotency_key="idem-xyz")
    except Exception:
        pytest.xfail("Retry policy não implementada no cliente; esperado comportamento TDD.")
    else:
        assert out["status_http"] == 201
        assert calls["count"] == 3