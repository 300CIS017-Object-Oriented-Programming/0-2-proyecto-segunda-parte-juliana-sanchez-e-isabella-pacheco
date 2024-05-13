from view.reporte import Reporte
from model.events.Event_bar import EventBar 
from model.events.Event_philanthropic import EventPhilanthropic
from model.events.Event_theater import EventTheater

class GestionController:
    def __init__(self):
        self.events = None
        self.artist = None
        self.reporte = Reporte()
    
    def create_event(self,selected_event_type,artist_name,event_name,event_place,event_date,opening_event_time,direccion_event,event_city,diferent):
        if selected_event_type == 'Bar':
            self.events.push(EventBar(event_name, artist_name, event_place,event_date,opening_event_time, direccion_event,event_city,diferent))