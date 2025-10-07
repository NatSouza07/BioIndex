from typing import Optional, List, Dict
from modulos.gerenciador_io import GerenciadorTabela
from modulos.arvore_binaria import ArvoreBinaria

class GerenciadorServicos:
    def __init__(self):
        self.io_tabelas: Dict[str, GerenciadorTabela] = {}
        self.indices: Dict[str, ArvoreBinaria] = {}
        self.IO_TABELAS = self.io_tabelas
        self.INDICES = self.indices

        self._inicializar_gerenciadores()

        from CRUDs.crud_cidades import CrudCidades
        from CRUDs.crud_pacientes import CrudPacientes
        from CRUDs.crud_especialidades import CrudEspecialidades
        from CRUDs.crud_medicos import CrudMedicos
        from CRUDs.crud_exames import CrudExames
        from CRUDs.crud_consultas import CrudConsultas
        from CRUDs.crud_diarias import CrudDiarias

        self.crud_cidades = CrudCidades(self)
        self.crud_pacientes = CrudPacientes(self)
        self.crud_especialidades = CrudEspecialidades(self)
        self.crud_medicos = CrudMedicos(self)
        self.crud_exames = CrudExames(self)
        self.crud_diarias = CrudDiarias(self)
        self.crud_consultas = CrudConsultas(self)

        import modulos.regras_negocio as regras_negocio
        self.regras_negocio = regras_negocio

    def _inicializar_gerenciadores(self):
        arquivos_indexados = [
            "cidades.txt", "pacientes.txt", "especialidades.txt",
            "medicos.txt", "exames.txt", "consultas.txt", "diarias.txt",
        ]
        for nome_arquivo in arquivos_indexados:
            nome_tabela = nome_arquivo.replace('.txt', '')
            self.io_tabelas[nome_tabela] = GerenciadorTabela(nome_arquivo)
            self.indices[nome_tabela] = ArvoreBinaria()
        self.carregar_indices_iniciais()

    def carregar_indices_iniciais(self):
        for nome_tabela, io_manager in self.io_tabelas.items():
            self.indices[nome_tabela] = ArvoreBinaria()
            registros = io_manager.ler_todos()
            for num_linha, registro_dados in enumerate(registros, 1):
                try:
                    chave_primaria_int = int(registro_dados[0])
                    self.indices[nome_tabela].inserir(chave_primaria_int, num_linha)
                except (ValueError, IndexError):
                    print(f"Aviso: Linha inválida ou chave não numérica no arquivo {nome_tabela}.txt, linha {num_linha - 1}. Ignorando.")

    def remover_fisicamente_registro(self, nome_tabela: str, chave: str) -> bool:
        io_manager = self.io_tabelas.get(nome_tabela)
        if io_manager is None:
            return False
        registros_atuais = io_manager.ler_todos()
        registros_mantidos = [reg for reg in registros_atuais if reg[0] != chave]
        if len(registros_mantidos) == len(registros_atuais):
            return False
        io_manager.reescrever_arquivo_completo(registros_mantidos)
        self.carregar_indices_iniciais()
        return True

    def lookup_cidade(self, cod_cidade: str) -> Optional[List[str]]:
        try:
            chave_busca_int = int(cod_cidade)
        except ValueError:
            return None
        num_linha = self.indices['cidades'].buscar(chave_busca_int)
        if num_linha is None:
            return None
        return self.io_tabelas['cidades'].ler_linha(num_linha)

    def lookup_paciente(self, cod_paciente: str) -> Optional[List[str]]:
        try:
            chave_busca_int = int(cod_paciente)
        except ValueError:
            return None
        num_linha = self.indices['pacientes'].buscar(chave_busca_int)
        if num_linha is None:
            return None
        return self.io_tabelas['pacientes'].ler_linha(num_linha)

    def lookup_medico(self, cod_medico: str) -> Optional[List[str]]:
        try:
            chave_busca_int = int(cod_medico)
        except ValueError:
            return None
        num_linha = self.indices['medicos'].buscar(chave_busca_int)
        if num_linha is None:
            return None
        return self.io_tabelas['medicos'].ler_linha(num_linha)

    def lookup_exame(self, cod_exame: str) -> Optional[List[str]]:
        try:
            chave_busca_int = int(cod_exame)
        except ValueError:
            return None
        num_linha = self.indices['exames'].buscar(chave_busca_int)
        if num_linha is None:
            return None
        return self.io_tabelas['exames'].ler_linha(num_linha)

    def lookup_especialidade(self, cod_especialidade: str) -> Optional[List[str]]:
        try:
            chave_busca_int = int(cod_especialidade)
        except ValueError:
            return None
        num_linha = self.indices['especialidades'].buscar(chave_busca_int)
        if num_linha is None:
            return None
        return self.io_tabelas['especialidades'].ler_linha(num_linha)

    def buscar_diaria(self, cod_dia: str, cod_especialidade: str) -> Optional[List[str]]:
        io_manager_diarias = self.io_tabelas.get('diarias')
        if not io_manager_diarias:
            return None
        todos_registros = io_manager_diarias.ler_todos()
        for registro in todos_registros:
            if registro[0] == cod_dia and registro[1] == str(cod_especialidade):
                return registro
        return None

    def atualizar_vagas_mais_um(self, cod_dia: str, cod_especialidade: str) -> bool:
        io_manager_diarias = self.io_tabelas.get('diarias')
        if not io_manager_diarias:
            return False
        todos_registros = io_manager_diarias.ler_todos()
        registro_encontrado = False
        for registro in todos_registros:
            if registro[0] == cod_dia and registro[1] == str(cod_especialidade):
                try:
                    vagas_atual = int(registro[2])
                except (ValueError, IndexError):
                    vagas_atual = 0
                registro[2] = str(vagas_atual + 1)
                registro_encontrado = True
                break
        if not registro_encontrado:
            novo_registro_diaria = [cod_dia, str(cod_especialidade), '1']
            todos_registros.append(novo_registro_diaria)
        io_manager_diarias.reescrever_arquivo_completo(todos_registros)
        self.carregar_indices_iniciais()
        return True

    def atualizar_vagas_menos_um(self, cod_dia: str, cod_especialidade: str) -> bool:
        io_manager_diarias = self.io_tabelas.get('diarias')
        if not io_manager_diarias:
            return False
        todos_registros = io_manager_diarias.ler_todos()
        registro_encontrado = False
        for registro in todos_registros:
            if registro[0] == cod_dia and registro[1] == str(cod_especialidade):
                try:
                    vagas_atual = int(registro[2])
                except (ValueError, IndexError):
                    vagas_atual = 0
                registro[2] = str(max(vagas_atual - 1, 0))
                registro_encontrado = True
                break
        if not registro_encontrado:
            return False
        io_manager_diarias.reescrever_arquivo_completo(todos_registros)
        self.carregar_indices_iniciais()
        return True

    def validar_vagas(self, data: str, cod_especialidade: str) -> bool:
        registro_especialidade = self.lookup_especialidade(cod_especialidade)

        if not registro_especialidade:
            print(f"Erro: Especialidade {cod_especialidade} não existe.")
            return False

        try:
            limite_diario = int(registro_especialidade[3])
        except (ValueError, IndexError):
            print("Erro: Limite Diário da Especialidade corrompido")
            return False

        registro_diaria = self.buscar_diaria(data, cod_especialidade)

        if not registro_diaria:
            vagas_ocupadas = 0
        else:
            try:
                vagas_ocupadas = int(registro_diaria[2])
            except (ValueError, IndexError):
                print("Erro: Quantidade de Consultas da Diária corrompida")
                return False

        if vagas_ocupadas < limite_diario:
            print(f"Vaga disponível: {vagas_ocupadas} de {limite_diario} agendadas.")
            return True
        else:
            print(f"Limite atingido: {vagas_ocupadas} de {limite_diario} agendadas.")
            return False
