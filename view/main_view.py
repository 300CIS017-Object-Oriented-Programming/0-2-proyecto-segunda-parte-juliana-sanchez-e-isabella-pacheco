import streamlit as st

def draw_admin_page():
    selected_thing_to_do = st.radio('Menu:', options=('Create Event', 'Edit an existing Event', 'Generate a Report'), index=0, horizontal=False,)
    if selected_thing_to_do == 'Create Event':
        draw_creation_event_page()

def draw_creation_event_page():
    selected_event_type = st.radio('Select the type',options=('Bar', 'Theater', 'Philanthropic'), index=0, horizontal=True,)
    fill_information_event(selected_event_type)

def fill_information_event(selected_event_type):
    st.write(f'Usted está creando un evento de tipo {selected_event_type}')
    artist_name = st.text_input("Artist Name", placeholder='Julianozca')
    event_name = st.text_input("Event Name", placeholder='Julianozca')
    event_place = st.text_input("Event Place", placeholder='Julianozca')
    event_date = st.text_input("Event Date", placeholder='Julianozca')
    opening_event_time =st.text_input("Artist Name", placeholder='Julianozca')
    direccion_event = st.text_input("Artist Name", placeholder='Julianozca')
    event_city = st.text_input("Artist Name", placeholder='Julianozca')