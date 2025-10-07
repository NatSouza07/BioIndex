from typing import Optional, List, Dict, Any
from modulos.modelos import Consulta

class CrudConsultas:
    NOME_TABELA = "consultas"

    def __init__(self, servicos):
        self.servicos = servicos
        self.io_manager = servicos.io_tabelas.get(self.NOME_TABELA)
        self.bst = servicos.indices.get(self.NOME_TABELA)

    def gerar_proximo_codigo(self) -> int:
        cods = [int(r[0]) for r in self.io_manager.ler_todos() if r[0].isdigit()]
        return max(cods, default=0) + 1

    def cadastrar_consulta(self, consulta_obj: Consulta) -> bool:
        registro_exame = self.servicos.lookup_exame(str(consulta_obj.cod_exame))
        if not registro_exame:
            return False
        cod_especialidade = registro_exame[2]
        if not self.servicos.validar_vagas(consulta_obj.data, cod_especialidade):
            return False
        chave = consulta_obj.cod_consulta
        if self.bst.buscar(chave):
            return False
        registro = consulta_obj.to_list()
        nova_linha = len(self.io_manager.ler_todos()) + 1
        self.io_manager.inserir_linha(registro)
        self.bst.inserir(chave, nova_linha)
        cod_dia = consulta_obj.data.replace("-", "")
        self.servicos.atualizar_vagas_mais_um(cod_dia, cod_especialidade)
        return True

    def excluir_consulta(self, cod_consulta: int) -> bool:
        cod_consulta = int(cod_consulta)
        registro = self.buscar_consulta(cod_consulta)
        if not registro:
            return False
        cod_exame = registro[3]
        registro_exame = self.servicos.lookup_exame(cod_exame)
        if not self.servicos.remover_fisicamente_registro(self.NOME_TABELA, str(cod_consulta)):
            return False
        if registro_exame:
            cod_especialidade = registro_exame[2]
            cod_dia = registro[4].replace("-", "")
            self.servicos.atualizar_vagas_menos_um(cod_dia, cod_especialidade)
        return True

    def buscar_consulta(self, cod_consulta: int) -> Optional[List[str]]:
        num_linha = self.bst.buscar(cod_consulta)
        if num_linha is None:
            return None
        return self.io_manager.ler_linha(num_linha)

    def consultar_consulta_completa(self, cod_consulta: int) -> Optional[Dict[str, Any]]:
        registro = self.buscar_consulta(cod_consulta)
        if not registro:
            return None
        cod_paciente, cod_medico, cod_exame = registro[1], registro[2], registro[3]
        dados_paciente = self.servicos.lookup_paciente(cod_paciente)
        paciente_nome = f"{cod_paciente} - {dados_paciente[1]}" if dados_paciente else "N/A"
        cidade_nome = "N/A"
        if dados_paciente:
            dados_cidade = self.servicos.lookup_cidade(dados_paciente[5])
            if dados_cidade:
                cidade_nome = dados_cidade[1]
        dados_medico = self.servicos.lookup_medico(cod_medico)
        medico_nome = f"{cod_medico} - {dados_medico[1]}" if dados_medico else "N/A"
        dados_exame = self.servicos.lookup_exame(cod_exame)
        exame_desc = f"{cod_exame} - {dados_exame[1]}" if dados_exame else "N/A"
        valor_total = 0
        if dados_exame and dados_medico:
            dados_valor = self.calcular_valor_total_consulta_final(dados_medico[5], cod_exame)
            if dados_valor:
                valor_total = dados_valor["valor_total"]
        return {
            "cod_consulta": registro[0],
            "paciente": paciente_nome,
            "cidade": cidade_nome,
            "medico": medico_nome,
            "exame": exame_desc,
            "data": registro[4],
            "hora": registro[5],
            "valor_total": valor_total
        }

    def calcular_valor_total_consulta_final(self, cod_especialidade: str, cod_exame: str) -> Optional[dict]:
        registro_especialidade = self.servicos.lookup_especialidade(cod_especialidade)
        registro_exame = self.servicos.lookup_exame(cod_exame)
        if not registro_especialidade or not registro_exame:
            return None
        valor_total = self.servicos.regras_negocio.calcular_valor_total_consulta(
            float(registro_especialidade[2]), float(registro_exame[3])
        )
        return {"valor_total": valor_total}

    def gerar_relatorio_consultas_ordenado(self) -> List[Dict[str, Any]]:
        relatorio = []
        if hasattr(self.bst, "in_order"):
            lista_chaves = self.bst.in_order()
        else:
            lista_chaves = []
        for chave, _ in lista_chaves:
            consulta = self.consultar_consulta_completa(chave)
            if consulta:
                relatorio.append(consulta)
        return relatorio
