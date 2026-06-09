from __future__ import annotations

from typing import Any


class TSAPServiceLayer:
    """
    Stub mínimo do adapter SAP usado pelos testes.
    Métodos implementados para expor o contrato (podem lançar NotImplementedError).
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Inicialização mínima do cliente SAP (configuração stub)."""
        self._cfg = kwargs

    def login(self, user: str | None = None, pwd: str | None = None) -> None:
        """Autenticar (stub)."""
        raise NotImplementedError("login ainda não implementado (stub de contrato)")

    def get_product(self, item_code: str, correlation_id: str | None = None) -> dict[str, Any]:
        """
        Ler produto do SAP (stub).
        Retorna dicionário mínimo esperado pelos testes ou lança NotImplementedError.
        """
        raise NotImplementedError("get_product ainda não implementado (stub de contrato)")

    def logout(self) -> None:
        """Encerrar sessão (stub)."""
        raise NotImplementedError("logout ainda não implementado (stub de contrato)")