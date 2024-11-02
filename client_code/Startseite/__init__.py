from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.    
    self.drop_down_1.items += anvil.server.call("return_text_from_file", 'name, JID')
    self.placeholder_removed = False
    users = anvil.server.call("get_benutzer", 'vorname, nachname')
    for vorname, nachname in users:
      self.drop_down_2.items += [f'{vorname} {nachname}']
    self.placeholder2_removed = False
    self.date_picker_1.min_date = datetime.date.today()
    self.date_picker_2.min_date = datetime.date.today()

  def drop_down_1_change(self, **event_args):
    if not self.placeholder_removed:
      self.drop_down_1.items = self.drop_down_1.items[1:]
      self.placeholder_removed = True
    jid = self.drop_down_1.items[self.drop_down_1.selected_value - 1][1]
    data = anvil.server.call("get_zimmer", jid, '*')
    users = anvil.server.call("get_benutzer", 'vorname, nachname, PID')
    new_row = []
    for eintrag in data:
      if self.drop_down_2.selected_value == "Wer bist du?":
        add = {'ZimmerNr.': eintrag[3], 'Schlafplätze': eintrag[4], 'Preiskategorie': anvil.server.call('get_preiskategorie', eintrag[1], 'name')}
        new_row.append(add)
      else:
        for user in users:
          if (f'{user[0]} {user[1]}' == self.drop_down_2.selected_value) & (anvil.server.call('get_preiskategorie', eintrag[1], 'name') == anvil.server.call('get_preiskategorie', user[2], 'name')):
              add = {'ZimmerNr.': eintrag[3], 'Schlafplätze': eintrag[4], 'Preiskategorie': anvil.server.call('get_preiskategorie', eintrag[1], 'name')}
              new_row.append(add)
    self.repeating_panel_1.items = new_row

  def drop_down_2_change(self, **event_args):
    if not self.placeholder2_removed:
      self.drop_down_2.items = self.drop_down_2.items[1:]
      self.placeholder2_removed = True
    users = anvil.server.call("get_benutzer", 'vorname, nachname, PID')
    new_row = []
    for user in users:
      if f'{user[0]} {user[1]}' != self.drop_down_2.selected_value:
        add = {'vorname': user[0], 'nachname': user[1]}
        new_row.append(add)
      else:
        if self.drop_down_1.selected_value != "Wähle eine Jugendherberge...":
          jid = self.drop_down_1.items[self.drop_down_1.selected_value - 1][1]
          data = anvil.server.call("get_zimmer", jid, '*')
          new_rooms = []
          for eintrag in data:
            if anvil.server.call('get_preiskategorie', eintrag[1], 'name') == anvil.server.call('get_preiskategorie', user[2], 'name'):
              add = {'ZimmerNr.': eintrag[3], 'Schlafplätze': eintrag[4], 'Preiskategorie': anvil.server.call('get_preiskategorie', eintrag[1], 'name')}
              new_rooms.append(add)
          self.repeating_panel_1.items = new_rooms
        else:
          pass
    self.repeating_panel_2.items = new_row

  def get_selected_radio_info(self):
    for row in self.repeating_panel_1.get_components():
      radio_btn = row.get_components()[0]
      plaetze = row.get_components()[2]
      zimmer_num = row.get_components()[1]
      
      if radio_btn.selected:
        return {
          'zimmer_num': zimmer_num.text, 'plaetze': plaetze.text
        }
    
    return None

  def get_selected_checkboxes(self):
    selected_persons = []
    count = 1
    
    for row in self.repeating_panel_2.get_components():
        checkbox = row.get_components()[0]
        vorname = row.get_components()[1]
        nachname = row.get_components()[2]
        
        if checkbox.checked:
            count += 1
            selected_persons.append({
                'vorname': vorname.text,
                'nachname': nachname.text
            })
    
    return {
        'count': count,
        'persons': selected_persons
    }
  
  def outlined_button_1_click(self, **event_args):
    room = self.get_selected_radio_info()
    booked_users = self.get_selected_checkboxes()
    start = self.date_picker_1.date
    end = self.date_picker_2.date
    try:
      if start >= end:
        alert("Bitte wählen Sie einen gültigen Datum.")
      else:
        if not room['plaetze'] < booked_users['count']:
          jid = self.drop_down_1.items[self.drop_down_1.selected_value - 1][1]
          alert(anvil.server.call('insert_booking', room['zimmer_num'], booked_users['persons'], self.drop_down_2.selected_value, start, end, jid))
          data = anvil.server.call("get_zimmer", jid, '*')
          users = anvil.server.call("get_benutzer", 'vorname, nachname, PID')
          new_row = []
          for eintrag in data:
            for user in users:
              if (f'{user[0]} {user[1]}' == self.drop_down_2.selected_value) & (anvil.server.call('get_preiskategorie', eintrag[1], 'name') == anvil.server.call('get_preiskategorie', user[2], 'name')):
                  add = {'ZimmerNr.': eintrag[3], 'Schlafplätze': eintrag[4], 'Preiskategorie': anvil.server.call('get_preiskategorie', eintrag[1], 'name')}
                  new_row.append(add)
          self.repeating_panel_1.items = new_row
        else:
          alert("Bitte wählen Sie so viele Gäste, wie die Anzahl an Schlafplätzen.")
    except:
      alert("Bitte wählen Sie alles nötige aus.")
