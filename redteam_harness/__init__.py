"""Red-Team Harness — multi-provider LLM safety evaluation toolkit."""

from .core import CaseResult, load_cases, evaluate_case, summarize, severity_rate, severity_failed_count
from .providers import get_provider, list_providers, register_provider

__version__ = "0.1.0"
