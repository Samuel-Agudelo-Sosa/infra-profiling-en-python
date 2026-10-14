import time

def es_primo(num):
    """Devuelve True si num es primo. Implementación deliberadamente ingenua."""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def suma_primos(n):
    """Suma todos los primos menores que n."""
    return sum(i for i in range(2, n) if es_primo(i))


def suma_primos_rapida(n):
    if n < 2:
        return 0
    criba = [True] * n
    criba[0] = criba[1] = False
    for p in range(2, int(n**0.5) + 1):
        if criba[p]:
            for j in range(p * p, n, p):
                criba[j] = False

    return sum([i for i in range(2, n) if criba[i]])