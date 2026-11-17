import sqlite3
from typing import List, Tuple

class Account_db:
    def __init__(self, db_file) -> None:
        self.connection = sqlite3.connect(db_file, check_same_thread=False, timeout=20)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self) -> None:
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name TEXT,
                                        main_password TEXT)""")

    def new_account(self, name: str, main_password: str) -> None:
        with self.connection:
            self.cursor.execute("""INSERT INTO passwords (name, main_password) VALUES (?, ?)""", (name, main_password))
        self.connection.commit()

    def check_account(self, name: str) -> bool:
        with self.connection:
            result = self.cursor.execute("""SELECT * FROM passwords WHERE name = ?""", (name,))
            result = result.fetchone()
            return result

    def get_data(self) -> List[Tuple[str, str]]:
        with self.connection:
            self.cursor.execute("""SELECT name, main_password FROM passwords""")
            data = self.cursor.fetchall()
        return data

    def delete_account(self, name: str) -> None:
        with self.connection:
            self.cursor.execute("""DELETE FROM passwords WHERE name = ?""", (name,))
        self.connection.commit()

    def redact_account(self, name: str, main_password: str) -> None:

        with self.connection:
            self.cursor.execute("""UPDATE passwords SET main_password = ? WHERE name = ?""", (main_password, name,))
        self.connection.commit()


if __name__ == '__main__':
    pass