import streamlit as st

from view.reporte import Reporte
from model.events.Event_bar import EventBar 
from model.events.Event_philanthropic import EventPhilanthropic
from model.events.Event_theater import EventTheater

class GestionController:
    def __init__(self):
        self.events_bar = {}
        self.events_theater = {}
        self.events_philanthropic = {}
        self.artist = None
        self.reporte = Reporte()
    
    def create_event(self,selected_event_type,artist_name,event_name,event_place,event_date,opening_event_time,direccion_event,event_city,diferent):
        if selected_event_type == 'Bar':
            self.events_bar[event_name]= (EventBar(event_name, artist_name, event_place,event_date,opening_event_time, direccion_event,event_city,diferent))
        elif selected_event_type == 'Theater':
            self.events_theater[event_name]=(EventTheater(event_name, artist_name, event_place,event_date,opening_event_time, direccion_event,event_city,diferent))
        else :
            self.events_philanthropic[event_name]=(EventPhilanthropic(event_name, artist_name, event_place,event_date,opening_event_time, direccion_event,event_city,diferent))

    def visualize_event(self, selected_event_type):
        if selected_event_type == 'Bar':
            for event in self.events_bar:
                st.write(event)
        elif selected_event_type == 'Theater':
            for event in self.events_theater:
                st.write(event)
        else:
            for event in self.events_philanthropic:
                st.write(event)
