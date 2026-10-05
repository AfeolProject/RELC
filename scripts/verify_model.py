"""Exact-arithmetic research verifier. NOT a cryptographic implementation.

Predictable test randomness; no serialization, secure RNG, or side-channel
protection. Functions model equations in Draft 0.2, not a deployment API.
License: CC BY-SA 4.0, consistent with this research repository.
"""
from fractions import Fraction
from random import Random

N, K, Q, ETA, M_PK, M_U, M_V = 256, 3, 65537, 2, 32768, 32768, 256
D = Q // 2
BOUND = K * N * (ETA**2 + ETA + ETA**2 + ETA) + ETA + 128


def center(x, modulus):
    x %= modulus
    return x - modulus if x > modulus // 2 else x


def round_to(x, q, modulus):
    return ((2 * modulus * (x % q) + q) // (2 * q)) % modulus


def lift(z, q, modulus):
    return ((2 * q * (z % modulus) + modulus) // (2 * modulus)) % q


def error(x, q, modulus):
    return center(lift(round_to(x, q, modulus), q, modulus) - x, q)


def statistics(q, modulus):
    errors = [error(x, q, modulus) for x in range(q)]
    s1, s2 = sum(errors), sum(x*x for x in errors)
    return (max(map(abs, errors)), s1, s2,
            Fraction(s2, q) - Fraction(s1, q)**2)


def ring_mul(a, b, q=Q):
    """Negacyclic convolution, arbitrary-precision integers, then mod q."""
    assert len(a) == len(b) == N
    out = [0] * N
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            t = i + j
            if t >= N:
                out[t-N] -= x*y
            else:
                out[t] += x*y
    return [x % q for x in out]


def inner(a, b):
    out = [0] * N
    for x, y in zip(a, b):
        out = [u+v for u, v in zip(out, ring_mul(x, y))]
    return [x % Q for x in out]


def cbd(rng, count=N):
    return [sum(rng.randrange(2) for _ in range(ETA))
            - sum(rng.randrange(2) for _ in range(ETA)) for _ in range(count)]


def decode(y):
    def distance(a, b):
        return min((a-b) % Q, (b-a) % Q)
    return int(distance(y, D) < distance(y, 0))


def trial(rng):
    A = [[[rng.randrange(Q) for _ in range(N)] for _ in range(K)]
         for _ in range(K)]
    s, e, r, e1 = [[cbd(rng) for _ in range(K)] for _ in range(4)]
    e2, message = cbd(rng), [rng.randrange(2) for _ in range(N)]
    t = [[(x+y) % Q for x,y in zip(inner(row,s), noise)]
         for row,noise in zip(A,e)]
    b = [[round_to(x,Q,M_PK) for x in row] for row in t]
    a = [[(x+y) % Q for x,y in zip(inner([A[i][j] for i in range(K)],r), e1[j])]
         for j in range(K)]
    u = [[round_to(x,Q,M_U) for x in row] for row in a]
    lb = [[lift(x,Q,M_PK) for x in row] for row in b]
    lu = [[lift(x,Q,M_U) for x in row] for row in u]
    w = [(x+y) % Q for x,y in zip(inner(lb,r),e2)]
    z = [(x+D*m) % Q for x,m in zip(w,message)]
    v = [round_to(x,Q,M_V) for x in z]
    lv = [lift(x,Q,M_V) for x in v]
    y = [(x-u) % Q for x,u in zip(lv,inner(lu,s))]
    epsb = [[center(x-y,Q) for x,y in zip(row,original)]
            for row,original in zip(lb,t)]
    epsu = [[center(x-y,Q) for x,y in zip(row,original)]
            for row,original in zip(lu,a)]
    epsv = [center(x-y,Q) for x,y in zip(lv,z)]
    er, br, es, us = inner(e,r), inner(epsb,r), inner(e1,s), inner(epsu,s)
    residual = [(er[i]+br[i]-es[i]-us[i]+e2[i]+epsv[i]) % Q for i in range(N)]
    assert all((y[i]-D*message[i]) % Q == residual[i] for i in range(N))
    assert max(abs(center(x,Q)) for x in residual) <= BOUND
    assert [decode(x) for x in y] == message
    return max(abs(center(x,Q)) for x in residual)


def verify():
    expected = {(3329,512):(3,3,12041), (3329,1024):(2,2,3076),
                (3329,8):(208,208,48038016),
                (Q,M_PK):(1,1,32769), (Q,M_V):(128,128,357941248)}
    for (q,modulus), values in expected.items():
        result = statistics(q,modulus)
        assert result[:3] == values
        print(f'q={q} M={modulus}: max={result[0]} S1={result[1]} '
              f'S2={result[2]} variance={result[3]}')
    assert BOUND == 9346 and 2*BOUND < D
    # All allowed scalar residuals, both message centers; supplements the proof.
    for bit in (0,1):
        assert all(decode(D*bit+noise) == bit for noise in range(-BOUND,BOUND+1))
    rng = Random(20261005)
    observed = max(trial(rng) for _ in range(8))
    print(f'Correctness margin: B={BOUND}; 2B={2*BOUND} < d={D}.')
    print(f'8 seeded polynomial trials passed; maximum observed residual={observed}.')
    print('Mathematical regression checks passed. No security claim established.')


if __name__ == '__main__':
    verify()
