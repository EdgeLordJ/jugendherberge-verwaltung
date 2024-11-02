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
def return_text_from_file(cols='*'):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {cols} FROM jugendherbergen'))
  return res

@anvil.server.callable
def get_zimmer(jid, columns='*'):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {columns} FROM zimmer WHERE JID = {jid} AND belegt IS NOT 1'))
  conn.close()
  return res

@anvil.server.callable
def get_preiskategorie(pid, cols):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {cols} FROM preiskategorie WHERE PID = {pid}'))
  conn.close()
  return res[0][0]

@anvil.server.callable
def get_benutzer(cols='*'):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {cols} FROM Benutzer'))
  conn.close()
  return res

@anvil.server.callable
def insert_booking(room, users, reg_user, start, end, jid):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  reg_vorname, reg_nachname = reg_user.split(" ")
  zid = list(cursor.execute(f'SELECT ZID FROM zimmer WHERE JID = {jid} AND zimmernummer = {room}'))[0][0]
  bid = list(cursor.execute(f'SELECT BID FROM Benutzer WHERE vorname = "{reg_vorname}" AND nachname = "{reg_nachname}"'))[0][0]
  cursor.execute(f'UPDATE zimmer SET belegt = 1 WHERE ZID = {zid}')
  cursor.execute(f'INSERT INTO Buchung (ZID, BID, anreise, abreise) VALUES ({zid}, {bid}, "{start}", "{end}")')
  for user in users:
    cursor.execute(f'INSERT INTO MitGebuchteBenutzer (BID, vorname, nachname) VALUES ({bid}, "{user["vorname"]}", "{user["nachname"]}")')
  conn.commit()
  conn.close()
  return "Buchung erfolgreich"