import flet as ft
from CRUDs.crud_consultas import CrudConsultas
from CRUDs.crud_pacientes import CrudPacientes
from CRUDs.crud_medicos import CrudMedicos
from CRUDs.crud_exames import CrudExames
from CRUDs.crud_cidades import CrudCidades

def consultas_view(page: ft.Page, servicos):
    crud_consultas: CrudConsultas = servicos.crud_consultas
    crud_pacientes: CrudPacientes = servicos.crud_pacientes
    crud_medicos: CrudMedicos = servicos.crud_medicos
    crud_exames: CrudExames = servicos.crud_exames
    crud_cidades: CrudCidades = servicos.crud_cidades

    white_text_style = ft.TextStyle(color=ft.Colors.WHITE)
    selected_id = {"value": ""}

    tabela_consultas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", style=white_text_style)),
            ft.DataColumn(ft.Text("Paciente", style=white_text_style)),
            ft.DataColumn(ft.Text("Cidade", style=white_text_style)),
            ft.DataColumn(ft.Text("Médico", style=white_text_style)),
            ft.DataColumn(ft.Text("Exame", style=white_text_style)),
            ft.DataColumn(ft.Text("Valor", style=white_text_style)),
            ft.DataColumn(ft.Text("Selecionar", style=white_text_style)),
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

    def get_dropdown(label, options, expand=None):
        return ft.Dropdown(
            label=label,
            options=options,
            border_radius=5,
            content_padding=10,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK,
            label_style=ft.TextStyle(color=ft.Colors.BLACK54),
            focused_border_color=ft.Colors.BLUE_900,
            expand=expand
        )

    def get_text_field(label, hint_text, expand=None):
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            border_radius=5,
            height=45,
            content_padding=10,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK,
            label_style=ft.TextStyle(color=ft.Colors.BLACK54),
            focused_border_color=ft.Colors.BLUE_900,
            cursor_color=ft.Colors.BLUE_900,
            expand=expand
        )

    paciente_dropdown = get_dropdown(
        "Paciente",
        [ft.dropdown.Option(p[1]) for p in crud_pacientes.ler_pacientes_exaustivamente()]
    )
    cidade_dropdown = get_dropdown(
        "Cidade",
        [ft.dropdown.Option(c[1]) for c in crud_cidades.ler_cidades_exaustivamente()]
    )
    medico_dropdown = get_dropdown(
        "Médico",
        [ft.dropdown.Option(m[1]) for m in crud_medicos.ler_medicos_exaustivamente()]
    )
    exame_dropdown = get_dropdown(
        "Exame",
        [ft.dropdown.Option(e[1]) for e in crud_exames.ler_exames_exaustivamente()]
    )
    data_field = get_text_field("Data", "DD/MM/AAAA", expand=1)
    hora_field = get_text_field("Hora", "HH:MM", expand=1)
    valor_field = get_text_field("Valor Total", "Calculado automaticamente", expand=1)

    def atualizar_tabela(filtro=""):
        tabela_consultas.rows.clear()
        relatorio = crud_consultas.gerar_relatorio_consultas_ordenado()
        filtro_lower = (filtro or "").lower()
        for c in relatorio:
            if (filtro_lower in str(c["cod_consulta"]).lower()
                or filtro_lower in c["paciente_nome"].lower()
                or filtro_lower in c["paciente_cidade"].lower()):
                tabela_consultas.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(c["cod_consulta"], color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(c["paciente_nome"], color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(c["paciente_cidade"], color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(c["medico_nome"], color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(c["exame_descricao"], color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(f'R$ {c["valor_consulta_total"]:.2f}', color=ft.Colors.WHITE)),
                            ft.DataCell(
                                ft.IconButton(
                                    ft.Icons.SEARCH,
                                    icon_color=ft.Colors.BLUE_300,
                                    tooltip="Selecionar consulta",
                                    on_click=lambda e, cid=c["cod_consulta"]: preencher_formulario(cid)
                                )
                            ),
                        ]
                    )
                )
        page.update()

    def preencher_formulario(cod_consulta: str):
        consulta = crud_consultas.consultar_consulta_completa(cod_consulta)
        if not consulta:
            return
        selected_id["value"] = consulta["cod_consulta"]
        paciente_dropdown.value = consulta["paciente_nome"]
        cidade_dropdown.value = consulta["paciente_cidade"]
        medico_dropdown.value = consulta["medico_nome"]
        exame_dropdown.value = consulta["exame_descricao"]
        data_field.value = consulta["data"]
        hora_field.value = consulta["hora"]
        valor_field.value = f'R$ {consulta["valor_consulta_total"]:.2f}'
        page.update()

    def on_inserir_click(_):
        page.snack_bar = ft.SnackBar(ft.Text("Função de inserir ainda será implementada."))
        page.snack_bar.open = True
        page.update()

    def on_salvar_click(_):
        page.snack_bar = ft.SnackBar(ft.Text("Função de salvar (editar) ainda será implementada."))
        page.snack_bar.open = True
        page.update()

    def on_excluir_click(_):
        if not selected_id["value"]:
            return
        crud_consultas.excluir_consulta(selected_id["value"])
        selected_id["value"] = ""
        atualizar_tabela()
        page.update()

    barra_pesquisa = ft.TextField(
        hint_text="Pesquisar por Paciente, Cidade ou Data...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=5,
        height=40,
        content_padding=10,
        bgcolor=ft.Colors.BLUE_GREY_600,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_GREY_500,
        focused_border_color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        on_change=lambda e: atualizar_tabela(e.control.value),
    )

    botoes_form = ft.Column(
        [
            ft.Text("Detalhes de Consultas", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            paciente_dropdown,
            cidade_dropdown,
            medico_dropdown,
            exame_dropdown,
            ft.Row([data_field, hora_field, valor_field], spacing=10),
            ft.Row(
                [
                    ft.ElevatedButton(
                        text="Inserir",
                        icon=ft.Icons.ADD,
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        on_click=on_inserir_click,
                    ),
                    ft.ElevatedButton(
                        text="Salvar",
                        icon=ft.Icons.SAVE,
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                        on_click=on_salvar_click,
                    ),
                    ft.ElevatedButton(
                        text="Excluir",
                        icon=ft.Icons.DELETE,
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE,
                        on_click=on_excluir_click,
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=10,
            ),
        ],
        spacing=15,
        expand=True,
    )

    coluna_lista = ft.Column(
        [
            ft.Text("Lista de Consultas", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            barra_pesquisa,
            ft.Container(content=tabela_consultas, expand=True),
        ],
        spacing=10,
        expand=True,
    )

    lista_consultas = ft.Container(
        content=coluna_lista,
        padding=20,
        margin=ft.margin.only(right=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    formulario_consulta = ft.Container(
        content=botoes_form,
        padding=20,
        margin=ft.margin.only(left=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    conteudo_principal = ft.Row(
        [
            ft.Container(content=lista_consultas, expand=6),
            ft.Container(content=formulario_consulta, expand=4),
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    container_view_body = ft.Container(
        content=conteudo_principal,
        expand=True,
        padding=ft.padding.only(left=20, right=20, top=20, bottom=20),
    )

    atualizar_tabela()

    return ft.View(
        "/consultas",
        [
            ft.AppBar(
                title=ft.Text("Agenda de Consultas"),
                bgcolor=ft.Colors.BLUE_GREY_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                leading_width=60,
            ),
            container_view_body,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_800
    )
