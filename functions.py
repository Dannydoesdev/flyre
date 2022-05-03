import psycopg2
from flask import session
import os
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=flyre')

# Run a SQL SELECT query and return all rows of results
# Example:
# results = sql_fetch('SELECT * FROM food WHERE id = %s', [id])
def sql_fetch(query, parameters=[]):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor(cursor_factory=RealDictCursor)
  cur.execute(query, parameters)
  results = cur.fetchall()
  conn.close()
  return results


# Run a SQL INSERT/UPDATE/DELETE query and do a commit.
# Example:
# sql_write('INSERT INTO food (name, price) VALUES (%s, %s)', [name, price])
def sql_write(query, parameters=[]):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor(cursor_factory=RealDictCursor)
  cur.execute(query, parameters)
  conn.commit()
  conn.close()

