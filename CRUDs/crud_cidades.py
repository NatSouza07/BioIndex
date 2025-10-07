from modulos.modelos import Cidade

class CrudCidades:
    NOME_TABELA = "cidades"

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def gerar_proximo_codigo(self) -> int:
        registros = self.ler_cidades_exaustivamente()
        codigos_existentes = set()
        for r in registros:
            try:
                codigos_existentes.add(int(r[0]))
            except (ValueError, TypeError, IndexError):
                continue
        codigo = 1
        while codigo in codigos_existentes:
            codigo += 1
        return codigo

    def cadastrar_cidade(self, cidade_obj: Cidade) -> bool:
        try:
            if cidade_obj.cod_cidade is None:
                cidade_obj.cod_cidade = self.gerar_proximo_codigo()
            chave_primaria_int = int(cidade_obj.cod_cidade)
            registro_a_salvar = cidade_obj.to_list()
            novo_num_linha = self.io_manager.anexar_registro(registro_a_salvar)
            self.bst.inserir(chave_primaria_int, novo_num_linha)
            try:
                self.servicos.carregar_indices_iniciais()
            except (AttributeError, RuntimeError):
                pass
            return True
        except (ValueError, TypeError, OSError) as e:
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

    def atualizar_cidade(self, cod_cidade: str, descricao: str, estado: str) -> bool:
        try:
            registros = self.io_manager.ler_todos()
            cod_str = str(cod_cidade)
            encontrado = False
            for i, reg in enumerate(registros):
                if reg and reg[0] == cod_str:
                    registros[i] = [cod_str, descricao, estado]
                    encontrado = True
                    break
            if not encontrado:
                return False
            self.io_manager.reescrever_arquivo_completo(registros)
            try:
                self.servicos.carregar_indices_iniciais()
            except (AttributeError, RuntimeError):
                pass
            return True
        except (OSError, ValueError, TypeError) as e:
            print(f"Erro ao atualizar cidade: {e}")
            return False

    def excluir_cidade(self, cod_cidade: str) -> bool:
        try:
            result = self.servicos.remover_fisicamente_registro(self.NOME_TABELA, cod_cidade)
            if result:
                try:
                    chave_int = int(cod_cidade)
                    self.bst.remover(chave_int)
                except (ValueError, KeyError):
                    pass
                try:
                    self.servicos.carregar_indices_iniciais()
                except (AttributeError, RuntimeError):
                    pass
            return result
        except (OSError, ValueError, TypeError) as e:
            print(f"Erro ao excluir cidade: {e}")
            return False

    def ler_cidades_exaustivamente(self) -> list[list[str]]:
        try:
            return self.io_manager.ler_todos()
        except (OSError, AttributeError, TypeError):
            return []
