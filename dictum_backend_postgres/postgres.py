from typing import Optional

from dictum.backends.mixins.datediff import DatediffCompilerMixin
from dictum.backends.sql_alchemy import SQLAlchemyBackend, SQLAlchemyCompiler
from sqlalchemy import Float, Integer
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import cast, func


class PostgresCompiler(DatediffCompilerMixin, SQLAlchemyCompiler):
    def div(self, a, b):
        """Dictum's division is like Python's, e.g. 1/2 == 0.5,
        while in Postgres 1/2 == 0, so we need to cast the first
        arg to float.
        """
        return cast(a, Float) / b

    def datepart(self, args: list):
        # cast cause date_part returns double
        return cast(func.date_part(*args), Integer)

    def datetrunc(self, args: list):
        return func.date_trunc(*args)

    def datediff_day(self, args: list):
        start = self.datetrunc(["day", args[0]])
        end = self.datetrunc(["day", args[1]])
        return self.datepart(["day", end - start])  # the argument is an interval

    def now(self, _):
        return func.now()

    def today(self, _):
        return self.todate(func.now())


class PostgresBackend(SQLAlchemyBackend):
    type = "postgres"
    compiler_cls = PostgresCompiler

    def __init__(
        self,
        database: str = "postgres",
        host: str = "localhost",
        port: int = 5432,
        username: str = "postgres",
        password: Optional[str] = None,
        pool_size: Optional[int] = 5,
    ):
        super().__init__(
            database=database,
            host=host,
            port=port,
            username=username,
            password=password,
            pool_size=pool_size,
        )

    @property
    def url(self) -> str:
        url_params = {
            k: v
            for k, v in self.parameters.items()
            if k not in {"pool_size", "default_schema"}
        }
        return URL.create(drivername="postgresql", **url_params)
