from modulos.modelos import Exame

class CrudExames:
    NOME_TABELA = 'exames'

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def cadastrar_exame(self, exame_obj: Exame) -> bool:
        registro_a_salvar = exame_obj.to_list()
        chave_primaria = exame_obj.cod_exame

        if self.bst.buscar(chave_primaria) is not None:
            print(f"Erro: Exame com código '{chave_primaria}' já existe.")
            return False

        try:
            novo_num_linha = self.io_manager.anexar_registro(registro_a_salvar)
            self.bst.inserir(chave_primaria, novo_num_linha)
            return True

        except ValueError as e:
            print(f"Erro ao cadastrar exame: {e}")
            return False

    def buscar_exame(self, cod_exame: str) -> list[str] | None:
        try:
            chave_busca_int = int(cod_exame)

        except ValueError:
            return None

        num_linha = self.bst.buscar(chave_busca_int)

        if num_linha is None:
            return None

        return self.io_manager.ler_linha(num_linha)

    def excluir_exame(self, cod_exame: str) -> bool:
        return self.servicos.remover_fisicamente_registro(self.NOME_TABELA, cod_exame)

    def ler_exames_exaustivamente(self) -> list[list[str]]:
        return self.io_manager.ler_todos()
