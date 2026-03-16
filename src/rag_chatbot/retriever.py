from .embedder import Embedder
from .exceptions import EmptyStoreError
from .models import SearchResult
from .vector_store import VectorStore


class Retriever:
    """질문을 벡터화하여 VectorStore에서 관련 청크를 검색합니다."""

    def __init__(self, embedder: Embedder, vector_store: VectorStore) -> None:
        self._embedder = embedder
        self._vector_store = vector_store

    def retrieve(self, query: str) -> list[SearchResult]:
        """
        질문과 관련된 청크를 검색합니다.

        VectorStore가 비어있으면 EmptyStoreError를 발생시킵니다.
        """
        if self._vector_store.is_empty():
            raise EmptyStoreError("검색 가능한 문서가 없습니다. 먼저 문서를 등록해주세요.")

        query_embedding = self._embedder.embed(query)
        return self._vector_store.search(query_embedding)
