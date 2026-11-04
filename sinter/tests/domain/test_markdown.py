from sinter.domain.services.markdown import index_markdown, section_content
from sinter.domain.services.text import gh_anchor


def test_github_anchor_unaccents_and_removes_punctuation() -> None:
    assert gh_anchor("Decisões: Política (v2)!") == "decisoes-politica-v2"


def test_duplicate_headings_get_numeric_suffixes() -> None:
    index = index_markdown("# Regras\n## Regras\n# Regras")
    assert [h.anchor for h in index.headings] == ["regras", "regras-1", "regras-2"]


def test_duplicate_suffixes_do_not_collide_with_natural_heading() -> None:
    text = "# Regras\nfirst\n# Regras\nsecond\n# Regras-1\nthird"
    index = index_markdown(text)

    assert [h.anchor for h in index.headings] == ["regras", "regras-1", "regras-1-1"]
    assert section_content(text, index, "regras-1").startswith("# Regras\nsecond")
    assert section_content(text, index, "regras-1-1").startswith("# Regras-1\nthird")


def test_natural_suffix_before_duplicate_still_has_unique_anchors() -> None:
    index = index_markdown("# Regras-1\nfirst\n# Regras\nsecond\n# Regras\nthird")
    assert [h.anchor for h in index.headings] == ["regras-1", "regras", "regras-2"]


def test_section_ends_at_same_or_higher_heading() -> None:
    text = "# A\nintro\n## B\nbody\n### C\ninner\n## D\nlast\n# E"
    index = index_markdown(text)
    assert section_content(text, index, "b") == "## B\nbody\n### C\ninner"


def test_headings_inside_fences_are_ignored() -> None:
    index = index_markdown("# A\n```md\n# fake\n```\n## B\n~~~\n# no\n~~~")
    assert [h.title for h in index.headings] == ["A", "B"]


def test_long_fence_only_closes_with_matching_length_and_empty_tail() -> None:
    text = "# Intro\n````python\n# code\n```\n```` not-closed\n~~~\n# still code\n````\n# Real"
    index = index_markdown(text)

    assert [h.title for h in index.headings] == ["Intro", "Real"]
    assert "# code" in section_content(text, index, "intro")
    assert "# still code" in section_content(text, index, "intro")


def test_tilde_fence_does_not_close_on_backticks() -> None:
    index = index_markdown("# Intro\n~~~md\n# code\n```\n~~~\n# Real")
    assert [h.title for h in index.headings] == ["Intro", "Real"]


def test_atx_closing_hashes_require_preceding_whitespace() -> None:
    index = index_markdown("# C#\nbody\n# API_client\nbody\n# Closing ###")
    assert [(h.title, h.anchor) for h in index.headings] == [
        ("C#", "c"),
        ("API_client", "api_client"),
        ("Closing", "closing"),
    ]


def test_heading_summary_has_line_sizes_and_no_content() -> None:
    index = index_markdown("# A\nsecret\n## B\nmore")
    assert [(h.anchor, h.size_lines) for h in index.headings] == [("a", 4), ("b", 2)]


def test_missing_anchor_returns_none() -> None:
    text = "# A"
    assert section_content(text, index_markdown(text), "missing") is None
