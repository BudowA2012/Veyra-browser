import sqlite3
from pathlib import Path

DB_PATH = Path("data") / "veyra.db"


class Database:

    def __init__(self):

        DB_PATH.parent.mkdir(exist_ok=True)

        self.connection = sqlite3.connect(DB_PATH)

        self._create_tables()

    def _create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shortcuts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL
            )
        """)

        self.connection.commit()