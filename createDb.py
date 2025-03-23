# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 10:11:20 2025

@author: markt
"""

import sqlite3

def create_database():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS words")
    cursor.execute("""
        CREATE TABLE words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            french TEXT NOT NULL,
            english TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def populate_database_from_file(filename):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    with open(filename, "r") as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) == 3:
                _, french, english = parts
                cursor.execute("INSERT INTO words (french, english) VALUES (?, ?) ON CONFLICT DO NOTHING", (french, english))
    conn.commit()
    conn.close()


create_database()
populate_database_from_file("french-englist.txt")

