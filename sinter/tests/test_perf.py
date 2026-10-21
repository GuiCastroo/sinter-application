"""NFR-3: validate de um catálogo com 500 itens em até 3 s."""

import time
from pathlib import Path

import pytest

from sinter.adapters.inbound.cli.app import run

ORG = """apiVersion: sinter.dev/v1
kind: Organization
metadata: { id: org-acme, name: ACME, status: approved }
spec:
  schemaVersion: 1
  areas: [{ id: area-varejo, name: Varejo }]
"""
REPOS = """apiVersion: sinter.dev/v1
kind: RepositoryList
metadata: { id: repositories, name: Repos, status: approved }
spec:
  repositories: [{ id: repo-api, url: "git@x:api.git" }]
"""


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.mark.perf
def test_validate_500_itens_em_ate_3_segundos(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write(tmp_path / "organization.yaml", ORG)
    _write(tmp_path / "repositories.yaml", REPOS)
    items = 0
    for d in range(20):
        code = f"D{d:02d}"
        subs = [f"sub-d{d:02d}-s{s:02d}" for s in range(24)]
        _write(
            tmp_path / f"domains/d{d:02d}/domain.yaml",
            f"""apiVersion: sinter.dev/v1
kind: Domain
metadata: {{ id: dom-d{d:02d}, name: D, domainId: {code}, area: area-varejo, status: approved }}
spec:
  parent: org-acme
  purpose: P.
  subdomains: [{", ".join(subs)}]
""",
        )
        items += 1
        for s, sub in enumerate(subs):
            _write(
                tmp_path / f"domains/d{d:02d}/subdomains/{sub}.yaml",
                f"""apiVersion: sinter.dev/v1
kind: Subdomain
metadata: {{ id: {sub}, name: S, domain: dom-d{d:02d}, status: approved }}
spec:
  purpose: P.
  applications:
    - id: app-d{d:02d}-a{s:02d}
      name: A
      lifecycle: modern
      repositories: [{{ repo: repo-api, role: api, platform: java }}]
""",
            )
            items += 1
    assert items >= 500

    start = time.perf_counter()
    code = run(["validate", str(tmp_path)])
    elapsed = time.perf_counter() - start
    assert "0 erros" in capsys.readouterr().out
    assert code == 0
    assert elapsed < 3.0, f"validate levou {elapsed:.2f}s"
