import flet as ft

from CRUDs.crud_cidades import CrudCidades
from CRUDs.crud_pacientes import CrudPacientes
from CRUDs.crud_consultas import CrudConsultas
from CRUDs.crud_diarias import CrudDiarias
from CRUDs.crud_especialidades import CrudEspecialidades
from CRUDs.crud_exames import CrudExames
from CRUDs.crud_medicos import CrudMedicos
from modulos.servicos import GerenciadorServicos

from views.cidades_view import cidades_view
from views.pacientes_view import pacientes_view
from views.consultas_view import consultas_view
from views.diarias_view import diarias_view
from views.especialidades_view import especialidades_view
from views.exames_view import exames_view
from views.medicos_view import medicos_view
from views.relatorios_view import relatorios_view

class ViewManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.servicos = GerenciadorServicos()
        self.crud_cidades = CrudCidades(self.servicos)
        self.crud_pacientes = CrudPacientes(self.servicos)
        self.crud_consultas = CrudConsultas(self.servicos)
        self.crud_diarias = CrudDiarias(self.servicos)
        self.crud_especialidades = CrudEspecialidades(self.servicos)
        self.crud_exames = CrudExames(self.servicos)
        self.crud_medicos = CrudMedicos(self.servicos)

        page.title = "BioIndex"
        page.window_width = 1200
        page.window_height = 850
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.bgcolor = "#fafafa"

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go(self.page.route)

    def route_change(self, _):
        self.page.views.clear()

        modulos_navegacao_final = ft.Row(
            [
                self._menu_button("Cidades", ft.Icons.LOCATION_CITY, "/cidades"),
                self._menu_button("Pacientes", ft.Icons.PEOPLE, "/pacientes"),
                self._menu_button("Consultas", ft.Icons.CALENDAR_MONTH, "/consultas"),
                self._menu_button("Diárias", ft.Icons.HOTEL, "/diarias"),
                self._menu_button("Especialidades", ft.Icons.HEALING, "/especialidades"),
                self._menu_button("Exames", ft.Icons.SCIENCE, "/exames"),
                self._menu_button("Médicos", ft.Icons.LOCAL_HOSPITAL, "/medicos"),
                self._menu_button("Relatórios", ft.Icons.INSIGHTS, "/relatorios"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        )

        menu_principal_view = ft.View(
            "/",
            [
                ft.AppBar(
                    leading=ft.Container(
                        content=ft.Image(src="logo.png", height=60, fit=ft.ImageFit.CONTAIN),
                        padding=ft.padding.only(left=20),
                        alignment=ft.alignment.center_left,
                    ),
                    leading_width=200,
                    title=modulos_navegacao_final,
                    center_title=True,
                    bgcolor=ft.Colors.BLUE_GREY_100,
                    elevation=0,
                    actions=[
                        ft.IconButton(
                            ft.Icons.PERSON_OUTLINE,
                            tooltip="Meu Perfil",
                            icon_color=ft.Colors.BLUE_700,
                        ),
                        ft.VerticalDivider(width=10),
                    ],
                ),
                ft.Stack(
                    [
                        ft.Image(
                            src="background.png",
                            fit=ft.ImageFit.COVER,
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#fafafa",
        )
        self.page.views.append(menu_principal_view)

        rota = self.page.route

        if rota == "/cidades":
            view = cidades_view(self.page, self.crud_cidades)
            self.page.views.append(view)
        elif rota == "/pacientes":
            view, carregar_tabela = pacientes_view(self.page, self.crud_pacientes)
            self.page.views.append(view)
            carregar_tabela()
        elif rota == "/consultas":
            view = consultas_view(self.page)
            self.page.views.append(view)
        elif rota == "/diarias":
            view = diarias_view(self.page)
            self.page.views.append(view)
        elif rota == "/especialidades":
            view_data = especialidades_view(self.page, self.crud_especialidades)
            self.page.views.append(view_data["conteudo"])
            view_data["carregar_tabela"]()
        elif rota == "/exames":
            view = exames_view(self.page, self.crud_exames)
            self.page.views.append(view)
        elif rota == "/medicos":
            view, carregar_tabela = medicos_view(self.page, self.crud_medicos)
            self.page.views.append(view)
            self.page.update()
            carregar_tabela()
        elif rota == "/relatorios":
            view, carregar_tabela = relatorios_view(self.page, self.servicos)
            self.page.views.append(view)
            self.page.update()
            carregar_tabela()

        self.page.update()

    def view_pop(self, _):
        if self.page.views:
            self.page.views.pop()
            if self.page.views:
                top_view = self.page.views[-1]
                self.page.go(top_view.route)

    def _menu_button(self, texto: str, icone, rota: str):
        return ft.Container(
            content=ft.Column(
                [
                    ft.IconButton(
                        icone,
                        on_click=lambda e: self.page.go(rota),
                        icon_color=ft.Colors.BLUE_700,
                        icon_size=26,
                        style=ft.ButtonStyle(padding=0),
                    ),
                    ft.Text(texto, size=12, color=ft.Colors.BLUE_700),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=ft.padding.only(right=15, bottom=10),
        )
