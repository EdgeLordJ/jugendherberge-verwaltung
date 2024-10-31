import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
@anvil.server.callable
def return_text_from_file(rows='*'):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {rows} FROM jugendherbergen'))
  print(res)
  return res

@anvil.server.callable
def get_zimmer(jid, columns='*'):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {columns} FROM zimmer WHERE JID = {jid}'))
  print(res)
  conn.close()
  return res

@anvil.server.callable
def get_preiskategorie(pid, col):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {col} FROM preiskategorie WHERE PID = {pid}'))
  print(res[0][0])
  conn.close()
  return res[0][0]