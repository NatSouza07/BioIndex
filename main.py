import flet as ft
from pathlib import Path
# import modulos.servicos as servicos
# from modulos.servicos import GerenciadorServicos

# GERENCIADOR = GerenciadorServicos()

def inicializar_estruturas_dados():
    caminho_dados = Path("dados")
    caminho_dados.mkdir(exist_ok=True)

    arquivos_necessarios = [
        "cidades.txt",
        "pacientes.txt",
        "especialidades.txt",
        "medicos.txt",
        "exames.txt",
        "consultas.txt",
        "diarias.txt",
        "contadores.txt"
    ]

    for nome_arquivo in arquivos_necessarios:
        caminho_arquivo= caminho_dados / nome_arquivo
        if not caminho_arquivo.exists():
            caminho_arquivo.touch()
            print(f"Arquivo de dados '{caminho_arquivo}' criado.")

def main(page: ft.Page):
    page.title = 'BioIndex'
    page.window_width =  800
    page.window_height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = ft.Colors.BLUE_GREY_50

    cabecalho = ft.Container(
        content = ft.Text(
            "Bem-vindo ao BioIndex",
            size = 30,
            weight = ft.FontWeight.BOLD,
            color = ft.Colors.BLUE_700
        ),
        padding = ft.padding.all(20),
        alignment = ft.alignment.center,
        width = 800
    )

    instrucao = ft.Text(
        "Backend (lógica de dados) inicializada com sucesso. Pronto para a navegação.",
        size = 16,
        color = ft.Colors.WHITE70
    )

    page.add(
        ft.Container(
            content = ft.Column(
                [
                    cabecalho,
                    ft.Divider(),
                    ft.Container(
                        content = instrucao,
                        padding = ft.padding.all(30),
                        bgcolor = ft.Colors.BLUE_GREY_700,
                        border_radius = 10
                    )
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 20
            ),
            padding = ft.padding.all(20),
            width = 800
        )
    )

    page.update()

if __name__ == '__main__':

    print("Inicializando: Verificando estrutura de  arquivos...")
    inicializar_estruturas_dados()

    print ("Inicializando: Carregando dados e construindo índices em memória...")
   #servicos.carregar_indices_inicais()

    print("Inicializando: Interface gráfica pronta.")
    ft.app(target=main)