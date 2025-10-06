from modulos.modelos import Diaria

class CrudDiarias:
    NOME_TABELA = 'diarias'

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def cadastrar_diaria(self, diaria_obj: Diaria) -> bool:
        chave_composta_str = diaria_obj.gerar_chave_composta()
        registro_a_salvar = diaria_obj.to_list()

        if self.bst.buscar(chave_composta_str) is not None:
            print(f"Erro: Diária com chave '{chave_composta_str}' já existe.")
            return False

        try:
            novo_num_linha = self.io_manager.anexar_registro(registro_a_salvar)
            self.bst.inserir(chave_composta_str, novo_num_linha)
            return True

        except ValueError as e:
            print(f"Erro ao cadastrar diária: {e}")
            return False

    def buscar_diaria(self, cod_dia: str, cod_especialidade: str) -> list[str] | None:
        chave_busca_str = f"{cod_dia}|{cod_especialidade}"
        num_linha = self.bst.buscar(chave_busca_str)

        if num_linha is None:
            return None
        return self.io_manager.ler_linha(num_linha)

    def excluir_diaria(self, cod_dia: str, cod_especialidade: str) -> bool:
        chave_busca_str = f"{cod_dia}|{cod_especialidade}"
        return self.servicos.remover_fisicamente_registro(self.NOME_TABELA, chave_busca_str)

    def ler_diarias_exaustivamente(self) -> list[list[str]]:
        return self.io_manager.ler_todos()

    def atualizar_vagas_mais_um(self, cod_dia: str, cod_especialidade: str):
        diaria = self.buscar_diaria(cod_dia, cod_especialidade)

        if not diaria:
            print("Erro: Diária não encontrada para atualizar vagas")
            return False

        try:
            vagas_atual = int(diaria[2])

        except (ValueError, IndexError):
            vagas_atual = 0

        diaria[2] = str(vagas_atual + 1)
        self.io_manager.reescrever_arquivo_completo(self.io_manager.ler_todos())
        self.servicos.carregar_indices_iniciais()
        return True

    def atualizar_vagas_menos_um(self, cod_dia: str, cod_especialidade: str):
        diaria = self.buscar_diaria(cod_dia, cod_especialidade)

        if not diaria:
            print("Erro: Diária não encontrada para atualizar vagas")
            return False

        try:
            vagas_atual = int(diaria[2])

        except (ValueError, IndexError):
            vagas_atual = 0

        diaria[2] = str(max(vagas_atual - 1, 0))
        self.io_manager.reescrever_arquivo_completo(self.io_manager.ler_todos())
        self.servicos.carregar_indices_iniciais()
        return True
