
import flet as ft

def main(pagina: ft.Page):
    pagina.title = 'BioIndex'
    pagina.window_widht =  800
    pagina.window_height = 600
    pagina.add(ft.Text("Bem-vindo á BioIndex!", size=30))

ft.app(target=main)