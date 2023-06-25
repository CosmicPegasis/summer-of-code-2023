import unittest
import sqlite3
import os
import requests
import multiprocessing
from pathlib import Path
from db_handler import DatabaseHandler, LinksDatabaseHandler
from http.server import BaseHTTPRequestHandler, HTTPServer
from server import WebRequestHandler

class DatabaseHandlerTests(unittest.TestCase):
    def setUp(self):
        if Path("./links.db").is_file():
            os.remove("./links.db")
        self.con = sqlite3.connect("links.db")

    def test_table_exists_db_not_created(self):
        self.assertEqual(DatabaseHandler.table_exists(self.con.cursor(), "links"), False)
    
    def test_table_exists_table_created(self):
        cur = self.con.cursor()
        cur.execute("CREATE TABLE links (s_url STRING PRIMARY KEY, d_url STRING)")
        self.assertEqual(DatabaseHandler.table_exists(cur, "links"), True)
        cur.close()
    
    def tearDown(self) -> None:
        if Path("./links.db").is_file():
            os.remove("./links.db")
        
class LinksDatabaseHandlerTests(unittest.TestCase):
    def setUp(self):
        if Path("./links.db").is_file():
            os.remove("./links.db")
        self.con = sqlite3.connect("links.db")
        self.cur = self.con.cursor()

    def test_create_link(self):
        LinksDatabaseHandler.create_link("abcd", "google.com")
        res = self.cur.execute("SELECT * FROM links")
        self.assertEqual(res.fetchone(), ('abcd', 'google.com'))
        self.cur.close()

    def test_create_link_when_one_link_already_exists(self):
        self.cur.execute("CREATE TABLE links (surl STRING PRIMARY KEY, durl STRING)")
        self.cur.execute("INSERT INTO links VALUES('aviral', 'google.com')")
        self.con.commit()
        self.con.close()

        LinksDatabaseHandler.create_link("abcd", "youtube.com")
        self.con = sqlite3.connect('links.db')
        self.cur = self.con.cursor()
        res = self.cur.execute("SELECT * FROM links")
        self.assertEqual(res.fetchall(), [('aviral', 'google.com'), ('abcd', 'youtube.com')])

    def test_read(self):
        LinksDatabaseHandler.create_link("aviral", "youtube.com")
        link = LinksDatabaseHandler.read_link("aviral")
        self.assertEqual(link, "youtube.com")
            
    def test_read_key_not_exists(self):
            self.cur.execute("CREATE TABLE links (s_url STRING PRIMARY KEY, d_url STRING)")
            self.assertRaises(KeyError, LinksDatabaseHandler.read_link, "aviral")

    def tearDown(self) -> None:
        self.con.close()
        if Path("./links.db").is_file():
            os.remove("./links.db")


class WebServerTests(unittest.TestCase):
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    def setUp(self):
        if Path("./links.db").is_file():
            os.remove("./links.db")

        self.x = multiprocessing.Process(target=self.server.serve_forever)
        print("Listening on port 8000")
        self.x.start()
        
    def test_post_requests(self):
        res = requests.post("http://localhost:8000/create/aviral/youtube.com")
        self.assertEqual(res.status_code, 201)

        con = sqlite3.connect("links.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM links")        
        self.assertEqual(res.fetchall(), [("aviral", "youtube.com")])
        os.remove("./links.db")

    def test_get_requests(self):
        requests.post("http://localhost:8000/create/aviral/youtube.com")
        res = requests.get("http://localhost:8000/redirect/aviral", allow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers["Cache-Control"], "no-cache")
        self.assertEqual(res.headers["Location"], "http://youtube.com")

    def test_get_requests_table_not_exist(self):
        res = requests.get("http://localhost:8000/redirect/aviral")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.text, "Not Found")

    def test_get_requests_key_not_exist(self):
        requests.post("http://localhost:8000/create/aviral/youtube.com")
        res = requests.get("http://localhost:8000/redirect/singh")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.text, "Not Found")

    def tearDown(self):
        if Path("./links.db").is_file():
            os.remove("./links.db")
        self.x.terminate()

if __name__ == "__main__":
    unittest.main()