from modulos.modelos import Consulta

class CrudConsultas:
    NOME_TABELA = 'consultas'

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def cadastrar_consulta(self, consulta_obj: Consulta) -> bool:
        registro_exame = self.servicos.lookup_paciente(str(consulta_obj.cod_exame))

        if not registro_exame:
            print(f"Erro: Exame {consulta_obj.cod_exame} não encontrado.")
            return False

        cod_especialidade_para_vaga = registro_exame[2]

        tem_vaga = self.servicos.validar_vagas(consulta_obj.data, cod_especialidade_para_vaga)

        if not tem_vaga:
            print("Agendamento recusado: Limite de consultas diárias atingido.")
            return False

        try:
            chave = consulta_obj.cod_consulta
            registro_a_salvar = consulta_obj.to_list()
            novo_num_linha = self.io_manager.anexar_registro(registro_a_salvar)
            self.bst.inserir(chave, novo_num_linha)

            self.servicos.atualizar_diarias_mais_um(consulta_obj.data, cod_especialidade_para_vaga)

            return True

        except ValueError as e:
            print(f"Erro ao cadastrar consulta: {e}")
            return False

    def excluir_consulta(self, cod_consulta: int) -> bool:
        registro_consulta = self.buscar_consulta(cod_consulta)

        if not registro_consulta:
            print(f"Erro: Consulta com código {cod_consulta} não encontrada para exclusão.")
            return False

        cod_exame_fk = registro_consulta[3]
        data_consulta = registro_consulta[4]

        registro_exame = self.servicos.lookup_exame(cod_exame_fk)

        if not registro_exame:
            print("Erro: Exame da consulta não encontrado.")
            return False

        cod_especialidade_para_vaga = registro_exame[2]

        removida_com_sucesso = self.servicos.remover_fisicamente_registro(self.NOME_TABELA, str(cod_consulta))

        if not removida_com_sucesso:
            print(f"Erro: Falha na remoção física da consulta {cod_consulta}")
            return False

        self.servicos.atualizar_diarias_menos_um(data_consulta, cod_especialidade_para_vaga)
        return True

    def buscar_consulta(self, cod_consulta: int) -> list[str] | None:
        num_linha = self.bst.buscar(cod_consulta)

        if num_linha is None:
            return None

        return self.io_manager.ler_linha(num_linha)

    def consultar_consulta_completa(self, cod_consulta: int) -> dict | None:
        registro_consulta = self.buscar_consulta(cod_consulta)

        if not registro_consulta:
            return None

        cod_paciente_fk = registro_consulta[1]
        cod_medico_fk = registro_consulta[2]
        cod_exame_fk = registro_consulta[3]
        data_consulta = registro_consulta[4]

        dados_paciente = self.servicos.lookup_paciente(cod_paciente_fk)

        if not dados_paciente:
            return {"Erro": "Paciente relacionado à consulta não encontrado."}

        registro_exame = self.servicos.lookup_exame(cod_exame_fk)

        if not registro_exame:
            return {"Erro": "Exame relacionado à consulta não encontrado."}

        descricao_exame = registro_exame[1]
        cod_especialidade_fk = registro_exame[2]

        registro_medico = self.servicos.lookup_medico(cod_medico_fk)

        if not registro_medico:
            return {"Erro": "Médico relacionado à consulta não encontrado."}

        nome_medico = registro_medico[1]

        dados_valor_total = self.calcular_valor_total_consulta_final(cod_especialidade_fk, cod_exame_fk)
        valor_total = dados_valor_total["valor_total"] if dados_valor_total else 0.0

        return {
            "cod_consulta": registro_consulta[0],
            "data": data_consulta,
            "hora": registro_consulta[5],
            "paciente_nome": dados_paciente["nome"],
            "paciente_cidade": dados_paciente["nome_cidade"],
            "paciente_uf": dados_paciente["uf_cidade"],
            "medico_nome": nome_medico,
            "cod_medico": cod_medico_fk,
            "exame_descricao": descricao_exame,
            "cod_exame": cod_exame_fk,
            "cod_especialidade": cod_especialidade_fk,
            "valor_consulta_total": valor_total
        }

    def gerar_relatorio_consultas_ordenado(self) -> list[dict]:
        codigos_ordenados = self.bst.in_order_traversal_keys()
        relatorio = []
        for cod in codigos_ordenados:
            consulta = self.consultar_consulta_completa(cod)

            if consulta and "Erro" not in consulta:
                relatorio.append(consulta)

        return relatorio

    def calcular_valor_total_consulta_final(self, cod_especialidade: str, cod_exame: str) -> dict | None:
        registro_especialidade = self.servicos.lookup_especialidade(cod_especialidade)

        if not registro_especialidade:
            print(f"Erro: Especialidade {cod_especialidade} não encontrada.")
            return None

        try:
            valor_especialidade = float(registro_especialidade[2])

        except (ValueError, IndexError):
            print("Erro: Valor da Especialidade está corrompido")
            return None

        registro_exame = self.servicos.lookup_exame(cod_exame)

        if not registro_exame:
            print(f"Erro: Exame {cod_exame} não encontrado.")
            return None

        try:
            valor_exame = float(registro_exame[3])

        except (ValueError, IndexError):
            print("Erro: Valor do Exame corrompido")
            return None

        valor_total = self.servicos.regras_negocio.calcular_valor_total_consulta(valor_especialidade, valor_exame)
        return {
            "cod_especialidade": cod_especialidade,
            "cod_exame": cod_exame,
            "valor_especialidade": valor_especialidade,
            "valor_exame": valor_exame,
            "valor_total": valor_total
        }
