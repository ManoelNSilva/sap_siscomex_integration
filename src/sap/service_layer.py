from __future__ import annotations


class TSAPServiceLayer:
    def __init__(self, base_url: str = "", timeout: tuple[int, int] = (5, 30)) -> None:
        self.base_url = base_url
        self.timeout = timeout
