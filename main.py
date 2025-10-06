import flet as ft
from pathlib import Path

CAMINHO_DADOS = Path("dados")


def inicializar_estruturas_dados():
    CAMINHO_DADOS.mkdir(exist_ok=True)

    arquivos_necessarios = [
        "cidades.txt",
        "pacientes.txt",
        "especialidades.txt",
        "medicos.txt",
        "exames.txt",
        "consultas.txt",
        "diarias.txt",
        "contadores.txt"
    ]

    for nome_arquivo in arquivos_necessarios:
        caminho_arquivo = CAMINHO_DADOS / nome_arquivo
        if not caminho_arquivo.exists():
            caminho_arquivo.touch()
            print(f"Arquivo de dados '{caminho_arquivo}' criado.")


def TemplateDataTable():
    white_text_style = ft.TextStyle(color=ft.Colors.WHITE)

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", style=white_text_style)),
            ft.DataColumn(ft.Text("Nome", style=white_text_style), numeric=False),
            ft.DataColumn(ft.Text("CPF", style=white_text_style)),
            ft.DataColumn(ft.Text("Status", style=white_text_style)),
            ft.DataColumn(ft.Text("Ações", style=white_text_style)),
        ],
        rows=[],
        show_bottom_border=True,
        heading_row_color=ft.Colors.BLUE_GREY_700,
        data_row_color={
            "default": ft.Colors.BLUE_GREY_700,
            "hovered": ft.Colors.BLUE_GREY_600,
        },
        data_row_min_height=40,
        data_row_max_height=40,
    )

def TemplateFormulario():
    label_color = ft.Colors.BLACK54
    focused_color = ft.Colors.BLUE_900

    def get_text_field(label, hint_text, expand=None):
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            border_radius=5,
            height=45,
            content_padding=10,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK,
            label_style=ft.TextStyle(color=label_color),
            focused_border_color=focused_color,
            cursor_color=focused_color,
            expand=expand
        )

    def get_dropdown(label, options, expand=None):
        return ft.Dropdown(
            label=label,
            options=options,
            border_radius=5,
            content_padding=10,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK,
            label_style=ft.TextStyle(color=label_color),
            focused_border_color=focused_color,
            expand=expand
        )

    return ft.Column(
        [
            ft.Text("Detalhes / Edição do Paciente", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),

            get_text_field(label="Nome Completo", hint_text="Digite o nome do paciente"),
            get_text_field(label="CPF", hint_text="000.000.000-00"),

            ft.Row(
                [
                    get_text_field(label="Data de Nascimento", hint_text="DD/MM/AAAA", expand=1),
                    get_dropdown(
                        label="Status",
                        expand=1,
                        options=[
                            ft.dropdown.Option("Ativo"),
                            ft.dropdown.Option("Inativo"),
                        ]
                    ),
                ],
                spacing=10
            ),

            get_dropdown(
                label="Cidade (Lookup)",
                options=[
                    ft.dropdown.Option("São Paulo"),
                    ft.dropdown.Option("Rio de Janeiro"),
                ]
            ),

            ft.Divider(height=20, thickness=1, color=ft.Colors.BLUE_GREY_500),

            ft.Row([
                ft.ElevatedButton(text="Salvar", icon=ft.Icons.SAVE, bgcolor=ft.Colors.GREEN_700,
                                  color=ft.Colors.WHITE,
                                  style=ft.ButtonStyle(padding=ft.padding.only(left=20, right=20))),
                ft.OutlinedButton(
                    text="Cancelar",
                    icon=ft.Icons.CANCEL,
                    style=ft.ButtonStyle(
                        padding=ft.padding.only(left=20, right=20),
                        color=ft.Colors.WHITE,
                        side=ft.BorderSide(1, ft.Colors.WHITE)
                    )
                ),
            ], alignment=ft.MainAxisAlignment.END, spacing=10)
        ],
        spacing=15
    )


def pacientes_view(page: ft.Page):
    barra_pesquisa = ft.TextField(
        hint_text="Pesquisar por Nome, CPF ou ID...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=5,
        height=40,
        content_padding=10,
        bgcolor=ft.Colors.BLUE_GREY_600,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_GREY_500,
        focused_border_color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
    )

    coluna_lista = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Lista de Pacientes", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.ElevatedButton(
                        text="Adicionar Novo",
                        icon=ft.Icons.ADD,
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),

            barra_pesquisa,

            ft.Container(
                content=TemplateDataTable(),
                expand=True,
            )
        ],
        spacing=15,
        expand=True,
    )

    lista_pacientes = ft.Container(
        content=coluna_lista,
        padding=20,
        margin=ft.margin.only(right=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    formulario_paciente = ft.Container(
        content=TemplateFormulario(),
        padding=20,
        margin=ft.margin.only(left=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    conteudo_principal = ft.Row(
        [
            ft.Container(content=lista_pacientes, expand=6),
            ft.Container(content=formulario_paciente, expand=4),
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    container_view_body = ft.Container(
        content=conteudo_principal,
        expand=True,
        padding=ft.padding.only(left=20, right=20, top=20, bottom=20),
    )

    return ft.View(
        "/pacientes",
        [
            ft.AppBar(
                title=ft.Text("Gerenciamento de Pacientes"),
                bgcolor=ft.Colors.BLUE_GREY_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/")),
                leading_width=60,
            ),

            container_view_body
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor="#fafafa"
    )


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
                        ft.IconButton(ft.Icons.PEOPLE, on_click=lambda e: self.page.go("/pacientes"),
                                      icon_color=ft.Colors.BLUE_700, icon_size=28, style=ft.ButtonStyle(padding=0)),
                        ft.Text("Pacientes", size=12, color=ft.Colors.BLUE_700)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
                        alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.only(right=15, bottom=10)
                ),

                ft.Container(
                    content=ft.Column([
                        ft.Container(height=5),
                        ft.IconButton(ft.Icons.CALENDAR_MONTH, on_click=lambda e: self.page.go("/consultas"),
                                      icon_color=ft.Colors.BLUE_700, icon_size=28, style=ft.ButtonStyle(padding=0)),
                        ft.Text("Agenda", size=12, color=ft.Colors.BLUE_700)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
                        alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.only(right=15, bottom=10)
                ),

                ft.Container(
                    content=ft.Column([
                        ft.Container(height=5),
                        ft.IconButton(ft.Icons.SORT_BY_ALPHA, on_click=lambda e: self.page.go("/relatorio"),
                                      icon_color=ft.Colors.BLUE_700, icon_size=28, style=ft.ButtonStyle(padding=0)),
                        ft.Text("Relatório", size=12, color=ft.Colors.BLUE_700)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
                        alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.only(right=15, bottom=10)
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

        if self.page.route == "/pacientes":
            self.page.views.append(pacientes_view(self.page))

        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)


def main(page: ft.Page):
    inicializar_estruturas_dados()
    ViewManager(page)


if __name__ == '__main__':
    print("Inicializando: Verificando estrutura de arquivos...")
    inicializar_estruturas_dados()

    print("Inicializando: Carregando dados e construindo índices em memória...")

    print("Inicializando: Interface gráfica pronta.")
    ft.app(target=main, assets_dir="assets")
