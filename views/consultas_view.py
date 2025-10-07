import flet as ft
from CRUDs.crud_medicos import CrudMedicos
from CRUDs.crud_pacientes import CrudPacientes
from CRUDs.crud_consultas import CrudConsultas
from CRUDs.crud_exames import CrudExames
from modulos.modelos import Consulta

def consultas_view(
    page: ft.Page,
    crud_medicos: CrudMedicos,
    crud_pacientes: CrudPacientes,
    crud_consultas: CrudConsultas,
    crud_exames: CrudExames
):

    paciente_field = ft.Dropdown(
        label="Paciente",
        options=[ft.DropdownOption(f"{p[0]} - {p[1]}") for p in crud_pacientes.ler_pacientes_exaustivamente()],
        width=300,
        border_radius=5,
        bgcolor=ft.Colors.BLUE_GREY_600,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_GREY_500,
        focused_border_color=ft.Colors.WHITE,
    )

    medico_field = ft.Dropdown(
        label="Médico",
        options=[ft.DropdownOption(f"{m[0]} - {m[1]} - {m[5]}") for m in crud_medicos.ler_medicos_exaustivamente()],
        width=300,
        border_radius=5,
        bgcolor=ft.Colors.BLUE_GREY_600,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_GREY_500,
        focused_border_color=ft.Colors.WHITE,
    )

    exame_field = ft.Dropdown(
        label="Exame",
        options=[ft.DropdownOption(f"{e[0]} - {e[1]}") for e in crud_exames.ler_todos()],
        width=300,
        border_radius=5,
        bgcolor=ft.Colors.BLUE_GREY_600,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_GREY_500,
        focused_border_color=ft.Colors.WHITE,
    )

    data_field = ft.TextField(
        label="Data",
        hint_text="dd/mm/aaaa",
        border_radius=5,
        height=45,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        focused_border_color=ft.Colors.BLUE_900,
        cursor_color=ft.Colors.BLUE_900
    )

    hora_field = ft.TextField(
        label="Hora",
        hint_text="HH:MM",
        border_radius=5,
        height=45,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        focused_border_color=ft.Colors.BLUE_900,
        cursor_color=ft.Colors.BLUE_900
    )

    tabela_consultas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Paciente", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Médico", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Exame", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Data", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Hora", color=ft.Colors.WHITE)),
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

    def atualizar_tabela():
        tabela_consultas.rows.clear()
        for c in crud_consultas.gerar_relatorio_consultas_ordenado():
            tabela_consultas.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c["cod_consulta"]), color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(c["paciente"], color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(c["medico"], color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(c["exame"], color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(c["data"], color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(c["hora"], color=ft.Colors.WHITE)),
                    ]
                )
            )
        page.update()

    def on_inserir_click(_):
        if not paciente_field.value or not medico_field.value or not exame_field.value or not data_field.value.strip() or not hora_field.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            cod_paciente = int(paciente_field.value.split(" - ")[0])
            cod_medico = int(medico_field.value.split(" - ")[0])
            cod_exame = int(exame_field.value.split(" - ")[0])
            cod_consulta = crud_consultas.gerar_proximo_codigo()

            consulta = Consulta(
                cod_consulta=cod_consulta,
                cod_paciente=cod_paciente,
                cod_medico=cod_medico,
                cod_exame=cod_exame,
                data=data_field.value.strip(),
                hora=hora_field.value.strip()
            )

            crud_consultas.cadastrar_consulta(consulta)

            paciente_field.value = None
            medico_field.value = None
            exame_field.value = None
            data_field.value = ""
            hora_field.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("Consulta cadastrada com sucesso!"))
            page.snack_bar.open = True
            atualizar_tabela()
            page.update()

        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {e}"))
            page.snack_bar.open = True
            page.update()

    botoes_form = ft.Column(
        [
            ft.Text("Cadastro de Consultas", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            paciente_field,
            medico_field,
            exame_field,
            data_field,
            hora_field,
            ft.Row(
                [
                    ft.ElevatedButton(text="Inserir", icon=ft.Icons.ADD, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=on_inserir_click),
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=10,
            )
        ],
        spacing=15,
        expand=True
    )

    coluna_lista = ft.Column(
        [
            ft.Text("Lista de Consultas", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(content=tabela_consultas, expand=True),
        ],
        spacing=10,
        expand=True
    )

    lista_consultas = ft.Container(content=coluna_lista, padding=20, margin=ft.margin.only(right=10),
                                   bgcolor=ft.Colors.BLUE_GREY_700, border_radius=10, expand=True)
    formulario_consulta = ft.Container(content=botoes_form, padding=20, margin=ft.margin.only(left=10),
                                      bgcolor=ft.Colors.BLUE_GREY_700, border_radius=10, expand=True)

    conteudo_principal = ft.Row(
        [
            ft.Container(content=lista_consultas, expand=6),
            ft.Container(content=formulario_consulta, expand=4),
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH
    )

    container_view_body = ft.Container(content=conteudo_principal, expand=True,
                                       padding=ft.padding.all(20))

    atualizar_tabela()

    view = ft.View(
        "/consultas",
        [
            ft.AppBar(title=ft.Text("Gerenciamento de Consultas"),
                      bgcolor=ft.Colors.BLUE_GREY_700,
                      leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                      leading_width=60),
            container_view_body,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_800
    )

    return view
