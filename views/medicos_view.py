import flet as ft

def template_data_table():
    white_text_style = ft.TextStyle(color=ft.Colors.WHITE)
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", style=white_text_style)),
            ft.DataColumn(ft.Text("Nome do Médico", style=white_text_style)),
            ft.DataColumn(ft.Text("CRM", style=white_text_style)),
            ft.DataColumn(ft.Text("Especialidade", style=white_text_style)),
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

    def get_text_field(label, hint_text, width=None):
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
        )

    return ft.Column(
        [
            ft.Text(
                "Detalhes / Edição do Médico",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            get_text_field("Nome do Médico", "Digite o nome", width=300),
            get_text_field("CRM", "Digite o CRM", width=150),
            get_text_field("Especialidade", "Digite a especialidade", width=200),
            ft.Divider(height=20, thickness=1, color=ft.Colors.BLUE_GREY_500),
            ft.Row(
                [
                    ft.ElevatedButton(
                        text="Salvar",
                        icon=ft.Icons.SAVE,
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(padding=ft.padding.only(left=20, right=20)),
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

def medicos_view(page: ft.Page, crud_medicos):
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

    tabela_medicos = template_data_table()
    status_text = ft.Text("", color=ft.Colors.AMBER_200)

    coluna_lista = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Lista de Médicos", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
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
            ft.Container(content=tabela_medicos, expand=True),
        ],
        spacing=15,
        expand=True,
    )

    lista_medicos = ft.Container(
        content=coluna_lista,
        padding=20,
        margin=ft.margin.only(right=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    formulario_medico = ft.Container(
        content=template_formulario(),
        padding=20,
        margin=ft.margin.only(left=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    conteudo_principal = ft.Row(
        [
            ft.Container(content=lista_medicos, expand=6),
            ft.Container(content=formulario_medico, expand=4),
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
        "/medicos",
        [
            ft.AppBar(
                title=ft.Text("Gerenciamento de Médicos"),
                bgcolor=ft.Colors.BLUE_GREY_700,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda e: page.go("/")
                ),
                leading_width=60,
            ),
            container_view_body,
            status_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_800,
    )

    def carregar_tabela():
        tabela_medicos.rows.clear()
        try:
            medicos = crud_medicos.ler_medicos_exaustivamente()
            for item in medicos:
                tabela_medicos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(item["id"]), color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(item["nome"], color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(item["crm"], color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(item["especialidade"], color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Row(
                                [
                                    ft.IconButton(ft.Icons.EDIT_NOTE, icon_color=ft.Colors.CYAN_300),
                                    ft.IconButton(ft.Icons.DELETE_FOREVER, icon_color=ft.Colors.RED_400),
                                ]
                            )),
                        ]
                    )
                )
            if tabela_medicos.page:
                tabela_medicos.update()
        except Exception as err:
            print(f"Erro ao carregar médicos: {err}")

    view.on_view_pop = lambda _: carregar_tabela()
    return view, carregar_tabela
