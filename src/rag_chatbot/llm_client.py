from .exceptions import LLMError
from .models import Config, SearchResult

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions based solely on the provided context. "
    "Do not speculate or use knowledge outside of the given context. "
    "If the answer cannot be found in the context, say so clearly."
)


class LLMClient:
    def __init__(self, config: Config) -> None:
        self._config = config
        if config.llm_provider == "anthropic":
            from anthropic import Anthropic
            self._anthropic = Anthropic(api_key=config.anthropic_api_key)
        else:
            from openai import OpenAI
            self._openai = OpenAI(api_key=config.openai_api_key)

    def generate(self, question: str, context: list[SearchResult]) -> str:
        context_text = "\n\n".join(
            f"[출처: {r.source}]\n{r.text}" for r in context
        )
        user_message = f"Context:\n{context_text}\n\nQuestion: {question}"

        if self._config.llm_provider == "anthropic":
            return self._generate_anthropic(user_message)
        return self._generate_openai(user_message)

    def _generate_openai(self, user_message: str) -> str:
        from openai import OpenAIError
        try:
            response = self._openai.chat.completions.create(
                model=self._config.llm_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            raise LLMError(f"LLM API 호출에 실패했습니다: {e}") from e

    def _generate_anthropic(self, user_message: str) -> str:
        from anthropic import AnthropicError
        try:
            response = self._anthropic.messages.create(
                model=self._config.anthropic_model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
            return response.content[0].text
        except AnthropicError as e:
            raise LLMError(f"Anthropic API 호출에 실패했습니다: {e}") from e
