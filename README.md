# RELC — Rounding-Explicit Lattice Cryptographic Research

**Status:** Proposed research draft 0.2; not production software
**Author:** Dragan Mitić
**License:** CC BY-SA 4.0

RELC studies explicit rounding errors in module-lattice encryption models.
The current proposal is a correctness-first redesign with no public hint.
It contains a worst-case proof of decryption correctness for a conservative
parameter profile, plus reproducible scalar statistics and test software.

It has no assigned security level and no established IND-CPA, IND-CCA, or QROM
security guarantee. Correct decryption does not imply secure encryption.
The increased modulus was chosen for correctness; its hardness needs review.

## Specification

[Draft 0.2](spec/RELC_Specification_v0.2_Draft.md) is the current proposal.
The December 2025 draft is withdrawn: its hint exposes message bits, its
correction is ineffective, and its numerical/security claims require correction.
The replacement document includes a correction record; Git history preserves
the previous text.

## Repository

- `spec/`: specification and withdrawal notice
- `scripts/verify_model.py`: exact-arithmetic, test-only verifier
- `tests/`: mathematical regression tests
- `SECURITY.md`: research-only security policy

## Verify

Python 3.10 or later; no third-party dependencies:

```sh
python scripts/verify_model.py
python -m unittest discover -s tests -v
```

The verifier uses predictable randomness for reproducibility. It is not an
implementation suitable for encrypting actual data. Independent cryptanalysis,
security reductions, concrete attack estimates, and implementation review remain
open. For production use, consult standardized schemes such as ML-KEM.
