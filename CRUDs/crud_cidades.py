from modulos.modelos import Cidade

class CrudCidades:
    NOME_TABELA = 'cidades'

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def cadastrar_cidade(self, cidade_obj: Cidade) -> bool:
        registro_a_salvar = cidade_obj.to_list()

        try:
            novo_num_linha = self.io_manager.anexar_registro(registro_a_salvar)

            chave_primaria_int = cidade_obj.cod_cidade

            self.bst.inserir(chave_primaria_int, novo_num_linha)
            return True

        except ValueError as e:
            print(f"Erro ao cadastrar cidade: {e}")
            return False


    def buscar_cidade(self, cod_cidade: str) -> list[str] | None:
        try:
            chave_busca_int = int(cod_cidade)

        except ValueError:
            return None

        num_linha = self.bst.buscar(chave_busca_int)

        if num_linha is None:
            return None

        return self.io_manager.ler_linha(num_linha)


    def excluir_cidade(self, cod_cidade: str) -> bool:
        return self.servicos.remover_fisicamente_registro(self.NOME_TABELA, cod_cidade)


    def ler_cidades_exaustivamente(self) -> list[list[str]]:
        return self.io_manager.ler_todos()


    def lookup_cidade(self, cod_cidade_fk: str) -> list[str] | None:

        try:
            chave_busca_int = int(cod_cidade_fk)

        except ValueError:
            return None

        num_linha = self.bst.buscar(chave_busca_int)

        if num_linha is None:
            return None

        registro_cidade = self.io_manager.ler_linha(num_linha)

        return registro_cidade