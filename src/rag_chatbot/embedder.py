import json

from .models import Config


class Embedder:
    def __init__(self, config: Config) -> None:
        self._config = config
        if config.llm_provider == "bedrock":
            import boto3
            self._bedrock = boto3.client(
                "bedrock-runtime", region_name=config.aws_region
            )
        else:
            from openai import OpenAI
            self._openai = OpenAI(api_key=config.openai_api_key)

    def embed(self, text: str) -> list[float]:
        if self._config.llm_provider == "bedrock":
            return self._embed_bedrock(text)
        return self._embed_openai(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        # Bedrock Titan은 배치 API가 없으므로 개별 호출
        return [self.embed(t) for t in texts]

    def _embed_openai(self, text: str) -> list[float]:
        response = self._openai.embeddings.create(
            model=self._config.embedding_model,
            input=text,
        )
        return response.data[0].embedding

    def _embed_bedrock(self, text: str) -> list[float]:
        body = json.dumps({"inputText": text})
        response = self._bedrock.invoke_model(
            modelId=self._config.bedrock_embedding_model,
            body=body,
            contentType="application/json",
            accept="application/json",
        )
        result = json.loads(response["body"].read())
        return result["embedding"]
