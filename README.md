# RELC — Rounding-Explicit Lattice Cryptographic Framework

**Status:** Draft  
**Version:** AFEOL-RELC-768R  
**Author:** Dragan Mitić  
**License:** CC BY-SA 4.0  

RELC (AFEOL RELC) is a rounding-explicit cryptographic framework based on
module-lattice constructions.

Unlike conventional lattice schemes that treat compression and rounding
as implementation details, RELC models rounding as a first-class
cryptographic primitive with:

- exact empirical error statistics,
- formally bounded correctness,
- explicit failure probability,
- and provable CCA security via the FO transform.

## Repository Structure

RELC/
├── spec/ # Normative mathematical specification
├── docs/ # Explanatory documents (future)
├── reference/ # Reference material and papers
├── scripts/ # Verification & analysis scripts
└── tests/ # Correctness / failure simulations


## Canonical Specification

The authoritative specification is located at:

spec/RELC_Specification_v1.0_Draft.md


## Disclaimer

This project is a research artifact.
It is **not production software** and has not undergone
independent cryptographic review or standardization.

For production use, consult NIST-standardized schemes such as ML-KEM.
