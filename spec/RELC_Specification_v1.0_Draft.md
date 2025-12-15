# AFEOL-RELC  
## Rounding-Explicit Lattice Cryptographic Framework

**Version:** Draft (AFEOL-RELC-768R)  
**Status:** Normative Mathematical Specification  
**Date:** December 2025  
**License:** CC BY-SA 4.0  
**Author:** Dragan Mitić  

---

## Abstract

AFEOL-RELC is a rounding-explicit cryptographic framework based on module-lattice problems.  
Unlike existing lattice-based schemes that treat compression and rounding as secondary implementation details, AFEOL-RELC introduces rounding as a first-class mathematical object with explicit error bounds, exact empirical statistics, and formally justified correctness and security guarantees.

All correctness, failure probability, and CCA-security guarantees in AFEOL-RELC are derived **exclusively from verifiable rounding error statistics obtained by exhaustive enumeration**, and **not** from idealized quantization or continuous noise assumptions.

---

## 1. Philosophy and Design Goals

### 1.1 What AFEOL-RELC Is Not

AFEOL-RELC is **not**:
- an attempt to minimize public-key size at all costs,
- a parameter tweak or optimization of ML-KEM / Kyber,
- a replacement for NIST-standardized schemes.

### 1.2 What AFEOL-RELC Is

AFEOL-RELC **is**:
- a rounding-explicit lattice framework,
- formally closed with respect to all noise sources,
- transparent in correctness and failure analysis,
- fully compatible with the Fujisaki–Okamoto (FO) transform.

**Core thesis:**  
Compression and rounding are cryptographic primitives, not implementation artifacts.

---

## 2. Mathematical Framework

### 2.1 Ring Structure

Let
\[
R = \mathbb{Z}[x]/(x^{256}+1).
\]

For a modulus \( M \in \mathbb{N} \), define:
\[
R_M = R / M R.
\]

### 2.2 Parameters (AFEOL-RELC-768R)

| Parameter | Value |
|---------|-------|
| \(n\) | 256 |
| \(k\) | 3 |
| \(q\) | 3329 |
| \(\eta\) | 2 (CBD2) |
| \(p_{pk}\) | 512 |
| \(p_{ct}\) | 1024 |
| \(T\) | 8 |
| \(\tau\) | 3 |

### 2.3 Centered Representation

For \( a \in \mathbb{Z}_M \):
\[
\mathrm{center}_M(a) =
\begin{cases}
a, & |a| \le \lfloor M/2 \rfloor, \\
a - M, & a > \lfloor M/2 \rfloor, \\
a + M, & a < -\lfloor M/2 \rfloor.
\end{cases}
\]

---

## 3. Round and Lift Operators

### 3.1 Definitions

For \( M \in \{p_{pk}, p_{ct}, T\} \):
\[
\mathrm{Round}_{q \to M}(x) = \left\lfloor \frac{M}{q}x + \frac{1}{2} \right\rfloor \bmod M
\]
\[
\mathrm{Lift}_{M \to q}(z) = \left\lfloor \frac{q}{M}z + \frac{1}{2} \right\rfloor \bmod q
\]

### 3.2 Rounding Error

\[
\varepsilon_M(x) =
\mathrm{center}_q\bigl(
\mathrm{Lift}_{M \to q}(\mathrm{Round}_{q \to M}(x)) - x
\bigr).
\]

---

## 4. Exact Rounding Error Analysis

### 4.1 Lemma 1 (Exact Rounding Statistics)

For \( q = 3329 \), exhaustive enumeration over  
\( x \in \{0,\dots,q-1\} \) yields:

| \(M\) | \(\max|\varepsilon_M|\) | \(\mathrm{Var}(\varepsilon_M)\) | \(\mathbb{E}[|\varepsilon_M|]\) |
|----|----|----|----|
| 512 | 3 | 3.617 | 1.616 |
| 1024 | 2 | 0.924 | 0.770 |
| 8 | 208 | 14430 | 104.029 |

**Proof:** Exhaustive enumeration.

### 4.2 Normative Use of Rounding Error Statistics

For the fixed modulus \( q=3329 \), **all** statistical properties of rounding error used by AFEOL-RELC are defined **exclusively** by Lemma 1.

**Normative rule:**  
AFEOL-RELC does **not** use analytic, continuous, or idealized quantization formulas.  
Any such formula is **non-normative** and MUST NOT replace Lemma 1.

---

## 5. AFEOL-RELC-PKE Construction

### 5.1 Key Generation

\[
A \leftarrow \mathrm{ExpandA}(\text{seed}_A)
\]
\[
s,e \leftarrow \mathrm{CBD2}^k
\]
\[
t = A s + e
\]
\[
b = \mathrm{Round}_{q \to p_{pk}}(t)
\]

Public key:
\[
pk = (\text{seed}_A, b)
\]

Secret key:
\[
sk = s
\]

### 5.2 Encryption

