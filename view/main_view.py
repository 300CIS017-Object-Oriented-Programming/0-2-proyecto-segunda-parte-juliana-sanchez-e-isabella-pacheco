import streamlit as st

def draw_admin_page(gui_controler):
    selected_thing_to_do = st.radio('Menu:', options=('Create Event', 'Edit an existing Event', 'Generate a Report'), index=0, horizontal=False,)
    if selected_thing_to_do == 'Create Event':
        draw_creation_event_page(gui_controler)

def draw_creation_event_page(gui_controler):
    selected_event_type = st.radio('Select the type',options=('Bar', 'Theater', 'Philanthropic'), index=0, horizontal=True,)
    fill_information_event(gui_controler,selected_event_type)

def fill_information_event(gui_controler, selected_event_type):
    st.write(f'Usted está creando un evento de tipo {selected_event_type}')
    artist_name = st.text_input("Artist Name", placeholder='Julianozca')
    event_name = st.text_input("Event Name", placeholder='Julianozca')
    event_place = st.text_input("Event Place", placeholder='Julianozca')
    event_date = st.text_input("Event Date", placeholder='Julianozca')
    opening_event_time =st.text_input("Artist Name", placeholder='Julianozca')
    direccion_event = st.text_input("Artist Name", placeholder='Julianozca')
    event_city = st.text_input("Artist Name", placeholder='Julianozca')
    if selected_event_type == 'Bar':
        artist_payment = "aqui va un input"
        gui_controler.gestion_controler.create_event(selected_event_type,artist_name,event_name,event_place,event_date,opening_event_time,direccion_event,event_city,artist_payment)
    elif selected_event_type == 'Theater':
        alquiler_price = "aqui va un input"
        gui_controler.gestion_controler.create_event(selected_event_type,artist_name,event_name,event_place,event_date,opening_event_time,direccion_event,event_city,alquiler_price)
    else:
        sponsor_name = "aqui va un input"
        sponsor_help = "aqui va un input"
        gui_controler.gestion_controler.create_event(selected_event_type,artist_name,event_name,event_place,event_date,opening_event_time,direccion_event,event_city,None)
        st.button(on_click=gui_controler.gestion_controler.set_sponsor(event_name,sponsor_name,sponsor_help))
    if selected_event_type != 'Philanthropic':
        category_ticket_name = st.text_input("Artist Name", placeholder='Julianozca')
        category_ticket_value = "aqui va un input"
        st.button(on_click=gui_controler.gestion_controler.set_category_ticket(event_name,category_ticket_name,category_ticket_value))
        
    
        