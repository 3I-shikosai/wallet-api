import psycopg2
from psycopg2.extensions import connection
import hashlib

from .schemas import UserData
from . import config


# -------------------------------------------------
# パスワードを認証
# -------------------------------------------------


def encode_sha256(src: str) -> str:
    return hashlib.sha256(src.encode()).hexdigest()


def verify_password(password: str):
    if encode_sha256(password) == config.ADMIN_PASSWORD:
        return True
    else:
        return False


# -------------------------------------------------
# データベース操作系
# -------------------------------------------------


DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "postgres"


def get_conn() -> connection:
    conn: connection = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )
    try:
        yield conn
    finally:
        conn.close()


# ----------------------------------
# "users"テーブルが存在しなければ作成する
# ----------------------------------
def init_db():
    conn_generator = get_conn()
    with next(conn_generator) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT EXISTS(SELECT 1 FROM "
                "pg_tables WHERE "
                "schemaname = 'public' "
                "AND "
                "tablename = 'users');"
            )
            if cur.fetchone()[0]:
                print('[DB INIT] Table "user" already exists!!')
            else:
                cur.execute(
                    "CREATE TABLE users ("
                    "user_id char(8) PRIMARY KEY,"
                    "balance integer);"
                )
                conn.commit()
                print('[DB INIT] Created Table "user"')


class UserService:
    def __init__(self, conn: connection):
        self.__conn = conn

    def __del__(self):
        self.__conn.close()

    # --------------------------------------------
    # ユーザーの存在確認
    # --------------------------------------------
    def is_user_exists(self, user_id: str):
        try:
            with self.__conn.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM users WHERE user_id = '{user_id}';"
                )
                result = cur.fetchone()

                if result is None:
                    return False
                else:
                    return True

        except Exception as e:
            print(f"[DB ERROR] is_user_exists: {e}")

    # --------------------------------------------
    # 新規ユーザーを作成
    # --------------------------------------------
    def create_user(self, user_id: str, balance: int):
        try:
            with self.__conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users "
                    "(user_id, balance) "
                    "VALUES "
                    f"('{user_id}', {balance})"
                )
                self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            print(f"[DB ERROR] create_user: {e}")

    # --------------------------------------------
    # ユーザーを削除
    # --------------------------------------------
    def delete_user(self, user_id: str):
        with self.__conn.cursor() as cur:
            cur.execute(f"DELETE FROM users WHERE user_id = '{user_id}';")
            self.__conn.commit()

    # --------------------------------------------
    # ユーザーの全データを取得
    # --------------------------------------------
    def get_data(self, user_id: str) -> UserData:
        with self.__conn.cursor() as cur:
            cur.execute(
                "SELECT "
                "user_id, balance "
                "FROM users WHERE user_id = "
                f"'{user_id}';"
            )
            user_record = cur.fetchone()

            # もし合致するuser_idがなかったら -> None
            if user_record is None:
                print("[DB ERROR] get_data: user not found")
                return None

            return UserData(
                user_id=user_record[0],
                balance=user_record[1],
            )

    # --------------------------------------------
    # ユーザーの残高を取得
    # --------------------------------------------
    def get_balance(self, user_id: str):
        try:
            with self.__conn.cursor() as cur:
                cur.execute(
                    f"SELECT balance FROM users WHERE user_id = '{user_id}';"
                )
                user_record = cur.fetchone()

                # もし合致するuser_idがなかったら -> None
                if user_record is None:
                    return None

                return user_record[0]

        except Exception as e:
            print(f"[DB ERROR] get_balance: {e}")

    # --------------------------------------------
    # ユーザーの残高を変更
    # --------------------------------------------
    def set_balance(self, user_id: str, balance: int):
        try:
            with self.__conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET balance = "
                    f"{balance} "
                    "WHERE user_id = "
                    f"'{user_id}';"
                )
                self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            print(f"[DB ERROR] set_balance: {e}")
