import flet as ft
from modulos.modelos import Exame

def exames_view(page: ft.Page, crud_exames):
    white_text_style = ft.TextStyle(color=ft.Colors.WHITE)
    selected_id = {"value": ""}

    tabela_exames = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", style=white_text_style)),
            ft.DataColumn(ft.Text("Descrição", style=white_text_style)),
            ft.DataColumn(ft.Text("Especialidade", style=white_text_style)),
            ft.DataColumn(ft.Text("Valor (R$)", style=white_text_style)),
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

    descricao_field = ft.TextField(
        label="Descrição do Exame",
        hint_text="Digite a descrição do exame",
        border_radius=5,
        height=45,
        content_padding=10,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
    )

    valor_field = ft.TextField(
        label="Valor do Exame (R$)",
        hint_text="Digite o valor",
        border_radius=5,
        height=45,
        content_padding=10,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    especialidades = crud_exames.servicos.crud_especialidades.ler_especialidades_exaustivamente()
    especialidades_options = [ft.DropdownOption(f"{e[0]} - {e[1]}") for e in especialidades]
    especialidade_dropdown = ft.Dropdown(
        label="Especialidade",
        options=especialidades_options,
        width=300,
        border_radius=5,
        bgcolor=ft.Colors.BLUE_GREY_600,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_GREY_500,
        focused_border_color=ft.Colors.WHITE,
    )

    def gerar_proximo_codigo():
        exames = crud_exames.ler_todos()
        cods = [int(ex[0]) for ex in exames if ex[0].isdigit()]
        return max(cods, default=0) + 1

    def atualizar_tabela(filtro=""):
        tabela_exames.rows.clear()
        exames = crud_exames.ler_todos()
        filtro_lower = (filtro or "").lower()
        for ex in exames:
            cod, descricao, cod_especialidade, valor_exame = ex
            registro = crud_exames.consultar_completo(int(cod))
            if filtro_lower in cod.lower() or filtro_lower in descricao.lower() or filtro_lower == "":
                especialidade_texto = f"{registro.get('codigo_especialidade','')} - {registro.get('especialidade_nome','')}"
                tabela_exames.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(cod, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(descricao, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(especialidade_texto, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(f"R$ {registro.get('valor_exame',0):.2f}", color=ft.Colors.WHITE)),
                            ft.DataCell(ft.IconButton(ft.Icons.SEARCH, icon_color=ft.Colors.CYAN_300, on_click=lambda e, cod_ex=cod: preencher_formulario(cod_ex))),
                        ]
                    )
                )
        page.update()

    def preencher_formulario(cod_exame):
        registro = crud_exames.consultar_completo(int(cod_exame))
        if registro:
            selected_id["value"] = str(registro.get("codigo_exame",""))
            descricao_field.value = registro.get("descricao_exame","")
            valor_field.value = str(registro.get("valor_exame",""))
            especialidade_dropdown.value = f"{registro.get('codigo_especialidade','')} - {registro.get('especialidade_nome','')}"
            page.update()

    def limpar_formulario():
        selected_id["value"] = ""
        descricao_field.value = ""
        valor_field.value = ""
        especialidade_dropdown.value = None
        page.update()

    def on_inserir_click(_):
        if not especialidade_dropdown.value:
            return
        codigo = gerar_proximo_codigo()
        cod_especialidade = int(especialidade_dropdown.value.split(" - ")[0])
        exame_obj = Exame(
            cod_exame=codigo,
            descricao=descricao_field.value.strip(),
            cod_especialidade=cod_especialidade,
            valor_exame=float(valor_field.value)
        )
        crud_exames.cadastrar(exame_obj)
        limpar_formulario()
        atualizar_tabela()

    def on_salvar_click(_):
        if not selected_id["value"]:
            return
        cod = int(selected_id["value"])
        cod_especialidade = int(especialidade_dropdown.value.split(" - ")[0])
        exame_obj = Exame(
            cod_exame=cod,
            descricao=descricao_field.value.strip(),
            cod_especialidade=cod_especialidade,
            valor_exame=float(valor_field.value)
        )
        crud_exames.atualizar(exame_obj)
        limpar_formulario()
        atualizar_tabela()

    def on_excluir_click(_):
        if selected_id["value"]:
            crud_exames.excluir(int(selected_id["value"]))
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
            ft.Text("Detalhes de Exames", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            descricao_field,
            valor_field,
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
            ft.Text("Lista de Exames", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            barra_pesquisa,
            ft.Container(content=tabela_exames, expand=True),
        ],
        spacing=10,
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
        content=botoes_form,
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

    atualizar_tabela()

    return ft.View(
        "/exames",
        [
            ft.AppBar(
                title=ft.Text("Gerenciamento de Exames"),
                bgcolor=ft.Colors.BLUE_GREY_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                leading_width=60,
            ),
            container_view_body
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_800
    )
