# CRUDs/crud_consultas.py

from modulos.modelos import Consulta
from servicos import GerenciadorServicos
from typing import Optional, List, Dict, Any

class CrudConsultas:
    NOME_TABELA = 'consultas'

    def __init__(self, servicos: GerenciadorServicos):
        self.servicos = servicos
        self.io_manager = servicos.IO_TABELAS.get(self.NOME_TABELA)
        self.bst = servicos.INDICES.get(self.NOME_TABELA)

    def cadastrar_consulta(self, consulta_obj: Consulta) -> bool:
        registro_exame = self.servicos.lookup_exame(str(consulta_obj.cod_exame))
        if not registro_exame:
            print(f"Erro: Exame {consulta_obj.cod_exame} não encontrado.")
            return False

        cod_especialidade_para_vaga = registro_exame[2]

        tem_vaga = self.servicos.validar_vagas(consulta_obj.data, cod_especialidade_para_vaga)
        if not tem_vaga:
            print("Agendamento recusado: Limite de consultas diárias atingido para esta especialidade.")
            return False

        try:
            chave = consulta_obj.codigo
            if self.bst.buscar(chave):
                print(f"Erro: Consulta com código {chave} já existe.")
                return False

            registro_a_salvar = [
                str(consulta_obj.codigo), str(consulta_obj.cod_paciente),
                str(consulta_obj.cod_medico), str(consulta_obj.cod_exame),
                consulta_obj.data, consulta_obj.hora
            ]

            nova_linha = len(self.io_manager.ler_todos()) + 1
            self.io_manager.salvar_novo_registro(registro_a_salvar)
            self.bst.inserir(chave, nova_linha)

            cod_dia = consulta_obj.data.replace('-', '')
            self.servicos.atualizar_vagas_mais_um(cod_dia, cod_especialidade_para_vaga)
            return True

        except Exception as e:
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
            print("Aviso: Exame da consulta não encontrado, mas a consulta será removida.")

        removida_com_sucesso = self.servicos.remover_fisicamente_registro(self.NOME_TABELA, str(cod_consulta))

        if not removida_com_sucesso:
            print(f"Erro: Falha na remoção física da consulta {cod_consulta}")
            return False

        if registro_exame:
            cod_especialidade_para_vaga = registro_exame[2]
            cod_dia = data_consulta.replace('-', '')
            self.servicos.atualizar_vagas_menos_um(cod_dia, cod_especialidade_para_vaga)

        return True

    def buscar_consulta(self, cod_consulta: int) -> Optional[List[str]]:
        num_linha = self.bst.buscar(cod_consulta)
        if num_linha is None:
            return None
        return self.io_manager.ler_linha(num_linha)

    def consultar_consulta_completa(self, cod_consulta: int) -> Optional[Dict[str, Any]]:
        registro_consulta = self.buscar_consulta(cod_consulta)
        if not registro_consulta:
            return None

        cod_paciente_fk = registro_consulta[1]
        cod_medico_fk = registro_consulta[2]
        cod_exame_fk = registro_consulta[3]

        dados_paciente = self.servicos.lookup_paciente(cod_paciente_fk)
        paciente_nome = dados_paciente[1] if dados_paciente else "Paciente não encontrado"
        cidade_nome = "N/A"
        cidade_uf = "N/A"
        if dados_paciente:
            dados_cidade = self.servicos.lookup_cidade(dados_paciente[5])
            if dados_cidade:
                cidade_nome = dados_cidade[1]
                cidade_uf = dados_cidade[2]

        dados_medico = self.servicos.lookup_medico(cod_medico_fk)
        medico_nome = dados_medico[1] if dados_medico else "Médico não encontrado"

        dados_exame = self.servicos.lookup_exame(cod_exame_fk)
        exame_descricao = dados_exame[1] if dados_exame else "Exame não encontrado"

        valor_total = 0.0
        if dados_exame and dados_medico:
            medico_cod_especialidade = dados_medico[5]
            dados_valor = self.calcular_valor_total_consulta_final(medico_cod_especialidade, cod_exame_fk)
            if dados_valor:
                valor_total = dados_valor["valor_total"]

        return {
            "cod_consulta": registro_consulta[0],
            "data": registro_consulta[4],
            "hora": registro_consulta[5],
            "paciente_nome": paciente_nome,
            "paciente_cidade": cidade_nome,
            "paciente_uf": cidade_uf,
            "medico_nome": medico_nome,
            "exame_descricao": exame_descricao,
            "valor_consulta_total": valor_total
        }

    def gerar_relatorio_consultas_ordenado(self) -> List[Dict[str, Any]]:
        registros_ordenados = self.bst.em_ordem()
        relatorio = []
        for chave, _ in registros_ordenados:
            consulta_completa = self.consultar_consulta_completa(chave)
            if consulta_completa:
                relatorio.append(consulta_completa)
        return relatorio

    def calcular_valor_total_consulta_final(self, cod_especialidade: str, cod_exame: str) -> Optional[dict]:
        registro_especialidade = self.servicos.lookup_especialidade(cod_especialidade)
        if not registro_especialidade:
            return None
        try:
            valor_especialidade = float(registro_especialidade[2])
        except (ValueError, IndexError):
            return None

        registro_exame = self.servicos.lookup_exame(cod_exame)
        if not registro_exame:
            return None
        try:
            valor_exame = float(registro_exame[3])
        except (ValueError, IndexError):
            return None

        valor_total = self.servicos.regras_negocio.calcular_valor_total_consulta(valor_especialidade, valor_exame)
        return {
            "cod_especialidade": cod_especialidade,
            "cod_exame": cod_exame,
            "valor_especialidade": valor_especialidade,
            "valor_exame": valor_exame,
            "valor_total": valor_total
        }

    def faturamento_por_dia(self, data_filtro: str) -> float:
        faturamento_total = 0.0
        todos_registros = self.io_manager.ler_todos()
        for registro in todos_registros:
            if registro[4] == data_filtro:
                cod_medico = registro[2]
                cod_exame = registro[3]
                dados_medico = self.servicos.lookup_medico(cod_medico)
                if dados_medico:
                    cod_especialidade = dados_medico[5]
                    dados_valor = self.calcular_valor_total_consulta_final(cod_especialidade, cod_exame)
                    if dados_valor:
                        faturamento_total += dados_valor["valor_total"]
        return faturamento_total

    def faturamento_por_periodo(self, data_inicio: str, data_fim: str) -> float:
        faturamento_total = 0.0
        todos_registros = self.io_manager.ler_todos()
        for registro in todos_registros:
            data_consulta = registro[4]
            if data_inicio <= data_consulta <= data_fim:
                cod_medico = registro[2]
                cod_exame = registro[3]
                dados_medico = self.servicos.lookup_medico(cod_medico)
                if dados_medico:
                    cod_especialidade = dados_medico[5]
                    dados_valor = self.calcular_valor_total_consulta_final(cod_especialidade, cod_exame)
                    if dados_valor:
                        faturamento_total += dados_valor["valor_total"]
        return faturamento_total

    def faturamento_por_medico(self, cod_medico_filtro: str) -> float:
        faturamento_total = 0.0
        todos_registros = self.io_manager.ler_todos()
        for registro in todos_registros:
            if registro[2] == cod_medico_filtro:
                cod_medico = registro[2]
                cod_exame = registro[3]
                dados_medico = self.servicos.lookup_medico(cod_medico)
                if dados_medico:
                    cod_especialidade = dados_medico[5]
                    dados_valor = self.calcular_valor_total_consulta_final(cod_especialidade, cod_exame)
                    if dados_valor:
                        faturamento_total += dados_valor["valor_total"]
        return faturamento_total

    def faturamento_por_especialidade(self, cod_especialidade_filtro: str) -> float:
        faturamento_total = 0.0
        todos_registros = self.io_manager.ler_todos()
        for registro in todos_registros:
            cod_medico = registro[2]
            cod_exame = registro[3]
            dados_medico = self.servicos.lookup_medico(cod_medico)
            if dados_medico and dados_medico[5] == cod_especialidade_filtro:
                cod_especialidade = dados_medico[5]
                dados_valor = self.calcular_valor_total_consulta_final(cod_especialidade, cod_exame)
                if dados_valor:
                    faturamento_total += dados_valor["valor_total"]
        return faturamento_total