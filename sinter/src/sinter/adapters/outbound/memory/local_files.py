"""LocalFiles em memória, para testes."""


class MemoryLocalFiles:
    def __init__(self) -> None:
        self.files: dict[str, str] = {}

    def read(self, path: str) -> str | None:
        return self.files.get(path)

    def write(self, path: str, text: str) -> None:
        self.files[path] = text
