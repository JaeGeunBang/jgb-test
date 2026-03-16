from pathlib import Path

from .config import Config
from .document_loader import DocumentLoader
from .embedder import Embedder
from .exceptions import EmptyStoreError, LLMError
from .llm_client import LLMClient
from .models import ConversationTurn
from .retriever import Retriever
from .text_splitter import TextSplitter
from .vector_store import VectorStore


class Chatbot:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._loader = DocumentLoader()
        self._splitter = TextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )
        self._embedder = Embedder(config)
        self._vector_store = VectorStore(config)
        self._retriever = Retriever(self._embedder, self._vector_store)
        self._llm_client = LLMClient(config)
        self._history: list[ConversationTurn] = []

    def ingest(self, file_path: str) -> None:
        """DocumentLoader → TextSplitter → Embedder → VectorStore 파이프라인."""
        text = self._loader.load(file_path)
        chunks = self._splitter.split(text)
        embeddings = self._embedder.embed_batch(chunks)
        source = Path(file_path).name
        self._vector_store.add(chunks, embeddings, source)

    def ask(self, question: str) -> str:
        """Retriever → LLMClient 파이프라인, 대화 히스토리 유지."""
        context = self._retriever.retrieve(question)
        answer = self._llm_client.generate(question, context)
        self._history.append(ConversationTurn(question=question, answer=answer))
        return answer

    def run_cli(self) -> None:
        """대화형 입력 루프. exit/quit 입력 시 종료."""
        print("RAG 챗봇에 오신 것을 환영합니다. 종료하려면 'exit' 또는 'quit'을 입력하세요.")
        while True:
            try:
                user_input = input("\n질문: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n챗봇을 종료합니다.")
                break

            if user_input.lower() in {"exit", "quit"}:
                print("챗봇을 종료합니다.")
                break

            if not user_input:
                continue

            try:
                answer = self.ask(user_input)
                print(f"\n답변: {answer}")
            except EmptyStoreError as e:
                print(f"\n{e}")
            except LLMError:
                print("\n오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
