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
