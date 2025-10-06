from modulos.gerenciador_io import GerenciadorTabela
from modulos.arvore_binaria import ArvoreBinaria

INDICES = {}
IO_TABELAS = {}

class GerenciadorServicos:
    def __init__(self):
        self._inicializar_gerenciadores()

        from CRUDs.crud_cidades import CrudCidades
        from CRUDs.crud_pacientes import CrudPacientes
        from CRUDs.crud_especialidades import CrudEspecialidades
        from CRUDs.crud_medicos import CrudMedicos
        #from CRUDs.crud_exames import CrudExames
        from CRUDs.crud_consultas import CrudConsultas
        from CRUDs.crud_diarias import CrudDiarias

        self.crud_cidades = CrudCidades(self)
        self.crud_pacientes = CrudPacientes(self)
        self.crud_especialidades = CrudEspecialidades(self)
        self.crud_medicos = CrudMedicos(self)
        #self.crud_exames = CrudExames(self)
        self.crud_diarias = CrudDiarias(self)
        self.crud_consultas = CrudConsultas(self)

        # Disponibilizar regras de negócio
        import modulos.regras_negocio as regras_negocio
        self.regras_negocio = regras_negocio

    def _inicializar_gerenciadores(self):
        arquivos_indexados = [
            "cidades.txt",
            "pacientes.txt",
            "especialidades.txt",
            "medicos.txt",
            "exames.txt",
            "consultas.txt",
            "diarias.txt",
        ]

        for nome_arquivo in arquivos_indexados:
            nome_tabela = nome_arquivo.replace('.txt', '')
            IO_TABELAS[nome_tabela] = GerenciadorTabela(nome_arquivo)
            INDICES[nome_tabela] = ArvoreBinaria()

        self.carregar_indices_iniciais()

    @staticmethod
    def carregar_indices_iniciais():
        for nome_tabela, io_manager in IO_TABELAS.items():
            INDICES[nome_tabela] = ArvoreBinaria()
            registros = io_manager.ler_todos()

            for num_linha, registro_dados in enumerate(registros, 1):
                chave_primaria = registro_dados[0]
                INDICES[nome_tabela].inserir(chave_primaria, num_linha)

    def remover_fisicamente_registro(self, nome_tabela: str, chave: str) -> bool:
        io_manager = IO_TABELAS.get(nome_tabela)
        if io_manager is None:
            return False

        registros_atuais = io_manager.ler_todos()
        registros_mantidos = []
        registro_removido_encontrado = False

        for registro in registros_atuais:
            if registro[0] != chave:
                registros_mantidos.append(registro)
            else:
                registro_removido_encontrado = True

        if not registro_removido_encontrado:
            return False

        io_manager.reescrever_arquivo_completo(registros_mantidos)
        self.carregar_indices_iniciais()
        return True

    def lookup_cidade(self, cod_cidade: str) -> list[str] | None:
        try:
            chave_busca_int = int(cod_cidade)

        except ValueError:
            return None

        num_linha = self.INDICES['cidades'].buscar(chave_busca_int)

        if num_linha is None:
            return None

        registro_cidade = self.IO_TABELAS['cidades'].ler_linha(num_linha)
        return registro_cidade

    def lookup_paciente(self, cod_paciente: str) -> list[str] | None:
        try:
            chave_busca_int = int(cod_paciente)

        except ValueError:
            return None

        num_linha = self.INDICES['pacientes'].buscar(chave_busca_int)

        if num_linha is None:
            return None

        registro_paciente = self.IO_TABELAS['pacientes'].ler_linha(num_linha)
        return registro_paciente

    def lookup_medico(self, cod_medico: str) -> list[str] | None:
        try:
            chave_busca_int = int(cod_medico)

        except ValueError:
            return None

        num_linha = self.INDICES['medicos'].buscar(chave_busca_int)

        if num_linha is None:
            return None

        registro_medico = self.IO_TABELAS['medicos'].ler_linha(num_linha)
        return registro_medico

    def lookup_especialidade(self, cod_especialidade: str) -> list[str] | None:
        try:
            chave_busca_int = int(cod_especialidade)

        except ValueError:
            return None

        num_linha = self.INDICES['especialidades'].buscar(chave_busca_int)

        if num_linha is None:
            return None

        registro_especialidade = self.IO_TABELAS['especialidades'].ler_linha(num_linha)
        return registro_especialidade

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