import os

from dotenv import load_dotenv

from .exceptions import ConfigError
from .models import Config


def load_config(env_file: str = ".env") -> Config:
    """
    .env 파일 및 환경 변수에서 설정을 로드합니다.
    LLM_PROVIDER=bedrock 이면 AWS 자격증명을 사용하고,
    LLM_PROVIDER=openai(기본값)이면 OPENAI_API_KEY가 필수입니다.
    """
    load_dotenv(env_file)

    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    missing_keys = []
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if provider == "openai" and not openai_api_key:
        missing_keys.append("OPENAI_API_KEY")

    if missing_keys:
        raise ConfigError(f"필수 설정이 누락되었습니다: {missing_keys}")

    return Config(
        llm_provider=provider,
        openai_api_key=openai_api_key,
        llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002"),
        chunk_size=int(os.getenv("CHUNK_SIZE", "500")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "50")),
        top_k=int(os.getenv("TOP_K", "3")),
        vector_store_path=os.getenv("VECTOR_STORE_PATH", "./chroma_db"),
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        bedrock_llm_model=os.getenv(
            "BEDROCK_LLM_MODEL", "anthropic.claude-3-5-sonnet-20241022-v2:0"
        ),
        bedrock_embedding_model=os.getenv(
            "BEDROCK_EMBEDDING_MODEL", "amazon.titan-embed-text-v2:0"
        ),
    )
