from flask import abort
import pymysql
from util.DB import DB

db_pool = DB.init_db_pool()

# ユーザークラス
class User:
    @classmethod
    def create(cls, uid, name, email, password, kindergarten_schoolname, kindergarten_start_year, kindergarten_end_year, elementary_schoolname, elementary_start_year, elementary_end_year):
        try:
            conn = db_pool.get_conn()
        except Exception as e:
            print(f'Connection Pool Error: {e}')
            abort(500, description="Database connection error")
        try:
            with conn.cursor() as cur:
                sql = """
                    INSERT INTO users (uid, user_name, email, password, kindergarten_schoolname, kindergarten_start_year, kindergarten_end_year, elementary_schoolname, elementary_start_year, elementary_end_year)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cur.execute(sql, (uid, name, email, password, kindergarten_schoolname, kindergarten_start_year, kindergarten_end_year, elementary_schoolname, elementary_start_year, elementary_end_year))
                uid = cur.lastrowid
                conn.commit()
                return uid
        except pymysql.Error as e:
            print(f'Database Error: {e}')
            abort(500, description=f"Database Error: {e}")
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_email(cls, email):
        try:
            conn = db_pool.get_conn()
        except Exception as e:
            print(f'Connection Pool Error: {e}')
            abort(500, description="Database connection error")

        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email,))
                user = cur.fetchone()
                if user is None:
                    print(f"No user found with email: {email}")
                return user
        except pymysql.Error as e:
            print(f'Database Error: {e}')
            abort(500, description=f"Database Error: {e}")
        finally:
            db_pool.release(conn)


