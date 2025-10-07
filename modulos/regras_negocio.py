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