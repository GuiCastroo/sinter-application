"""ManifestCodec com ruamel.yaml em round-trip: dados + linha de cada trecho."""

import re
from copy import copy
from io import StringIO
from typing import Any, get_args, get_origin

from pydantic import BaseModel
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.error import MarkedYAMLError, YAMLError
from ruamel.yaml.tokens import CommentToken

from sinter.domain.model.registry import KINDS
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

    def format(self, text: str) -> str:
        """Retorna a forma canônica, mantendo comentários e escalares de round-trip."""
        yaml = YAML(typ="rt")
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.line_break = "\n"  # type: ignore[assignment]
        try:
            docs = list(yaml.load_all(text))
        except MarkedYAMLError as exc:
            mark = exc.problem_mark or exc.context_mark
            line = mark.line + 1 if mark is not None else None
            raise ManifestSyntaxError(f"YAML inválido: {exc.problem or exc}", line) from exc
        except YAMLError as exc:
            raise ManifestSyntaxError(f"YAML inválido: {exc}", None) from exc

        for doc in docs:
            if not isinstance(doc, CommentedMap):
                continue
            kind = doc.get("kind")
            info = KINDS.get(kind) if isinstance(kind, str) else None
            model = info.model if info is not None else None
            if model is not None:
                try:
                    model.model_validate(doc)
                except (ValueError, TypeError):
                    # Um manifesto inválido ainda recebe o envelope canônico; seus
                    # campos internos não são reordenados como se fossem válidos.
                    model = None
            _reorder_mapping(doc, model)
            _trim_comment_whitespace(doc)

        stream = StringIO()
        yaml.dump_all(docs, stream)
        output = stream.getvalue()
        if output and not output.endswith("\n"):
            output += "\n"
        return output


def _trim_comment_whitespace(value: Any) -> None:
    if isinstance(value, CommentedMap | CommentedSeq):
        ca = value.ca
        for comments in (ca.comment, ca.items, ca.end, ca.pre):
            _trim_comment_tokens(comments)
        children = value.values() if isinstance(value, CommentedMap) else value
        for child in children:
            _trim_comment_whitespace(child)


def _trim_comment_tokens(value: Any) -> None:
    if isinstance(value, CommentToken):
        normalized = value.value.replace("\r\n", "\n").replace("\r", "\n")
        value.value = re.sub(r"[ \t]+(?=\n?$)", "", normalized, flags=re.MULTILINE)
    elif isinstance(value, dict):
        for child in value.values():
            _trim_comment_tokens(child)
    elif isinstance(value, list | tuple):
        for child in value:
            _trim_comment_tokens(child)


def _field_key(name: str, field: Any) -> str:
    return field.serialization_alias or field.alias or name


def _is_model(annotation: Any) -> bool:
    return isinstance(annotation, type) and issubclass(annotation, BaseModel)


def _reorder_value(value: Any, annotation: Any) -> None:
    origin = get_origin(annotation)
    if origin in (list, tuple, set, frozenset):
        for arg in get_args(annotation):
            if isinstance(value, CommentedSeq):
                for item in value:
                    _reorder_value(item, arg)
            return
    if origin is dict:
        args = get_args(annotation)
        if len(args) == 2 and isinstance(value, CommentedMap):
            for item in value.values():
                _reorder_value(item, args[1])
        return
    if origin is not None:  # e.g. Optional[Model] / Model | None
        for arg in get_args(annotation):
            _reorder_value(value, arg)
        return
    if _is_model(annotation) and isinstance(value, CommentedMap):
        _reorder_mapping(value, annotation)


def _reorder_mapping(mapping: CommentedMap, model: type[BaseModel] | None) -> None:
    """Reorder keys in place; ruamel keeps key comments attached on insert."""
    fields_by_key: dict[str, Any] = {}
    if model is not None:
        fields_by_key = {
            _field_key(name, field): field for name, field in model.model_fields.items()
        }

    if model is None:
        preferred = [key for key in ("apiVersion", "kind", "metadata", "spec") if key in mapping]
    else:
        preferred = [key for key in fields_by_key if key in mapping]
    ordered = [*preferred, *(key for key in mapping if key not in preferred)]

    if model is not None:
        for key in ordered:
            field = fields_by_key.get(str(key))
            if field is not None:
                _reorder_value(mapping[key], field.annotation)

    comments = {key: copy(value) for key, value in mapping.ca.items.items()}
    for index, key in enumerate(ordered):
        mapping.insert(index, key, mapping[key])
    # ruamel's insert can leave a preceding comment at its old positional slot.
    # Rebind the saved comment metadata by key after the reorder.
    for key, comment in comments.items():
        mapping.ca.items[key] = comment
