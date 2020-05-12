from .db import AuthBookBackend


def get_backend():
    default_backend = AuthBookBackend
    return default_backend
