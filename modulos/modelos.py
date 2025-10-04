from dataclasses import dataclass

class Cidade:
    def __init__(self, cod_cidade: int, descricao: str, estado: str):
        self.cod_cidade = cod_cidade
        self.descricao = descricao
        self.estado = estado

    def __repr__(self):
        return f"Cidade(cod='{self.cod_cidade}', nome='{self.descricao}', UF='{self.estado}')"

    def to_list(self) -> list[str]:
        return [str(self.cod_cidade), self.descricao, self.estado]

@dataclass
class Paciente:
    cod_paciente: int
    nome: str
    data_nascimento: str
    endereco: str
    telefone: str
    cod_cidade: int
    peso: float
    altura: float

@dataclass
class Especialidade:
    cod_especialidade: int
    descricao: str
    valor_consulta: float
    limite_diario: int

@dataclass
class Medico:
    cod_medico: int
    nome: str
    endereco: str
    telefone: str
    cod_cidade: int
    cod_especialidade: int

@dataclass
class Exame:
    cod_exame: int
    descricao: str
    cod_especialidade: int
    valor_exame: float

@dataclass
class Consulta:
    cod_consulta: int
    cod_paciente: int
    cod_medico: int
    cod_exame: int
    data: str
    hora: str

@dataclass
class Diaria:
    cod_dia: str
    cod_especialidade: int
    quantidade_consultas: int

