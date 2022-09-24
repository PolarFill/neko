def roll():
    import random

    resultado = random.randint(1, 6)
    return resultado

def roll_custom(limit):
    import random

    int(limit)
    resultado = random.randint(1, limit)
    return resultado