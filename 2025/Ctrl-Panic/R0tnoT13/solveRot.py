from z3 import *
# Leaked values: k -> S xor ROTR(S, k)
leaks = {
    8: 183552667878302390742187834892988820241,
    4: 303499033263465715696839767032360064630,
    16: 206844958160238142919064580247611979450,
    2: 163378902990129536295589118329764595602,
    64: 105702179473185502572235663113526159091,
    32: 230156190944614555973250270591375837085,
}
solver = Solver()

# 128-bit internal state
S = [Bool(f"S_{i}") for i in range(128)]

# Anchor bits
solver.add(S[0] == True)
solver.add(S[127] == False)

def get_bit(x, i):
    return (x >> i) & 1

# Add equations
for k, value in leaks.items():
    for i in range(128):
        bit = get_bit(value, i)
        solver.add(Xor(S[i], S[(i + k) % 128]) == BoolVal(bit == 1))

assert solver.check() == sat
model = solver.model()

# Rebuild S
state = 0
for i in range(128):
    if model[S[i]]:
        state |= (1 << i)

print(f"Recovered S: {hex(state)}")
