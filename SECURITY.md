# Security Policy

## Status

RELC (AFEOL RELC) is a **research-only cryptographic framework**.

This repository contains **normative mathematical specifications and analysis**
of rounding-explicit lattice constructions.  
It is **NOT production software** and **MUST NOT** be used in real-world
security-critical systems.

No guarantees are made regarding:
- implementation security,
- side-channel resistance,
- constant-time behavior,
- resistance to practical attacks.

## Supported Versions

There are **no supported production versions**.

All versions, including tagged drafts, are provided **for academic research,
review, and discussion only**.

## Reporting Security Issues

If you discover a potential issue related to:
- mathematical correctness,
- security assumptions,
- failure probability analysis,
- rounding or noise modeling errors,

please report it **privately**.

### Contact

**Email:** afeol@proton.me  
**Subject:** `RELC Security Report`

Please include:
- a clear description of the issue,
- affected section(s) of the specification,
- any supporting analysis or references.

## Coordinated Disclosure

Best-effort coordinated disclosure is supported for **specification-level
issues**.  
There are no guaranteed response or remediation timelines.

## Disclaimer

This project has **not undergone independent cryptographic review,
formal standardization, or certification**.

For production use, refer to **NIST-standardized schemes** such as ML-KEM.
