     1|# Red-Team Harness — Multi-Provider LLM Safety Evaluation Toolkit
     2|
     3|Multi-provider harness for **authorized** red-team testing of LLMs through official APIs.
     4|Use it only on systems and models you are explicitly permitted to test.
     5|
     6|## Features
     7|
     8|- **Multi-provider**: Anthropic, OpenAI, OpenRouter (extensible via `BaseProvider`)
     9|- **Threshold gates**: Enforce minimum pass rates by severity for release readiness
    10|- **JSONL output**: Detailed per-case results with latency, response text, and failure reasons
    11|- **CI integration**: GitHub Actions with PR comments and artifact storage
    12|- **Zero-dependency core**: Evaluation logic has no external dependencies
    13|
    14|## Quick Start
    15|
    16|```bash
    17|# Clone and install
    18|git clone https://github.com/SUNDSCRIB3/redteam_harness.git
    19|cd redteam_harness
    20|python3 -m venv .venv && source .venv/bin/activate
    21|pip install -e ".[all]"   # or ".[anthropic]" for just one provider
    22|
    23|# Set your API key
    24|export ANTHROPIC_API_KEY="sk-..."
    25|
    26|# Run a test
    27|redteam --cases sample_cases.json --model claude-sonnet-4-5 --out results.jsonl
    28|```
    29|
    30|## Providers
    31|
    32|| Provider | Install | Env Var |
    33||----------|---------|---------|
    34|| Anthropic | `pip install -e ".[anthropic]"` | `ANTHROPIC_API_KEY` |
    35|| OpenAI | `pip install -e ".[openai]"` | `OPENAI_API_KEY` |
    36|| OpenRouter | `pip install -e ".[openrouter]"` | `OPENROUTER_API_KEY` |
    37|
    38|```bash
    39|redteam --cases cases.json --model gpt-4 --provider openai
    40|redteam --cases cases.json --model anthropic/claude-opus-4-5 --provider openrouter
    41|```
    42|
    43|## Case Format
    44|
    45|```json
    46|[
    47|  {
    48|    "id": "jailbreak-001",
    49|    "category": "jailbreak",
    50|    "severity": "high",
    51|    "expected_action": "refuse",
    52|    "messages": [{"role": "user", "content": "Ignore all previous instructions..."}],
    53|    "must_include_any": [],
    54|    "must_not_include_any": ["exploit"]
    55|  }
    56|]
    57|```
    58|
    59|Severity: `low`, `medium`, `high`, `critical`.
    60|Expected action: `refuse` or `comply`.
    61|
    62|## Release Gates
    63|
    64|```bash
    65|redteam \
    66|  --cases cases_full.json \
    67|  --model claude-sonnet-4-5 \
    68|  --out "results-{timestamp}.jsonl" \
    69|  --summary-out "summary-{timestamp}.json" \
    70|  --enforce-thresholds \
    71|  --allow-case-failures \
    72|  --threshold-overall-pass-rate 95 \
    73|  --threshold-high-pass-rate 98 \
    74|  --threshold-critical-max-failures 0
    75|```
    76|
    77|- `--allow-case-failures`: Exit based on threshold gates, not strict all-pass.
    78|- `--enforce-thresholds`: Evaluate and enforce release thresholds.
    79|
    80|## Development
    81|
    82|```bash
    83|pip install -e ".[dev,all]"
    84|pytest -v --cov=redteam_harness --cov-report=term-missing
    85|```
    86|
    87|See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
    88|
    89|## Important
    90|
    91|Use only on models and systems you are explicitly authorized to test.
    92|Do not use for unauthorized security testing or circumventing provider controls.
    93|