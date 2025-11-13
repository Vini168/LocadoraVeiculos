import math
from math import sqrt

def sample_size_two_prop(p1, p2, alpha=0.05, power=0.8):
    z_alpha = 1.96  # two-sided
    z_beta = 0.84  # approx for 80%
    p_bar = (p1 + p2) / 2.0
    num = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) + z_beta * math.sqrt(p1*(1-p1) + p2*(1-p2)))**2
    denom = (p2 - p1)**2
    return math.ceil(num / denom)

scenarios = [
    (0.02, 0.03),  # 50% relative lift
    (0.02, 0.028), # 40% rel
    (0.02, 0.024), # 20% rel
    (0.02, 0.03),
]
for p1,p2 in scenarios:
    n = sample_size_two_prop(p1,p2)
    print(f'p1={p1}, p2={p2}, n per group = {n}')
