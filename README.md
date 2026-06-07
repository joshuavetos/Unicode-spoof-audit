# Unicode Spoof Audit

Unicode Spoof Audit is a reproducible harness for generating Unicode spoofing corpora and evaluating policy controls for security-sensitive identifiers and non-authoritative display names.

## Threat Model

Visually deceptive identifiers can bypass human review while remaining distinct at the byte level. A protected identifier such as `Admin` can be imitated with characters such as Cyrillic `а`, producing a string that looks similar to a person but is not byte-identical.

This project evaluates defensive boundaries rather than privilege escalation. Authorization must never be granted by visual similarity, display-name analysis, or advisory risk scoring.

## Policy Boundaries

1. **Strict identifier policy** for usernames, service accounts, slugs, internal IDs, and other authoritative identifiers.
   - Allows only `[A-Za-z0-9_-]`.
   - Rejects reserved names after casefold normalization.
   - Rejects all Unicode outside the ASCII allowlist.
2. **Display-name policy** for profile metadata and user-facing labels.
   - Allows Unicode when it is not an authority gate.
   - Rejects BiDi and invisible layout controls.
   - Rejects dangerous Unicode categories.
   - Rejects mixed-script labels except common CJK-family combinations.
   - Flags combining marks as advisory risk.

## Reproduction Steps

```bash
python examples/generate_corpus.py
python examples/run_audit.py
python examples/benchmark_all.py
```

Generated corpus data is written to `corpus/generated/admin_spoof_corpus.json`.

## Representative Results

| Input | Identifier Policy | Display Policy |
| --- | --- | --- |
| `Admin` | Rejected: reserved identity collision | Rejected: reserved identity collision |
| `admіn` | Rejected: strict ASCII allowlist violation | Rejected: mixed-script composition |
| `Josh_90` | Secure | Approved |
| `共有` | Rejected: strict ASCII allowlist violation | Approved |
| `José` | Rejected: strict ASCII allowlist violation | Risk flagged: combining mark |
| `abc‮txt` | Rejected: strict ASCII allowlist violation | Rejected: layout control |
