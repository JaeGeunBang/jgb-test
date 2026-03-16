# 요구사항 문서

## 소개

Python 기반의 RAG(Retrieval-Augmented Generation) 챗봇 시스템입니다.
사용자가 문서를 업로드하면, 해당 문서를 벡터 DB에 저장하고, 사용자의 질문에 대해 관련 문서를 검색하여 LLM이 답변을 생성합니다.
CLI 또는 간단한 인터페이스를 통해 대화형으로 사용할 수 있습니다.

## 용어 정의

- **Chatbot**: 사용자의 질문을 받아 RAG 파이프라인을 통해 답변을 생성하는 시스템
- **Document_Loader**: 파일(PDF, TXT, Markdown 등)을 읽어 텍스트를 추출하는 컴포넌트
- **Text_Splitter**: 긴 텍스트를 일정 크기의 청크(chunk)로 분할하는 컴포넌트
- **Embedder**: 텍스트 청크를 벡터로 변환하는 컴포넌트
- **Vector_Store**: 벡터 임베딩을 저장하고 유사도 검색을 수행하는 컴포넌트
- **Retriever**: 사용자 질문과 관련된 청크를 Vector_Store에서 검색하는 컴포넌트
- **LLM**: 검색된 컨텍스트와 질문을 바탕으로 최종 답변을 생성하는 언어 모델
- **Chunk**: 문서를 분할한 텍스트 단위
- **Context**: Retriever가 검색한 관련 청크들의 집합

---

## 요구사항

### 요구사항 1: 문서 수집 및 인덱싱

**User Story:** 개발자로서, 로컬 문서 파일을 시스템에 등록하여 챗봇이 해당 내용을 기반으로 답변할 수 있도록 하고 싶다.

#### 인수 기준

1. WHEN 사용자가 파일 경로를 제공하면, THE Document_Loader SHALL TXT, PDF, Markdown 형식의 파일을 읽어 텍스트를 추출한다
2. IF 지원하지 않는 파일 형식이 제공되면, THEN THE Document_Loader SHALL 지원하지 않는 형식임을 나타내는 오류 메시지를 반환한다
3. IF 파일이 존재하지 않으면, THEN THE Document_Loader SHALL 파일을 찾을 수 없다는 오류 메시지를 반환한다
4. WHEN 텍스트 추출이 완료되면, THE Text_Splitter SHALL 텍스트를 최대 500자 단위의 청크로 분할하며, 청크 간 50자의 오버랩을 유지한다
5. WHEN 청크 분할이 완료되면, THE Embedder SHALL 각 청크를 벡터로 변환한다
6. WHEN 벡터 변환이 완료되면, THE Vector_Store SHALL 벡터와 원본 텍스트를 함께 저장한다

---

### 요구사항 2: 질문 기반 문서 검색

**User Story:** 개발자로서, 사용자의 질문과 관련된 문서 내용을 빠르게 검색하여 정확한 답변의 근거를 확보하고 싶다.

#### 인수 기준

1. WHEN 사용자가 질문을 입력하면, THE Retriever SHALL 질문을 벡터로 변환하여 Vector_Store에서 코사인 유사도 기준 상위 3개의 청크를 검색한다
2. WHILE Vector_Store에 저장된 문서가 없는 상태에서, THE Retriever SHALL 검색 가능한 문서가 없다는 안내 메시지를 반환한다
3. THE Retriever SHALL 검색된 각 청크와 함께 출처 파일명을 반환한다

---

### 요구사항 3: 답변 생성

**User Story:** 개발자로서, 검색된 문서 내용을 바탕으로 LLM이 자연스러운 답변을 생성하도록 하고 싶다.

#### 인수 기준

1. WHEN Retriever가 관련 청크를 반환하면, THE LLM SHALL 해당 청크를 컨텍스트로 포함한 프롬프트를 구성하여 답변을 생성한다
2. THE LLM SHALL 컨텍스트에 없는 내용에 대해 추측하지 않고, 제공된 문서에서 찾을 수 없다는 사실을 명시한다
3. WHEN LLM 호출이 실패하면, THE Chatbot SHALL 오류가 발생했음을 사용자에게 알리고 재시도를 안내한다

---

### 요구사항 4: 대화형 CLI 인터페이스

**User Story:** 개발자로서, 터미널에서 챗봇과 대화하며 기능을 테스트하고 싶다.

#### 인수 기준

1. THE Chatbot SHALL 터미널에서 실행 가능한 CLI 인터페이스를 제공한다
2. WHEN 사용자가 질문을 입력하면, THE Chatbot SHALL 3초 이내에 답변 생성을 시작한다 (LLM 응답 시간 제외)
3. WHEN 사용자가 `exit` 또는 `quit`을 입력하면, THE Chatbot SHALL 세션을 종료한다
4. THE Chatbot SHALL 대화 세션 내에서 이전 질문과 답변의 히스토리를 유지하여 문맥을 이어간다

---

### 요구사항 5: 설정 관리

**User Story:** 개발자로서, LLM 모델명, 임베딩 모델, 청크 크기 등의 설정을 코드 수정 없이 변경하고 싶다.

#### 인수 기준

1. THE Chatbot SHALL 설정값(LLM 모델명, 임베딩 모델명, 청크 크기, 청크 오버랩, 검색 결과 수)을 환경 변수 또는 `.env` 파일을 통해 읽는다
2. IF 필수 설정값(API 키 등)이 누락된 경우, THEN THE Chatbot SHALL 누락된 설정 항목을 명시하는 오류 메시지를 출력하고 종료한다
3. WHERE 설정값이 제공되지 않은 경우, THE Chatbot SHALL 사전 정의된 기본값을 사용한다
