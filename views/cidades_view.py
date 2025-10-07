import flet as ft
from CRUDs.crud_cidades import CrudCidades
from modulos.modelos import Cidade

def cidades_view(page: ft.Page, crud_cidades: CrudCidades):
    white_text_style = ft.TextStyle(color=ft.Colors.WHITE)
    selected_id = {"value": ""}

    tabela_cidades = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", style=white_text_style)),
            ft.DataColumn(ft.Text("Nome da Cidade", style=white_text_style)),
            ft.DataColumn(ft.Text("UF", style=white_text_style)),
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

    nome_cidade_field = ft.TextField(
        label="Nome da Cidade",
        hint_text="Digite o nome da cidade",
        border_radius=5,
        height=45,
        content_padding=10,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        label_style=ft.TextStyle(color=ft.Colors.BLACK54),
        focused_border_color=ft.Colors.BLUE_900,
        cursor_color=ft.Colors.BLUE_900,
    )

    uf_field = ft.TextField(
        label="UF",
        hint_text="Digite a UF",
        border_radius=5,
        height=45,
        content_padding=10,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        label_style=ft.TextStyle(color=ft.Colors.BLACK54),
        focused_border_color=ft.Colors.BLUE_900,
        cursor_color=ft.Colors.BLUE_900,
        expand= True,
    )

    def atualizar_tabela(filtro=""):
        try:
            crud_cidades.servicos.carregar_indices_iniciais()
        except (AttributeError, RuntimeError):
            pass
        tabela_cidades.rows.clear()
        try:
            cidades = crud_cidades.ler_cidades_exaustivamente()
        except (OSError, TypeError) as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar cidades: {err}"))
            page.snack_bar.open = True
            page.update()
            return
        filtro_lower = (filtro or "").lower()
        for cidade in cidades:
            if len(cidade) < 3:
                continue
            cod, nome, uf = str(cidade[0]), cidade[1], cidade[2]
            if filtro_lower in cod.lower() or filtro_lower in nome.lower() or filtro_lower == "":
                tabela_cidades.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(cod, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(nome, color=ft.Colors.WHITE)),
                            ft.DataCell(ft.Text(uf, color=ft.Colors.WHITE)),
                            ft.DataCell(
                                ft.IconButton(
                                    ft.Icons.SEARCH,
                                    icon_color=ft.Colors.BLUE_300,
                                    tooltip="Selecionar cidade",
                                    on_click=lambda e, cid=cod: preencher_formulario(cid)
                                )
                            ),
                        ]
                    )
                )
        page.update()

    def preencher_formulario(cod_cidade: str):
        registro = crud_cidades.buscar_cidade(cod_cidade)
        if registro:
            selected_id["value"] = registro[0]
            nome_cidade_field.value = registro[1]
            uf_field.value = registro[2]
            page.update()

    def on_inserir_click(_):
        nome = nome_cidade_field.value.strip()
        uf = uf_field.value.strip()
        if not nome or not uf:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"))
            page.snack_bar.open = True
            page.update()
            return
        try:
            codigo = crud_cidades.gerar_proximo_codigo()
            cidade_obj = Cidade(cod_cidade=codigo, descricao=nome, estado=uf)
            if crud_cidades.cadastrar_cidade(cidade_obj):
                nome_cidade_field.value = ""
                uf_field.value = ""
                selected_id["value"] = ""
                page.snack_bar = ft.SnackBar(ft.Text("Cidade inserida com sucesso!"))
                page.snack_bar.open = True
                atualizar_tabela()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Erro ao inserir cidade."))
                page.snack_bar.open = True
        except (ValueError, TypeError, OSError) as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {err}"))
            page.snack_bar.open = True
        page.update()

    def on_salvar_click(_):
        if not selected_id["value"]:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione uma cidade para salvar (editar)."))
            page.snack_bar.open = True
            page.update()
            return
        nome = nome_cidade_field.value.strip()
        uf = uf_field.value.strip()
        if not nome or not uf:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"))
            page.snack_bar.open = True
            page.update()
            return
        ok = crud_cidades.atualizar_cidade(selected_id["value"], nome, uf)
        if ok:
            page.snack_bar = ft.SnackBar(ft.Text("Cidade atualizada com sucesso!"))
            page.snack_bar.open = True
            selected_id["value"] = ""
            nome_cidade_field.value = ""
            uf_field.value = ""
            atualizar_tabela()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao atualizar cidade."))
            page.snack_bar.open = True
        page.update()

    def on_excluir_click(cod_cidade: str):
        if not cod_cidade:
            page.snack_bar = ft.SnackBar(ft.Text("Código inválido."))
            page.snack_bar.open = True
            page.update()
            return
        ok = crud_cidades.excluir_cidade(cod_cidade)
        if ok:
            if selected_id["value"] == cod_cidade:
                selected_id["value"] = ""
                nome_cidade_field.value = ""
                uf_field.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("Cidade excluída com sucesso!"))
            page.snack_bar.open = True
            atualizar_tabela()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao excluir cidade."))
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
        on_change=lambda e: atualizar_tabela(e.control.value),
    )

    botoes_form = ft.Column(
        [
            ft.Text("Detalhes de Cidades", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            nome_cidade_field,
            uf_field,
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
                        on_click=lambda _: on_excluir_click(selected_id["value"]),
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
            ft.Text("Lista de Cidades", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            barra_pesquisa,
            ft.Container(content=tabela_cidades, expand=True),
        ],
        spacing=10,
        expand=True,
    )

    lista_cidades = ft.Container(
        content=coluna_lista,
        padding=20,
        margin=ft.margin.only(right=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    formulario_cidade = ft.Container(
        content=botoes_form,
        padding=20,
        margin=ft.margin.only(left=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        expand=True,
    )

    conteudo_principal = ft.Row(
        [
            ft.Container(content=lista_cidades, expand=6),
            ft.Container(content=formulario_cidade, expand=4),
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
        "/cidades",
        [
            ft.AppBar(
                title=ft.Text("Gerenciamento de Cidades"),
                bgcolor=ft.Colors.BLUE_GREY_700,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                leading_width=60,
            ),
            container_view_body,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_800,
    )
