from core.storage.database import Database


class ShortcutRepository:

    def __init__(self):

        self.db = Database()

    def get_all(self):

        cursor = self.db.connection.cursor()

        cursor.execute("""
            SELECT id,name,url
            FROM shortcuts
            ORDER BY id
        """)

        return cursor.fetchall()

    def add(self,name,url):

        cursor = self.db.connection.cursor()

        cursor.execute("""
            INSERT INTO shortcuts(name,url)
            VALUES (?,?)
        """,(name,url))

        self.db.connection.commit()

    def update(self,id,name,url):

        cursor = self.db.connection.cursor()

        cursor.execute("""
            UPDATE shortcuts
            SET name=?,url=?
            WHERE id=?
        """,(name,url,id))

        self.db.connection.commit()

    def delete(self,id):

        cursor = self.db.connection.cursor()

        cursor.execute("""
            DELETE FROM shortcuts
            WHERE id=?
        """,(id,))

        self.db.connection.commit()