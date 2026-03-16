# 구현 계획: RAG 챗봇

## 개요

Python 기반 RAG 챗봇 시스템을 단계적으로 구현합니다. 프로젝트 구조 설정부터 시작하여 각 컴포넌트를 독립적으로 구현하고, 마지막에 전체 파이프라인을 연결합니다.

## 태스크

- [x] 1. 프로젝트 구조 및 기반 설정
  - `src/rag_chatbot/` 패키지 디렉토리 생성
  - `requirements.txt` 작성 (openai, chromadb, pypdf, python-dotenv, pytest, hypothesis)
  - `src/rag_chatbot/exceptions.py`에 커스텀 예외 계층 구현 (`RagChatbotError`, `UnsupportedFormatError`, `EmptyStoreError`, `LLMError`, `ConfigError`)
  - `src/rag_chatbot/models.py`에 데이터 모델 정의 (`SearchResult`, `ConversationTurn`, `Config`)
  - _요구사항: 1.2, 1.3, 2.2, 3.3, 5.2_

- [x] 2. Config 컴포넌트 구현
  - [x] 2.1 `src/rag_chatbot/config.py`에 `Config` 클래스 구현
    - `python-dotenv`로 `.env` 파일 및 환경 변수 로드
    - 선택적 환경 변수에 기본값 적용
    - `OPENAI_API_KEY` 누락 시 `ConfigError` 발생 및 누락 항목 명시
    - _요구사항: 5.1, 5.2, 5.3_

  - [ ]* 2.2 `Config` 기본값 적용 속성 테스트 작성
    - **속성 6: 설정 기본값 적용**
    - **검증 대상: 요구사항 5.3**

  - [ ]* 2.3 `Config` 필수값 누락 오류 속성 테스트 작성
    - **속성 7: 필수 설정 누락 시 명시적 오류**
    - **검증 대상: 요구사항 5.2**

  - [ ]* 2.4 `Config` 단위 테스트 작성
    - 기본값 적용, 환경 변수 오버라이드, 필수값 누락 오류 케이스
    - _요구사항: 5.1, 5.2, 5.3_

- [x] 3. DocumentLoader 컴포넌트 구현
  - [x] 3.1 `src/rag_chatbot/document_loader.py`에 `DocumentLoader` 클래스 구현
    - TXT, MD 파일 표준 라이브러리로 읽기
    - PDF 파일 `pypdf`로 텍스트 추출
    - 파일 없음 → `FileNotFoundError`, 미지원 형식 → `UnsupportedFormatError` 발생
    - _요구사항: 1.1, 1.2, 1.3_

  - [ ]* 3.2 `DocumentLoader` 단위 테스트 작성
    - TXT/MD/PDF 각 형식 로드, 파일 없음 오류, 미지원 형식 오류
    - `tmp_path` fixture 사용
    - _요구사항: 1.1, 1.2, 1.3_

- [x] 4. TextSplitter 컴포넌트 구현
  - [x] 4.1 `src/rag_chatbot/text_splitter.py`에 `TextSplitter` 클래스 구현
    - `chunk_size`(기본 500), `chunk_overlap`(기본 50) 파라미터 지원
    - 오버랩을 포함한 슬라이딩 윈도우 방식으로 청크 분할
    - _요구사항: 1.4_

  - [ ]* 4.2 청크 분할 크기 불변성 속성 테스트 작성
    - **속성 1: 청크 분할 크기 불변성**
    - **검증 대상: 요구사항 1.4**

  - [ ]* 4.3 청크 오버랩 보존 속성 테스트 작성
    - **속성 2: 청크 오버랩 보존**
    - **검증 대상: 요구사항 1.4**

  - [ ]* 4.4 `TextSplitter` 단위 테스트 작성
    - 짧은 텍스트(청크 1개), chunk_size 경계, 오버랩 경계 케이스
    - _요구사항: 1.4_

- [x] 5. 체크포인트 - 기반 컴포넌트 테스트 통과 확인
  - 모든 테스트가 통과하는지 확인하고, 문제가 있으면 사용자에게 알린다.

- [x] 6. Embedder 컴포넌트 구현
  - [x] 6.1 `src/rag_chatbot/embedder.py`에 `Embedder` 클래스 구현
    - OpenAI `text-embedding-ada-002` API 호출로 단일/배치 임베딩 생성
    - `Config`에서 임베딩 모델명 주입
    - _요구사항: 1.5_

  - [ ]* 6.2 `Embedder` 단위 테스트 작성
    - `unittest.mock`으로 OpenAI API 모킹
    - 단일 임베딩, 배치 임베딩 케이스
    - _요구사항: 1.5_

