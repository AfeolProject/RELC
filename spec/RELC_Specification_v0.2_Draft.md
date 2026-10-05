# AFEOL-RELC — Correctness-first rounding-explicit research model

**Version:** Draft 0.2 (2026-10-05)
**Profile:** RELC-CF-65537; no assigned security level
**Status:** Proposed mathematical research model; not a deployment specification
**Author:** Dragan Mitić
**License:** CC BY-SA 4.0

## 1. Scope and claims

This draft replaces the mathematical model in the December 2025 draft. It
removes its message-dependent hint and ineffective modular correction,
changes parameters, and embeds the message before the final compression.
This is a substantive redesign, not a correction of decimal constants alone.

The claim established here is deterministic decryption correctness under the
stated algebra, sampling support, and exact arithmetic. No IND-CPA, IND-CCA,
QROM, concrete attack-cost, constant-time, or production-security guarantee is
claimed. A functioning encryption/decryption model is not evidence of secrecy.
In particular, increasing q to obtain a correctness margin may make lattice
attacks easier. These parameters were selected for correctness, not hardness.

This construction follows the familiar module-LWE encryption pattern with
explicit compression errors. No priority or novelty claim is made.

## 2. Algebra and sampling

Let R = Z[X]/(X^256 + 1), and R_q = R/qR for q = 65537.
All polynomial products are negacyclic: X^256 = -1.
Let n = 256 and k = 3. Vectors have k polynomials; matrices have k by k
polynomials. Ring arithmetic is modulo q unless explicitly stated otherwise.

A is sampled uniformly from R_q^(k by k), independently of other randomness.
It is public and included in the mathematical public key. No seed expansion
algorithm or pseudorandomness reduction is specified by this draft.

CBD2 is the distribution a1 + a2 - b1 - b2 for four independent unbiased bits.
Every coefficient of s, e, r, e1, and e2 is sampled independently from CBD2.
Thus every such integer coefficient is in {-2,-1,0,1,2}; eta = 2.
Randomness for encryption is fresh. Messages are vectors m in {0,1}^256.
Security-oriented randomness and serialization are implementation obligations,
not supplied by the test-only verifier.

| Parameter | Value |
|---|---:|
| n | 256 |
| k | 3 |
| q | 65537 |
| eta | 2 |
| M_pk | 32768 |
| M_u | 32768 |
| M_v | 256 |
| message offset d = floor(q/2) | 32768 |

## 3. Exact operators

For an integer a, [a]_M is its unique representative in {0,...,M-1}.
Define center_M(a) by reducing first, then subtracting M if [a]_M > floor(M/2).
For even M this convention selects +M/2 at the midpoint.

For x in Z_q and z in Z_M:

    Round_M(x) = floor(M [x]_q / q + 1/2) mod M
    Lift_M(z)  = floor(q [z]_M / M + 1/2) mod q
    epsilon_M(x) = center_q(Lift_M(Round_M(x)) - [x]_q)