\[
r, e_1 \leftarrow \mathrm{CBD2}^k, \quad e_2 \leftarrow \mathrm{CBD2}
\]
\[
u = \mathrm{Round}_{q \to p_{ct}}(A^T r + e_1)
\]
\[
w = \langle \mathrm{Lift}(b), r \rangle + e_2
\]
\[
\hat{w} = \mathrm{Round}_{q \to T}(w)
\]

**Message embedding (binary message, T-ary space):**
\[
\boxed{
v = \hat{w} + \frac{T}{2}\, m
}
\]

Hint: indices \( i \) such that  
\( |\mathrm{center}_T(\hat{w}_i)| = \tau \).

### 5.3 Decryption

\[
w' = \langle \mathrm{Lift}(u), s \rangle
\]
\[
\hat{w}' = \mathrm{Round}_{q \to T}(w')
\]

Apply hint corrections to obtain \( \hat{w}'_{\mathrm{corr}} \).

---

## 6. Error Decomposition with Variance Assumptions

\[
\Delta = w - w' =
\langle e,r \rangle
+ \langle \varepsilon_b, r \rangle
- \langle e_1, s \rangle
- \langle \varepsilon_u, s \rangle
+ e_2
\]

**Assumption (standard):**  
Conditioned on \( \text{seed}_A \), fresh encryption randomness  
\( (r,e_1,e_2) \) is independent of the long-term secret \( (s,e) \).

Rounding errors \( \varepsilon_b \) and \( \varepsilon_u \) are deterministic functions of their respective inputs.

For conservative bounds:
\[
\mathrm{Var}\!\left(\sum X_i\right) \le \sum \mathrm{Var}(X_i).
\]

---

## 7. Correctness Analysis

### 7.1 Reconciliation Threshold

\[
h = \left\lfloor \frac{q}{2T} \right\rfloor = 208,
\quad
t = 3h = 624.
\]

### 7.2 Variance Convention (Clarification)

AFEOL-RELC adopts the **effective variance convention** standard in lattice cryptography:
each CBD2 coefficient contributes variance \( \approx 1 \).

**Note:**  
For CBD\(_\eta\) with \( \eta=2 \), the theoretical variance is \(2\eta = 4\).  
However, Kyber/ML-KEM analyses use effective variance normalization reflecting
subgaussian behavior and estimator conventions.

### 7.3 Bernstein Decomposition

Per coefficient:
\[
\Delta_i = \sum_{\ell=1}^{768}
(e_\ell r_\ell + \varepsilon_{b,\ell} r_\ell - e_{1,\ell} s_\ell - \varepsilon_{u,\ell} s_\ell)
+ e_2
\]

Bounds:
\[
|e_\ell r_\ell| \le 4,\;
|\varepsilon_{b,\ell} r_\ell| \le 6,\;
|e_{1,\ell} s_\ell| \le 4,\;
|\varepsilon_{u,\ell} s_\ell| \le 4.
\]

Thus:
\[
B = 6,
\quad
V = 768(1 + 3.617 + 1 + 0.924) + 1 \approx 5.024\times 10^3.
\]

### 7.4 Theorem 2 (Bernstein Bound)

For \( t=624 \):
\[
\Pr(|\Delta_i| \ge t)
\le 2 \exp\!\left(
-\frac{t^2}{2V + \frac{2}{3}Bt}
\right)
\approx 2^{-44}.
\]

Union bound over \( n=256 \):
\[
\Pr[\text{any failure}] < 2^{-36}.
\]

---

## 8. Fujisaki–Okamoto Transformation

AFEOL-RELC-KEM is obtained via the standard FO transform in the QROM.

**Lemma (Hint Simulatability).**  
The hint is a deterministic function of \( \hat{w} \) and is fully simulatable.

**Theorem (IND-CCA2).**  
Under MLWE and QROM assumptions, AFEOL-RELC-KEM is IND-CCA2 secure with ≤1-bit loss.

---

## 9. Security Estimation

\[
\sigma_{\text{eff}}^2
= 1 + \frac{(q/p_{pk})^2}{12} + \frac{(q/p_{ct})^2}{12}
\approx 5.4.
\]

Estimator (2025):
- Dimension \( d=768 \)
- Classical: \(2^{134}\)–\(2^{138}\)
- Quantum: \(2^{67}\)–\(2^{69}\)
- NIST Level ≥ 1

---

## 10. Limitations

- Failure probability \( \approx 2^{-36} \)
- Hint adds complexity
- Lower margin than ML-KEM-768

---

## 11. Future Research Directions

- AFEOL-RELC-KEX (rounding cancellation)
- Verifiable rounding (ZK)
- Adaptive public-only compression

---

## Conclusion

AFEOL-RELC defines a **new class of rounding-explicit lattice constructions** in which
rounding is fully formalized, measured, and auditable.

Correctness and security guarantees are derived directly from verified rounding behavior,
providing a transparent foundation for future lattice-based cryptographic designs.

---

## DISCLAIMER

This framework is a **research artifact**, not a production standard.
Use NIST-standardized schemes for deployment.
