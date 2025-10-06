import flet as ft
from views.pacientes_view import pacientes_view
from views.cidades_view import cidades_view

class ViewManager:
    def __init__(self, page: ft.Page):
        self.page = page

        page.title = 'BioIndex'
        page.window_width = 1000
        page.window_height = 800
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.bgcolor = "#fafafa"

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

        self.page.go(self.page.route)

    def route_change(self, route):
        self.page.views.clear()

        modulos_navegacao_row = ft.Row(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=5),
                        ft.IconButton(ft.Icons.LOCATION_CITY, on_click=lambda e: self.page.go("/cidades"),
                                      icon_color=ft.Colors.BLUE_700, icon_size=28, style=ft.ButtonStyle(padding=0)),
                        ft.Text("Cidades", size=12, color=ft.Colors.BLUE_700)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
                        alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.only(right=15, bottom= 10)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=5),
                        ft.IconButton(ft.Icons.PEOPLE, on_click=lambda e: self.page.go("/pacientes"),
                                      icon_color=ft.Colors.BLUE_700, icon_size=28, style=ft.ButtonStyle(padding=0)),
                        ft.Text("Pacientes", size=12, color=ft.Colors.BLUE_700)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
                        alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.only(right=15, bottom= 10)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=5),
                        ft.IconButton(ft.Icons.CALENDAR_MONTH, on_click=lambda e: self.page.go("/consultas"),
                                      icon_color=ft.Colors.BLUE_700, icon_size=28, style=ft.ButtonStyle(padding=0)),
                        ft.Text("Agenda", size=12, color=ft.Colors.BLUE_700)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
                        alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.only(right=15, bottom= 10)
                ),

                ft.Container(
                    content=ft.Column([
                        ft.Container(height=5),
                        # Botão Relatório
                        ft.IconButton(ft.Icons.SORT_BY_ALPHA, on_click=lambda e: self.page.go("/relatorio"),
                                      icon_color=ft.Colors.BLUE_700, icon_size=28, style=ft.ButtonStyle(padding=0)),
                        ft.Text("Relatório", size=12, color=ft.Colors.BLUE_700)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
                        alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.only(right=15, bottom= 10)
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.START
        )

        modulos_navegacao_final = ft.Container(
            content=modulos_navegacao_row,
            alignment=ft.alignment.bottom_center,
            expand=True,
        )

        menu_principal_view = ft.View(
            "/",
            [
                ft.AppBar(
                    leading=ft.Container(
                        content=ft.Image(src="logo.png", height=60, fit=ft.ImageFit.CONTAIN),
                        padding=ft.padding.only(left=20),
                        alignment=ft.alignment.center_left
                    ),
                    leading_width=500,

                    title=modulos_navegacao_final,
                    center_title=True,
                    bgcolor=ft.Colors.BLUE_GREY_100,
                    elevation=0,

                    actions=[
                        ft.IconButton(ft.Icons.PERSON_OUTLINE, tooltip="Meu Perfil", icon_color=ft.Colors.BLUE_700),
                        ft.VerticalDivider(width=10)
                    ]
                ),

                ft.Stack(
                    [
                        ft.Image(
                            src="background.png",
                            fit=ft.ImageFit.COVER,
                            expand=True
                        ),
                    ],
                    expand=True
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll="NONE",
            bgcolor="#fafafa"
        )
        self.page.views.append(menu_principal_view)

        if self.page.route == "/cidades":
            self.page.views.append(cidades_view(self.page))
        elif self.page.route == "/pacientes":
            self.page.views.append(pacientes_view(self.page))

        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
