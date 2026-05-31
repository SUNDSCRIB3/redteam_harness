"""Provider abstraction for multi-LLM support."""

from abc import ABC, abstractmethod
from typing import Any

# Registry of provider implementations
_PROVIDERS: dict[str, type["BaseProvider"]] = {}


class BaseProvider(ABC):
    """Abstract base for LLM providers."""

    @abstractmethod
    def create_completion(self, *,
        model: str,
        messages: list[dict[str, Any]],
        system: str | None = None,
        max_tokens: int = 512,
        temperature: float = 0.0,
    ) -> str:
        """Send a completion request and return the response text."""


def register_provider(name: str) -> callable:
    """Decorator to register a provider implementation."""
    def decorator(cls: type[BaseProvider]) -> type[BaseProvider]:
        _PROVIDERS[name] = cls
        return cls
    return decorator


def get_provider(name: str, **kwargs) -> BaseProvider:
    """Get a provider instance by name."""
    if name not in _PROVIDERS:
        raise ValueError(f"Unknown provider: {name}. Available: {list(_PROVIDERS.keys())}")
    return _PROVIDERS[name](**kwargs)


def list_providers() -> list[str]:
    """List all registered providers."""
    return list(_PROVIDERS.keys())


# === Built-in Providers ===

@register_provider("anthropic")
class AnthropicProvider(BaseProvider):
    """Anthropic Messages API provider."""

    def __init__(self, api_key: str | None = None):
        import os
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")

    def create_completion(self, *, model, messages, system=None, max_tokens=512, temperature=0.0):
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system or "",
            messages=messages,
        )
        chunks = []
        for block in getattr(resp, "content", []):
            if getattr(block, "type", None) == "text":
                chunks.append(block.text)
        return "\n".join(chunks).strip()


@register_provider("openai")
class OpenAIProvider(BaseProvider):
    """OpenAI Chat Completions API provider."""

    def __init__(self, api_key: str | None = None):
        import os
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")

    def create_completion(self, *, model, messages, system=None, max_tokens=512, temperature=0.0):
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        formatted_messages = []
        if system:
            formatted_messages.append({"role": "system", "content": system})
        formatted_messages.extend(messages)
        resp = client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()


@register_provider("openrouter")
class OpenRouterProvider(BaseProvider):
    """OpenRouter API provider (3rd-party API gateway)."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        import os
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = base_url or "https://openrouter.ai/api/v1"

    def create_completion(self, *, model, messages, system=None, max_tokens=512, temperature=0.0):
        from openai import OpenAI
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        formatted_messages = []
        if system:
            formatted_messages.append({"role": "system", "content": system})
        formatted_messages.extend(messages)
        resp = client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()
