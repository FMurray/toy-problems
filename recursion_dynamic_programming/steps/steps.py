def triple_step(n: int) -> int:
    if n < 0:
        return 0
    elif n == 0:
        return 1
    else:
        return triple_step(n - 1) + triple_step(n - 2) + triple_step(n - 3)