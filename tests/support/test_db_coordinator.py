from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy import Engine, create_engine, inspect, text

from shiori.app.core.config import get_settings

settings = get_settings()


class TestDbCoordinator:
    __test__ = True

    EXCLUDE_TABLES = {"alembic_version"}

    def apply_alembic(self) -> None:
        alembic_cfg = AlembicConfig("alembic.ini")
        command.upgrade(alembic_cfg, "head")

    def truncate_all(self) -> None:
        url = settings.WRITER_DB_URL.replace("aiomysql", "pymysql")
        engine = create_engine(url=url)
        tables = self._get_all_tables(engine=engine)
        for table in tables:
            with engine.begin() as connection:
                connection.execute(text(f"TRUNCATE TABLE {table}"))

    def _get_all_tables(self, *, engine: Engine) -> list[str]:
        inspector = inspect(engine)
        tables = []

        for table_name in inspector.get_table_names():
            if table_name in self.EXCLUDE_TABLES:
                continue

            tables.append(table_name)

        return tables
