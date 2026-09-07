from core.storage.database import Database


class ShortcutRepository:

    def __init__(self):

        self.db = Database()

    # ==================================================
    # GET ALL
    # ==================================================

    def get_all(self):

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            SELECT id, name, url
            FROM shortcuts
            ORDER BY id
            """
        )

        return cursor.fetchall()

    # ==================================================
    # ADD
    # ==================================================

    def add(
        self,
        name,
        url,
    ):

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            INSERT INTO shortcuts(
                name,
                url
            )
            VALUES (?, ?)
            """,
            (
                name,
                url,
            ),
        )

        self.db.connection.commit()

    # ==================================================
    # UPDATE
    # ==================================================

    def update(
        self,
        shortcut_id,
        name,
        url,
    ):

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            UPDATE shortcuts
            SET
                name = ?,
                url = ?
            WHERE id = ?
            """,
            (
                name,
                url,
                shortcut_id,
            ),
        )

        self.db.connection.commit()

    # ==================================================
    # DELETE
    # ==================================================

    def delete(
        self,
        shortcut_id,
    ):

        cursor = (
            self.db.connection.cursor()
        )

        cursor.execute(
            """
            DELETE FROM shortcuts
            WHERE id = ?
            """,
            (
                shortcut_id,
            ),
        )

        self.db.connection.commit()