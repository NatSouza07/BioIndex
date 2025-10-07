from modulos.modelos import Paciente

class CrudPacientes:
    NOME_TABELA = "pacientes"

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def gerar_proximo_codigo(self) -> int:
        registros = self.ler_pacientes_exaustivamente()
        cods = [int(r[0]) for r in registros if r[0].isdigit()]
        return max(cods) + 1 if cods else 1

    def cadastrar_paciente(self, paciente_obj: Paciente) -> bool:
        cod_cidade_fk = str(paciente_obj.cod_cidade)
        if not self.servicos.lookup_cidade(cod_cidade_fk):
            print(f"Erro FK: Código de cidade '{cod_cidade_fk}' não encontrado")
            return False

        registro_a_salvar = paciente_obj.to_list()
        try:
            if self.bst.buscar(paciente_obj.cod_paciente) is not None:
                self.excluir_paciente(str(paciente_obj.cod_paciente))

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
        try:
            chave_int = int(cod_paciente)
        except ValueError:
            return False

        num_linha = self.bst.buscar(chave_int)
        if num_linha is None:
            return False

        ok_fisico = self.servicos.remover_fisicamente_registro(self.NOME_TABELA, cod_paciente)
        if ok_fisico:
            self.bst.remover(chave_int)
            return True
        return False

    def ler_pacientes_exaustivamente(self) -> list[list[str]]:
        return self.io_manager.ler_todos()

    def atualizar_paciente(self, paciente_obj: Paciente) -> bool:
        try:
            registro_atualizado = paciente_obj.to_list()
            num_linha = self.bst.buscar(int(paciente_obj.cod_paciente))
            if num_linha is not None:
                self.io_manager.atualizar_linha(num_linha, registro_atualizado)
                return True
            return False
        except Exception as e:
            print(f"Erro ao atualizar paciente: {e}")
            return False

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

        return {"imc": imc, "diagnostico": diagnostico, "paciente_registro": registro}

    def consultar_paciente_completo(self, cod_paciente: str) -> dict | None:
        registro = self.buscar_paciente(cod_paciente)
        if not registro:
            return None

        cod_cidade_fk = registro[5] if len(registro) > 5 else "N/A"
        registro_cidade = self.servicos.lookup_cidade(cod_cidade_fk)
        nome_cidade = registro_cidade[1] if registro_cidade else "Cidade não encontrada"
        uf_cidade = registro_cidade[2] if registro_cidade else "N/A"

        dados_imc = self.calcular_diagnostico_paciente(cod_paciente)
        imc = dados_imc.get("imc") if dados_imc else "N/A"
        diagnostico = dados_imc.get("diagnostico") if dados_imc else "N/A"

        return {
            "cod_paciente": registro[0],
            "nome": registro[1],
            "data_nascimento": registro[2],
            "endereco": registro[3],
            "telefone": registro[4] if len(registro) > 4 else "",
            "cod_cidade_fk": cod_cidade_fk,
            "nome_cidade": nome_cidade,
            "uf_cidade": uf_cidade,
            "peso": registro[6],
            "altura": registro[7],
            "imc": imc,
            "diagnostico": diagnostico,
        }
