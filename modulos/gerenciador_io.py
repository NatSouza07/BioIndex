from pathlib import Path
import csv

CAMINHO_DADOS = Path("dados")

class GerenciadorTabela:
    def __init__(self, nome_arquivo: str):
        self.nome_arquivo = nome_arquivo
        self.caminho_arquivo = CAMINHO_DADOS / nome_arquivo

    def ler_todos(self) -> list[list[str]]:
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8', newline='') as f:
                leitor = csv.reader(f, delimiter=';')
                return [linha for linha in leitor if linha]
        except FileNotFoundError:
            return []

    def ler_linha(self, num_linha: int) -> list[str]:
        registros = self.ler_todos()
        if 1 <= num_linha <= len(registros):
            return registros[num_linha - 1]
        return []

    def anexar_registro(self, registro: list[str]) -> int:
        registros = self.ler_todos()
        with open(self.caminho_arquivo, 'a', encoding='utf-8', newline='') as f:
            escritor = csv.writer(f, delimiter=';')
            escritor.writerow(registro)
        return len(registros) + 1

    def reescrever_arquivo_completo(self, registros: list[list[str]]):
        with open(self.caminho_arquivo, 'w', encoding='utf-8', newline='') as f:
            escritor = csv.writer(f, delimiter=';')
            escritor.writerows(registros)
