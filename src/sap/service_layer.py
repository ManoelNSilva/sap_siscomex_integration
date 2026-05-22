class TSAPServiceLayer:
    """Cliente  base para integração com SAP Service Layer."""

    def __init__(self, base_url: str = "", timeout: tuple[int, int] = (5, 30)):
        self.base_url = base_url
        self.timeout = timeout
