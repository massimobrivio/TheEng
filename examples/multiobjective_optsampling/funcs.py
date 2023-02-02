def objective(x, *args):
    out = dict(f1=100 * (x[0] ** 2 + x[1] ** 2), f2=1e6 * (x[0] - 1) ** 2 + x[1] ** 2)
    return out
