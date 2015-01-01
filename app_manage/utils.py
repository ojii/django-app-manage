from contextlib import contextmanager


NULL = object()


@contextmanager
def ensure_cleanup():
    cleanup = []
    try:
        yield cleanup
    finally:
        for callback in cleanup:
            try:
                callback()
            except:
                pass


def with_metaclass(meta, *bases):
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})
