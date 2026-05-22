class TSISCOMEXClient:
    """Cliente base para integração com o SISCOMEX."""

    def __init__(self, base_url: str, timeout: tuple[int, int] = (5, 30)):
        self.base_url = base_url
        self.timeout = timeout

    def get_required_attributes(self):
        return []

    def create_product(self, payload: dict):
        return {"ok": False, "payload": payload}

    def update_product(self, product_id: str, payload: dict):
        return {"ok": False, "product_id": product_id, "payload": payload}

    def deactivate_product(self, product_id: str):
        return {"ok": False, "product_id": product_id}

    def reactivate_product(self, product_id: str):
        return {"ok": False, "product_id": product_id}
