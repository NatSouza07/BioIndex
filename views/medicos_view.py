import flet as ft
from modulos.modelos import Medico

def medicos_view(page: ft.Page, crud_medicos):
    white_text_style = ft.TextStyle(color=ft.Colors.WHITE)
    selected_id = {"value": ""}

    tabela_medicos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", style=white_text_style)),
            ft.DataColumn(ft.Text("Nome", style=white_text_style)),
            ft.DataColumn(ft.Text("Especialidade", style=white_text_style)),
            ft.DataColumn(ft.Text("Cidade - UF", style=white_text_style)),
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

    def gerar_proximo_codigo():
        registros = crud_medicos.ler_medicos_exaustivamente()
        cods = [int(r[0]) for r in registros if r[0].isdigit()]
        return max(cods, default=0) + 1

    nome_field = ft.TextField(label="Nome do Médico", hint_text="Digite o nome", border_radius=5, height=45, content_padding=10, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK)
    endereco_field = ft.TextField(label="Endereço", hint_text="Digite o endereço", border_radius=5, height=45, content_padding=10, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK)
    telefone_field = ft.TextField(label="Telefone", hint_text="Digite o telefone", border_radius=5, height=45, content_padding=10, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK)

    cidades = crud_medicos.servicos.crud_cidades.ler_cidades_exaustivamente()
    cidades_options = [ft.DropdownOption(f"{c[0]} - {c[1]} - {c[2]}") for c in cidades]
    cidade_dropdown = ft.Dropdown(label="Cidade", options=cidades_options, width=250, border_radius=5, bgcolor=ft.Colors.BLUE_GREY_600, color=ft.Colors.WHITE, border_color=ft.Colors.BLUE_GREY_500, focused_border_color=ft.Colors.WHITE)

    especialidades = crud_medicos.servicos.crud_especialidades.ler_especialidades_exaustivamente()
    especialidades_options = [
        ft.DropdownOption(f"{e[0]} - {e[1]} - {e[2]} - {e[3]}") for e in especialidades
    ]
    especialidade_dropdown = ft.Dropdown(label="Especialidade", options=especialidades_options, width=300, border_radius=5, bgcolor=ft.Colors.BLUE_GREY_600, color=ft.Colors.WHITE, border_color=ft.Colors.BLUE_GREY_500, focused_border_color=ft.Colors.WHITE)

    def atualizar_tabela(filtro=""):
        tabela_medicos.rows.clear()
        medicos = crud_medicos.ler_medicos_exaustivamente()
        filtro_lower = (filtro or "").lower()
        for m in medicos:
            if len(m) < 6:
                continue
            cod, nome, endereco, telefone, cod_cidade, cod_especialidade = m
            registro = crud_medicos.consultar_completo(cod)
            if filtro_lower in cod.lower() or filtro_lower in nome.lower() or filtro_lower == "":
                especialidade_texto = f"{registro.get('especialidade_codigo','')} - {registro.get('especialidade_desc','')} - {registro.get('especialidade_valor','')} - {registro.get('especialidade_limite','')}"
                tabela_medicos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(cod, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(nome, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(especialidade_texto, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(f"{registro.get('cidade_nome','')} - {registro.get('cidade_estado','')}", color=ft.Colors.WHITE)),
                            ft.DataCell(ft.IconButton(ft.Icons.SEARCH, icon_color=ft.Colors.CYAN_300, on_click=lambda e, mcod=cod: preencher_formulario(mcod)))
                        ]
                    )
                )
        page.update()

    def preencher_formulario(cod_medico):
        registro = crud_medicos.consultar_completo(cod_medico)
        if registro:
            selected_id["value"] = str(registro.get("codigo",""))
            nome_field.value = registro.get("nome","")
            endereco_field.value = registro.get("endereco","")
            telefone_field.value = registro.get("telefone","")
            cidade_dropdown.value = f"{registro.get('cidade_codigo','')} - {registro.get('cidade_nome','')} - {registro.get('cidade_estado','')}"
            especialidade_dropdown.value = f"{registro.get('especialidade_codigo','')} - {registro.get('especialidade_desc','')} - {registro.get('especialidade_valor','')} - {registro.get('especialidade_limite','')}"
            page.update()

    def limpar_formulario():
        selected_id["value"] = ""
        nome_field.value = ""
        endereco_field.value = ""
        telefone_field.value = ""
        cidade_dropdown.value = None
        especialidade_dropdown.value = None
        page.update()

    def on_inserir_click(_):
        if not cidade_dropdown.value or not especialidade_dropdown.value:
            return
        codigo = gerar_proximo_codigo()
        cod_cidade = int(cidade_dropdown.value.split(" - ")[0])
        cod_especialidade = int(especialidade_dropdown.value.split(" - ")[0])
        medico_obj = Medico(cod_medico=codigo, nome=nome_field.value.strip(), endereco=endereco_field.value.strip(), telefone=telefone_field.value.strip(), cod_cidade=cod_cidade, cod_especialidade=cod_especialidade)
        crud_medicos.cadastrar_medico(medico_obj)
        limpar_formulario()
        atualizar_tabela()

    def on_salvar_click(_):
        if not selected_id["value"]:
            return
        cod = selected_id["value"]
        cod_cidade = int(cidade_dropdown.value.split(" - ")[0])
        cod_especialidade = int(especialidade_dropdown.value.split(" - ")[0])
        registros = crud_medicos.ler_medicos_exaustivamente()
        for i, reg in enumerate(registros):
            if reg[0] == cod:
                registros[i] = [cod, nome_field.value.strip(), endereco_field.value.strip(), telefone_field.value.strip(), cod_cidade, cod_especialidade]
                break
        crud_medicos.io_manager.reescrever_arquivo_completo(registros)
        limpar_formulario()
        atualizar_tabela()

    def on_excluir_click(_):
        if selected_id["value"]:
            crud_medicos.excluir_medico(selected_id["value"])
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
        on_change=lambda e: atualizar_tabela(e.control.value)
    )

    botoes_form = ft.Column(
        [
            ft.Text("Detalhes de Médicos", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            nome_field,
            endereco_field,
            telefone_field,
            cidade_dropdown,
            especialidade_dropdown,
            ft.Container(expand=True),
            ft.Row([
                ft.ElevatedButton("Inserir", icon=ft.Icons.ADD, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=on_inserir_click),
                ft.ElevatedButton("Salvar", icon=ft.Icons.SAVE, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=on_salvar_click),
                ft.ElevatedButton("Excluir", icon=ft.Icons.DELETE, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=on_excluir_click),
            ], alignment=ft.MainAxisAlignment.END, spacing=10)
        ],
        spacing=15,
        expand=True,
    )

    coluna_lista = ft.Column(
        [
            ft.Text("Lista de Médicos", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            barra_pesquisa,
            ft.Container(content=tabela_medicos, expand=True),
        ],
        spacing=10,
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
        content=botoes_form,
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

    atualizar_tabela()

    return ft.View(
        "/medicos",
        [
            ft.AppBar(
                title=ft.Text("Gerenciamento de Médicos"),
                bgcolor=ft.Colors.BLUE_GREY_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                leading_width=60,
            ),
            container_view_body
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_800
    ), atualizar_tabela
