from contextlib import contextmanager
from collections import defaultdict
try:
    import thread as threading
except ImportError:
    import threading

REGISTRY = defaultdict(list)


@contextmanager
def listen():
    try:
        yield REGISTRY[threading.get_ident()]
    finally:
        del REGISTRY[threading.get_ident()]


def send(value):
    REGISTRY[threading.get_ident()].append(value)
