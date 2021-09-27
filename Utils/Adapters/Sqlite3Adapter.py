import io
import sqlite3


class Sqlite3Adapter:

    def __init__(self):
        self.file = "Players"

        try:
            with open(self.file, "r"):
                pass

        except FileNotFoundError:

            try:
                self._restore_from_file(f"{self.file}_copy.sql")
            except FileNotFoundError:

                with sqlite3.connect(self.file) as connection:
                    try:
                        cursor = connection.cursor()
                        cursor.execute(
                            '''
                            CREATE TABLE PLAYERS
                            (
                                NAME VARCHAR(50) PRIMARY KEY,
                                PASSWORD VARCHAR(50),
                                POINTS INTEGER
                            )
                            '''
                        )

                        connection.commit()

                    except sqlite3.OperationalError:
                        pass

                    finally:
                        self._create_copy()

    def create_user(self, name, password):
        try:
            with sqlite3.connect(self.file) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    '''
                    INSERT INTO PLAYERS VALUES
                    (?, ?, ?)
                    '''
                    , (name, password, 0)
                )

                connection.commit()
            return True

        except sqlite3.IntegrityError:
            return False

    def read_user(self, name):
        with sqlite3.connect(self.file) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM PLAYERS WHERE NAME = (?)", (name,))
            player = cursor.fetchone()

            return player

    def update_users(self, players_to_update):
        query_params = [(x[1], x[0], x[0]) for x in players_to_update]
        with sqlite3.connect(self.file) as connection:
            cursor = connection.cursor()
            cursor.executemany(
                '''
                UPDATE PLAYERS
                SET POINTS = (SELECT sum(POINTS + (?)) 
                FROM PLAYERS
                WHERE NAME = (?))
                WHERE NAME = (?)
                ''', query_params)
            connection.commit()

    # def delete_user(self, name):
    #     pass

    def _create_copy(self):
        with sqlite3.connect(self.file) as connection:
            with io.open(f"{self.file}_copy.sql", "w") as copy:
                for data in connection.iterdump():
                    copy.write(data)

    def _restore_from_file(self, file):
        with open(file, "r") as copy:
            script = copy.read()

        with sqlite3.connect(self.file) as connection:
            cursor = connection.cursor()
            cursor.executescript(script)

    def get_users(self):
        with sqlite3.connect(self.file) as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT NAME, POINTS FROM PLAYERS''')
            result = cursor.fetchall()

            return result


if __name__ == "__main__":
    s = Sqlite3Adapter()

    al = s.read_user("Alejo")
    ve = s.read_user("Venus")
    print(al)
    print(ve)
    s.update_users([("Alejo", 5), ("Venus", 123)])
    al = s.read_user("Alejo")
    ve = s.read_user("Venus")
    print(al)
    print(ve)
