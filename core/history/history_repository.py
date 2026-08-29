from datetime import datetime

from core.storage.database import Database


class HistoryRepository:

    def __init__(self):
        self.db = Database()
        self._create_table()

    def _create_table(self):

        cursor = self.db.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT NOT NULL,
                visited_at TEXT NOT NULL
            )
        """)

        self.db.connection.commit()

    def add(self, title: str, url: str):

        if not url:
            return

        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            INSERT INTO history (
                title,
                url,
                visited_at
            )
            VALUES (?, ?, ?)
            """,
            (
                title or url,
                url,
                datetime.now().isoformat(),
            ),
        )

        self.db.connection.commit()

    def get_all(self):

        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT id, title, url, visited_at
            FROM history
            ORDER BY visited_at DESC
            """
        )

        return cursor.fetchall()

    def delete(self, history_id: int):

        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            DELETE FROM history
            WHERE id = ?
            """,
            (history_id,),
        )

        self.db.connection.commit()

    def clear(self):

        cursor = self.db.connection.cursor()

        cursor.execute(
            "DELETE FROM history"
        )

        self.db.connection.commit()