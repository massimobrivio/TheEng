def objective_1(x, *args):
    out = dict(f1=100 * (x[0] ** 2 + x[1] ** 2), f2=1e6 * (x[0] - 1) ** 2 + x[1] ** 2)
    return out


def objective_2(x, *args):
    out = dict(f1=x[0] ** 2 * x[1])
    return out


def objective_3(x, *args):
    out = dict(f1=x[0] ** 2)
    return out


def objective_4(x, *args):
    out = dict(f1=100 * x[0], f2=3 * (x[0] - 1) ** 2)
    return out


def objective_5(x, *args):
    out = dict(f1=2 * x[0], f2=2 * x[0], f3=2 * x[0])
    return out
