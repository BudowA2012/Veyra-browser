from datetime import datetime

from core.storage.database import Database


class HistoryRepository:

    def __init__(
        self,
    ):
        self.db = Database()

        self._create_table()

    # ======================================================
    # TABLE
    # ======================================================

    def _create_table(
        self,
    ):

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT NOT NULL,
                visited_at TEXT NOT NULL
            )
            """
        )

        self.db.connection.commit()

    # ======================================================
    # ADD
    # ======================================================

    def add(
        self,
        title: str,
        url: str,
    ):

        if not url:
            return

        cursor = (
            self.db.connection.cursor()
        )

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

    # ======================================================
    # GET ALL
    # ======================================================

    def get_all(
        self,
    ):

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            SELECT
                id,
                title,
                url,
                visited_at
            FROM history
            ORDER BY visited_at DESC
            """
        )

        return cursor.fetchall()

    # ======================================================
    # SEARCH
    # ======================================================

    def search(
        self,
        query: str,
        limit: int = 8,
    ):

        query = (
            query
            .strip()
            .lower()
        )

        if not query:
            return []

        cursor = (
            self.db.connection.cursor()
        )

        pattern = (
            f"%{query}%"
        )

        cursor.execute(
            """
            SELECT
                title,
                url,
                MAX(visited_at) AS last_visit
            FROM history
            WHERE
                LOWER(title) LIKE ?
                OR LOWER(url) LIKE ?
            GROUP BY url
            ORDER BY last_visit DESC
            LIMIT ?
            """,
            (
                pattern,
                pattern,
                limit,
            ),
        )

        return cursor.fetchall()

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        history_id: int,
    ):

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            DELETE FROM history
            WHERE id = ?
            """,
            (
                history_id,
            ),
        )

        self.db.connection.commit()

    # ======================================================
    # CLEAR
    # ======================================================

    def clear(
        self,
    ):

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            DELETE FROM history
            """
        )

        self.db.connection.commit()