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

    def excluir_medico(self, cod_medico: str) -> bool:
        return self.servicos.remover_fisicamente_registro(self.NOME_TABELA, cod_medico)

    def ler_medicos_exaustivamente(self) -> list[list[str]]:
        return self.io_manager.ler_todos()

