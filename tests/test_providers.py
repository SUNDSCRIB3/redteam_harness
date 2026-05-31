"""Tests for provider abstraction."""

import pytest
from redteam_harness.providers import get_provider, list_providers, AnthropicProvider, OpenAIProvider, OpenRouterProvider


class TestProviderRegistry:
    def test_list_providers(self):
        providers = list_providers()
        assert "anthropic" in providers
        assert "openai" in providers
        assert "openrouter" in providers

    def test_get_anthropic(self):
        p = get_provider("anthropic")
        assert isinstance(p, AnthropicProvider)

    def test_get_openai(self):
        p = get_provider("openai")
        assert isinstance(p, OpenAIProvider)

    def test_get_openrouter(self):
        p = get_provider("openrouter")
        assert isinstance(p, OpenRouterProvider)

    def test_get_unknown(self):
        with pytest.raises(ValueError, match="Unknown provider"):
            get_provider("nonexistent")


class TestAnthropicProvider:
    def test_init_with_key(self):
        p = AnthropicProvider(api_key="test-key")
        assert p.api_key == "test-key"

    def test_init_from_env(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "env-key")
        p = AnthropicProvider()
        assert p.api_key == "env-key"


class TestOpenAIProvider:
    def test_init_with_key(self):
        p = OpenAIProvider(api_key="test-key")
        assert p.api_key == "test-key"

    def test_init_from_env(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "env-key")
        p = OpenAIProvider()
        assert p.api_key == "env-key"


class TestOpenRouterProvider:
    def test_init_with_key(self):
        p = OpenRouterProvider(api_key="test-key")
        assert p.api_key == "test-key"

    def test_init_from_env(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "env-key")
        p = OpenRouterProvider()
        assert p.api_key == "env-key"

    def test_custom_base_url(self):
        p = OpenRouterProvider(api_key="test", base_url="https://custom.example.com/api/v1")
        assert p.base_url == "https://custom.example.com/api/v1"
