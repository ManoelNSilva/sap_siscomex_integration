from __future__ import annotations


class TSISCOMEXClient:
    def __init__(self, base_url: str, timeout: tuple[int, int] = (5, 30)) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def get_required_attributes(self, ncm: str) -> list[dict]:
        return []

    def create_product(self, payload: dict) -> dict:
        return {"status": "not_implemented"}

    def update_product(self, product_id: str, payload: dict) -> dict:
        return {"status": "not_implemented"}

    def deactivate_product(self, product_id: str) -> dict:
        return {"status": "not_implemented"}

    def reactivate_product(self, product_id: str) -> dict:
        return {"status": "not_implemented"}
