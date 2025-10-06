from dataclasses import dataclass

class Cidade:
    def __init__(self, cod_cidade: int, descricao: str, estado: str):
        self.cod_cidade = cod_cidade
        self.descricao = descricao
        self.estado = estado

    def __repr__(self):
        return (f"Cidade(cod='{self.cod_cidade}', "
                f"nome='{self.descricao}', "
                f"UF='{self.estado}')")

    def to_list(self) -> list[str]:
        return [str(self.cod_cidade), self.descricao, self.estado]

class Paciente:
    def __init__(self,
                 cod_paciente: int,
                 nome: str,
                 data_nascimento: str,
                 endereco: str,
                 telefone: str,
                 cod_cidade: int,
                 peso: float,
                 altura: float):
        self.cod_paciente = cod_paciente
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.telefone = telefone
        self.cod_cidade = cod_cidade
        self.peso = peso
        self.altura = altura

    def __repr__(self):
        return (f"Paciente(cod={self.cod_paciente}, "
                f"nome={self.nome}, "
                f"nascimento={self.data_nascimento}, "
                f"endereco={self.endereco}, "
                f"telefone={self.telefone}, "
                f"FK_Cidade={self.cod_cidade}, "
                f"peso={self.peso}, "
                f"altura={self.altura})"
        )

    def to_list(self) -> list[str]:
        return [
            str(self.cod_paciente),
            self.nome,
            self.data_nascimento,
            self.endereco,
            self.telefone,
            str(self.cod_cidade),
            str(self.peso),
            str(self.altura),
        ]

@dataclass
class Especialidade:
    cod_especialidade: int
    descricao: str
    valor_consulta: float
    limite_diario: int

    def to_list(self) -> list[str]:
        return [
            str(self.cod_especialidade),
            self.descricao,
            str(self.valor_consulta),
            str(self.limite_diario),
        ]

@dataclass
class Medico:
    cod_medico: int
    nome: str
    endereco: str
    telefone: str
    cod_cidade: int
    cod_especialidade: int

    def to_list(self) -> list[str]:
        return [
            str(self.cod_medico),
            self.nome,
            self.endereco,
            self.telefone,
            str(self.cod_cidade),
            str(self.cod_especialidade),
        ]

@dataclass
class Exame:
    cod_exame: int
    descricao: str
    cod_especialidade: int
    valor_exame: float

    def to_list(self) -> list[str]:
        return [
            str(self.cod_exame),
            self.descricao,
            str(self.cod_especialidade),
            str(self.valor_exame),
        ]

@dataclass
class Consulta:
    cod_consulta: int
    cod_paciente: int
    cod_medico: int
    cod_exame: int
    data: str
    hora: str

    def to_list(self) -> list[str]:
        return [
            str(self.cod_consulta),
            str(self.cod_paciente),
            str(self.cod_medico),
            str(self.cod_exame),
            self.data,
            self.hora,
        ]

@dataclass
class Diaria:
    cod_dia: str
    cod_especialidade: int
    quantidade_consultas: int

    def gerar_chave_composta(self) -> str:
        return f"{self.cod_dia}|{self.cod_especialidade}"

    def to_list(self) -> list[str]:
        return [
            self.cod_dia,
            str(self.cod_especialidade),
            str(self.quantidade_consultas),
        ]
