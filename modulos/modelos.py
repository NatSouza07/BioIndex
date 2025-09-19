from dataclasses import dataclass

@dataclass
class Cidade:
    codigo: int
    descricao: str
    estado: str

@dataclass
class Paciente:
    codigo: int
    nome: str
    data_nascimento: str
    endereco: str
    telefone: str
    codigo_cidade: int
    peso: float
    altura: float

@dataclass
class Especialidade:
    codigo: int
    descricao: str
    valor_consulta: float
    limite_diario: int

@dataclass
class Medico:
    codigo: int
    nome: str
    endereco: str
    telefone: str
    codigo_cidade: int
    codigo_especialidade: int

@dataclass
class Exame:
    codigo: int
    descricao: str
    codigo_especialidade: int
    valor_exame: float

@dataclass
class Consulta:
    codigo: int
    codigo_paciente: int
    codigo_medico: int
    codigo_exame: int
    data: str
    hora: str

@dataclass
class Diaria:
    codigo_dia: str #Formato "AAAAMMDD"
    codigo_especialidade: int
    quantidade_consultas: int   