import hashlib

import chromadb

from .models import Config, SearchResult


class VectorStore:
    """ChromaDB 기반 로컬 영속 벡터 스토어."""

    COLLECTION_NAME = "rag_documents"

    def __init__(self, config: Config) -> None:
        self._client = chromadb.PersistentClient(path=config.vector_store_path)
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, chunks: list[str], embeddings: list[list[float]], source: str) -> None:
        """청크, 임베딩, 출처 파일명을 저장합니다."""
        if not chunks:
            return

        ids = [
            hashlib.sha256(f"{source}:{i}:{chunk}".encode()).hexdigest()
            for i, chunk in enumerate(chunks)
        ]
        metadatas = [{"source": source} for _ in chunks]

        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )

    def search(self, query_embedding: list[float], top_k: int = 3) -> list[SearchResult]:
        """코사인 유사도 기준 상위 top_k 결과를 반환합니다."""
        count = self._collection.count()
        if count == 0:
            return []

        n_results = min(top_k, count)
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        search_results: list[SearchResult] = []
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, dist in zip(documents, metadatas, distances):
            score = 1.0 - dist  # cosine distance → similarity
            search_results.append(
                SearchResult(
                    text=doc,
                    source=meta.get("source", ""),
                    score=score,
                )
            )

        return search_results

    def is_empty(self) -> bool:
        """저장된 문서가 없으면 True를 반환합니다."""
        return self._collection.count() == 0
