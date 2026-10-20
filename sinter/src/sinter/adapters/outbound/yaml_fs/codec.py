"""ManifestCodec com ruamel.yaml em round-trip: dados + linha de cada trecho."""

from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.error import MarkedYAMLError, YAMLError

from sinter.domain.validation.finding import Segment
from sinter.ports.outbound.manifest_codec import ManifestSyntaxError, ManifestText


def _plain(node: Any, path: tuple[Segment, ...], positions: dict[tuple[Segment, ...], int]) -> Any:
    """Converte nós do ruamel em tipos da biblioteca padrão, anotando a linha (1-based)."""
    if isinstance(node, CommentedMap):
        out: dict[str, Any] = {}
        for key, value in node.items():
            child = (*path, str(key))
            line, _col = node.lc.key(key)
            positions[child] = line + 1
            out[str(key)] = _plain(value, child, positions)
        return out
    if isinstance(node, CommentedSeq):
        items: list[Any] = []
        for i, value in enumerate(node):
            child = (*path, i)
            line, _col = node.lc.item(i)
            positions[child] = line + 1
            items.append(_plain(value, child, positions))
        return items
    if isinstance(node, bool) or node is None:
        return node
    if isinstance(node, int):
        return int(node)
    if isinstance(node, float):
        return float(node)
    if isinstance(node, str):
        return str(node)
    return node  # datas: datetime.date / datetime.datetime


class RuamelCodec:
    def __init__(self) -> None:
        self._yaml = YAML(typ="rt")

    def split(self, text: str) -> list[ManifestText]:
        try:
            raw_docs = list(self._yaml.load_all(text))
        except MarkedYAMLError as exc:
            mark = exc.problem_mark or exc.context_mark
            line = mark.line + 1 if mark is not None else None
            raise ManifestSyntaxError(f"YAML inválido: {exc.problem or exc}", line) from exc
        except YAMLError as exc:
            raise ManifestSyntaxError(f"YAML inválido: {exc}", None) from exc

        docs: list[ManifestText] = []
        for index, raw in enumerate(d for d in raw_docs if d is not None):
            positions: dict[tuple[Segment, ...], int] = {}
            if isinstance(raw, CommentedMap | CommentedSeq):
                positions[()] = raw.lc.line + 1
            data = _plain(raw, (), positions)
            docs.append(ManifestText(index=index, data=data, positions=positions))
        return docs
