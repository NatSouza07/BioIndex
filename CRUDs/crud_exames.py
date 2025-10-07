from typing import List, Optional,Dict, Any
from modulos.modelos import Exame
from servicos import GerenciadorServicos

class CrudExames:
    NOME_TABELA = 'exames'
    def __init__(self, servicos: GerenciadorServicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def cadastrar(self, exame_obj: Exame) -> bool:
        if not self.servicos.lookup_especialidade(str(exame_obj.cod_especialidade)):
            print(f"Erro FK: Especialidade com código '{exame_obj.cod_especialidade}' não encontrada.")
            return False
        registro_salvar = [
            str(exame_obj.codigo),
            exame_obj.descricao,
            str(exame_obj.codigo_especialidade),
            str(exame_obj.valor_exame)
        ]
        chave_primaria = exame_obj.cod_exame


        if self.bst.buscar(chave_primaria) is not None:
            print(f"Erro: Exame com código'{chave_primaria}' já existe.")
            return False

        try:
            novo_num_linha = self.io_manager.anexar_registro(registro_salvar)
            self.bst.inserir(chave_primaria, novo_num_linha)
            print (f"Exame '{exame_obj.descricao}' cadastrado com sucesso.")
            return True
        except Exception as e:
            print(f"Erro inesperado ao cadastrar exame: {e}")
            return False
    def buscar(self, cod_exame: str) -> Optional[list]:
        try:
            chave_busca_int = int(cod_exame)
        except ValueError:
            print("Erro: Código do exame deve ser um número")
            return None
        num_linha = self.bst.buscar(chave_busca_int)
        if num_linha is None:
            return None
        return self.io_manager.ler_linha(num_linha)

    def consultar_completo(self, cod_exame: str) -> Optional[Dict[str, Any]]:

        registro_exame = self.buscar(cod_exame)

        if registro_exame is None:
            return None

        cod_especialidade_fk = registro_exame[2]

        registro_especialidade = self.servicos.lookup_especialidade(cod_especialidade_fk)

        resultado_completo = {
            "codigo_exame": int(registro_exame[0]),
            "descricao_exame": registro_exame[1],
            "valor_exame": float(registro_exame[3]),
            "codigo_especialidade": int(cod_especialidade_fk),
            "especialidade_nome": registro_especialidade[
                1] if registro_especialidade else "Especialidade não encontrada"
        }

        return resultado_completo

    def excluir(self, cod_exame: str) -> bool:

        return self.servicos.remover_fisicamente_registro(self.NOME_TABELA, cod_exame)

    def ler_todos(self)-> List[list]:
        return self.io_manager.ler_todos()

