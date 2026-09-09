from datetime import datetime

from core.storage.database import (
    Database,
)


class BookmarkRepository:

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
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL
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

        title = (
            title
            .strip()
        )

        url = (
            url
            .strip()
        )

        if not url:
            return False

        if not title:

            title = url

        cursor = (
            self.db.connection.cursor()
        )

        try:

            cursor.execute(
                """
                INSERT INTO bookmarks (
                    title,
                    url,
                    created_at
                )
                VALUES (?, ?, ?)
                """,
                (
                    title,
                    url,
                    datetime.now().isoformat(),
                ),
            )

            self.db.connection.commit()

            return True

        except Exception:

            return False

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
                created_at
            FROM bookmarks
            ORDER BY created_at DESC
            """
        )

        return (
            cursor.fetchall()
        )

    # ======================================================
    # SEARCH
    # ======================================================

    def search(
        self,
        query,
    ):

        query = (
            query
            .strip()
        )

        if not query:

            return (
                self.get_all()
            )

        pattern = (
            f"%{query}%"
        )

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            SELECT
                id,
                title,
                url,
                created_at
            FROM bookmarks
            WHERE
                title LIKE ?
                OR url LIKE ?
            ORDER BY created_at DESC
            """,
            (
                pattern,
                pattern,
            ),
        )

        return (
            cursor.fetchall()
        )

    # ======================================================
    # CHECK
    # ======================================================

    def is_bookmarked(
        self,
        url,
    ):

        url = (
            url
            .strip()
        )

        if not url:
            return False

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            SELECT id
            FROM bookmarks
            WHERE url = ?
            LIMIT 1
            """,
            (
                url,
            ),
        )

        return (
            cursor.fetchone()
            is not None
        )

    # ======================================================
    # DELETE BY ID
    # ======================================================

    def delete(
        self,
        bookmark_id,
    ):

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            DELETE FROM bookmarks
            WHERE id = ?
            """,
            (
                bookmark_id,
            ),
        )

        self.db.connection.commit()

    # ======================================================
    # DELETE BY URL
    # ======================================================

    def remove_url(
        self,
        url,
    ):

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            DELETE FROM bookmarks
            WHERE url = ?
            """,
            (
                url,
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
            DELETE FROM bookmarks
            """
        )

        self.db.connection.commit()