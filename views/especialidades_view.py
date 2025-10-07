import flet as ft
from CRUDs.crud_especialidades import CrudEspecialidades
from modulos.modelos import Especialidade

def especialidades_view(page: ft.Page, crud_especialidades: CrudEspecialidades):
    white_text_style = ft.TextStyle(color=ft.Colors.WHITE)
    selected_id = {"value": 0}

    tabela_especialidades = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", style=white_text_style)),
            ft.DataColumn(ft.Text("Nome da Especialidade", style=white_text_style)),
            ft.DataColumn(ft.Text("Valor Consulta", style=white_text_style)),
            ft.DataColumn(ft.Text("Limite Diário", style=white_text_style)),
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

    nome_field = ft.TextField(
        label="Nome da Especialidade",
        hint_text="Digite o nome",
        border_radius=5,
        height=45,
        content_padding=10,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        label_style=ft.TextStyle(color=ft.Colors.BLACK54),
        focused_border_color=ft.Colors.BLUE_900,
        cursor_color=ft.Colors.BLUE_900,
    )

    valor_field = ft.TextField(
        label="Valor Consulta",
        hint_text="Digite o valor",
        border_radius=5,
        height=45,
        content_padding=10,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        label_style=ft.TextStyle(color=ft.Colors.BLACK54),
        focused_border_color=ft.Colors.BLUE_900,
        cursor_color=ft.Colors.BLUE_900,
    )

    limite_field = ft.TextField(
        label="Limite Diário",
        hint_text="Digite o limite",
        border_radius=5,
        height=45,
        content_padding=10,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        label_style=ft.TextStyle(color=ft.Colors.BLACK54),
        focused_border_color=ft.Colors.BLUE_900,
        cursor_color=ft.Colors.BLUE_900,
        expand=True,
    )

    def carregar_tabela(filtro=""):
        tabela_especialidades.rows.clear()
        especialidades = crud_especialidades.ler_especialidades_exaustivamente()
        filtro_lower = (filtro or "").lower()
        for esp in especialidades:
            cod, nome, valor, limite = str(esp[0]), esp[1], f"R$ {float(esp[2]):.2f}", str(esp[3])
            if filtro_lower in cod.lower() or filtro_lower in nome.lower() or filtro_lower == "":
                tabela_especialidades.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(cod, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(nome, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(valor, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(limite, color=ft.Colors.WHITE)),
                            ft.DataCell(
                                ft.IconButton(
                                    ft.Icons.SEARCH,
                                    icon_color=ft.Colors.BLUE_300,
                                    tooltip="Selecionar especialidade",
                                    on_click=lambda e, cid=cod: preencher_formulario(cid)
                                )
                            ),
                        ]
                    )
                )
        page.update()

    def preencher_formulario(cod_esp: str):
        registro = crud_especialidades.buscar_especialidade(cod_esp)
        if registro:
            selected_id["value"] = int(registro[0])
            nome_field.value = registro[1]
            valor_field.value = registro[2]
            limite_field.value = registro[3]
            page.update()

    def on_inserir_click(_):
        nome, valor, limite = nome_field.value.strip(), valor_field.value.strip(), limite_field.value.strip()
        if not nome or not valor or not limite:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"))
            page.snack_bar.open = True
            page.update()
            return
        try:
            codigo = max([int(esp[0]) for esp in crud_especialidades.ler_especialidades_exaustivamente()] or [0]) + 1
            esp_obj = Especialidade(
                cod_especialidade=int(codigo),
                descricao=nome,
                valor_consulta=float(valor),
                limite_diario=int(limite)
            )
            if crud_especialidades.cadastrar_especialidade(esp_obj):
                nome_field.value = valor_field.value = limite_field.value = ""
                selected_id["value"] = 0
                page.snack_bar = ft.SnackBar(ft.Text("Especialidade inserida com sucesso!"))
                page.snack_bar.open = True
                carregar_tabela()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Erro ao inserir especialidade."))
                page.snack_bar.open = True
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {err}"))
            page.snack_bar.open = True
        page.update()

    def on_salvar_click(_):
        if selected_id["value"] == 0:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione uma especialidade para salvar."))
            page.snack_bar.open = True
            page.update()
            return
        nome, valor, limite = nome_field.value.strip(), valor_field.value.strip(), limite_field.value.strip()
        if not nome or not valor or not limite:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"))
            page.snack_bar.open = True
            page.update()
            return
        try:
            esp_obj = Especialidade(
                cod_especialidade=int(selected_id["value"]),
                descricao=nome,
                valor_consulta=float(valor),
                limite_diario=int(limite)
            )
            if crud_especialidades.atualizar_especialidade(esp_obj):
                page.snack_bar = ft.SnackBar(ft.Text("Especialidade atualizada com sucesso!"))
                page.snack_bar.open = True
                selected_id["value"] = 0
                nome_field.value = valor_field.value = limite_field.value = ""
                carregar_tabela()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Erro ao atualizar especialidade."))
                page.snack_bar.open = True
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao atualizar especialidade: {err}"))
            page.snack_bar.open = True
        page.update()

    def on_excluir_click(_):
        if selected_id["value"] == 0:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione uma especialidade para excluir."))
            page.snack_bar.open = True
            page.update()
            return
        if crud_especialidades.excluir_especialidade(str(selected_id["value"])):
            selected_id["value"] = 0
            nome_field.value = valor_field.value = limite_field.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("Especialidade excluída com sucesso!"))
            page.snack_bar.open = True
            carregar_tabela()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao excluir especialidade."))
            page.snack_bar.open = True
        page.update()

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
        on_change=lambda e: carregar_tabela(e.control.value),
    )

    botoes_form = ft.Column(
        [
            ft.Text("Detalhes de Especialidades", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            nome_field,
            valor_field,
            limite_field,
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
            ft.Text("Lista de Especialidades", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            barra_pesquisa,
            ft.Container(content=tabela_especialidades, expand=True),
        ],
        spacing=10,
        expand=True,
    )

    lista_especialidades = ft.Container(content=coluna_lista, padding=20, margin=ft.margin.only(right=10), bgcolor=ft.Colors.BLUE_GREY_700, border_radius=10, expand=True)
    formulario_especialidade = ft.Container(content=botoes_form, padding=20, margin=ft.margin.only(left=10), bgcolor=ft.Colors.BLUE_GREY_700, border_radius=10, expand=True)

    conteudo_principal = ft.Row(
        [
            ft.Container(content=lista_especialidades, expand=6),
            ft.Container(content=formulario_especialidade, expand=4),
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    container_view_body = ft.Container(content=conteudo_principal, expand=True, padding=ft.padding.only(left=20, right=20, top=20, bottom=20))
    carregar_tabela()

    view = ft.View(
        "/especialidades",
        [
            ft.AppBar(
                title=ft.Text("Gerenciamento de Especialidades"),
                bgcolor=ft.Colors.BLUE_GREY_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                leading_width=60,
            ),
            container_view_body,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_800,
    )

    return {"conteudo": view, "carregar_tabela": carregar_tabela}
