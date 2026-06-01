# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ |

## Reporting a Vulnerability

**Do not file a public issue.** Red-Team Harness tests LLM safety responses — vulnerabilities in the harness itself could be used to bypass safety evaluations, manipulate results, or access API keys.

Report vulnerabilities privately:
- GitHub: [Report a vulnerability](https://github.com/lukebancroft4-max/redteam_harness/security/advisories/new)
- Email: [security contact email placeholder]

We aim to respond within 48 hours and provide a resolution within 7 days.

## Scope

- API key exposure or leakage
- Result manipulation or injection
- Evasion of threshold/gate enforcement
- Command injection via CLI arguments or case files
- Supply chain issues in packaging (PyPI)

## Out of Scope

- Issues in the LLM being tested (that's what the harness is for)
- Social engineering
- Physical security
