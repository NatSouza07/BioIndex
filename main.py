import flet as ft
from pathlib import Path
from views.main_view import ViewManager

CAMINHO_DADOS = Path("dados")

def inicializar_estruturas_dados():
    CAMINHO_DADOS.mkdir(exist_ok=True)

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
        caminho_arquivo = CAMINHO_DADOS / nome_arquivo
        if not caminho_arquivo.exists():
            caminho_arquivo.touch()

def main(page: ft.Page):
    inicializar_estruturas_dados()
    ViewManager(page)

if __name__ == '__main__':
    print("Inicializando: Verificando estrutura de arquivos...")
    inicializar_estruturas_dados()

    print("Inicializando: Interface gráfica pronta.")
    ft.app(target=main, assets_dir="assets")
