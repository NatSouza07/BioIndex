import flet as ft

def relatorios_view(page, crud_servicos):
    titulo = ft.Text(
        "BioIndex",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.CYAN_300,
    )

    filtro_tipo = ft.Dropdown(
        label="Tipo de Relatório",
        options=[
            ft.dropdown.Option("Pacientes"),
            ft.dropdown.Option("Consultas"),
            ft.dropdown.Option("Diárias"),
            ft.dropdown.Option("Médicos"),
            ft.dropdown.Option("Exames"),
            ft.dropdown.Option("Especialidades"),
        ],
        value="Pacientes",
        width=250,
        border_radius=5,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        border_color=ft.Colors.BLUE_GREY_300,
        focused_border_color=ft.Colors.BLUE_GREY_500,
    )

    status_text = ft.Text("", color=ft.Colors.AMBER_200)

    tabela = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Carregando...", color=ft.Colors.WHITE))],
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

    def carregar_tabela(_=None):
        tabela.columns.clear()
        tabela.rows.clear()
        tipo = filtro_tipo.value

        if tipo == "Pacientes":
            colunas = ["ID", "Nome", "CPF", "Status"]
            registros = crud_servicos.crud_pacientes.ler_pacientes_exaustivamente()
        elif tipo == "Consultas":
            colunas = ["ID", "Paciente", "Médico", "Data", "Status"]
            registros = crud_servicos.crud_consultas.ler_consultas_exaustivamente()
        elif tipo == "Diárias":
            colunas = ["ID", "Especialidade", "Data", "Vagas"]
            registros = crud_servicos.crud_diarias.ler_diarias_exaustivamente()
        elif tipo == "Médicos":
            colunas = ["ID", "Nome", "CRM", "Especialidade"]
            registros = crud_servicos.crud_medicos.ler_medicos_exaustivamente()
        elif tipo == "Exames":
            colunas = ["ID", "Nome", "Preço"]
            registros = crud_servicos.crud_exames.ler_exames_exaustivamente()
        elif tipo == "Especialidades":
            colunas = ["ID", "Nome", "Descrição"]
            registros = crud_servicos.crud_especialidades.ler_especialidades_exaustivamente()
        else:
            colunas = []
            registros = []

        for c in colunas:
            tabela.columns.append(ft.DataColumn(ft.Text(c, color=ft.Colors.WHITE)))

        for r in registros:
            tabela.rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(valor), color=ft.Colors.WHITE)) for valor in r.values()]
                )
            )

        tabela.update()
        status_text.value = f"Exibindo relatório de {tipo}"
        page.update()

    coluna_lista = ft.Column(
        [
            ft.Row(
                [
                    titulo,
                    ft.ElevatedButton(
                        text="Atualizar",
                        icon=ft.Icons.REFRESH,
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        on_click=carregar_tabela,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            filtro_tipo,
            ft.Container(content=tabela, expand=True),
            status_text,
        ],
        spacing=15,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    container_view_body = ft.Container(
        content=coluna_lista,
        expand=True,
        padding=ft.padding.only(left=20, right=20, top=20, bottom=20),
        bgcolor=ft.Colors.BLUE_GREY_800,
        border_radius=10,
    )

    view = ft.View(
        "/relatorios",
        [
            ft.AppBar(
                title=ft.Text("Relatórios"),
                bgcolor=ft.Colors.BLUE_GREY_700,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda e: page.go("/"),
                ),
                leading_width=60,
            ),
            container_view_body,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_900,
    )

    return view, carregar_tabela
