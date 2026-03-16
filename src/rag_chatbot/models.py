from dataclasses import dataclass, field


@dataclass
class SearchResult:
    text: str    # 청크 원본 텍스트
    source: str  # 출처 파일명
    score: float # 코사인 유사도 점수 (0.0 ~ 1.0)


@dataclass
class ConversationTurn:
    question: str
    answer: str


@dataclass
class Config:
    # LLM 제공자: "openai" 또는 "bedrock"
    llm_provider: str = "openai"
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-ada-002"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 3
    vector_store_path: str = "./chroma_db"
    # Bedrock 전용
    aws_region: str = "us-east-1"
    bedrock_llm_model: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    bedrock_embedding_model: str = "amazon.titan-embed-text-v2:0"
