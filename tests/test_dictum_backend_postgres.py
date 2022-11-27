import inspect
import shlex
import subprocess

from dictum_core.backends.secret import Secret

from dictum_backend_postgres import __version__
from dictum_backend_postgres.postgres import PostgresBackend


def test_version():
    assert __version__ == "0.1.6"


def test_entry_point():
    subprocess.check_call(
        shlex.split(
            "python -c 'from dictum_core.backends.base import Backend; "
            'assert "postgres" in Backend.registry\''
        )
    )


def test_default_schema():
    assert "default_schema" in PostgresBackend().parameters


def test_password_is_secret():
    assert (
        inspect.signature(PostgresBackend.__init__).parameters["password"].annotation
        is Secret
    )
