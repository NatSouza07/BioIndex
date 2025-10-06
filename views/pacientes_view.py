import flet as ft

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
