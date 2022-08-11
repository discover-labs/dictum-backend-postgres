import shlex
import subprocess

from dictum_backend_postgres import __version__
from dictum_backend_postgres.postgres import PostgresBackend


def test_version():
    assert __version__ == "0.1.4"


def test_entry_point():
    subprocess.check_call(
        shlex.split(
            "python -c 'from dictum_core.backends.base import Backend; "
            'assert "postgres" in Backend.registry\''
        )
    )


def test_default_schema():
    assert "default_schema" in PostgresBackend.parameters()
