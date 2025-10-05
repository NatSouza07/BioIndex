from .gerenciador_io import GerenciadorTabela
from .arvore_binaria import ArvoreBinaria
from .gerenciador_io import CAMINHO_DADOS
from .modelos import Paciente, Paciente, Consulta
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

    def cadastrar_diaria(self, diaria_obj: Diaria) -> bool:
        NOME_TABELA = 'diarias'
        io_manager = IO_TABELAS[NOME_TABELA]
        bst = INDICES[NOME_TABELA]

        chave_composta_str = diaria_obj.gerar_chave_composta()

        registro_a_salvar = diaria_obj.to_list()

        try:
            if bst.buscar(chave_composta_str) is not None:
                print(f"Erro: Diária com chave '{chave_composta_str}' já existe.")
                return False

            novo_num_linha = io_manager.anexar_registro(registro_a_salvar)

            bst.inserir(chave_composta_str, novo_num_linha)
            return True
        except ValueError as e:
            print(f"Erro ao cadastrar diária: {e}")
            return False

    def buscar_diaria(self, cod_dia: str, cod_especialidade: str) -> list[str] | None:
        NOME_TABELA = 'diarias'
        io_manager = IO_TABELAS[NOME_TABELA]
        bst = INDICES[NOME_TABELA]

        chave_busca_str = f"{cod_dia}|{cod_especialidade}"

        num_linha = bst.buscar(chave_busca_str)

        if num_linha is None:
            return None

        return io_manager.ler_linha(num_linha)

    def excluir_diaria(self, cod_dia: str, cod_especialidade: str) -> bool:
        chave_busca_str = f"{cod_dia}|{cod_especialidade}"

        return self.remover_fisicamente_registro('diarias', chave_busca_str)

    def calcular_valor_total_consulta_final(self, cod_especialidade: str, cod_exame: str) -> dict | None:
        registro_especialidade = self.lookup_especialidade(cod_especialidade)

        if not registro_especialidade:
            print(f"Erro: Especialidade {cod_especialidade} não encontrada.")
            return None

        try:
            valor_especialidade = float(registro_especialidade[2])
        except (ValueError, IndexError):
            print("Erro: Valor da Especialidade está corrompido")
            return None

        registro_exame = self.lookup_exame {cod_exame}

        if not registro_exame:
            print(f"Erro: Exame {cod_exame} não encontrado.")
            return None

        try:
            valor_exame = float(registro_exame[3])
        except (ValueError, IndexError):
            print("Erro: Valor da Exame corrompido")
            return None

        valor_total = regras_negocio.calcular_valor_total_consulta(valor_especialidade, valor_exame)

        return {
            "cod_especialidade": cod_especialidade,
            "cod_exame": cod_exame,
            "valor_especialidade": valor_especialidade,
            "valor_exame": valor_exame,
            "valor_total": valor_total,
        }

    def validar_vagas(self, data: str, cod_especialidade: str) -> bool:
        registro_especialidade = self.lookup.especialidade(cod_especialidade)

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
        else
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

    def cadastrar_consulta(self, consulta_obj: Consulta) -> bool:
        NOME_TABELA = 'consultas'
        io_manager = IO_TABELAS[NOME_TABELA]
        bst = INDICES[NOME_TABELA]

        registro_exame = self.lookup_exame(str(consulta_obj.cod_exame))

        if not registro_exame:
            print(f"Erro: Exame {consulta_obj.cod_exame} não encontrado.")
            return False

        cod_especialidade_para_vaga = registro_exame[2]

        tem_vaga = self.validar_vagas(consulta_obj.data, cod_especialidade_para_vaga)

        if not tem_vaga:
            print("Agendamento recusado: Limite de consultas diárias atingido.")
            return False

        try:
            chave = consulta_obj.cod_consulta

            registro_a_salvar = consulta_obj.to_list()
            novo_num_linha = io_manager.anexar_registro(registro_a_salvar)
            bst.inserir(chave, novo_num_linha)

            self.atualizar_diarias_mais_um(consulta_obj.data, cod_especialidade_para_vaga)

            return True
        except ValueError as e:
            print(f"Erro ao cadastrar consulta: {e}")
            return False

    def excluir_consulta(self, cod_consulta: int) -> bool:
        NOME_TABELA = 'consultas'
        chave = cod_consulta

        registro_consulta = self.buscar_consulta(chave)

        if not registro_consulta:
            print(f"Erro: Consulta com código {chave} não encotrada para exclusão.")
            return False

        cod_exame_fk = registro_consulta[3]
        data_consulta = registro_consulta[4]

        registro_exame = self.lookup_exame(cod_exame_fk)

        if not registro_exame:
            print("Erro: Exame da consulta não encontrado.")
            return False

        cod_especialidade_para_vaga = registro_exame[2]

        removida_com_sucesso = self.remover_fisicamente_registro(NOME_TABELA, chave)

        if not removida_com_sucesso:
            print(f"Erro: Falha na remoção física da consulta {chave}")
            return False

        self.atualizar_diarias_menos_um(data_consulta, cod_especialidade_para_vaga)

        return True

    def buscar_consulta(self, cod_consulta: int) -> list[str] | None:
        NOME_TABELA = 'consultas'
        return self.buscar_registro_por_chave(NOME_TABELA, cod_consulta)

    def consultar_consulta_completa(self, cod_consulta: int) -> dict | None:
        registro_consulta_str = self.buscar_consulta(cod_consulta)

        if not registro_consulta_str:
            return None

        cod_paciente_fk = registro_consulta_str[1]
        cod_medico_fk = registro_consulta_str[2]
        cod_exame_fk = registro_consulta_str[3]
        data_consulta = registro_consulta_str[4]

        dados_paciente_completo = self.consultar_paciente_completo(cod_paciente_fk)

        if not dados_paciente_completo:
            return {"Erro": "Paciente relacionado à consulta não encontrado."}

        registro_exame = self.lookup_exame(cod_exame_fk)

        if not registro_exame:
            return {"Erro": "Exame relacionado à consulta não encontrado."}

        descricao_exame = registro_exame[1]
        cod_especialidade.fk = registro_exame[2]

        registro_medico = self.lookup_medico(cod_medico_fk)

        if not registro_medico:
            return {"Erro": "Médico relacionado à consulta não encontrado."}

        nome_medico = registro_medico[1]

        dados_valor_total = self.calcular_valor_total_consulta_final(cod_especialidade_fk, cod_medico_fk)

        resultado = {
            "cod_consulta": registro_consulta_str[0],
            "data": data_consulta,
            "hora": registro_consulta_str[5],

            "paciente_nome": dados_paciente_completo["nome"],
            "paciente_cidade": dados_paciente_completo["nome_cidade"],
            "paciente_uf": dados_paciente_completo["uf_cidade"],

            "medico_nome": nome_medico,
            "cod_medico": cod_medico_fk,

            "exame_descricao": descricao_exame,
            "cod_exame": cod_exame_fk,
            "cod_especialidade": cod_especialidade_fk,

            "valor_consulta_total": dados_valor_total["valor_total"]
        }

        return resultado

    def gerar_relatorio_consultas_ordenado(self) -> list[dict]:
        NOME_TABELA = 'consultas'
        bst = INDICES[NOME_TABELA]

        codigos_ordenados = bst.in_order_traversal_keys()

        relatorio_completo = []

        for cod_consulta in codigos_ordenados:
            dados_completos = self.consultar_consulta_completa(cod_consulta)

            if dados_completos and "erro" not in dados_completos:
                relatorio_completo.append(dados_completos)

        return relatorio_completo

