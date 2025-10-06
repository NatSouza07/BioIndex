def calcular_imc(peso: float, altura: float) -> float:
    if altura <= 0 or peso <= 0:
        return 0.0

    return round(peso / (altura ** 2), 2)

def diagnostico_imc(imc: float) -> str:
    if imc == 0:
        return "Dados inválidos"
    elif imc < 18.5:
        return "Abaixo do Peso"
    elif imc < 24.9:
        return "Peso Normal"
    elif imc < 29.9:
        return "Sobrepeso"
    else:
        return "Obesidade"

def calcular_valor_total_consulta(valor_especialidade: float, valor_exame: float) -> float:
    return round(valor_especialidade * valor_exame, 2)

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