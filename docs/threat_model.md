# Threat Model

Unicode spoofing can create visually deceptive identifiers that appear to match protected names while remaining distinct at the code-point and byte levels.

Primary risks include identity spoofing, reviewer deception, phishing, impersonation, and attempted reserved-name validation bypasses. This repository does not model privilege escalation; escalation would require a downstream authorization system that incorrectly grants authority based on a spoofed identifier.
