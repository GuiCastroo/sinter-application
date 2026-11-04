"""Caso de uso do `sinter get <id> --level`."""

import difflib

from sinter.application.load import load
from sinter.domain.errors import SinterError
from sinter.domain.model.views import DomainLevel1, Level0, SubdomainLevel1
from sinter.domain.services import levels
from sinter.domain.services.summary import item_summary
from sinter.ports.inbound.common import Report
from sinter.ports.inbound.get import GetRequest, GetResult
from sinter.ports.outbound.catalog_files import CatalogFiles
from sinter.ports.outbound.manifest_codec import ManifestCodec


class Get:
    def __init__(self, files: CatalogFiles, codec: ManifestCodec) -> None:
        self._files = files
        self._codec = codec

    def __call__(self, request: GetRequest) -> GetResult:
        catalog, findings = load(self._files, self._codec)
        entries = catalog.find(request.id)
        if not entries:
            ids = sorted({e.id for e in catalog.entries})
            similar = difflib.get_close_matches(request.id, ids, n=3, cutoff=0.5)
            hint = f"; parecidos: {', '.join(similar)}" if similar else ""
            raise SinterError(
                "ITEM_NOT_FOUND",
                f"'{request.id}' não existe no catálogo{hint}",
                {"id": request.id, "suggestions": similar},
            )

        if not entries[0].valid:
            raise SinterError(
                "ITEM_NOT_FOUND",
                f"'{request.id}' existe, mas seu manifesto é inválido; rode validate",
                {"id": request.id, "suggestions": []},
            )

        manifest = catalog.manifest(request.id)
        item: DomainLevel1 | SubdomainLevel1 | Level0
        if manifest is None:
            item = levels.level0_of_entry(catalog, entries[0])
        elif request.level >= 1 and manifest.kind == "Domain":
            item = levels.domain_level1(catalog, manifest)
        elif request.level >= 1 and manifest.kind == "Subdomain":
            item = levels.subdomain_level1(catalog, manifest)
        else:
            item = levels.level0_of_manifest(catalog, manifest)

        head = item.level0 if isinstance(item, DomainLevel1 | SubdomainLevel1) else item
        shown = min(request.level, 1) if isinstance(item, DomainLevel1 | SubdomainLevel1) else 0
        return GetResult(
            level=shown,
            item=item,
            omitted=levels.omitted(request.id, shown, head.kind),
            summary=item_summary(head),
            report=Report.from_findings(findings),
        )
