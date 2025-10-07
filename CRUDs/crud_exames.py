from typing import List, Optional, Dict, Any
from modulos.modelos import Exame

class CrudExames:
    NOME_TABELA = "exames"

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.io_tabelas.get(self.NOME_TABELA)
        self.bst = servicos.indices.get(self.NOME_TABELA)

    def cadastrar(self, exame_obj: Exame) -> bool:
        if not self.servicos.lookup_especialidade(str(exame_obj.cod_especialidade)):
            print(f"Erro FK: Especialidade com código '{exame_obj.cod_especialidade}' não encontrada.")
            return False

        chave = exame_obj.cod_exame
        if self.bst.buscar(chave):
            print(f"Erro: Exame com código '{chave}' já existe.")
            return False

        registro = [
            str(exame_obj.cod_exame),
            exame_obj.descricao,
            str(exame_obj.cod_especialidade),
            str(exame_obj.valor_exame)
        ]

        try:
            todos = self.io_manager.ler_todos()
            todos.append(registro)
            self.io_manager.reescrever_arquivo_completo(todos)

            self._atualizar_indice()
            print(f"Exame '{exame_obj.descricao}' cadastrado com sucesso.")
            return True
        except Exception as e:
            print(f"Erro inesperado ao cadastrar exame: {e}")
            return False

    def buscar(self, cod_exame: int) -> Optional[List[str]]:
        num_linha = self.bst.buscar(cod_exame)
        if num_linha is None:
            return None
        return self.io_manager.ler_linha(num_linha)

    def consultar_completo(self, cod_exame: int) -> Optional[Dict[str, Any]]:
        registro = self.buscar(cod_exame)
        if not registro:
            return None
        cod_esp = registro[2]
        registro_esp = self.servicos.lookup_especialidade(cod_esp)
        return {
            "codigo_exame": int(registro[0]),
            "descricao_exame": registro[1],
            "valor_exame": float(registro[3]),
            "codigo_especialidade": int(cod_esp),
            "especialidade_nome": registro_esp[1] if registro_esp else "Especialidade não encontrada"
        }

    def atualizar(self, exame_obj: Exame) -> bool:
        todos = self.io_manager.ler_todos()
        for i, reg in enumerate(todos):
            if int(reg[0]) == exame_obj.cod_exame:
                todos[i] = [
                    str(exame_obj.cod_exame),
                    exame_obj.descricao,
                    str(exame_obj.cod_especialidade),
                    str(exame_obj.valor_exame)
                ]
                try:
                    self.io_manager.reescrever_arquivo_completo(todos)
                    self._atualizar_indice()
                    return True
                except Exception as e:
                    print(f"Erro ao atualizar exame: {e}")
                    return False
        print(f"Exame {exame_obj.cod_exame} não encontrado para atualização.")
        return False

    def excluir(self, cod_exame: int) -> bool:
        registro = self.buscar(cod_exame)
        if not registro:
            print(f"Erro: Exame {cod_exame} não encontrado para exclusão.")
            return False
        try:
            todos = self.io_manager.ler_todos()
            todos = [reg for reg in todos if int(reg[0]) != cod_exame]
            self.io_manager.reescrever_arquivo_completo(todos)
            self._atualizar_indice()
            return True
        except Exception as e:
            print(f"Erro ao excluir exame: {e}")
            return False

    def _atualizar_indice(self):
        self.bst = type(self.bst)()
        for i, reg in enumerate(self.io_manager.ler_todos()):
            chave = int(reg[0])
            self.bst.inserir(chave, i + 1)

    def ler_todos(self) -> List[List[str]]:
        return self.io_manager.ler_todos()