- [x] 7. VectorStore 컴포넌트 구현
  - [x] 7.1 `src/rag_chatbot/vector_store.py`에 `VectorStore` 클래스 구현
    - ChromaDB 로컬 영속 저장소 초기화 (`vector_store_path` 설정 사용)
    - `add()`: 청크, 임베딩, 출처 파일명 저장
    - `search()`: 코사인 유사도 기준 상위 `top_k` 결과 반환, `SearchResult` 리스트로 변환
    - `is_empty()`: 저장된 문서 유무 확인
    - _요구사항: 1.6, 2.1, 2.3_

  - [ ]* 7.2 인덱싱 후 검색 가능성 속성 테스트 작성
    - **속성 3: 인덱싱 후 검색 가능성 (Round Trip)**
    - **검증 대상: 요구사항 1.6, 2.1**
    - 인메모리 ChromaDB 인스턴스 사용

  - [ ]* 7.3 검색 결과 출처 포함 속성 테스트 작성
    - **속성 5: 검색 결과 출처 포함**
    - **검증 대상: 요구사항 2.3**

  - [ ]* 7.4 `VectorStore` 단위 테스트 작성
    - 추가 후 검색, 빈 스토어 확인, 출처 필드 포함 여부
    - _요구사항: 1.6, 2.1, 2.3_

- [x] 8. Retriever 컴포넌트 구현
  - [x] 8.1 `src/rag_chatbot/retriever.py`에 `Retriever` 클래스 구현
    - `Embedder`로 질문 벡터화 후 `VectorStore.search()` 호출
    - `VectorStore`가 비어있으면 `EmptyStoreError` 발생
    - _요구사항: 2.1, 2.2_

  - [ ]* 8.2 빈 스토어 안내 메시지 속성 테스트 작성
    - **속성 4: 빈 스토어 안내 메시지**
    - **검증 대상: 요구사항 2.2**

  - [ ]* 8.3 `Retriever` 단위 테스트 작성
    - 빈 스토어 호출 시 `EmptyStoreError`, 정상 검색 케이스
    - _요구사항: 2.1, 2.2_

- [x] 9. LLMClient 컴포넌트 구현
  - [x] 9.1 `src/rag_chatbot/llm_client.py`에 `LLMClient` 클래스 구현
    - `SearchResult` 리스트를 컨텍스트로 포함한 프롬프트 구성
    - 컨텍스트에 없는 내용은 추측하지 않도록 시스템 프롬프트 설정
    - OpenAI Chat Completions API 호출, 실패 시 `LLMError` 발생
    - _요구사항: 3.1, 3.2, 3.3_

  - [ ]* 9.2 `LLMClient` 단위 테스트 작성
    - `unittest.mock`으로 OpenAI API 모킹
    - 정상 응답, API 실패 시 `LLMError` 케이스
    - _요구사항: 3.1, 3.2, 3.3_

- [x] 10. 체크포인트 - 전체 컴포넌트 테스트 통과 확인
  - 모든 테스트가 통과하는지 확인하고, 문제가 있으면 사용자에게 알린다.

- [x] 11. Chatbot 클래스 및 CLI 구현
  - [x] 11.1 `src/rag_chatbot/chatbot.py`에 `Chatbot` 클래스 구현
    - `ingest()`: DocumentLoader → TextSplitter → Embedder → VectorStore 파이프라인 연결
    - `ask()`: Retriever → LLMClient 파이프라인 연결, `ConversationTurn` 히스토리 유지
    - `run_cli()`: 입력 루프 구현, `exit`/`quit` 입력 시 종료, LLM 오류 시 재시도 안내 출력
    - _요구사항: 1.1~1.6, 2.1~2.3, 3.1~3.3, 4.1~4.4_

  - [ ]* 11.2 `Chatbot` 단위 테스트 작성
    - `exit`/`quit` 입력 시 세션 종료, LLM 오류 시 재시도 안내 메시지 출력
    - _요구사항: 3.3, 4.3_

- [x] 12. 진입점 및 패키지 마무리
  - [x] 12.1 `src/rag_chatbot/__main__.py` 또는 `main.py` 진입점 작성
    - `Config` 로드 → `Chatbot` 초기화 → `run_cli()` 호출
    - `ConfigError` 발생 시 오류 메시지 출력 후 종료
    - _요구사항: 4.1, 5.1, 5.2_

  - [x] 12.2 `src/rag_chatbot/__init__.py` 작성 및 공개 API 정리
    - _요구사항: 4.1_

- [x] 13. 최종 체크포인트 - 전체 테스트 통과 확인
  - 모든 테스트가 통과하는지 확인하고, 문제가 있으면 사용자에게 알린다.

## 참고

- `*` 표시된 태스크는 선택 사항으로, MVP 구현 시 건너뛸 수 있습니다.
- 각 태스크는 특정 요구사항을 참조하여 추적 가능성을 보장합니다.
- 속성 기반 테스트는 `hypothesis` 라이브러리를 사용하며 최소 100회 반복 실행합니다.
- LLM 및 OpenAI API 호출은 `unittest.mock`으로 모킹하여 테스트 격리를 유지합니다.
