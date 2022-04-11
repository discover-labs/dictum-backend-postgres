import shlex
import subprocess
import time
from pathlib import Path

import psycopg2
import pytest
from dictum.tests.conftest import chinook, engine, project  # noqa: F401

from dictum_backend_postgres.postgres import PostgresBackend

container_name = "dictum-postgres-backend-test"


def stop(fail=False):
    cmd = shlex.split(f"docker stop {container_name}")
    try:
        subprocess.check_call(cmd)
    except subprocess.SubprocessError:
        if fail:
            raise


@pytest.fixture(scope="session")
def backend():
    script = Path(__file__).parent / "chinook.sql"
    cmd = shlex.split(
        f"docker run -d --rm --name {container_name} -p 5432:5432 "
        "-e POSTGRES_USER=chinook -e POSTGRES_PASSWORD=chinook "
        f"-v {script}:/script.sql "
        "postgres"
    )
    subprocess.check_call(cmd)
    params = dict(
        host="localhost", dbname="chinook", user="chinook", password="chinook"
    )
    for _ in range(30):
        try:
            psycopg2.connect(**params)
            break
        except psycopg2.OperationalError:
            time.sleep(1)

    restore_cmd = shlex.split(
        f"docker container exec {container_name} "
        "psql -U chinook -W chinook -f /script.sql"
    )
    subprocess.check_call(restore_cmd)
    try:
        yield PostgresBackend(
            database=params["dbname"],
            host=params["host"],
            username=params["user"],
            password=params["password"],
        )
    finally:
        stop()
