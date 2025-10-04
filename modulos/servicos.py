from .gerenciador_io import GerenciadorTabela
from .arvore_binaria import ArvoreBinaria
from .gerenciador_io import CAMINHO_DADOS
from .modelos import Paciente, Paciente
from .import regras_negocio

INDICES = {}
IO_TABELAS = {}

class GerenciadorServicos:
    def __init__(self):
        self._inicializar_gerenciadores()

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

    def cadastrar_cidade(self, cidade_obj) -> bool:
        NOME_TABELA = 'cidades'
        io_manager = IO_TABELAS(NOME_TABELA)
        bst = INDICES[NOME_TABELA]

        registro_a_salvar = cidade_obj.to_list()

        try:
            novo_num_linha = io_manager.anexar_registro(registro_a_salvar)
            chave_primaria_int = cidade_obj.cod_cidade
            bst.inserir(chave_primaria_int, novo_num_linha)
            return True
        except ValueError as 0:
            print(f"Erro ao cadastrar cidade: {e}")
            return False

    def buscar_cidade(self, cod_cidade: str) -> list[str] | None:
        NOME_TABELA = 'cidades'
        io_manager = IO_TABELAS(NOME_TABELA)
        bst = INDICES[NOME_TABELA]

        try:
            chave_busca_int = int(cod_cidade)
        except ValueError:
            return None

        num_linha = bst.buscar(chave_busca_int)

        if num_linha is None:
            return None

        return io_manager.ler_linha(num_linha)

    def excluir_cidade(self, cod_cidade: str) -> bool:
        return self.remover_fisicamente_registro('cidades', cod_cidade)

    def ler_cidades_exaustivamente(self) -> list[list[str]]:
        return IO_TABELAS['cidades'].ler_todos()

    def lookup_cidade(self, cod_cidade_fk: str) -> list[str] | None:
        NOME_TABELA = 'cidades'
        bst = INDICES.get(NOME_TABELA)
        io_manager = IO_TABELAS.get(NOME_TABELA)

        if bst is None or io_manager is None:
            return None

        try:
            chave_busca_int = int(cod_cidade_fk)
        except ValueError:
            return None

        num_linha = bst.buscar(chave_busca_int)

        if num_linha is None:
            return None

        registro_cidade = io_manager.ler_linha(num_linha)

        return registro_cidade

    def cadastrar_paciente(self, paciente_obj: Paciente) -> bool:
        NOME_TABELA = 'pacientes'
        io_manager = IO_TABELAS[NOME_TABELA]
        bst = INDICES[NOME_TABELA]

        cod_cidade_fk = str(paciente_obj.cod_cidade)

        if not self.lookup_cidade(cod_cidade_fk):
            print(f"Erro FK: Código de cidade '{cod_cidade_fk}' não encontrado")
            return False

        registro_a_salvar = paciente_obj.to_list()

        try:
            novo_num_linha = io_manager.anexar_registro(registro_a_salvar)
            chave_primaria_int = paciente_obj.cod_paciente

            bst.inserir(chave_primaria_int, novo_num_linha)
            return True
        except ValueError as e:
            print(f"Erro ao cadastrar paciente: {e}")
            return False

    def buscar_paciente(self, cod_paciente: str) -> list[str] | None:
        NOME_TABELA = 'pacientes'
        io_manager = IO_TABELAS[NOME_TABELA]
        bst = INDICES[NOME_TABELA]

        try:
            chave_busca_int = int(cod_paciente)
        except ValueError:
            return None

        num_linha = bst.buscar(chave_busca_int)

        if num_linha is None:
            return None

        return io_manager.ler_linha(num_linha)

    def excluir_paciente(self, cod_paciente: str) -> bool:
        return self.remover_fisicamente_registro('pacientes', cod_paciente)

    def ler_pacientes_exaustivamente(self) -> list[list[str]]:
        return IO_TABELAS['pacientes'].ler_todos()

    def calcular_diagnostico_paciente(self, cod_paciente: str) -> dict | None:
        registro = self.buscar_paciente(cod_paciente)

        if not registro:
            return None

        try:
            peso = float(registro[6])
            altura = float(registro[7])
        except (ValueError, IndexError):
            return {"erro": "Dados de peso/altura inválidos no registro."}

        imc = regras_negocio.calcular_imc(peso, altura)
        diagnostico = regras_negocio.diagnostico(imc)

        return {
            "imc": imc,
            "diagnostico": diagnostico,
            "paciente_registro": registro,
        }

    def consultar_paciente_completo(self, cod_paciente: str) -> dict | None:
        registro_paciente_str = self.buscar_paciente(cod_paciente)

        if not registro_paciente_str:
            return None

        try:
            cod_cidade_fk = registro_paciente_str[5]
            registro_cidade_str = self.lookup_cidade(cod_cidade_fk)

            if registro_cidade_str:
                nome_cidade = registro_cidade_str[1]
                uf_cidade = registro_cidade_str[2]
            else:
                nome_cidade = "Cidade não encontrada! (Erro FK)"
                uf_cidade = "N/A"

        except IndexError:
            nome_cidade = "Registro corrompido"
            uf_cidade = "N/A"

        try:
            peso = float(registro_paciente_str[6])
            altura = float(registro_paciente_str[7])

            dados_imc = self.calcular_diagnostico_paciente(cod_paciente)

            imc = dados_imc.get('imc')
            diagnostico = dados_imc.get('diagnostico')

        except (ValueError, IndexError):
            imc = "N/A"
            diagnostico = "Dados inválidos"

        resultado = {
            "cod_paciente": registro_paciente_str[0],
            "nome": registro_paciente_str[1],
            "data_nascimento": registro_paciente_str[2],
            "endereco": registro_paciente_str[3],
            "telefone": registro_paciente_str[4],
            "cod_cidade_fk": cod_cidade_fk,
            "nome_cidade": nome_cidade,
            "uf_cidade": uf_cidade,
            "peso": registro_paciente_str[6],
            "altura": registro_paciente_str[7],
            "imc": imc,
            "diagnostico": diagnostico
        }

        return resultado