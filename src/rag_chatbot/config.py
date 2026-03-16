import os

from dotenv import load_dotenv

from .exceptions import ConfigError
from .models import Config


def load_config(env_file: str = ".env") -> Config:
    """
    .env 파일 및 환경 변수에서 설정을 로드합니다.
    LLM_PROVIDER에 따라 필수 API 키가 달라집니다:
    - openai: OPENAI_API_KEY 필수
    - anthropic: ANTHROPIC_API_KEY 필수
    """
    load_dotenv(env_file)

    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    missing_keys = []

    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")

    if provider == "openai" and not openai_api_key:
        missing_keys.append("OPENAI_API_KEY")
    elif provider == "anthropic" and not anthropic_api_key:
        missing_keys.append("ANTHROPIC_API_KEY")

    if missing_keys:
        raise ConfigError(f"필수 설정이 누락되었습니다: {missing_keys}")

    return Config(
        llm_provider=provider,
        openai_api_key=openai_api_key,
        anthropic_api_key=anthropic_api_key,
        llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002"),
        chunk_size=int(os.getenv("CHUNK_SIZE", "500")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "50")),
        top_k=int(os.getenv("TOP_K", "3")),
        vector_store_path=os.getenv("VECTOR_STORE_PATH", "./chroma_db"),
        anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
    )
