from ._anvil_designer import BenutzerTemplateTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class BenutzerTemplate(BenutzerTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  # Hole die Benutzerdaten und weise sie dem Repeating Panel zu
    users = anvil.server.call("get_benutzer", 'vorname, nachname')
    benutzer_liste = [{"vorname": user[0], "nachname": user[1]} for user in users]
    
    self.repeating_panel_2.items = benutzer_liste