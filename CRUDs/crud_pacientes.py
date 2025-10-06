from modulos.modelos import Paciente

class CrudPacientes:
    NOME_TABELA = 'pacientes'

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def cadastrar_paciente(self, paciente_obj: Paciente) -> bool:
        cod_cidade_fk = str(paciente_obj.cod_cidade)

        if not self.lookup_cidade(cod_cidade_fk):
            print(f"Erro FK: Código de cidade '{cod_cidade_fk}' não encontrado")
            return False

        registro_a_salvar = paciente_obj.to_list()

        try:
            novo_num_linha = self.io_manager.anexar_registro(registro_a_salvar)
            chave_primaria_int = paciente_obj.cod_paciente
            self.bst.inserir(chave_primaria_int, novo_num_linha)
            return True

        except ValueError as e:
            print(f"Erro ao cadastrar paciente: {e}")
            return False

    def buscar_paciente(self, cod_paciente: str) -> list[str] | None:
        try:
            chave_busca_int = int(cod_paciente)

        except ValueError:
            return None

        num_linha = self.bst.buscar(chave_busca_int)

        if num_linha is None:
            return None

        return self.io_manager.ler_linha(num_linha)

    def excluir_paciente(self, cod_paciente: str) -> bool:
        return self.servicos.remover_fisicamente_registro(self.NOME_TABELA, cod_paciente)

    def ler_pacientes_exaustivamente(self) -> list[list[str]]:
        return self.io_manager.ler_todos()

    def calcular_diagnostico_paciente(self, cod_paciente: str) -> dict | None:
        registro = self.buscar_paciente(cod_paciente)

        if not registro:
            return None

        try:
            peso = float(registro[6])
            altura = float(registro[7])

        except (ValueError, IndexError):
            return {"erro": "Dados de peso/altura inválidos no registro."}

        imc = self.servicos.regras_negocio.calcular_imc(peso, altura)
        diagnostico = self.servicos.regras_negocio.diagnostico_imc(imc)

        return {
            "imc": imc,
            "diagnostico": diagnostico,
            "paciente_registro": registro,
        }

    def consultar_paciente_completo(self, cod_paciente: str) -> dict | None:
        registro = self.buscar_paciente(cod_paciente)

        if not registro:
            return None

        try:
            cod_cidade_fk = registro[5]
            registro_cidade = self.lookup_cidade(cod_cidade_fk)
            nome_cidade = registro_cidade[1] if registro_cidade else "Cidade não encontrada! (Erro FK)"
            uf_cidade = registro_cidade[2] if registro_cidade else "N/A"

        except IndexError:
            nome_cidade = "Registro corrompido"
            uf_cidade = "N/A"

        dados_imc = self.calcular_diagnostico_paciente(cod_paciente)
        imc = dados_imc.get("imc") if dados_imc else "N/A"
        diagnostico = dados_imc.get("diagnostico") if dados_imc else "Dados inválidos"

        return {
            "cod_paciente": registro[0],
            "nome": registro[1],
            "data_nascimento": registro[2],
            "endereco": registro[3],
            "telefone": registro[4],
            "cod_cidade_fk": cod_cidade_fk,
            "nome_cidade": nome_cidade,
            "uf_cidade": uf_cidade,
            "peso": registro[6],
            "altura": registro[7],
            "imc": imc,
            "diagnostico": diagnostico
        }

    def lookup_cidade(self, cod_cidade_fk: str) -> list[str] | None:
        return self.servicos.crud_cidades.lookup_cidade(cod_cidade_fk)
