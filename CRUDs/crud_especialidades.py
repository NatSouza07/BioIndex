from modulos.modelos import Especialidade

class CrudEspecialidades:
    NOME_TABELA = 'especialidades'

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def cadastrar_especialidade(self, especialidade_obj: Especialidade) -> bool:
        registro_a_salvar = especialidade_obj.to_list()
        chave_primaria = especialidade_obj.cod_especialidade

        if self.bst.buscar(chave_primaria) is not None:
            print(f"Erro: Especialidade com código '{chave_primaria}' já existe.")
            return False

        try:
            novo_num_linha = self.io_manager.anexar_registro(registro_a_salvar)
            self.bst.inserir(chave_primaria, novo_num_linha)
            return True

        except ValueError as e:
            print(f"Erro ao cadastrar especialidade: {e}")
            return False

    def buscar_especialidade(self, cod_especialidade: str) -> list[str] | None:
        try:
            chave_busca_int = int(cod_especialidade)

        except ValueError:
            return None

        num_linha = self.bst.buscar(chave_busca_int)

        if num_linha is None:
            return None

        return self.io_manager.ler_linha(num_linha)

    def excluir_especialidade(self, cod_especialidade: str) -> bool:
        return self.servicos.remover_fisicamente_registro(self.NOME_TABELA, cod_especialidade)

    def ler_especialidades_exaustivamente(self) -> list[list[str]]:
        return self.io_manager.ler_todos()
