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
    print(anvil.server.call("say_hello", "sauron"))
    print(anvil.server.call('return_text_from_file'))

    # items = []
    # for x in anvil.server.call('return_text_from_file'):
    #   items.append((x[1], x[0]))
    self.drop_down_1.items = anvil.server.call("return_text_from_file", 'name, JID')

  def drop_down_1_change(self, **event_args):
    jid = self.drop_down_1.items[self.drop_down_1.selected_value - 1][1]
    data = anvil.server.call("get_zimmer", jid, '*')
    new_row = []
    print(jid)
    print(anvil.server.call("get_zimmer", jid, '*'))
    for eintrag in data:
      add = {'ZimmerNr.': eintrag[1], 'Schlafplätze': eintrag[2], 'PreisProNacht': eintrag[3]}
      new_row.append(add)
    self.repeating_panel_1.items = new_row
    
