from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.    
    self.drop_down_1.items += anvil.server.call("return_text_from_file", 'name, JID')
    self.placeholder_removed = False

  def drop_down_1_change(self, **event_args):
    if not self.placeholder_removed:
      self.drop_down_1.items = self.drop_down_1.items[1:]
      self.placeholder_removed = True
    jid = self.drop_down_1.items[self.drop_down_1.selected_value - 1][1]
    data = anvil.server.call("get_zimmer", jid, '*')
    new_row = []
    print(jid)
    print(anvil.server.call("get_zimmer", jid, '*'))
    for eintrag in data:
      add = {'ZimmerNr.': eintrag[3], 'Schlafplätze': eintrag[4], 'Preiskategorie': anvil.server.call('get_preiskategorie', eintrag[1], 'name')}
      new_row.append(add)
    self.repeating_panel_1.items = new_row

  