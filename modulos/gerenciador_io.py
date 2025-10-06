from pathlib import Path
import csv

CAMINHO_DADOS = Path("dados")

def ler_registros(nome_arquivo: str) -> list[list[str]]:
    caminho_arquivo = CAMINHO_DADOS/nome_arquivo
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8', newline='') as f:
            leitor = csv.reader(f, delimiter=';')
            return [linha for linha in leitor if linha]
    except FileNotFoundError:
        return []

def salvar_novo_registro(nome_arquivo: str, registros: list):
    caminho_arquivo = CAMINHO_DADOS/nome_arquivo
    with open(caminho_arquivo, 'a', encoding='utf-8', newline='') as f:
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(registros)

def reescrever_arquivo_completo(nome_arquivo: str, registros: list[list]):
    caminho_arquivo = CAMINHO_DADOS / nome_arquivo
    with open(caminho_arquivo, 'w', encoding='utf-8', newline='') as f:
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(registros)