# Unicode Spoof Audit

Generate Unicode spoofing corpora, benchmark detection strategies, and evaluate identifier security policies against reproducible attack surfaces.

## Overview

Unicode Spoof Audit tests a common interface-trust failure:

A string can look identical or highly similar to a human reviewer while remaining different at the byte level.

Example:

```text
Admin
Admаn
```

The second string contains a Cyrillic `а` (`U+0430`) instead of a Latin `a` (`U+0061`).

This repository provides tooling to:

- Generate Unicode spoof corpora
- Measure detector coverage
- Benchmark detector cost
- Compare heuristic detection against deterministic prevention
- Evaluate identifier security policies

## Current Corpus

Generated from the protected identifier:

```text
Admin
```

Current benchmark corpus:

- 1,771 generated variants
- Homoglyph substitutions
- Mixed-script variants
- BiDi controls
- Invisible characters
- Combining marks

## Benchmark Results

| Metric | Result |
| --- | --- |
| Generated variants | 1,771 |
| Mixed-script detection | 1,523 |
| Rejected variants | 1,738 |
| Risk-flagged variants | 25 |
| Aggregate coverage | 99.55% |
| Residual unflagged variants | 8 |

### Runtime

| Configuration | Runtime |
| --- | --- |
| Script + skeleton | ~0.0147s |
| Script + skeleton + edit distance | ~0.1540s |

Observed edit-distance overhead:

```text
947.57%
```

## Security Model

### Strict Identifier Policy

Used for:

- Usernames
- Service accounts
- Routing slugs
- Internal IDs
- Other authoritative identifiers

Allowed character set:

```text
[A-Za-z0-9_-]
```

Policy behavior:

- Reject all Unicode outside the allowlist
- Reject reserved identities after NFKC canonical normalization
- Treat identifiers as the authoritative security boundary

### Display Name Policy

Used for:

- Display names
- Profile labels
- User-facing metadata

Policy behavior:

- Allow Unicode
- Reject BiDi controls
- Reject invisible layout controls
- Reject dangerous Unicode categories
- Reject NFKC compatibility collisions with reserved identities
- Reject mixed-script compositions
- Flag combining marks

Display names are not authority-bearing identifiers.

## Example Results

| Input | Identifier Policy | Display Policy |
| --- | --- | --- |
| `Admin` | Rejected | Rejected |
| `admіn` | Rejected | Rejected |
| `Josh_90` | Secure | Approved |
| `共有` | Rejected | Approved |
| `José` | Rejected | Risk flagged |
| `abc‮txt` | Rejected | Rejected |

## Repository Layout

```text
unicode-spoof-audit/
├── benchmarks/
├── corpus/
├── detectors/
├── docs/
├── examples/
├── tests/
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Quick Start

Generate the corpus:

```bash
python examples/generate_corpus.py
```

Run the audit:

```bash
python examples/run_audit.py
```

Run benchmarks:

```bash
python examples/benchmark_all.py
```

Generated corpus output:

```text
corpus/generated/admin_spoof_corpus.json
```

## Scope

Coverage metrics apply only to the generated corpus used during this audit.

Results should not be interpreted as measurements of:

- All Unicode spoofing techniques
- All fonts
- All rendering engines
- All browsers
- All user interfaces
- All possible identifiers

## License

See `LICENSE`.
