def foo(a, b: 'annotating b', c: int) -> float:
    print(a + b + c)

def d(x: 'an argument that defaults to 5' = 5):
    print(x)

def div(a: 'the dividend',
        b: 'the divisor (must be different than 0)') \
        -> 'the result of dividing a by b':
    """Divide a by b"""
    return a / b

from pathlib import Path, PurePath


p = Path(__file__)
print(p.resolve())
for d in dir(p):
    if not d.startswith('_'):
        print(d)

print(p.cwd())
