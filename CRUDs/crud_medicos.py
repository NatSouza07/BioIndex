from typing import Dict, Any, Optional
from modulos.modelos import Medico

class CrudMedicos:
    NOME_TABELA = 'medicos'

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def cadastrar_medico(self, medico_obj: Medico) -> bool:
        registro_a_salvar = medico_obj.to_list()
        chave_primaria = medico_obj.cod_medico

        if not self.servicos.lookup_cidade(str(medico_obj.cod_cidade)):
            print(f"Erro FK: Cidade {medico_obj.cod_cidade} não encontrada.")
            return False

        if not self.servicos.lookup_especialidade(str(medico_obj.cod_especialidade)):
            print(f"Erro FK: Especialidade {medico_obj.cod_especialidade} não encontrada.")
            return False

        if self.bst.buscar(chave_primaria) is not None:
            print(f"Erro: Médico com código '{chave_primaria}' já existe.")
            return False

        try:
            novo_num_linha = self.io_manager.anexar_registro(registro_a_salvar)
            self.bst.inserir(chave_primaria, novo_num_linha)
            return True
        except ValueError as e:
            print(f"Erro ao cadastrar médico: {e}")
            return False

    def buscar_medico(self, cod_medico: str) -> list[str] | None:
        try:
            chave_busca_int = int(cod_medico)
        except ValueError:
            return None

        num_linha = self.bst.buscar(chave_busca_int)
        if num_linha is None:
            return None

        return self.io_manager.ler_linha(num_linha)

    def consultar_completo(self, cod_medico: str) -> Optional[Dict[str, Any]]:
        registro_medico = self.buscar_medico(cod_medico)
        if registro_medico is None:
            return None

        cod_cidade_fk = registro_medico[4]
        cod_especialidade_fk = registro_medico[5]

        registro_cidade = self.servicos.lookup_cidade(cod_cidade_fk)
        registro_especialidade = self.servicos.lookup_especialidade(cod_especialidade_fk)

        resultado_completo = {
            "codigo": int(registro_medico[0]),
            "nome": registro_medico[1],
            "endereco": registro_medico[2],
            "telefone": registro_medico[3],

            "cidade_codigo": int(cod_cidade_fk),
            "cidade_nome": registro_cidade[1] if registro_cidade else "Cidade não encontrada",
            "cidade_estado": registro_cidade[2] if registro_cidade else "N/A",

            "especialidade_codigo": int(cod_especialidade_fk),
            "especialidade_desc": registro_especialidade[1] if registro_especialidade else "Especialidade não encontrada",
            "especialidade_valor": float(registro_especialidade[2]) if registro_especialidade else 0.0,
            "especialidade_limite": int(registro_especialidade[3]) if registro_especialidade else 0
        }
        return resultado_completo

    def excluir_medico(self, cod_medico: str) -> bool:
        num_linha = self.bst.buscar(int(cod_medico))
        if num_linha is None:
            return False
        self.bst.remover(int(cod_medico))
        return self.servicos.remover_fisicamente_registro(self.NOME_TABELA, cod_medico)

    def ler_medicos_exaustivamente(self) -> list[list[str]]:
        return self.io_manager.ler_todos()

    def atualizar_medico(self, medico_obj: Medico) -> bool:
        registro_existente = self.buscar_medico(str(medico_obj.cod_medico))
        if registro_existente is None:
            print(f"Erro: Médico com código '{medico_obj.cod_medico}' não encontrado para atualizar.")
            return False

        if not self.servicos.lookup_cidade(str(medico_obj.cod_cidade)):
            print(f"Erro FK: Cidade {medico_obj.cod_cidade} não encontrada.")
            return False

        if not self.servicos.lookup_especialidade(str(medico_obj.cod_especialidade)):
            print(f"Erro FK: Especialidade {medico_obj.cod_especialidade} não encontrada.")
            return False

        try:
            registro_atualizado = medico_obj.to_list()
            num_linha = self.bst.buscar(medico_obj.cod_medico)
            if num_linha is None:
                return False
            self.io_manager.atualizar_linha(num_linha, registro_atualizado)
            return True
        except ValueError as e:
            print(f"Erro ao atualizar médico: {e}")
            return False
