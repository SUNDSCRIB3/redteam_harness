# Contributing to Red-Team Harness

Thanks for helping make LLMs safer! Red-Team Harness is a multi-provider safety evaluation toolkit for testing language models against jailbreak, bias, and compliance scenarios.

## Getting started

```bash
git clone https://github.com/lukebancroft4-max/redteam_harness.git
cd redteam_harness
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,all]"
pytest
```

## How to contribute

### Add a new provider

1. Subclass `BaseProvider` in `redteam_harness/providers/__init__.py`
2. Decorate with `@register_provider("provider-name")`
3. Add tests in `tests/test_providers.py`
4. Update `pyproject.toml` with the optional dependency group

### Add test cases

Test cases are JSON arrays. Create a new `.json` file with entries like:

```json
[
  {
    "id": "unique-id",
    "category": "jailbreak | bias | compliance | capability",
    "severity": "low | medium | high | critical",
    "expected_action": "refuse | comply",
    "messages": [
      {"role": "user", "content": "Test prompt here"}
    ],
    "must_include_any": ["required string"],
    "must_not_include_any": ["forbidden string"]
  }
]
```

### Detection logic improvements

The `core.py` module handles:
- `REFUSAL_MARKERS` — strings indicating refusal
- `NEGATION_MARKERS` — strings indicating negation context
- `is_refusal_like()` — refusal pattern detection
- `has_forbidden_term_in_unsafe_context()` — forbidden content detection

Add new markers or improve regex patterns to catch more refusal variants.

## Testing

```bash
pytest -v --cov=redteam_harness --cov-report=term-missing
```

All contributions should include tests. Target 90%+ coverage.

## Code style

- Python 3.9+ compatible
- Type hints on public APIs
- Docstring summaries on classes and functions
- 4-space indent, no trailing whitespace
