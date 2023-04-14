import enum
import random
import sqlite3


class StatusOfBet(enum.Enum):
    WIN = 0
    LOSS = 1


class DB:
    def __init__(self):
        self.connect = sqlite3.connect('db.sqlite3')
        self.cursor = self.connect.cursor()

    def add_user(self, user_id: int):
        try:
            self.cursor.executemany(
                'INSERT INTO USERS (user_id, state, subscribe, bet) VALUES (?, ?, ?, ?)',
                [(user_id, 0, 0, random.randint(10, 15)), ]
            )
            self.connect.commit()
        except sqlite3.IntegrityError:
            pass

    def get_user(self, user_id: int):
        try:
            return self.cursor.execute(f"SELECT * FROM USERS WHERE user_id = {user_id}").fetchall()[0]
        except IndexError:
            self.add_user(user_id)
            return self.get_user(user_id)

    def get_users(self):
        return self.cursor.execute('SELECT * FROM USERS').fetchall()

    def set_state(self, user_id: int, state_value: int):
        self.cursor.execute(
            f'UPDATE USERS SET state = {state_value} WHERE user_id = {user_id}'
        )
        self.connect.commit()

    def set_bet(self, user_id, status):
        if status == StatusOfBet.WIN.value:
            self.generate_bet(user_id, [100, 180])

        if status == StatusOfBet.LOSS.value:
            bet = self.get_user(user_id)[3]
            new_bet = int(bet * random.randint(15, 22) / 10)
            if new_bet > 2010:
                self.generate_bet(user_id, [200, 400])
            else:
                self.cursor.execute(
                    f'UPDATE USERS SET bet = {new_bet} WHERE user_id = {user_id}'
                )
                self.connect.commit()

    def generate_bet(self, user_id, ran):
        self.cursor.execute(
            f'UPDATE USERS SET bet = {random.randint(*ran)} WHERE user_id = {user_id}'
        )
        self.connect.commit()

    def set_mostbet_id(self, user_id, mostbet_id):
        self.cursor.execute(
            f'UPDATE USERS SET mostbet_id = {mostbet_id} WHERE user_id = {user_id}'
        )
        self.connect.commit()

