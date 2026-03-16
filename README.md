# RAG Chatbot

Python 기반의 RAG(Retrieval-Augmented Generation) 챗봇 시스템입니다. 문서를 업로드하고 벡터 DB에 저장한 후, 사용자의 질문에 대해 관련 문서를 검색하여 LLM이 답변을 생성합니다.

## 주요 기능

- **문서 수집 및 인덱싱**: TXT, PDF, Markdown 파일을 읽어 벡터 DB에 저장
- **질문 기반 검색**: 사용자 질문과 관련된 문서 내용을 유사도 기준으로 검색
- **LLM 답변 생성**: 검색된 문서를 컨텍스트로 활용하여 정확한 답변 생성
- **대화형 CLI**: 터미널에서 대화 세션을 유지하며 질문과 답변 진행
- **유연한 설정**: 환경 변수로 LLM 모델, 임베딩 모델, 청크 크기 등 설정 가능

## 설치

```bash
pip install -r requirements.txt
```

## 설정

`.env` 파일을 생성하고 다음 설정을 추가하세요:

```env
# LLM Provider (openai 또는 bedrock)
LLM_PROVIDER=openai

# OpenAI 설정 (LLM_PROVIDER=openai인 경우 필수)
OPENAI_API_KEY=your_openai_api_key

# LLM 모델 (기본값: gpt-4o-mini)
LLM_MODEL=gpt-4o-mini

# 임베딩 모델 (기본값: text-embedding-ada-002)
EMBEDDING_MODEL=text-embedding-ada-002

# 텍스트 분할 설정
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# 검색 결과 수 (기본값: 3)
TOP_K=3

# 벡터 스토어 경로 (기본값: ./chroma_db)
VECTOR_STORE_PATH=./chroma_db

# AWS Bedrock 설정 (LLM_PROVIDER=bedrock인 경우)
AWS_REGION=us-east-1
BEDROCK_LLM_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
BEDROCK_EMBEDDING_MODEL=amazon.titan-embed-text-v2:0
```

## 사용법

챗봇을 실행하세요:

```bash
python -m src.rag_chatbot
```

CLI에서 문서를 인덱싱하고 질문을 입력할 수 있습니다. 종료하려면 `exit` 또는 `quit`을 입력하세요.

## 아키텍처

- **DocumentLoader**: 파일에서 텍스트 추출
- **TextSplitter**: 텍스트를 청크로 분할
- **Embedder**: 텍스트를 벡터로 변환
- **VectorStore**: ChromaDB를 사용한 벡터 저장 및 검색
- **Retriever**: 질문과 관련된 문서 검색
- **LLMClient**: LLM을 통한 답변 생성
- **Chatbot**: 전체 파이프라인 조율 및 CLI 인터페이스

## 테스트

```bash
pytest
```

## 라이선스

MIT
