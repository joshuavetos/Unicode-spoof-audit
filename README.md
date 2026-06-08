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

- 1,900 generated variants
- Homoglyph substitutions
- Mixed-script variants
- BiDi controls
- Invisible characters
- Combining marks

## Benchmark Results

| Metric | Result |
| --- | --- |
| Generated variants | 1,900 |
| Mixed-script detection | 1,523 |
| Rejected variants | 1,867 |
| Risk-flagged variants | 25 |
| Aggregate coverage | 99.58% |
| Residual unflagged variants | 8 |

### Residual Unflagged Variants

These 8 variants are the current residual audit artifacts: they pass the advisory display-name checks even though they remain distinct from `Admin` at the byte level. They are not accepted by the strict identifier policy, which rejects them under the ASCII allowlist; the residual is specific to display-name analysis.

| Variant | Escaped form | UTF-8 hex | Why it remains unflagged | Audit significance |
| --- | --- | --- | --- | --- |
| `Аԁміп` | `\u0410\u0501\u043c\u0456\u043f` | `d090d481d0bcd196d0bf` | All letters classify as Cyrillic, so the mixed-script detector sees one significant script and no layout or combining controls. | Fully Cyrillic visual spoof of `Admin`; demonstrates that same-script homoglyph strings can evade mixed-script heuristics. |
| `Аԁⅿіп` | `\u0410\u0501\u217f\u0456\u043f` | `d090d481e285bfd196d0bf` | Cyrillic letters plus a Roman numeral compatibility character; the numeral is treated as Common, and compatibility normalization is only recorded as a flag, not a rejection. | Shows that compatibility-normalized symbols can combine with a single-script spoof without crossing a rejection threshold. |
| `Аⅾміп` | `\u0410\u217e\u043c\u0456\u043f` | `d090e285bed0bcd196d0bf` | Cyrillic letters plus one Roman numeral compatibility character; the display scorer records compatibility normalization but still approves it. | Same-script spoof with one Common-script compatibility symbol replacing a Latin-looking letter. |
| `Аⅾⅿіп` | `\u0410\u217e\u217f\u0456\u043f` | `d090e285bee285bfd196d0bf` | Cyrillic letters plus two Roman numeral compatibility characters; the Common-script numerals do not trigger mixed-script rejection. | Multi-symbol compatibility spoof that still looks close to `Admin` while avoiding layout, combining, and mixed-script rejection. |
| `ᎪⅾⅿᎥո` | `\u13aa\u217e\u217f\u13a5\u0578` | `e18eaae285bee285bfe18ea5d5b8` | Cherokee and Armenian code points are currently classified as Unknown, while the Roman numerals are Common; this leaves one significant script family after filtering. | Highlights script-classification coverage gaps outside Latin, Cyrillic, Greek, and CJK-family scripts. |
| `Admin🏻` | `Admin\U0001f3fb` | `41646d696ef09f8fbb` | The Fitzpatrick emoji modifier is category `Sk`, classified as Common, and is not a layout, illegal-category, combining, or mixed-script trigger. | Demonstrates that standalone emoji modifiers appended to protected-looking text remain approved as display metadata. |
| `Admin🏽` | `Admin\U0001f3fd` | `41646d696ef09f8fbd` | The Fitzpatrick emoji modifier is category `Sk`, classified as Common, and does not alter the Latin-only significant script set. | Same as above for a second skin-tone modifier. |
| `Admin🏻🏽` | `Admin\U0001f3fb\U0001f3fd` | `41646d696ef09f8fbbf09f8fbd` | Both emoji modifiers are Common-script symbols, so the value remains Latin-only for significant-script purposes. | Shows that multiple appended emoji modifiers remain unflagged when no rejected control or combining characters are present. |

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
