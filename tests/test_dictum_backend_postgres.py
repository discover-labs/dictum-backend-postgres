from dictum_core.backends.base import Backend

from dictum_backend_postgres import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_plugin():
    assert "postgres" in Backend.registry