These operators act coefficientwise. Half-integer ties round upwards.
Implementations must use exact integer arithmetic, for example:

    Round_M(x) = ((2*M*[x]_q + q) // (2*q)) % M
    Lift_M(z)  = ((2*q*[z]_M + M) // (2*M)) % q

### 3.1 Uniform worst-case compression bound

On the q-circle, rounding Mx/q moves the scaled point by at most 1/2.
Scaling back moves the original point by at most q/(2M). Lifting then
introduces at most a further 1/2. The triangle inequality for circular distance
gives |epsilon_M(x)| <= q/(2M) + 1/2. Since epsilon_M(x) is an integer,

    |epsilon_M(x)| <= floor(q/(2M) + 1/2).

This applies to every input, irrespective of its probability distribution.
For the chosen parameters it gives E_pk = E_u = 1 and E_v = 128.
Exhaustive enumeration confirms that these maxima are attained.

### 3.2 Reproducible finite-domain statistics

Statistics below use a uniformly selected scalar x from {0,...,q-1}.
They do not assert that actual encryption inputs are uniformly distributed.
Let S1 = sum_x epsilon_M(x) and S2 = sum_x epsilon_M(x)^2. Then
mean = S1/q and population variance = S2/q - (S1/q)^2, exactly.

| q | M | max absolute error | S1 | S2 |
|---:|---:|---:|---:|---:|
| 65537 | 32768 | 1 | 1 | 32769 |
| 65537 | 256 | 128 | 128 | 357941248 |

No nonzero mean is replaced by zero. Correctness below uses worst-case bounds,
not means, variances, independence, or a concentration inequality.

## 4. Public-key encryption model

### Key generation

Sample A, s, e as specified in section 2. Set

    t = A s + e
    b = Round_M_pk(t)
    pk = (A, b)
    sk = s

### Encryption

For message m, sample r, e1, e2 as specified in section 2. Set

    a = A^T r + e1
    u = Round_M_u(a)
    w = <Lift_M_pk(b), r> + e2
    z = w + d m
    v = Round_M_v(z)
    ciphertext = (u, v)

The inner product is over R_q. There is no hint, auxiliary index set, or
message-dependent side information.

### Decryption

For each coefficient i compute

    y = Lift_M_v(v) - <Lift_M_u(u), s>  (mod q)
    D_q(a,b) = min([a-b]_q, [b-a]_q)
    m'_i = 0 if D_q(y_i,0) <= D_q(y_i,d), otherwise 1

The tie rule is explicit. Valid encryptions never reach a tie under the
correctness theorem. Behavior on malformed byte encodings is unspecified;
this is a mathematical model, not a wire protocol or CCA-secure API.

## 5. Error identity and deterministic correctness proof

Define compression errors in centered integer representation:

    epsilon_b = Lift_M_pk(b) - t          (mod q)
    epsilon_u = Lift_M_u(u) - a           (mod q)
    epsilon_v = Lift_M_v(v) - z           (mod q)

Their coefficient bounds are 1, 1, and 128 respectively. Expanding decryption,
using commutativity of R_q and <As,r> = <A^T r,s>, gives

    y = d m + N                              (mod q)
    N = <e,r> + <epsilon_b,r> - <e1,s>
        - <epsilon_u,s> + e2 + epsilon_v     (as an integer polynomial in R)

This is a modular identity. N is the integer lift formed by the displayed
sum; it need not be defined as the centered lift of a sum at intermediate steps.

For integer polynomials f,g in R, each coefficient of fg is a signed sum of
n products. Therefore ||fg||_infinity <= n ||f||_infinity ||g||_infinity.
For a k-term inner product the bound is k times that amount. Consequently,

    ||N||_infinity
      <= k*n*(eta^2 + E_pk*eta + eta^2 + E_u*eta) + eta + E_v
      = 3*256*(4 + 2 + 4 + 2) + 2 + 128
      = 9346.

The two message centers have circular distance d = 32768. If y is within B
of its correct center, its distance from the other center is at least d-B.
Since 2*9346 = 18692 < 32768, the correct center is strictly nearer.

**Correctness theorem.** For every public matrix, every choice of bounded
sampling coefficients allowed by section 2, and every message, exact execution
of section 4 returns m' = m. Thus the mathematical decryption-failure
probability is zero under these assumptions. This does not cover arithmetic
overflow, faulty sampling, altered algorithms, malformed inputs, or hardware
faults, and does not establish confidentiality or authenticity.

The theorem uses a uniform bound for all outcomes, not an empirical estimate
from successful trials. Randomized tests supplement the proof; they do not
replace it.

## 6. Security status and remaining work

No KEM is defined here. H, H', G, encapsulation, decapsulation, rejection,
serialization, and domain separation are not defined. No FO reduction or
QROM theorem is asserted. PKE security must be analyzed before considering
any KEM transform.

Required research includes a precise hardness assumption and reduction for
the compressed public key and ciphertext, concrete lattice-attack estimates
for these exact distributions, and independent cryptanalysis. A variance-only
Gaussian mapping cannot establish these claims. Removing the known hint
leak does not prove absence of other attacks.

An efficient implementation, matrix expansion, wire format, side-channel
analysis, parameter optimization, and interoperability tests are future work.
For deployed security use established, reviewed, standardized schemes.

## 7. Correction record for the December 2025 draft

The former q=3329, k=3, T=8 profile is withdrawn as a proposed secure model.
Its public hint marks hat_w in {3,5}. Since v = hat_w + 4m mod 8, an observer
reads m=0 from v in {3,5}, and m=1 from v in {7,1}, at every marked index.
Adding +/-8 before a modulo-8 decoder cannot change the decoded residue.
Neither defect is repaired by correcting statistics or merely raising k.

The corrected old finite-domain statistics are recorded for reproducibility:

| q | M | max absolute error | S1 | S2 | Exact population variance |
|---:|---:|---:|---:|---:|---|
| 3329 | 512 | 3 | 3 | 12041 | 40084480 / 11082241 |
| 3329 | 1024 | 2 | 2 | 3076 | 10240000 / 11082241 |
| 3329 | 8 | 208 | 208 | 48038016 | 159918512000 / 11082241 |

The old 2^-36 failure bound, <=1-bit QROM loss, proven CCA security, and
priority claim are withdrawn. Their appearance in historical commits is not
an endorsement. Git history preserves the original text.

## 8. Verification and references

Run with Python 3.10 or later, standard library only:

    python scripts/verify_model.py
    python -m unittest discover -s tests -v

The verifier checks exact scalar statistics for both profiles and exercises
the algebra and decoding of the replacement model. It is test software with
predictable randomness, not a cryptographic library.

Background, not proofs of this model:

- CRYSTALS-Kyber, Algorithm Specifications and Supporting Documentation v3.02:
  https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf
- Banerjee, Peikert, Rosen, Pseudorandom Functions and Lattices (2011):
  https://eprint.iacr.org/2011/401
- NIST FIPS 203, ML-KEM:
  https://csrc.nist.gov/pubs/fips/203/final
