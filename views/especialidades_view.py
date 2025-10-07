import flet as ft
from CRUDs.crud_especialidades import CrudEspecialidades

def template_data_table():
    white_text_style = ft.TextStyle(color=ft.Colors.WHITE)
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", style=white_text_style)),
            ft.DataColumn(ft.Text("Nome da Especialidade", style=white_text_style)),
            ft.DataColumn(ft.Text("Ações", style=white_text_style)),
        ],
        rows=[],
        show_bottom_border=True,
        heading_row_color=ft.Colors.BLUE_GREY_700,
        data_row_color={
            ft.ControlState.DEFAULT: ft.Colors.BLUE_GREY_700,
            ft.ControlState.HOVERED: ft.Colors.BLUE_GREY_600,
        },
        data_row_min_height=40,
        data_row_max_height=40,
    )

def template_formulario():
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
            expand=expand,
        )

    return ft.Column(
        [
            ft.Text(
                "Detalhes / Edição da Especialidade",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            get_text_field(label="Nome da Especialidade", hint_text="Digite o nome"),
            ft.Divider(height=20, thickness=1, color=ft.Colors.BLUE_GREY_500),
            ft.Row(
                [
                    ft.ElevatedButton(
                        text="Salvar",
                        icon=ft.Icons.SAVE,
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            padding=ft.padding.only(left=20, right=20)
                        ),
                    ),
                    ft.OutlinedButton(
                        text="Cancelar",
                        icon=ft.Icons.CANCEL,
                        style=ft.ButtonStyle(
                            padding=ft.padding.only(left=20, right=20),
                            color=ft.Colors.WHITE,
                            side=ft.BorderSide(1, ft.Colors.WHITE),
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=10,
            ),
        ],
        spacing=15,
    )

def especialidades_view(page: ft.Page, crud_especialidades: CrudEspecialidades):
    barra_pesquisa = ft.TextField(
        hint_text="Pesquisar por Nome ou ID...",
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

    tabela_especialidades = template_data_table()

    coluna_lista = ft.Column(
        [
            ft.Row(
                [
                    ft.Text(
                        "Lista de Especialidades",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        text="Adicionar Novo",
                        icon=ft.Icons.ADD,
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            barra_pesquisa,
            ft.Container(content=tabela_especialidades, expand=True),
        ],
        spacing=15,
        expand=True,
    )

    lista_especialidades = ft.Container(
        content=coluna_lista,
        padding=20,
        margin=ft.margin.only(right=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    formulario_especialidade = ft.Container(
        content=template_formulario(),
        padding=20,
        margin=ft.margin.only(left=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    conteudo_principal = ft.Row(
        [
            ft.Container(content=lista_especialidades, expand=6),
            ft.Container(content=formulario_especialidade, expand=4),
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    container_view_body = ft.Container(
        content=conteudo_principal,
        expand=True,
        padding=ft.padding.only(left=20, right=20, top=20, bottom=20),
    )

    view = ft.View(
        "/especialidades",
        [
            ft.AppBar(
                title=ft.Text("Gerenciamento de Especialidades"),
                bgcolor=ft.Colors.BLUE_GREY_700,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK, on_click=lambda ev: page.go("/")
                ),
                leading_width=60,
            ),
            container_view_body,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_800,
    )

    def carregar_tabela():
        try:
            especialidades = crud_especialidades.ler_especialidades_exaustivamente()
            tabela_especialidades.rows.clear()
            for esp in especialidades:
                tabela_especialidades.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(esp[0]), color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(esp[1], color=ft.Colors.WHITE)),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            ft.Icons.EDIT,
                                            icon_size=18,
                                            icon_color=ft.Colors.BLUE_300,
                                        ),
                                        ft.IconButton(
                                            ft.Icons.DELETE,
                                            icon_size=18,
                                            icon_color=ft.Colors.RED_300,
                                        ),
                                    ]
                                )
                            ),
                        ]
                    )
                )
            page.update()
        except Exception as err:
            print(f"Erro ao carregar especialidades: {err}")

    carregar_tabela()

    return {"conteudo": view, "carregar_tabela": carregar_tabela}
