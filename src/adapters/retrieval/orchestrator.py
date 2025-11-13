from ...domain.ports import RetrievalPort, RetrievedData
from ...domain.models import Query, SourceProvider


class RetrievalOrchestrator(RetrievalPort):
    def __init__(self, adapters: list[RetrievalPort], enabled: list[SourceProvider]):
        self.adapters = adapters
        self.enabled = set(enabled)

    def retrieve(self, query: Query) -> RetrievedData:
        all_sources = []

        for adapter in self.adapters:
            if adapter.provider in self.enabled:
                data = adapter.retrieve(query)
                all_sources.extend(data.sources)

        return RetrievedData(sources=all_sources)
