import flet as ft

def template_data_table():
    white_text_style = ft.TextStyle(color=ft.Colors.WHITE)

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", style=white_text_style)),
            ft.DataColumn(ft.Text("Nome do Exame", style=white_text_style)),
            ft.DataColumn(ft.Text("Preço (R$)", style=white_text_style)),
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

    def get_text_field(label, hint_text, width=None, keyboard_type=None):
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            width=width,
            border_radius=5,
            height=45,
            content_padding=10,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK,
            label_style=ft.TextStyle(color=label_color),
            focused_border_color=focused_color,
            cursor_color=focused_color,
            keyboard_type=keyboard_type,
        )

    return ft.Column(
        [
            ft.Text(
                "Detalhes / Edição do Exame",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            get_text_field(label="Nome do Exame", hint_text="Digite o nome do exame", width=300),
            get_text_field(label="Preço (R$)", hint_text="Digite o preço", width=150, keyboard_type=ft.KeyboardType.NUMBER),
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

def exames_view(page: ft.Page, crud_exames):
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

    tabela_exames = template_data_table()

    try:
        exames = crud_exames.ler_todos()
        for ex in exames:
            tabela_exames.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(ex[0]), color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(ex[1], color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(f"R$ {ex[2]:.2f}", color=ft.Colors.WHITE)),
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
    except Exception as err:
        print(f"Erro ao carregar exames: {err}")

    coluna_lista = ft.Column(
        [
            ft.Row(
                [
                    ft.Text(
                        "Lista de Exames",
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
            ft.Container(content=tabela_exames, expand=True),
        ],
        spacing=15,
        expand=True,
    )

    lista_exames = ft.Container(
        content=coluna_lista,
        padding=20,
        margin=ft.margin.only(right=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    formulario_exame = ft.Container(
        content=template_formulario(),
        padding=20,
        margin=ft.margin.only(left=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    conteudo_principal = ft.Row(
        [
            ft.Container(content=lista_exames, expand=6),
            ft.Container(content=formulario_exame, expand=4),
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
        "/exames",
        [
            ft.AppBar(
                title=ft.Text("Gerenciamento de Exames"),
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
