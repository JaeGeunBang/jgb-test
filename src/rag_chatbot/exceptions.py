class RagChatbotError(Exception):
    """Base exception for all RAG chatbot errors."""


class UnsupportedFormatError(RagChatbotError):
    """Raised when a file with an unsupported format is provided."""


class EmptyStoreError(RagChatbotError):
    """Raised when a search is attempted on an empty vector store."""


class LLMError(RagChatbotError):
    """Raised when an LLM API call fails."""


class ConfigError(RagChatbotError):
    """Raised when required configuration values are missing."""
