from controllers.gestion_controler import  GestionController
from view.main_view import draw_admin_page

class GUIController:
    def __init__(self):
        self.run_page = 'main'
        self.gestion_controler = GestionController()


    def main(self):
        if self.run_page == 'main':
            draw_admin_page(self)