import flet as ft
from pathlib import Path
import modulos.servicos as servicos

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

def main(pagina: ft.Page):
    pagina.title = 'BioIndex'
    pagina.window_widht =  800
    pagina.window_height = 600
    pagina.add(ft.Text("Bem-vindo á BioIndex!", size=30))

ft.app(target=main)

if __name__ == '__main__':

    print("Inicializando: Verificando estrutura de  arquivos...")
    inicializar_estruturas_dados()

    print ("Inicializando: Carregando dados e construindo índices em memória...")
    servicos.carregar_indices_inicais()

    print("Inicializando: Interface gráfica pronta.")
    ft.app(target=main)