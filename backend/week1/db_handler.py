import sqlite3

class DatabaseHandler():
    @staticmethod
    def table_exists(cur: sqlite3.Cursor, table_name: str):
        try:
            cur.execute("SELECT * from {}".format(table_name))
            return True
        # Add specific exception condition
        except:
            return False


class LinksDatabaseHandler(DatabaseHandler):
    @staticmethod
    def create_link(s_url: str, d_url: str):
        # refactor out and ensure connection
        con = LinksDatabaseHandler.open_table()
        cur = con.cursor()
        cur.execute("INSERT INTO links VALUES('{}', '{}')".format(s_url, d_url))
        con.commit()
        con.close()
        return True

    @staticmethod
    def open_table():
        con = sqlite3.connect("links.db")
        cur = con.cursor()
        if not DatabaseHandler.table_exists(cur, "links"):
            cur.execute("CREATE TABLE links (s_url STRING PRIMARY KEY, d_url STRING)")
        cur.close()
        return con

    @staticmethod
    def read_link(s_url: str) -> str:
        con = sqlite3.connect("links.db")
        cur = con.cursor()
        if not DatabaseHandler.table_exists(cur, "links"):
            # Don't think will ever get called
            raise FileNotFoundError

        else:
            res = cur.execute("SELECT * FROM links WHERE s_url == '{}'".format(s_url)).fetchone()
            if not res:
                raise KeyError
            else:
                return res[1]