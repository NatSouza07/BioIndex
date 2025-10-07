import flet as ft
from CRUDs.crud_pacientes import CrudPacientes
from modulos.modelos import Paciente

def pacientes_view(page: ft.Page, crud_pacientes: CrudPacientes):
    white_text_style = ft.TextStyle(color=ft.Colors.WHITE)
    selected_id = {"value": ""}

    tabela_pacientes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", style=white_text_style)),
            ft.DataColumn(ft.Text("Nome", style=white_text_style)),
            ft.DataColumn(ft.Text("Cidade - UF", style=white_text_style)),
            ft.DataColumn(ft.Text("IMC", style=white_text_style)),
            ft.DataColumn(ft.Text("Diagnóstico", style=white_text_style)),
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

    nome_field = ft.TextField(label="Nome", hint_text="Digite o nome do paciente",
                              border_radius=5, height=45, content_padding=10,
                              bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
                              label_style=ft.TextStyle(color=ft.Colors.BLACK54),
                              focused_border_color=ft.Colors.BLUE_900, cursor_color=ft.Colors.BLUE_900)
    nascimento_field = ft.TextField(label="Data de Nascimento", hint_text="dd/mm/aaaa",
                                    border_radius=5, height=45, content_padding=10,
                                    bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
                                    label_style=ft.TextStyle(color=ft.Colors.BLACK54),
                                    focused_border_color=ft.Colors.BLUE_900, cursor_color=ft.Colors.BLUE_900)
    telefone_field = ft.TextField(label="Telefone", hint_text="Digite o telefone",
                                  border_radius=5, height=45, content_padding=10,
                                  bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
                                  label_style=ft.TextStyle(color=ft.Colors.BLACK54),
                                  focused_border_color=ft.Colors.BLUE_900, cursor_color=ft.Colors.BLUE_900)
    endereco_field = ft.TextField(label="Endereço", hint_text="Digite o endereço",
                                  border_radius=5, height=45, content_padding=10,
                                  bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
                                  label_style=ft.TextStyle(color=ft.Colors.BLACK54),
                                  focused_border_color=ft.Colors.BLUE_900, cursor_color=ft.Colors.BLUE_900)
    peso_field = ft.TextField(label="Peso (kg)", hint_text="Digite o peso",
                              border_radius=5, height=45, content_padding=10,
                              bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
                              label_style=ft.TextStyle(color=ft.Colors.BLACK54),
                              focused_border_color=ft.Colors.BLUE_900, cursor_color=ft.Colors.BLUE_900)
    altura_field = ft.TextField(label="Altura (m)", hint_text="Digite a altura (ex: 1.75)",
                                border_radius=5, height=45, content_padding=10,
                                bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
                                label_style=ft.TextStyle(color=ft.Colors.BLACK54),
                                focused_border_color=ft.Colors.BLUE_900, cursor_color=ft.Colors.BLUE_900)

    cidades = crud_pacientes.servicos.crud_cidades.ler_cidades_exaustivamente()
    cidades_options = [ft.DropdownOption(f"{c[0]} - {c[1]} - {c[2]}") for c in cidades]

    cidade_dropdown = ft.Dropdown(
        label="Cidade - UF",
        options=cidades_options,
        width=250,
        border_radius=5,
        bgcolor=ft.Colors.BLUE_GREY_600,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_GREY_500,
        focused_border_color=ft.Colors.WHITE,
    )

    def gerar_proximo_codigo():
        registros = crud_pacientes.ler_pacientes_exaustivamente()
        cods = []
        for r in registros:
            try:
                cods.append(int(r[0]))
            except (ValueError, TypeError):
                continue
        return (max(cods) + 1) if cods else 1

    def atualizar_tabela(filtro=""):
        tabela_pacientes.rows.clear()
        pacientes = crud_pacientes.ler_pacientes_exaustivamente()
        filtro_lower = (filtro or "").lower()
        for p in pacientes:
            cod = str(p[0])
            nome = p[1]
            consulta_completa = crud_pacientes.consultar_paciente_completo(cod)
            nome_cidade = consulta_completa.get("nome_cidade") if consulta_completa else "N/A"
            uf_cidade = consulta_completa.get("uf_cidade") if consulta_completa else "N/A"
            imc = str(consulta_completa.get("imc", "N/A")) if consulta_completa else "N/A"
            diagnostico = consulta_completa.get("diagnostico", "N/A") if consulta_completa else "N/A"
            if filtro_lower in cod.lower() or filtro_lower in nome.lower() or filtro_lower == "":
                tabela_pacientes.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(cod, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(nome, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(f"{nome_cidade} - {uf_cidade}", color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(imc, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(diagnostico, color=ft.Colors.WHITE)),
                            ft.DataCell(
                                ft.IconButton(
                                    ft.Icons.SEARCH,
                                    icon_color=ft.Colors.BLUE_300,
                                    tooltip="Selecionar paciente",
                                    on_click=lambda e, pid=cod: preencher_formulario(pid)
                                )
                            ),
                        ]
                    )
                )
        page.update()

    def preencher_formulario(cod_paciente: str):
        registro = crud_pacientes.buscar_paciente(cod_paciente)
        if registro:
            selected_id["value"] = str(registro[0])
            nome_field.value = registro[1]
            nascimento_field.value = registro[2]
            telefone_field.value = registro[4]
            endereco_field.value = registro[3]
            cidade_dropdown.value = str(registro[5])
            peso_field.value = str(registro[6])
            altura_field.value = str(registro[7])
            page.update()

    def limpar_formulario():
        selected_id["value"] = ""
        nome_field.value = nascimento_field.value = telefone_field.value = endereco_field.value = peso_field.value = altura_field.value = ""
        cidade_dropdown.value = None
        page.update()

    def on_inserir_click(_):
        if not cidade_dropdown.value:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione uma cidade."))
            page.snack_bar.open = True
            page.update()
            return
        try:
            selected_text = cidade_dropdown.value
            cod_cidade = int(selected_text.split(" - ")[0])
            peso = float(peso_field.value.strip() or 0)
            altura = float(altura_field.value.strip() or 0)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Cidade, peso ou altura inválidos."))
            page.snack_bar.open = True
            page.update()
            return
        codigo = gerar_proximo_codigo()
        paciente_obj = Paciente(
            cod_paciente=codigo,
            nome=nome_field.value.strip(),
            data_nascimento=nascimento_field.value.strip(),
            endereco=endereco_field.value.strip(),
            telefone=telefone_field.value.strip(),
            cod_cidade=cod_cidade,
            peso=peso,
            altura=altura
        )
        crud_pacientes.cadastrar_paciente(paciente_obj)
        limpar_formulario()
        atualizar_tabela()

    def on_salvar_click(_):
        if not selected_id["value"]:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione um paciente para salvar (editar)."))
            page.snack_bar.open = True
            page.update()
            return
        if not cidade_dropdown.value:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione uma cidade."))
            page.snack_bar.open = True
            page.update()
            return
        try:
            selected_text = cidade_dropdown.value
            cod_cidade = int(selected_text.split(" - ")[0])
            peso = float(peso_field.value.strip() or 0)
            altura = float(altura_field.value.strip() or 0)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Cidade, peso ou altura inválidos."))
            page.snack_bar.open = True
            page.update()
            return
        paciente_obj = Paciente(
            cod_paciente=int(selected_id["value"]),
            nome=nome_field.value.strip(),
            data_nascimento=nascimento_field.value.strip(),
            endereco=endereco_field.value.strip(),
            telefone=telefone_field.value.strip(),
            cod_cidade=cod_cidade,
            peso=peso,
            altura=altura
        )
        crud_pacientes.excluir_paciente(selected_id["value"])
        crud_pacientes.cadastrar_paciente(paciente_obj)
        limpar_formulario()
        atualizar_tabela()

    def on_excluir_click(_):
        if selected_id["value"]:
            crud_pacientes.excluir_paciente(selected_id["value"])
            limpar_formulario()
            atualizar_tabela()

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
        on_change=lambda e: atualizar_tabela(e.control.value),
    )

    botoes_form = ft.Column(
        [
            ft.Text("Detalhes do Pacientes", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            nome_field,
            nascimento_field,
            telefone_field,
            endereco_field,
            cidade_dropdown,
            peso_field,
            ft.Container(altura_field, expand=True),
            ft.Row(
                [
                    ft.ElevatedButton(text="Inserir", icon=ft.Icons.ADD, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=on_inserir_click),
                    ft.ElevatedButton(text="Salvar", icon=ft.Icons.SAVE, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=on_salvar_click),
                    ft.ElevatedButton(text="Excluir", icon=ft.Icons.DELETE, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=on_excluir_click),
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
            ft.Text("Lista de Pacientes", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            barra_pesquisa,
            ft.Container(content=tabela_pacientes, expand=True),
        ],
        spacing=10,
        expand=True,
    )

    lista_pacientes = ft.Container(content=coluna_lista, padding=20, margin=ft.margin.only(right=10),
                                   bgcolor=ft.Colors.BLUE_GREY_700, border_radius=10, expand=True)
    formulario_paciente = ft.Container(content=botoes_form, padding=20, margin=ft.margin.only(left=10),
                                      bgcolor=ft.Colors.BLUE_GREY_700, border_radius=10, expand=True)

    conteudo_principal = ft.Row(
        [
            ft.Container(content=lista_pacientes, expand=6),
            ft.Container(content=formulario_paciente, expand=4),
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    container_view_body = ft.Container(content=conteudo_principal, expand=True,
                                       padding=ft.padding.only(left=20, right=20, top=20, bottom=20))
    atualizar_tabela()

    view = ft.View(
        "/pacientes",
        [
            ft.AppBar(title=ft.Text("Gerenciamento de Pacientes"),
                      bgcolor=ft.Colors.BLUE_GREY_700,
                      leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                      leading_width=60),
            container_view_body,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_800,
    )

    return view, atualizar_tabela
